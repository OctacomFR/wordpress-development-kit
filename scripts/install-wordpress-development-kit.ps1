[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Destination,

    [string]$KitRoot = (Split-Path -Parent $PSScriptRoot),

    [switch]$SkipValidation
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
        throw "Conflit : '$Path' existe déjà mais ne pointe pas vers '$ExpectedTarget'. Aucun fichier ne sera écrasé."
    }
}

function New-SynchronizedFileLink {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$Target
    )

    if (Test-Path -LiteralPath $Path) {
        return $false
    }

    $pathRoot = [System.IO.Path]::GetPathRoot((Get-NormalizedPath -Path $Path))
    $targetRoot = [System.IO.Path]::GetPathRoot((Get-NormalizedPath -Path $Target))

    if ($pathRoot -ieq $targetRoot) {
        New-Item -ItemType HardLink -Path $Path -Target $Target -ErrorAction Stop | Out-Null
        return $true
    }

    try {
        New-Item -ItemType SymbolicLink -Path $Path -Target $Target -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        throw "Impossible de créer le lien AGENTS.md entre deux volumes. Activez le mode développeur Windows ou choisissez un dossier sur le même volume que le kit. Détail : $($_.Exception.Message)"
    }
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
            throw "Impossible de créer le lien '$Path' vers '$Target'. Activez le mode développeur Windows ou utilisez un volume NTFS local. Détail : $($_.Exception.Message)"
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

        throw "Le dossier dépend déjà d'une racine Git parente : '$normalizedDetectedRoot'. Choisissez la racine réelle du projet ou un dossier indépendant."
    }

    & git.exe init --quiet $Path
    if ($LASTEXITCODE -ne 0) {
        throw "Échec de l'initialisation Git dans '$Path'."
    }

    $confirmedProbe = Get-GitRootProbe -Path $Path
    if ($confirmedProbe.ExitCode -ne 0 -or
        (Get-NormalizedPath -Path $confirmedProbe.Root) -ine (Get-NormalizedPath -Path $Path)) {
        throw "La racine Git détectée ne correspond pas au dossier d'installation '$Path'."
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
        throw "Python Launcher 'py.exe' est requis pour valider l'installation. Utilisez -SkipValidation uniquement si vous prévoyez une validation manuelle."
    }

    $validator = Join-Path $InstalledRoot '.agents\skills\skill-gate\scripts\validate_workflow.py'
    $tests = Join-Path $InstalledRoot '.agents\skills\skill-gate\scripts\test_workflow.py'

    & $pythonLauncher.Source -3 $validator --repo $InstalledRoot
    if ($LASTEXITCODE -ne 0) {
        throw "La validation statique du workflow a échoué."
    }

    & $pythonLauncher.Source -3 $tests
    if ($LASTEXITCODE -ne 0) {
        throw "Les tests d'injection du skill-gate ont échoué."
    }

    $injector = Join-Path $InstalledRoot '.codex\hooks\inject_skill_gate.py'
    $injectedPolicy = '{}' | & $pythonLauncher.Source -3 $injector
    if ($LASTEXITCODE -ne 0 -or ($injectedPolicy -join "`n") -notmatch 'SKILL PREFLIGHT REQUIRED') {
        throw "L'injecteur skill-gate n'a pas produit la politique attendue depuis le workspace installé."
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
    throw "Git est requis afin que les hooks puissent résoudre la racine du projet."
}

if (-not $SkipValidation -and -not (Get-Command py.exe -ErrorAction SilentlyContinue)) {
    throw "Python Launcher 'py.exe' est requis pour la validation. Installez Python ou utilisez -SkipValidation en assumant la recette manuelle."
}

if ($destinationRoot -ieq $kitRoot) {
    throw "Le dossier choisi est déjà la racine du kit. Aucune installation n'est nécessaire."
}

$directorySeparator = [System.IO.Path]::DirectorySeparatorChar
$kitPrefix = $kitRoot.TrimEnd($directorySeparator) + $directorySeparator
$destinationPrefix = $destinationRoot.TrimEnd($directorySeparator) + $directorySeparator
if ($destinationRoot.StartsWith($kitPrefix, [System.StringComparison]::OrdinalIgnoreCase) -or
    $kitRoot.StartsWith($destinationPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Le kit et la destination ne doivent pas être imbriqués l'un dans l'autre. Kit : '$kitRoot'. Destination : '$destinationRoot'."
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

# Vérifier tous les conflits avant la première mutation du projet.
Assert-PathAvailableOrLinked -Path $destinationAgentsFile -ExpectedTarget $sourceAgentsFile -Kind File
Assert-PathAvailableOrLinked -Path $destinationSkillsDirectory -ExpectedTarget $sourceSkillsDirectory -Kind Directory
Assert-PathAvailableOrLinked -Path $destinationCodexDirectory -ExpectedTarget $sourceCodexDirectory -Kind Directory

$createdPaths = New-Object System.Collections.Generic.List[string]
$gitCreated = $false

try {
    $gitCreated = Ensure-ExactGitRoot -Path $destinationRoot

    if (New-SynchronizedFileLink -Path $destinationAgentsFile -Target $sourceAgentsFile) {
        $createdPaths.Add($destinationAgentsFile)
    }
    if (New-SynchronizedDirectoryLink -Path $destinationSkillsDirectory -Target $sourceSkillsDirectory) {
        $createdPaths.Add($destinationSkillsDirectory)
    }
    if (New-SynchronizedDirectoryLink -Path $destinationCodexDirectory -Target $sourceCodexDirectory) {
        $createdPaths.Add($destinationCodexDirectory)
    }

    if (-not (Test-SameFileLink -Path $destinationAgentsFile -ExpectedTarget $sourceAgentsFile)) {
        throw "Le lien AGENTS.md créé ne correspond pas à la source attendue."
    }
    if (-not (Test-SameDirectoryLink -Path $destinationSkillsDirectory -ExpectedTarget $sourceSkillsDirectory)) {
        throw "Le lien .agents créé ne correspond pas à la source attendue."
    }
    if (-not (Test-SameDirectoryLink -Path $destinationCodexDirectory -ExpectedTarget $sourceCodexDirectory)) {
        throw "Le lien .codex créé ne correspond pas à la source attendue."
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
Write-Host 'Installation terminée.'
Write-Host "Racine : $destinationRoot"
Write-Host "Racine Git : $gitRoot"
Write-Host "AGENTS.md : synchronisé avec $sourceAgentsFile"
Write-Host ".agents : synchronisé avec $sourceSkillsDirectory"
Write-Host ".codex : synchronisé avec $sourceCodexDirectory"
if (Test-Path -LiteralPath (Join-Path $destinationRoot 'AGENTS.md.lnk')) {
    Write-Host 'Note : AGENTS.md.lnk a été conservé. Codex utilise le vrai fichier AGENTS.md créé à côté.'
}
Write-Host ''
Write-Host 'Étapes manuelles restantes :'
Write-Host '1. Fermer toute session Codex ouverte sur ce dossier.'
Write-Host '2. Rouvrir le dossier comme workspace et le déclarer fiable.'
Write-Host '3. Exécuter /hooks, relire puis approuver les trois hooks.'
Write-Host '4. Exécuter /skills et vérifier la présence de skill-gate et des skills Octacom.'
