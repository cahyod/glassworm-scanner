import os
import sys
import hashlib
import re
import json
from pathlib import Path


def get_vscode_extensions_path():
    """
    Mendapatkan path ekstensi VS Code berdasarkan sistem operasi
    """
    if sys.platform.startswith('win'):  # Windows
        # Cek lokasi standar Windows
        win_path = Path.home() / '.vscode' / 'extensions'
        if win_path.exists():
            return str(win_path)
        
        # Coba lokasi alternatif di Program Files
        for base_path in [Path(os.environ.get('LOCALAPPDATA', '')), Path(os.environ.get('APPDATA', ''))]:
            if base_path != Path(''):
                alt_path = base_path / 'Programs' / 'Microsoft VS Code' / 'resources' / 'app' / 'extensions'
                if alt_path.exists():
                    return str(alt_path)
    
    elif sys.platform.startswith('darwin'):  # macOS
        mac_path = Path.home() / 'Library' / 'Application Support' / 'Code' / 'extensions'
        if mac_path.exists():
            return str(mac_path)
    
    # Default untuk Linux dan fallback
    return os.path.expanduser("~/.vscode/extensions")


def get_report_directory():
    """
    Mendapatkan direktori laporan berdasarkan sistem operasi
    """
    if sys.platform.startswith('win'):  # Windows
        return os.path.expanduser("~/glassworm-report")
    else:
        return os.path.expanduser("~/glassworm-report")


EXT_DIR = get_vscode_extensions_path()
REPORT_DIR = get_report_directory()

report = {
    "extensions": {}
}

SUSPICIOUS_PATTERNS = {
    "solana_c2": r"(solana|mainnet-beta|rpc)",
    "google_calendar_c2": r"googleapis\.com/calendar",
    "token_access": r"(GITHUB_TOKEN|npmrc|PAT|accessToken)",
    "obfuscation": r"(eval\(|Function\(|atob\(|btoa\(|base64)",
    "dangerous_apis": r"(child_process|spawn|exec)",
    "network_calls": r"(fetch\(|axios|http|https)",
    "suspicious_domains": r"(pastebin|ipfs|raw\.githubusercontent|tunnel)",
}

def hash_file(path):
    """Menghitung hash SHA256 dari file"""
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            h.update(f.read())
        return h.hexdigest()
    except:
        return None

def scan_file(path):
    """Memindai file untuk pola mencurigakan"""
    findings = []
    try:
        with open(path, "r", errors="ignore") as f:
            content = f.read()
            for tag, pattern in SUSPICIOUS_PATTERNS.items():
                if re.search(pattern, content, re.IGNORECASE):
                    findings.append(tag)
    except:
        pass
    return findings

def scan_extension(ext_path):
    """Memindai satu ekstensi untuk file mencurigakan"""
    ext_findings = {
        "files": {},
        "risk": "clean"
    }
    for root, dirs, files in os.walk(ext_path):
        for fn in files:
            if fn.endswith((".js", ".json", ".ts", ".jsx", ".tsx")):
                full = os.path.join(root, fn)
                fhash = hash_file(full)
                suspicious = scan_file(full)
                ext_findings["files"][full] = {
                    "hash": fhash,
                    "suspicious": suspicious
                }

    # Menentukan level risiko
    all_hits = sum(len(v["suspicious"]) for v in ext_findings["files"].values())
    if all_hits > 10:
        ext_findings["risk"] = "infected"
    elif all_hits > 3:
        ext_findings["risk"] = "suspicious"

    return ext_findings

def main():
    """Fungsi utama scanner"""
    # Buat direktori laporan jika belum ada
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    if not os.path.isdir(EXT_DIR):
        print(f"Extensions directory not found at: {EXT_DIR}")
        print("Make sure VS Code extensions are installed.")
        return

    print(f"[+] Scanning extensions in {EXT_DIR}")
    print(f"[+] Report directory: {REPORT_DIR}")
    
    for ext in os.listdir(EXT_DIR):
        path = os.path.join(EXT_DIR, ext)
        if os.path.isdir(path):  # Pastikan itu direktori
            print(f"[+] Scanning {ext}")
            report["extensions"][ext] = scan_extension(path)

    # Tulis laporan JSON
    report_path = os.path.join(REPORT_DIR, "report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)

    print(f"[+] JSON report written to {report_path}")

    # Generate laporan HTML
    html_content = generate_html_report()

    html_path = os.path.join(REPORT_DIR, "report.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[+] HTML report written to {html_path}")
    print(f"[+] Scan completed! Reports are available in {REPORT_DIR}")

def generate_html_report():
    """Menghasilkan HTML report"""
    return """<!DOCTYPE html>
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
        document.getElementById('report-content').innerHTML = '<p style="color:red;">Could not load report.json. The file might not exist or be accessible.</p><p>Please run the scanner first using:</p><p>Python: python gwscan_crossplatform.py</p><p>Windows: python gwscan_crossplatform.py</p>';
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
        <div class="summary-item">Total Extensions: ${total}</div>
        <div class="summary-item risk-clean">Clean: ${clean}</div>
        <div class="summary-item risk-suspicious">Suspicious: ${suspicious}</div>
        <div class="summary-item risk-infected">Infected: ${infected}</div>
    `;
}
</script>
</body>
</html>"""


if __name__ == "__main__":
    main()