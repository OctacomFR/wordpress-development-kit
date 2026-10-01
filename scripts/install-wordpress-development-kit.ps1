[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Destination,

    [string]$KitRoot = (Split-Path -Parent $PSScriptRoot),

    [switch]$SkipValidation,

    [switch]$AllowHardLinkFallback,

    [switch]$RefreshAgentLink
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-NormalizedPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    return [System.IO.Path]::GetFullPath($Path).TrimEnd('\', '/')
}

function Get-ExistingLinkTarget {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $item = Get-Item -LiteralPath $Path -Force
    $target = @($item.Target) | Select-Object -First 1
    if ([string]::IsNullOrWhiteSpace([string]$target)) {
        return $null
    }

    if (-not [System.IO.Path]::IsPathRooted([string]$target)) {
        $target = Join-Path -Path $item.Parent.FullName -ChildPath ([string]$target)
    }

    return Get-NormalizedPath -Path ([string]$target)
}

function Get-NtfsFileId {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $output = & fsutil.exe file queryFileID $Path 2>$null
    if ($LASTEXITCODE -ne 0) {
        return $null
    }

    $match = [regex]::Match(($output -join ' '), '0x[0-9a-fA-F]+')
    if (-not $match.Success) {
        return $null
    }

    return $match.Value.ToLowerInvariant()
}

function Get-GitRootProbe {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $previousErrorActionPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = 'SilentlyContinue'
        $output = & git.exe -C $Path rev-parse --show-toplevel 2>&1
        $exitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $previousErrorActionPreference
    }

    return [pscustomobject]@{
        ExitCode = $exitCode
        Root = if ($exitCode -eq 0 -and $output) { [string]$output } else { $null }
    }
}

function Test-SameFileLink {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$ExpectedTarget
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return $false
    }

    $sourceId = Get-NtfsFileId -Path $ExpectedTarget
    $destinationId = Get-NtfsFileId -Path $Path
    if ($sourceId -and $destinationId -and $sourceId -eq $destinationId) {
        return $true
    }

    $item = Get-Item -LiteralPath $Path -Force
    if ($item.LinkType -eq 'SymbolicLink') {
        $actualTarget = Get-ExistingLinkTarget -Path $Path
        return $actualTarget -ieq (Get-NormalizedPath -Path $ExpectedTarget)
    }

    return $false
}

function Test-SameDirectoryLink {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$ExpectedTarget
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        return $false
    }

    $item = Get-Item -LiteralPath $Path -Force
    if ($item.LinkType -notin @('Junction', 'SymbolicLink')) {
        return $false
    }

    $actualTarget = Get-ExistingLinkTarget -Path $Path
    return $actualTarget -ieq (Get-NormalizedPath -Path $ExpectedTarget)
}

function Assert-PathAvailableOrLinked {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$ExpectedTarget,

        [Parameter(Mandatory = $true)]
        [ValidateSet('File', 'Directory')]
        [string]$Kind
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }

    $matches = if ($Kind -eq 'File') {
        Test-SameFileLink -Path $Path -ExpectedTarget $ExpectedTarget
    }
    else {
        Test-SameDirectoryLink -Path $Path -ExpectedTarget $ExpectedTarget
    }

    if (-not $matches) {
        throw "Conflit : '$Path' existe deja mais ne pointe pas vers '$ExpectedTarget'. Aucun fichier ne sera ecrase."
    }
}

function New-SynchronizedFileLink {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$Target,

        [switch]$AllowHardLinkFallback
    )

    if (Test-Path -LiteralPath $Path) {
        return $false
    }

    $pathRoot = [System.IO.Path]::GetPathRoot((Get-NormalizedPath -Path $Path))
    $targetRoot = [System.IO.Path]::GetPathRoot((Get-NormalizedPath -Path $Target))

    try {
        New-Item -ItemType SymbolicLink -Path $Path -Target $Target -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        $symbolicLinkError = $_.Exception.Message
    }

    if ($AllowHardLinkFallback -and $pathRoot -ieq $targetRoot) {
        New-Item -ItemType HardLink -Path $Path -Target $Target -ErrorAction Stop | Out-Null
        Write-Warning "'$Path' utilise un hardlink de secours. Relancez l'installateur apres un remplacement physique de sa source."
        return $true
    }

    throw "Impossible de creer le lien symbolique '$Path'. Activez le mode developpeur Windows ou les droits requis. Le secours sur le meme volume exige -AllowHardLinkFallback. Detail : $symbolicLinkError"
}

function New-SynchronizedDirectoryLink {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$Target
    )

    if (Test-Path -LiteralPath $Path) {
        return $false
    }

    try {
        New-Item -ItemType Junction -Path $Path -Target $Target -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        try {
            New-Item -ItemType SymbolicLink -Path $Path -Target $Target -ErrorAction Stop | Out-Null
            return $true
        }
        catch {
            throw "Impossible de creer le lien '$Path' vers '$Target'. Activez le mode developpeur Windows ou utilisez un volume NTFS local. Detail : $($_.Exception.Message)"
        }
    }
}

function Ensure-ExactGitRoot {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $probe = Get-GitRootProbe -Path $Path
    if ($probe.ExitCode -eq 0 -and $probe.Root) {
        $normalizedDetectedRoot = Get-NormalizedPath -Path $probe.Root
        if ($normalizedDetectedRoot -ieq (Get-NormalizedPath -Path $Path)) {
            return $false
        }

        throw "Le dossier depend deja d'une racine Git parente : '$normalizedDetectedRoot'. Choisissez la racine reelle du projet ou un dossier independant."
    }

    & git.exe init --quiet $Path
    if ($LASTEXITCODE -ne 0) {
        throw "Echec de l'initialisation Git dans '$Path'."
    }

    $confirmedProbe = Get-GitRootProbe -Path $Path
    if ($confirmedProbe.ExitCode -ne 0 -or
        (Get-NormalizedPath -Path $confirmedProbe.Root) -ine (Get-NormalizedPath -Path $Path)) {
        throw "La racine Git detectee ne correspond pas au dossier d'installation '$Path'."
    }

    return $true
}

function Invoke-PythonValidation {
    param(
        [Parameter(Mandatory = $true)]
        [string]$InstalledRoot
    )

    $pythonExecutable = Get-Command python.exe -ErrorAction SilentlyContinue
    if (-not $pythonExecutable) {
        throw "Python 'python.exe' est requis pour valider l'installation et executer les hooks."
    }

    $validator = Join-Path $InstalledRoot '.agents\skills\skill-gate\scripts\validate_workflow.py'
    $tests = Join-Path $InstalledRoot '.agents\skills\skill-gate\scripts\test_workflow.py'

    $previousPythonIoEncoding = [Environment]::GetEnvironmentVariable('PYTHONIOENCODING', 'Process')
    try {
        $env:PYTHONIOENCODING = 'utf-8'

        & $pythonExecutable.Source -B $validator --repo $InstalledRoot
        if ($LASTEXITCODE -ne 0) {
            throw "La validation statique du workflow a echoue."
        }
    }
    finally {
        if ($null -eq $previousPythonIoEncoding) {
            Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
        }
        else {
            $env:PYTHONIOENCODING = $previousPythonIoEncoding
        }
    }

    & $pythonExecutable.Source -B $tests
    if ($LASTEXITCODE -ne 0) {
        throw "Les tests d'injection du skill-gate ont echoue."
    }

    $injector = Join-Path $InstalledRoot '.codex\hooks\inject_skill_gate.py'
    $injectedPolicy = '{}' | & $pythonExecutable.Source -B $injector
    if ($LASTEXITCODE -ne 0 -or ($injectedPolicy -join "`n") -notmatch 'SKILL PREFLIGHT REQUIRED') {
        throw "L'injecteur skill-gate n'a pas produit la politique attendue depuis le workspace installe."
    }

    $missionTests = Join-Path $kitRoot 'scripts\test-mission-controls.py'
    if (Test-Path -LiteralPath $missionTests -PathType Leaf) {
        & $pythonExecutable.Source -B $missionTests
        if ($LASTEXITCODE -ne 0) { throw "Les tests des controles de mission ont echoue." }
    }
}

function Assert-RealDirectory {
    param([string]$Path)
    if (Test-Path -LiteralPath $Path) {
        $item = Get-Item -LiteralPath $Path -Force
        if (-not $item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "Conflit : '$Path' doit etre un vrai dossier local, sans jonction."
        }
    }
}

function Remove-CreatedPath {
    param([string]$Path, [switch]$Recursive)
    $normalized = Get-NormalizedPath -Path $Path
    if ($normalized -ine $destinationRoot -and -not $normalized.StartsWith($destinationPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Retour arriere hors destination refuse : '$Path'."
    }
    $item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    if ($null -eq $item) { return }
    if ($item.PSIsContainer) {
        if ($Recursive -and -not ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            foreach ($child in (Get-ChildItem -LiteralPath $Path -Force)) {
                Remove-CreatedPath -Path $child.FullName -Recursive
            }
        }
        # Delete(false) retire seulement la jonction ou le dossier maintenant vide.
        [IO.Directory]::Delete($Path, $false)
    }
    else { Remove-Item -LiteralPath $Path -Force }
}

$kitRoot = Get-NormalizedPath -Path $KitRoot
$destinationRoot = Get-NormalizedPath -Path $Destination

if (-not (Test-Path -LiteralPath $kitRoot -PathType Container)) {
    throw "Kit introuvable : '$kitRoot'."
}

$sourceAgentsFile = Join-Path $kitRoot 'AGENTS.md'
$sourceSkillsDirectory = Join-Path $kitRoot '.agents'
$sourceCodexDirectory = Join-Path $kitRoot '.codex'
$installerRequirements = @(
    $sourceAgentsFile,
    $sourceSkillsDirectory,
    $sourceCodexDirectory,
    (Join-Path $sourceCodexDirectory 'hooks.json'),
    (Join-Path $sourceSkillsDirectory 'skills\skill-gate\SKILL.md'),
    (Join-Path $sourceSkillsDirectory 'skills\skill-gate\scripts\validate_workflow.py'),
    (Join-Path $sourceSkillsDirectory 'skills\skill-gate\scripts\test_workflow.py'),
    (Join-Path $sourceCodexDirectory 'hooks\tool_use_gate.py'),
    (Join-Path $sourceCodexDirectory 'hooks\oxygen_site_gate.py'),
    (Join-Path $sourceCodexDirectory 'hooks\mission_guard.py'),
    (Join-Path $kitRoot '.claude\settings.json'),
    (Join-Path $kitRoot '.claude\CLAUDE.md'),
    (Join-Path $kitRoot '.claude\hooks'),
    (Join-Path $kitRoot '.opencode\plugins')
)

foreach ($requiredPath in $installerRequirements) {
    if (-not (Test-Path -LiteralPath $requiredPath)) {
        throw "Source requise introuvable : '$requiredPath'."
    }
}

if (-not (Get-Command git.exe -ErrorAction SilentlyContinue)) {
    throw "Git est requis afin que les hooks puissent resoudre la racine du projet."
}

if (-not (Get-Command python.exe -ErrorAction SilentlyContinue)) {
    throw "Python 'python.exe' est requis pour les hooks et la validation."
}

if ($destinationRoot -ieq $kitRoot) {
    throw "Le dossier choisi est deja la racine du kit. Aucune installation n'est necessaire."
}

$directorySeparator = [System.IO.Path]::DirectorySeparatorChar
$kitPrefix = $kitRoot.TrimEnd($directorySeparator) + $directorySeparator
$destinationPrefix = $destinationRoot.TrimEnd($directorySeparator) + $directorySeparator
if ($destinationRoot.StartsWith($kitPrefix, [System.StringComparison]::OrdinalIgnoreCase) -or
    $kitRoot.StartsWith($destinationPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Le kit et la destination ne doivent pas etre imbriques l'un dans l'autre. Kit : '$kitRoot'. Destination : '$destinationRoot'."
}

if (Test-Path -LiteralPath $destinationRoot -PathType Leaf) {
    throw "La destination est un fichier : '$destinationRoot'."
}

$destinationAgentsFile = Join-Path $destinationRoot 'AGENTS.md'
$destinationSkillsDirectory = Join-Path $destinationRoot '.agents'
$destinationCodexDirectory = Join-Path $destinationRoot '.codex'
$localDirectories = @('.claude', '.opencode', '.octacom')
$fileLinks = @(
    @{ Path = (Join-Path $destinationRoot '.claude\settings.json'); Target = (Join-Path $kitRoot '.claude\settings.json') },
    @{ Path = (Join-Path $destinationRoot '.claude\CLAUDE.md'); Target = (Join-Path $kitRoot '.claude\CLAUDE.md') }
)
$directoryLinks = @(
    @{ Path = $destinationSkillsDirectory; Target = $sourceSkillsDirectory },
    @{ Path = $destinationCodexDirectory; Target = $sourceCodexDirectory },
    @{ Path = (Join-Path $destinationRoot '.claude\hooks'); Target = (Join-Path $kitRoot '.claude\hooks') },
    @{ Path = (Join-Path $destinationRoot '.claude\skills'); Target = (Join-Path $kitRoot '.agents\skills') },
    @{ Path = (Join-Path $destinationRoot '.opencode\plugins'); Target = (Join-Path $kitRoot '.opencode\plugins') }
)
$ignorePath = Join-Path $destinationRoot '.octacom\.gitignore'
$ignoreContent = "*`n"

# Verifier tous les conflits avant la premiere mutation du projet.
Assert-RealDirectory -Path $destinationRoot
$ancestor = Split-Path -Parent $destinationRoot
while ($ancestor) {
    Assert-RealDirectory -Path $ancestor
    $parent = Split-Path -Parent $ancestor
    if ($parent -eq $ancestor) { break }
    $ancestor = $parent
}
foreach ($directory in $localDirectories) { Assert-RealDirectory -Path (Join-Path $destinationRoot $directory) }
$stateDirectory = Join-Path $destinationRoot '.octacom'
if (Test-Path -LiteralPath $stateDirectory) {
    $pendingDirectories = [Collections.Generic.Queue[string]]::new()
    $pendingDirectories.Enqueue($stateDirectory)
    while ($pendingDirectories.Count -gt 0) {
        foreach ($item in (Get-ChildItem -LiteralPath $pendingDirectories.Dequeue() -Force)) {
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -or $item.LinkType) {
                throw "Conflit : l'etat local contient un lien '$($item.FullName)'."
            }
            if ($item.PSIsContainer) { $pendingDirectories.Enqueue($item.FullName) }
        }
    }
}
foreach ($link in $fileLinks) { Assert-PathAvailableOrLinked -Path $link.Path -ExpectedTarget $link.Target -Kind File }
foreach ($link in $directoryLinks) { Assert-PathAvailableOrLinked -Path $link.Path -ExpectedTarget $link.Target -Kind Directory }
if (Test-Path -LiteralPath $ignorePath) {
    $ignoreItem = Get-Item -LiteralPath $ignorePath -Force
    if ($ignoreItem.PSIsContainer -or $ignoreItem.LinkType -or ($ignoreItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -or
        [IO.File]::ReadAllText($ignorePath) -cne $ignoreContent) {
        throw "Conflit : '$ignorePath' contient une configuration etrangere."
    }
}
$gitProbe = Get-GitRootProbe -Path $destinationRoot
if ($gitProbe.ExitCode -eq 0 -and (Get-NormalizedPath $gitProbe.Root) -ine $destinationRoot) {
    throw "La destination depend d'une racine Git parente : '$($gitProbe.Root)'."
}

if ($RefreshAgentLink -and (Test-Path -LiteralPath $destinationAgentsFile -PathType Leaf)) {
    if (-not (Test-SameDirectoryLink -Path $destinationSkillsDirectory -ExpectedTarget $sourceSkillsDirectory) -or
        -not (Test-SameDirectoryLink -Path $destinationCodexDirectory -ExpectedTarget $sourceCodexDirectory)) {
        throw "Le rafraichissement de AGENTS.md exige des liens .agents et .codex deja geres par ce meme kit. Aucun fichier ne sera remplace."
    }
}
else {
    Assert-PathAvailableOrLinked -Path $destinationAgentsFile -ExpectedTarget $sourceAgentsFile -Kind File
}

$createdPaths = New-Object System.Collections.Generic.List[string]
$gitCreated = $false
$gitExisted = Test-Path -LiteralPath (Join-Path $destinationRoot '.git')
$agentsLinkBackupPath = $null
$agentsLinkRefreshed = $false

try {
    if (-not (Test-Path -LiteralPath $destinationRoot)) {
        $missingDirectories = [Collections.Generic.List[string]]::new()
        $nextDirectory = $destinationRoot
        while (-not (Test-Path -LiteralPath $nextDirectory)) {
            $missingDirectories.Add($nextDirectory)
            $nextDirectory = Split-Path -Parent $nextDirectory
        }
        # Aucun parent nouveau : garder le retour arriere confine a la destination nommee.
        if ($missingDirectories.Count -ne 1) { throw "Le parent de la destination doit deja exister : '$nextDirectory'." }
        New-Item -ItemType Directory -Path $destinationRoot | Out-Null
        $createdPaths.Add($destinationRoot)
    }
    $gitCreated = Ensure-ExactGitRoot -Path $destinationRoot

    foreach ($directory in $localDirectories) {
        $localPath = Join-Path $destinationRoot $directory
        if (-not (Test-Path -LiteralPath $localPath)) {
            New-Item -ItemType Directory -Path $localPath | Out-Null
            $createdPaths.Add($localPath)
        }
    }
    if (-not (Test-Path -LiteralPath $ignorePath)) {
        [IO.File]::WriteAllText($ignorePath, $ignoreContent, [Text.UTF8Encoding]::new($false))
        $createdPaths.Add($ignorePath)
    }

    if ($RefreshAgentLink -and (Test-Path -LiteralPath $destinationAgentsFile -PathType Leaf)) {
        $agentsLinkBackupPath = Join-Path $destinationRoot ('.AGENTS.md.octacom-backup.' + [guid]::NewGuid().ToString('N'))
        Move-Item -LiteralPath $destinationAgentsFile -Destination $agentsLinkBackupPath -ErrorAction Stop
        try {
            New-SynchronizedFileLink `
                -Path $destinationAgentsFile `
                -Target $sourceAgentsFile `
                -AllowHardLinkFallback:$AllowHardLinkFallback | Out-Null
        }
        catch {
            $refreshError = $_
            if (Test-Path -LiteralPath $destinationAgentsFile) {
                Remove-Item -LiteralPath $destinationAgentsFile -Force -ErrorAction SilentlyContinue
            }
            Move-Item -LiteralPath $agentsLinkBackupPath -Destination $destinationAgentsFile -ErrorAction Stop
            $agentsLinkBackupPath = $null
            throw $refreshError
        }

        $agentsLinkRefreshed = $true
    }
    elseif (New-SynchronizedFileLink `
        -Path $destinationAgentsFile `
        -Target $sourceAgentsFile `
        -AllowHardLinkFallback:$AllowHardLinkFallback) {
        $createdPaths.Add($destinationAgentsFile)
    }
    foreach ($link in $fileLinks) {
        if (New-SynchronizedFileLink -Path $link.Path -Target $link.Target -AllowHardLinkFallback:$AllowHardLinkFallback) {
            $createdPaths.Add($link.Path)
        }
    }
    foreach ($link in $directoryLinks) {
        if (New-SynchronizedDirectoryLink -Path $link.Path -Target $link.Target) {
            $createdPaths.Add($link.Path)
        }
    }

    if (-not (Test-SameFileLink -Path $destinationAgentsFile -ExpectedTarget $sourceAgentsFile)) {
        throw "Le lien AGENTS.md cree ne correspond pas a la source attendue."
    }
    if (-not (Test-SameDirectoryLink -Path $destinationSkillsDirectory -ExpectedTarget $sourceSkillsDirectory)) {
        throw "Le lien .agents cree ne correspond pas a la source attendue."
    }
    if (-not (Test-SameDirectoryLink -Path $destinationCodexDirectory -ExpectedTarget $sourceCodexDirectory)) {
        throw "Le lien .codex cree ne correspond pas a la source attendue."
    }
    foreach ($link in $fileLinks) {
        if (-not (Test-SameFileLink -Path $link.Path -ExpectedTarget $link.Target)) { throw "Lien invalide : '$($link.Path)'." }
    }
    foreach ($link in $directoryLinks) {
        if (-not (Test-SameDirectoryLink -Path $link.Path -ExpectedTarget $link.Target)) { throw "Lien invalide : '$($link.Path)'." }
    }

    if (-not $SkipValidation) {
        Invoke-PythonValidation -InstalledRoot $destinationRoot
    }

    if ($agentsLinkRefreshed -and $agentsLinkBackupPath -and (Test-Path -LiteralPath $agentsLinkBackupPath)) {
        Remove-Item -LiteralPath $agentsLinkBackupPath -Force -ErrorAction Stop
        $agentsLinkBackupPath = $null
    }
}
catch {
    $installationError = $_

    for ($index = $createdPaths.Count - 1; $index -ge 0; $index--) {
        $createdPath = $createdPaths[$index]
        if ($createdPath -ine $destinationRoot) { Remove-CreatedPath -Path $createdPath }
    }

    if ($agentsLinkRefreshed -and $agentsLinkBackupPath -and (Test-Path -LiteralPath $agentsLinkBackupPath)) {
        if (Test-Path -LiteralPath $destinationAgentsFile) {
            Remove-Item -LiteralPath $destinationAgentsFile -Force -ErrorAction SilentlyContinue
        }
        Move-Item -LiteralPath $agentsLinkBackupPath -Destination $destinationAgentsFile -ErrorAction SilentlyContinue
    }

    if ($gitCreated -or (-not $gitExisted -and (Test-Path -LiteralPath (Join-Path $destinationRoot '.git')))) {
        $createdGitDirectory = Join-Path $destinationRoot '.git'
        $resolvedGitDirectory = Get-NormalizedPath -Path $createdGitDirectory
        if ($resolvedGitDirectory.StartsWith($destinationPrefix, [System.StringComparison]::OrdinalIgnoreCase) -and
            (Test-Path -LiteralPath $createdGitDirectory -PathType Container)) {
            Assert-RealDirectory -Path $createdGitDirectory
            Remove-CreatedPath -Path $createdGitDirectory -Recursive
        }
    }

    if ($createdPaths.Contains($destinationRoot)) { Remove-CreatedPath -Path $destinationRoot }

    throw $installationError
}

$gitRoot = & git.exe -C $destinationRoot rev-parse --show-toplevel
$installedAgentsItem = Get-Item -LiteralPath $destinationAgentsFile -Force
$installedAgentsLinkType = if ($installedAgentsItem.LinkType) { $installedAgentsItem.LinkType } else { 'File' }

Write-Host ''
Write-Host 'Installation terminee.'
Write-Host "Racine : $destinationRoot"
Write-Host "Racine Git : $gitRoot"
Write-Host "AGENTS.md ($installedAgentsLinkType) : synchronise avec $sourceAgentsFile"
Write-Host ".agents : synchronise avec $sourceSkillsDirectory"
Write-Host ".codex : synchronise avec $sourceCodexDirectory"
Write-Host '.claude : dossier local, settings/CLAUDE.md/hooks/skills synchronises'
Write-Host '.opencode : dossier local, plugins synchronises'
Write-Host '.octacom : etat local isole, ignore par Git'
if ($installedAgentsLinkType -eq 'HardLink') {
    Write-Warning "AGENTS.md est un hardlink. Apres chaque git pull du kit, utilisez -RefreshAgentLink -AllowHardLinkFallback ou activez le mode developpeur puis utilisez -RefreshAgentLink."
}
if (Test-Path -LiteralPath (Join-Path $destinationRoot 'AGENTS.md.lnk')) {
    Write-Host 'Note : AGENTS.md.lnk a ete conserve. Codex utilise le vrai fichier AGENTS.md cree a cote.'
}
Write-Host ''
Write-Host 'Etapes manuelles restantes :'
Write-Host '1. Rouvrir le workspace et verifier sa confiance dans chaque interface utilisee.'
Write-Host '2. Suivre docs/compatibility-runtimes.md du kit pour Codex CLI/Desktop, Claude Code, OpenCode et T3.'
Write-Host '3. Prouver configuration active, catalogue et dispatch dans cette interface ; les tests locaux ne suffisent pas.'
