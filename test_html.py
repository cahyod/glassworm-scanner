body { font-family: Arial; margin: 20px; }
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
        document.getElementById('report-content').innerHTML = '<p style="color:red;">Could not load report.json. The file might not exist or be accessible.</p><p>Please run the scanner first using: ./glassworm-advanced.sh</p>';
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
                        html += '<span class="file-path">' + filePath + ': ' + fileData.suspicious.join(', ') + '</span>';
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
    
