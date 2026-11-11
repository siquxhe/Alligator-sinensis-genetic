# Report page/word count of a .docx via Word COM.
# IMPORTANT: always Quit + ReleaseComObject in finally, otherwise an invisible
# WINWORD process stays alive and keeps a lock on the file.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File docx_pages.ps1 -Path "C:\path\file.docx"

param(
    [Parameter(Mandatory = $true)][string]$Path
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $Path)) {
    Write-Output "ERROR: file not found: $Path"
    exit 1
}

$word = $null
$doc  = $null

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0

    # Open read-only so no ~$ lock file is created.
    # Note: Open() often returns null under PowerShell; use ActiveDocument instead.
    $null = $word.Documents.Open($Path, $false, $true)
    $doc = $word.ActiveDocument
    if (-not $doc -and $word.Documents.Count -ge 1) { $doc = $word.Documents.Item(1) }
    if (-not $doc) { throw "failed to open document (Documents.Count = 0)" }

    $pages = $doc.ComputeStatistics(2)   # 2 = wdStatisticPages
    $words = $doc.ComputeStatistics(0)   # 0 = wdStatisticWords
    Write-Output "PAGES=$pages"
    Write-Output "WORDS=$words"
}
catch {
    Write-Output ("ERROR: " + $_.Exception.Message)
    exit 1
}
finally {
    if ($doc) {
        try { $doc.Close($false) } catch {}
        try { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($doc) } catch {}
    }
    if ($word) {
        try { $word.Quit(0) } catch {}
        try { [void][Runtime.InteropServices.Marshal]::ReleaseComObject($word) } catch {}
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
    [GC]::Collect()

    # Safety net: kill only windowless WINWORD instances (i.e. ones we spawned).
    Start-Sleep -Milliseconds 500
    Get-Process WINWORD -ErrorAction SilentlyContinue |
        Where-Object { $_.MainWindowHandle -eq 0 } |
        ForEach-Object { try { $_.Kill() } catch {} }
}
