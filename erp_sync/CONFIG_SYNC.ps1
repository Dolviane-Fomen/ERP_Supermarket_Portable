param(
    [string]$PcName = $env:COMPUTERNAME,
    [int]$AgenceId = 0,
    [string[]]$RemoteShares = @()
)

$configPath = Join-Path $PSScriptRoot "erp_launcher_config.json"
if (!(Test-Path $configPath)) {
    Write-Host "Config introuvable: $configPath" -ForegroundColor Red
    exit 1
}

$config = Get-Content $configPath -Raw | ConvertFrom-Json
if (-not $config.machines) {
    $config | Add-Member -MemberType NoteProperty -Name machines -Value @{}
}

$targets = @()
foreach ($share in $RemoteShares) {
    $targets += @{
        name = (Split-Path $share -Leaf)
        path = $share
    }
}

$config.machines.$PcName = @{
    agence_id      = $AgenceId
    local_sync_dir = "C:/erp_sync"
    remote_targets = $targets
}

$config | ConvertTo-Json -Depth 6 | Set-Content $configPath -Encoding UTF8
Write-Host "Config mise à jour pour $PcName (agence $AgenceId)." -ForegroundColor Green

