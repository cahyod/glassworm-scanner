import os, hashlib, base64, re, json

EXT_DIR = os.path.expanduser("~/.vscode/extensions")
REPORT_DIR = os.path.expanduser("~/glassworm-report")
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
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            h.update(f.read())
        return h.hexdigest()
    except:
        return None

def scan_file(path):
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
    ext_findings = {
        "files": {},
        "risk": "clean"
    }
    for root, dirs, files in os.walk(ext_path):
        for fn in files:
            if fn.endswith(".js") or fn.endswith(".json"):
                full = os.path.join(root, fn)
                fhash = hash_file(full)
                suspicious = scan_file(full)
                ext_findings["files"][full] = {
                    "hash": fhash,
                    "suspicious": suspicious
                }

    # Tentukan level risiko
    all_hits = sum(len(v["suspicious"]) for v in ext_findings["files"].values())
    if all_hits > 10:
        ext_findings["risk"] = "infected"
    elif all_hits > 3:
        ext_findings["risk"] = "suspicious"

    return ext_findings

def main():
    if not os.path.isdir(EXT_DIR):
        print("Extensions directory not found.")
        return

    print(f"[+] Scanning extensions in {EXT_DIR}")
    for ext in os.listdir(EXT_DIR):
        path = os.path.join(EXT_DIR, ext)
        print(f"[+] Scanning {ext}")
        report["extensions"][ext] = scan_extension(path)

    report_path = os.path.join(REPORT_DIR, "report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)

    print(f"[+] JSON report written to {report_path}")
    
    # Generate HTML report
    html_content = """<!DOCTYPE html>
<html>
<head>
<title>GlassWorm Advanced Scan Report</title>
<style>
body { font-family: Arial; margin: 20px; }
.clean { color: green; }
.suspicious { color: orange; }
.infected { color: red; }
</style>
</head>
<body>
<h1>GlassWorm Advanced Scanner Report</h1>
<pre id="json"></pre>
<script>
fetch("report.json").then(r => r.json()).then(data => {
    const pre = document.getElementById("json");
    pre.textContent = JSON.stringify(data, null, 4);
});
</script>
</body>
</html>"""
    
    html_path = os.path.join(REPORT_DIR, "report.html")
    with open(html_path, "w") as f:
        f.write(html_content)
    
    print(f"[+] HTML report written to {html_path}")

if __name__ == "__main__":
    main()