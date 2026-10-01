[CmdletBinding()]
param([string]$KitRoot = (Split-Path -Parent $PSScriptRoot))

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$kitPath = [IO.Path]::GetFullPath($KitRoot).TrimEnd('\', '/')
$testRoot = Join-Path ([IO.Path]::GetTempPath()) ('octacom-install-' + [guid]::NewGuid().ToString('N'))
$testPrefix = [IO.Path]::GetFullPath($testRoot) + [IO.Path]::DirectorySeparatorChar
$installer = Join-Path $kitPath 'scripts\install-wordpress-development-kit.ps1'
$assertions = 0

function Assert-True {
    param([bool]$Condition, [string]$Message)
    if (-not $Condition) { throw "FAIL: $Message" }
    $script:assertions++
}

function Assert-Refused {
    param([scriptblock]$Action, [string]$Pattern)
    $caught = $null
    try { & $Action | Out-Host } catch { $caught = $_.Exception.Message }
    Assert-True ($null -ne $caught -and $caught -match $Pattern) "Refus attendu ($Pattern), obtenu : $caught"
}

function Assert-LocalDirectory {
    param([string]$Path)
    $item = Get-Item -LiteralPath $Path -Force
    Assert-True ($item.PSIsContainer -and -not ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) "Dossier local requis : $Path"
}

function Assert-DirectoryLink {
    param([string]$Path, [string]$Target)
    $item = Get-Item -LiteralPath $Path -Force
    Assert-True ($item.LinkType -in @('Junction', 'SymbolicLink')) "Lien de dossier requis : $Path"
    Assert-True ([IO.Path]::GetFullPath([string]@($item.Target)[0]).TrimEnd('\', '/') -ieq $Target.TrimEnd('\', '/')) "Cible exacte requise : $Path"
}

function Assert-FileLink {
    param([string]$Path, [string]$Target)
    $item = Get-Item -LiteralPath $Path -Force
    Assert-True ($item.LinkType -in @('SymbolicLink', 'HardLink')) "Lien de fichier requis : $Path"
    if ($item.LinkType -eq 'HardLink') {
        $sourceId = (& fsutil.exe file queryFileID $Target) -join ' '
        $linkedId = (& fsutil.exe file queryFileID $Path) -join ' '
        Assert-True ($sourceId -eq $linkedId) "Identite NTFS requise : $Path"
    }
    else {
        Assert-True ([IO.Path]::GetFullPath([string]@($item.Target)[0]).TrimEnd('\', '/') -ieq $Target.TrimEnd('\', '/')) "Cible exacte du symlink : $Path"
        Assert-True ((Get-FileHash -LiteralPath $Path).Hash -ceq (Get-FileHash -LiteralPath $Target).Hash) "Contenu de la cible : $Path"
    }
}

function Remove-TestTree {
    param([string]$Path)
    $absolute = [IO.Path]::GetFullPath($Path).TrimEnd('\', '/')
    if ($absolute -ine $testRoot -and -not $absolute.StartsWith($testPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Nettoyage hors racine temporaire refuse : $absolute"
    }
    $item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    if ($null -eq $item) { return }
    if ($item.PSIsContainer) {
        if (-not ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            foreach ($child in (Get-ChildItem -LiteralPath $Path -Force)) { Remove-TestTree $child.FullName }
        }
        [IO.Directory]::Delete($Path, $false)
    }
    else { Remove-Item -LiteralPath $Path -Force }
}

if ($testRoot.StartsWith($kitPath + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'La racine temporaire doit etre hors du kit.'
}

try {
    New-Item -ItemType Directory -Path $testRoot | Out-Null
    $workspaceA = Join-Path $testRoot 'site-a'
    $workspaceB = Join-Path $testRoot 'site-b'
    $sourceHash = (Get-FileHash -LiteralPath (Join-Path $kitPath 'AGENTS.md')).Hash

    # Conflit natif avant toute creation de Git ou lien de kit.
    New-Item -ItemType Directory -Path (Join-Path $workspaceB '.claude') -Force | Out-Null
    $foreign = Join-Path $workspaceB '.claude\settings.json'
    [IO.File]::WriteAllText($foreign, 'foreign-settings')
    Assert-Refused { & $installer -Destination $workspaceB -KitRoot $kitPath -AllowHardLinkFallback } 'Conflit'
    Assert-True ([IO.File]::ReadAllText($foreign) -ceq 'foreign-settings') 'Configuration etrangere preservee'
    Assert-True (-not (Test-Path (Join-Path $workspaceB '.git')) -and -not (Test-Path (Join-Path $workspaceB 'AGENTS.md'))) 'Conflit sans mutation'
    Remove-Item -LiteralPath $foreign

    foreach ($workspace in @($workspaceA, $workspaceB)) {
        & $installer -Destination $workspace -KitRoot $kitPath -AllowHardLinkFallback | Out-Host
        & $installer -Destination $workspace -KitRoot $kitPath -AllowHardLinkFallback | Out-Host
        $gitRoot = (& git.exe -C $workspace rev-parse --show-toplevel) -join ''
        Assert-True ([IO.Path]::GetFullPath($gitRoot) -ieq $workspace) 'Racine Git exacte et independante'
        foreach ($directory in @('.claude', '.opencode', '.octacom')) { Assert-LocalDirectory (Join-Path $workspace $directory) }
        foreach ($pair in @(
            @('AGENTS.md', 'AGENTS.md'), @('.claude\settings.json', '.claude\settings.json'), @('.claude\CLAUDE.md', '.claude\CLAUDE.md')
        )) { Assert-FileLink (Join-Path $workspace $pair[0]) (Join-Path $kitPath $pair[1]) }
        foreach ($pair in @(
            @('.agents', '.agents'), @('.codex', '.codex'), @('.claude\hooks', '.claude\hooks'),
            @('.claude\skills', '.agents\skills'), @('.opencode\plugins', '.opencode\plugins')
        )) { Assert-DirectoryLink (Join-Path $workspace $pair[0]) (Join-Path $kitPath $pair[1]) }
        & git.exe -C $workspace check-ignore --quiet .octacom/mission.json
        Assert-True ($LASTEXITCODE -eq 0) 'Etat mission ignore par Git'
        Assert-True (@(Get-ChildItem -LiteralPath (Join-Path $workspace '.octacom') -Force | Where-Object { $_.LinkType }).Count -eq 0) 'Etat sans liens'
    }

    # Reconnaissance idempotente d'un vrai hardlink NTFS autorise pour cette fixture.
    $hardAgentLink = Join-Path $workspaceA 'AGENTS.md'
    Remove-Item -LiteralPath $hardAgentLink -Force
    New-Item -ItemType HardLink -Path $hardAgentLink -Target (Join-Path $kitPath 'AGENTS.md') | Out-Null
    Assert-FileLink $hardAgentLink (Join-Path $kitPath 'AGENTS.md')
    & $installer -Destination $workspaceA -KitRoot $kitPath -AllowHardLinkFallback | Out-Host

    [IO.File]::WriteAllText((Join-Path $workspaceA '.octacom\mission.json'), '{"fixture":"a"}')
    Assert-True (-not (Test-Path (Join-Path $workspaceB '.octacom\mission.json'))) 'Etat mission non partage'
    Assert-True (-not (Test-Path (Join-Path $kitPath '.octacom\installation-test-sentinel'))) 'Aucun etat fixture ecrit dans le kit'
    $stateHardLink = Join-Path $workspaceB '.octacom\shared.json'
    New-Item -ItemType HardLink -Path $stateHardLink -Target (Join-Path $workspaceA '.octacom\mission.json') | Out-Null
    Assert-Refused { & $installer -Destination $workspaceB -KitRoot $kitPath -AllowHardLinkFallback } "l'etat local contient un lien"
    Remove-Item -LiteralPath $stateHardLink
    Assert-True (Test-Path (Join-Path $workspaceA '.octacom\mission.json')) 'Refus de hardlink preserve la mission source'

    $foreignPluginWorkspace = Join-Path $testRoot 'foreign-plugin'
    New-Item -ItemType Directory -Path (Join-Path $foreignPluginWorkspace '.opencode\plugins') -Force | Out-Null
    $pluginSentinel = Join-Path $foreignPluginWorkspace '.opencode\plugins\keep.txt'
    [IO.File]::WriteAllText($pluginSentinel, 'keep')
    Assert-Refused { & $installer -Destination $foreignPluginWorkspace -KitRoot $kitPath -AllowHardLinkFallback } 'Conflit'
    Assert-True ([IO.File]::ReadAllText($pluginSentinel) -ceq 'keep') 'Plugins etrangers preserves'
    Assert-True (-not (Test-Path (Join-Path $foreignPluginWorkspace '.git'))) 'Plugins etrangers refuses avant mutation'

    $sharedStateWorkspace = Join-Path $testRoot 'shared-state'
    New-Item -ItemType Directory -Path $sharedStateWorkspace | Out-Null
    New-Item -ItemType Junction -Path (Join-Path $sharedStateWorkspace '.octacom') -Target (Join-Path $workspaceA '.octacom') | Out-Null
    Assert-Refused { & $installer -Destination $sharedStateWorkspace -KitRoot $kitPath -AllowHardLinkFallback } 'vrai dossier local'
    Assert-True ([IO.File]::ReadAllText((Join-Path $workspaceA '.octacom\mission.json')) -match 'fixture') 'Refus de partage preserve la cible'

    $parentGit = Join-Path $testRoot 'parent-git'
    New-Item -ItemType Directory -Path (Join-Path $parentGit 'child') -Force | Out-Null
    & git.exe init --quiet $parentGit
    Assert-Refused { & $installer -Destination (Join-Path $parentGit 'child') -KitRoot $kitPath -AllowHardLinkFallback } 'racine Git parente'
    Assert-True (-not (Test-Path (Join-Path $parentGit 'child\.claude'))) 'Racine parente refusee avant mutation'

    # Copie locale invalide : provoquer l'echec apres creation des liens, sans toucher le kit.
    $invalidKit = Join-Path $testRoot 'invalid-kit'
    New-Item -ItemType Directory -Path $invalidKit | Out-Null
    foreach ($source in @('AGENTS.md', '.agents', '.codex', '.claude', '.opencode')) {
        Copy-Item -LiteralPath (Join-Path $kitPath $source) -Destination $invalidKit -Recurse -Force
    }
    [IO.File]::WriteAllText((Join-Path $invalidKit '.agents\skills\skill-gate\SKILL.md'), 'invalid fixture')
    $freshFailure = Join-Path $testRoot 'rollback-new'
    Assert-Refused { & $installer -Destination $freshFailure -KitRoot $invalidKit -AllowHardLinkFallback } 'validation statique'
    Assert-True (-not (Test-Path -LiteralPath $freshFailure)) 'Retour arriere supprime la nouvelle destination'
    $existingFailure = Join-Path $testRoot 'rollback-existing'
    New-Item -ItemType Directory -Path $existingFailure | Out-Null
    & git.exe init --quiet $existingFailure
    [IO.File]::WriteAllText((Join-Path $existingFailure 'keep.txt'), 'existing-user-file')
    Assert-Refused { & $installer -Destination $existingFailure -KitRoot $invalidKit -AllowHardLinkFallback } 'validation statique'
    Assert-True ([IO.File]::ReadAllText((Join-Path $existingFailure 'keep.txt')) -ceq 'existing-user-file') 'Retour arriere preserve les fichiers existants'
    Assert-True (Test-Path -LiteralPath (Join-Path $existingFailure '.git')) 'Retour arriere preserve le Git existant'
    foreach ($path in @('AGENTS.md', '.agents', '.codex', '.claude', '.opencode', '.octacom')) {
        Assert-True (-not (Test-Path -LiteralPath (Join-Path $existingFailure $path))) "Retour arriere complet : $path"
    }
    Assert-True ((Get-FileHash -LiteralPath (Join-Path $kitPath 'AGENTS.md')).Hash -ceq $sourceHash) 'Suppression des liens preserve leur source'
    Assert-True ([IO.File]::ReadAllText((Join-Path $invalidKit '.agents\skills\skill-gate\SKILL.md')) -ceq 'invalid fixture') 'Suppression des jonctions preserve leur cible'
    Write-Host "OK: $assertions assertions, deux installations NTFS isolees, idempotence, refus et retours arriere."
}
finally {
    Remove-TestTree $testRoot
}
