# GlassWorm Advanced Scanner

This is an advanced security scanner for VS Code extensions designed to detect potential GlassWorm malware and other malicious patterns. The scanner performs deep analysis of extension files without executing potentially malicious code.

## 🚀 Features

- **Deep scan** of VS Code extensions
- **Detection of malicious patterns**:
  - C2 communication (Solana, Google Calendar, direct RPC)
  - GitHub/NPM token access
  - Obfuscation and eval/base64 payloads
  - Hidden network beacons
  - Node.js child process abuse
- **File integrity checking** with hashing
- **Automated risk rating** (clean/suspicious/infected)
- **HTML and JSON report generation**
- **Static analysis only** (no malicious code execution)

## 📋 Requirements

- Ubuntu 24.04 (or compatible Linux system)
- Python 3
- VS Code with extensions installed
- Bash shell

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/cahyod/glassworm-scanner.git
   cd glassworm-scanner
   ```

2. **Make the scripts executable:**
   ```bash
   chmod +x glassworm-advanced.sh
   chmod +x run_scanner.sh
   ```

## ▶️ Running the Scanner

### Method 1: Using the wrapper script (Recommended)
```bash
./run_scanner.sh
```

### Method 2: Direct execution
```bash
./glassworm-advanced.sh
```

### Method 3: Direct Python execution
```bash
python3 gwscan.py
```

## 🖼️ Sample Results

Check out the sample scan results in the [images](images/) directory to see what the reports look like.

For the best experience when viewing the HTML report, you can:
- Open it with Firefox: `firefox ~/glassworm-report/report.html`
- Serve it via HTTP: `cd ~/glassworm-report && python3 -m http.server 8080` and access via `http://localhost:8080/report.html`

## 📊 Risk Rating System

- 🟢 **Clean**: Less than 4 suspicious indicators found
- 🟠 **Suspicious**: 4-10 suspicious indicators found
- 🔴 **Infected**: More than 10 suspicious indicators found

## 📈 Report Output

After scanning, reports are generated in `~/glassworm-report/`:

- `report.json` - Raw JSON data with all findings
- `report.html` - Interactive HTML report viewable in browser
- `gwscan.py` - Copy of the Python scanner script

The HTML report provides:
- Visual summary of scan results with counts of clean/suspicious/infected extensions
- Color-coded risk indicators (Clean, Suspicious, Infected)
- Detailed extension analysis showing suspicious files and patterns
- Browser-compatible display (works when opened with file:// protocol)
- Responsive design for easy navigation

## 📁 File Structure

The GlassWorm Scanner includes:

- `glassworm-advanced.sh` - Main executable bash script with embedded Python
- `gwscan.py` - Standalone Python scanner module
- `run_scanner.sh` - Convenience wrapper script
- `requirements.txt` - Python requirements (uses only standard library)
- `.gitignore` - Git ignore file for development
- `README.md` - This documentation

## 📈 Report Output

After scanning, reports are generated in `~/glassworm-report/`:

- `report.json` - Raw JSON data with all findings
- `report.html` - Interactive HTML report viewable in browser
- `gwscan.py` - Copy of the Python scanner script

The HTML report provides:
- Visual summary of scan results with counts of clean/suspicious/infected extensions
- Color-coded risk indicators (Clean, Suspicious, Infected)
- Detailed extension analysis showing suspicious files and patterns
- Browser-compatible display (works when opened with file:// protocol)
- Responsive design for easy navigation

## 🛠️ How It Works

The scanner:

1. **Discovers extensions** in `~/.vscode/extensions/`
2. **Walks through** each extension's directory
3. **Analyzes** `.js` and `.json` files for suspicious patterns
4. **Calculates** risk scores based on number of suspicious indicators
5. **Generates** both JSON and HTML reports with findings
6. **Rates** each extension as Clean, Suspicious, or Infected

## 🔍 Detection Patterns

The scanner looks for the following suspicious patterns in extension files:

- **Solana C2**: `(solana|mainnet-beta|rpc)`
- **Google Calendar C2**: `googleapis\.com/calendar`
- **Token Access**: `(GITHUB_TOKEN|npmrc|PAT|accessToken)`
- **Obfuscation**: `(eval\(|Function\(|atob\(|btoa\(|base64)`
- **Dangerous APIs**: `(child_process|spawn|exec)`
- **Network Calls**: `(fetch\(|axios|http|https)`
- **Suspicious Domains**: `(pastebin|ipfs|raw\.githubusercontent|tunnel)`

## 🔒 Security Notes

- Performs **static analysis only** - no potentially malicious code is executed
- **Does not modify** your extensions or VS Code installation
- **Safe to run** on your system
- All operations are read-only

## 🤝 Contributing

Feel free to modify and enhance the scanner based on your needs. The Python module `gwscan.py` can be easily extended with additional detection patterns or analysis features.

The project includes:
- `.gitignore` - Properly configured to exclude temporary files and reports
- `requirements.txt` - Documenting that only standard library modules are used

## Contact
E-mail: cahyod@yahoo.co.id
Github: https://github.com/cahyod/glassworm-scanner.git

## 📄 License

This tool is provided as-is for security research and protection purposes.