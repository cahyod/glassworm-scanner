<#
.SYNOPSIS
    GlassWorm Advanced Scanner untuk Windows
.DESCRIPTION
    Alat ini memindai ekstensi VS Code di Windows untuk mendeteksi potensi malware GlassWorm
.NOTES
    File: glassworm_windows.ps1
    Author: GlassWorm Security Team
    Platform: Windows 10/11
#>

# Set execution policy jika diperlukan
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "GlassWorm Advanced Scanner for Windows" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan

# Lokasi ekstensi VS Code di Windows
$VsCodeExtensionsPath = Join-Path $env:USERPROFILE ".vscode\extensions"

# Direktori laporan
$ReportDir = Join-Path $env:USERPROFILE "glassworm-report"

# Buat direktori laporan jika belum ada
if (!(Test-Path $ReportDir)) {
    New-Item -ItemType Directory -Path $ReportDir -Force | Out-Null
}

Write-Host "[+] Extensions directory: $VsCodeExtensionsPath" -ForegroundColor Green
Write-Host "[+] Report directory: $ReportDir" -ForegroundColor Green

# Cek apakah direktori ekstensi ada
if (!(Test-Path $VsCodeExtensionsPath)) {
    Write-Host "[-] VS Code extensions directory not found at: $VsCodeExtensionsPath" -ForegroundColor Red
    Write-Host "[-] Make sure VS Code is installed with extensions." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Definisikan pola mencurigakan
$SuspiciousPatterns = @{
    "solana_c2" = "(solana|mainnet-beta|rpc)"
    "google_calendar_c2" = "googleapis\.com/calendar"
    "token_access" = "(GITHUB_TOKEN|npmrc|PAT|accessToken)"
    "obfuscation" = "(eval\(|Function\(|atob\(|btoa\(|base64)"
    "dangerous_apis" = "(child_process|spawn|exec)"
    "network_calls" = "(fetch\(|axios|http|https)"
    "suspicious_domains" = "(pastebin|ipfs|raw\.githubusercontent|tunnel)"
}

# Fungsi untuk menghitung hash file
function Get-FileHash($FilePath) {
    try {
        $fileStream = [System.IO.File]::OpenRead($FilePath)
        $hashAlgorithm = [System.Security.Cryptography.SHA256]::Create()
        $hashBytes = $hashAlgorithm.ComputeHash($fileStream)
        $hashAlgorithm.Dispose()
        $fileStream.Dispose()
        
        # Konversi byte array ke hexadecimal
        $hashString = [System.BitConverter]::ToString($hashBytes).Replace('-', '').ToLower()
        return $hashString
    }
    catch {
        return $null
    }
}

# Fungsi untuk memindai file
function Invoke-FileScan($FilePath) {
    $findings = @()
    
    try {
        # Baca konten file dengan encoding yang benar
        $content = Get-Content -Path $FilePath -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
        
        if ($content) {
            foreach ($tag in $SuspiciousPatterns.Keys) {
                $pattern = $SuspiciousPatterns[$tag]
                if ($content -match $pattern) {
                    $findings += $tag
                }
            }
        }
    }
    catch {
        # Abaikan error saat membaca file
    }
    
    return $findings
}

# Fungsi untuk memindai satu ekstensi
function Invoke-ExtensionScan($ExtensionPath) {
    $extFindings = @{
        "files" = @{}
        "risk" = "clean"
    }
    
    # Jelajahi semua file dalam ekstensi
    $files = Get-ChildItem -Path $ExtensionPath -Recurse -Include "*.js", "*.json", "*.ts", "*.jsx", "*.tsx" -ErrorAction SilentlyContinue
    
    foreach ($file in $files) {
        $filePath = $file.FullName
        $fileHash = Get-FileHash -FilePath $filePath
        $suspicious = Invoke-FileScan -FilePath $filePath
        
        $extFindings["files"][$filePath] = @{
            "hash" = $fileHash
            "suspicious" = $suspicious
        }
    }
    
    # Hitung total temuan mencurigakan
    $allHits = 0
    foreach ($fileInfo in $extFindings["files"].Values) {
        $allHits += $fileInfo["suspicious"].Count
    }
    
    # Tentukan tingkat risiko
    if ($allHits -gt 10) {
        $extFindings["risk"] = "infected"
    }
    elseif ($allHits -gt 3) {
        $extFindings["risk"] = "suspicious"
    }
    
    return $extFindings
}

# Struktur laporan awal
$report = @{
    "extensions" = @{}
}

# Dapatkan semua direktori ekstensi
$extensions = Get-ChildItem -Path $VsCodeExtensionsPath -Directory -ErrorAction SilentlyContinue

Write-Host "[+] Found $($extensions.Count) extensions to scan..." -ForegroundColor Yellow

# Iterasi melalui setiap ekstensi
foreach ($ext in $extensions) {
    $extPath = $ext.FullName
    Write-Host "[+] Scanning $($ext.Name)" -ForegroundColor Green
    
    $extReport = Invoke-ExtensionScan -ExtensionPath $extPath
    $report["extensions"][$ext.Name] = $extReport
}

# Simpan laporan JSON
$reportPath = Join-Path $ReportDir "report.json"
$report | ConvertTo-Json -Depth 10 | Out-File -FilePath $reportPath -Encoding utf8

Write-Host "[+] JSON report written to $reportPath" -ForegroundColor Green

# Generate laporan HTML
$htmlContent = @"
<!DOCTYPE html>
<html>
<head>
<title>GlassWorm Advanced Scan Report</title>
<style>
body { font-family: Arial, sans-serif; margin: 20px; }
.clean { color: green; }
.suspicious { color: orange; }
.infected { color: red; }
.extension-name { font-weight: bold; margin-top: 10px; }
.file-path { margin-left: 20px; display: block; }
.risk-level { display: inline-block; padding: 2px 6px; border-radius: 3px; font-weight: bold; }
.risk-clean { background-color: #d4edda; color: #155724; }
.risk-suspicious { background-color: #fff3cd; color: #856404; }
.risk-infected { background-color: #f8d7da; color: #721c24; }
.summary { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
.summary-item { margin: 5px 0; }
</style>
</head>
<body>
<h1>GlassWorm Advanced Scanner Report</h1>
<div class="summary">
    <h2>Scan Summary</h2>
    <div id="summary-stats" class="summary-item"></div>
</div>
<div id="report-content"></div>

<script>
// Load JSON using dynamic import to work with local files
document.addEventListener('DOMContentLoaded', function() {
    // Try multiple approaches to load the JSON
    const xhr = new XMLHttpRequest();
    xhr.open('GET', 'report.json', true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 0 || xhr.status === 200) { // Handle local files (status 0) and HTTP (200)
                try {
                    const data = JSON.parse(xhr.responseText);
                    displayReport(data);
                    updateSummary(data);
                } catch (e) {
                    document.getElementById('report-content').innerHTML = '<p style="color:red;">Error parsing JSON: ' + e.message + '</p>';
                }
            } else {
                document.getElementById('report-content').innerHTML = '<p style="color:red;">Error loading report.json: HTTP ' + xhr.status + '</p>';
            }
        }
    };
    xhr.onerror = function() {
        // Fallback for when the report.json is not accessible
        document.getElementById('report-content').innerHTML = '<p style="color:red;">Could not load report.json. The file might not exist or be accessible.</p><p>Please run the scanner first using PowerShell:</p><p>PowerShell: .\\glassworm_windows.ps1</p>';
    };
    xhr.send();
});

function displayReport(data) {
    const contentDiv = document.getElementById('report-content');
    let html = '<h2>Extension Details</h2>';

    if (data.extensions) {
        for (const [extName, extData] of Object.entries(data.extensions)) {
            html += '<div class="extension-name">';
            html += extName + ' <span class="risk-level risk-' + extData.risk + '">' + extData.risk + '</span>';
            html += '</div>';

            if (extData.files) {
                for (const [filePath, fileData] of Object.entries(extData.files)) {
                    if (fileData.suspicious && fileData.suspicious.length > 0) {
                        html += '<span class="file-path">' + filePath.replace(/\\\\/g, '/') + ': ' + fileData.suspicious.join(', ') + '</span>';
                    }
                }
            }
        }
    } else {
        html += '<p>No extension data found</p>';
    }

    contentDiv.innerHTML += html;
}

function updateSummary(data) {
    if (!data.extensions) return;

    const total = Object.keys(data.extensions).length;
    let clean = 0, suspicious = 0, infected = 0;

    for (const ext of Object.values(data.extensions)) {
        if (ext.risk === 'clean') clean++;
        else if (ext.risk === 'suspicious') suspicious++;
        else if (ext.risk === 'infected') infected++;
    }

    const summaryDiv = document.getElementById('summary-stats');
    summaryDiv.innerHTML = `
        <div class="summary-item">Total Extensions: \${total}</div>
        <div class="summary-item risk-clean">Clean: \${clean}</div>
        <div class="summary-item risk-suspicious">Suspicious: \${suspicious}</div>
        <div class="summary-item risk-infected">Infected: \${infected}</div>
    `;
}
</script>
</body>
</html>
"@

$htmlPath = Join-Path $ReportDir "report.html"
$htmlContent | Out-File -FilePath $htmlPath -Encoding utf8

Write-Host "[+] HTML report written to $htmlPath" -ForegroundColor Green
Write-Host "[+] Scan completed! Reports are available in $ReportDir" -ForegroundColor Green

# Tanyakan apakah ingin membuka laporan
Write-Host "`nWould you like to open the HTML report now?" -ForegroundColor Yellow
$openReport = Read-Host "Enter 'y' to open the report in your default browser, or press Enter to exit"

if ($openReport -eq 'y' -or $openReport -eq 'Y') {
    Start-Process $htmlPath
}

Write-Host "`nThanks for using GlassWorm Advanced Scanner!" -ForegroundColor Green