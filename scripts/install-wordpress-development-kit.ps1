[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Destination,

    [string]$KitRoot = (Split-Path -Parent $PSScriptRoot),

    [switch]$SkipValidation,

    [switch]$AllowHardLinkFallback,

    [switch]$UpgradeAgentLink
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
        Write-Warning "AGENTS.md utilise un hardlink de secours. Relancez l'installateur apres chaque git pull du kit, car un remplacement physique du fichier source peut rompre la synchronisation."
        return $true
    }

    throw "Impossible de creer le lien symbolique AGENTS.md. Activez le mode developpeur Windows ou lancez PowerShell avec les droits requis. Le secours par hardlink est disponible sur le meme volume avec -AllowHardLinkFallback, mais il est moins fiable apres git pull. Detail : $symbolicLinkError"
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

    $pythonLauncher = Get-Command py.exe -ErrorAction SilentlyContinue
    if (-not $pythonLauncher) {
        throw "Python Launcher 'py.exe' est requis pour valider l'installation. Utilisez -SkipValidation uniquement si vous prevoyez une validation manuelle."
    }

    $validator = Join-Path $InstalledRoot '.agents\skills\skill-gate\scripts\validate_workflow.py'
    $tests = Join-Path $InstalledRoot '.agents\skills\skill-gate\scripts\test_workflow.py'

    $previousPythonIoEncoding = [Environment]::GetEnvironmentVariable('PYTHONIOENCODING', 'Process')
    try {
        $env:PYTHONIOENCODING = 'utf-8'

        & $pythonLauncher.Source -3 $validator --repo $InstalledRoot
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

    & $pythonLauncher.Source -3 $tests
    if ($LASTEXITCODE -ne 0) {
        throw "Les tests d'injection du skill-gate ont echoue."
    }

    $injector = Join-Path $InstalledRoot '.codex\hooks\inject_skill_gate.py'
    $injectedPolicy = '{}' | & $pythonLauncher.Source -3 $injector
    if ($LASTEXITCODE -ne 0 -or ($injectedPolicy -join "`n") -notmatch 'SKILL PREFLIGHT REQUIRED') {
        throw "L'injecteur skill-gate n'a pas produit la politique attendue depuis le workspace installe."
    }
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
    (Join-Path $sourceSkillsDirectory 'skills\skill-gate\scripts\test_workflow.py')
)

foreach ($requiredPath in $installerRequirements) {
    if (-not (Test-Path -LiteralPath $requiredPath)) {
        throw "Source requise introuvable : '$requiredPath'."
    }
}

if (-not (Get-Command git.exe -ErrorAction SilentlyContinue)) {
    throw "Git est requis afin que les hooks puissent resoudre la racine du projet."
}

if (-not $SkipValidation -and -not (Get-Command py.exe -ErrorAction SilentlyContinue)) {
    throw "Python Launcher 'py.exe' est requis pour la validation. Installez Python ou utilisez -SkipValidation en assumant la recette manuelle."
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

if (-not (Test-Path -LiteralPath $destinationRoot)) {
    New-Item -ItemType Directory -Path $destinationRoot -ErrorAction Stop | Out-Null
}

$destinationAgentsFile = Join-Path $destinationRoot 'AGENTS.md'
$destinationSkillsDirectory = Join-Path $destinationRoot '.agents'
$destinationCodexDirectory = Join-Path $destinationRoot '.codex'

# Verifier tous les conflits avant la premiere mutation du projet.
Assert-PathAvailableOrLinked -Path $destinationAgentsFile -ExpectedTarget $sourceAgentsFile -Kind File
Assert-PathAvailableOrLinked -Path $destinationSkillsDirectory -ExpectedTarget $sourceSkillsDirectory -Kind Directory
Assert-PathAvailableOrLinked -Path $destinationCodexDirectory -ExpectedTarget $sourceCodexDirectory -Kind Directory

$upgradeExistingAgentLink = $false
if ($UpgradeAgentLink -and (Test-Path -LiteralPath $destinationAgentsFile -PathType Leaf)) {
    $existingAgentLink = Get-Item -LiteralPath $destinationAgentsFile -Force
    $upgradeExistingAgentLink = $existingAgentLink.LinkType -ne 'SymbolicLink'
}

$createdPaths = New-Object System.Collections.Generic.List[string]
$gitCreated = $false
$agentsLinkUpgraded = $false

try {
    $gitCreated = Ensure-ExactGitRoot -Path $destinationRoot

    if ($upgradeExistingAgentLink) {
        Remove-Item -LiteralPath $destinationAgentsFile -Force -ErrorAction Stop
        try {
            New-SynchronizedFileLink `
                -Path $destinationAgentsFile `
                -Target $sourceAgentsFile `
                -AllowHardLinkFallback:$AllowHardLinkFallback | Out-Null
        }
        catch {
            $upgradeError = $_
            if (Test-Path -LiteralPath $destinationAgentsFile) {
                Remove-Item -LiteralPath $destinationAgentsFile -Force -ErrorAction SilentlyContinue
            }
            New-Item -ItemType HardLink -Path $destinationAgentsFile -Target $sourceAgentsFile -ErrorAction Stop | Out-Null
            throw $upgradeError
        }

        $agentsLinkUpgraded = (Get-Item -LiteralPath $destinationAgentsFile -Force).LinkType -eq 'SymbolicLink'
    }
    elseif (New-SynchronizedFileLink `
        -Path $destinationAgentsFile `
        -Target $sourceAgentsFile `
        -AllowHardLinkFallback:$AllowHardLinkFallback) {
        $createdPaths.Add($destinationAgentsFile)
    }
    if (New-SynchronizedDirectoryLink -Path $destinationSkillsDirectory -Target $sourceSkillsDirectory) {
        $createdPaths.Add($destinationSkillsDirectory)
    }
    if (New-SynchronizedDirectoryLink -Path $destinationCodexDirectory -Target $sourceCodexDirectory) {
        $createdPaths.Add($destinationCodexDirectory)
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

    if (-not $SkipValidation) {
        Invoke-PythonValidation -InstalledRoot $destinationRoot
    }
}
catch {
    $installationError = $_

    for ($index = $createdPaths.Count - 1; $index -ge 0; $index--) {
        $createdPath = $createdPaths[$index]
        if (Test-Path -LiteralPath $createdPath) {
            Remove-Item -LiteralPath $createdPath -Force -ErrorAction SilentlyContinue
        }
    }

    if ($agentsLinkUpgraded) {
        if (Test-Path -LiteralPath $destinationAgentsFile) {
            Remove-Item -LiteralPath $destinationAgentsFile -Force -ErrorAction SilentlyContinue
        }
        New-Item -ItemType HardLink -Path $destinationAgentsFile -Target $sourceAgentsFile -ErrorAction SilentlyContinue | Out-Null
    }

    if ($gitCreated) {
        $createdGitDirectory = Join-Path $destinationRoot '.git'
        $resolvedGitDirectory = Get-NormalizedPath -Path $createdGitDirectory
        if ($resolvedGitDirectory.StartsWith($destinationPrefix, [System.StringComparison]::OrdinalIgnoreCase) -and
            (Test-Path -LiteralPath $createdGitDirectory -PathType Container)) {
            Remove-Item -LiteralPath $createdGitDirectory -Recurse -Force -ErrorAction SilentlyContinue
        }
    }

    throw $installationError
}

$gitRoot = & git.exe -C $destinationRoot rev-parse --show-toplevel

Write-Host ''
Write-Host 'Installation terminee.'
Write-Host "Racine : $destinationRoot"
Write-Host "Racine Git : $gitRoot"
Write-Host "AGENTS.md : synchronise avec $sourceAgentsFile"
Write-Host ".agents : synchronise avec $sourceSkillsDirectory"
Write-Host ".codex : synchronise avec $sourceCodexDirectory"
if (Test-Path -LiteralPath (Join-Path $destinationRoot 'AGENTS.md.lnk')) {
    Write-Host 'Note : AGENTS.md.lnk a ete conserve. Codex utilise le vrai fichier AGENTS.md cree a cote.'
}
Write-Host ''
Write-Host 'Etapes manuelles restantes :'
Write-Host '1. Fermer toute session Codex ouverte sur ce dossier.'
Write-Host '2. Rouvrir le dossier comme workspace et le declarer fiable.'
Write-Host '3. Executer /hooks, relire puis approuver les trois hooks.'
Write-Host '4. Executer /skills et verifier la presence de skill-gate et des skills Octacom.'
