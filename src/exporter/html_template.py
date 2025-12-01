HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Compliance Report</title>
<style>
/* (truncated for readability — this contains your same CSS) */
</style>
</head>
<body>
    <div class="header">
        <h1>🏢 Compliance Check Report</h1>
        <p class="timestamp">Generated: {timestamp}</p>
    </div>
    <div class="summary">
        <div class="summary-card"><h3>Total Violations</h3><div class="value">{total_violations}</div></div>
        <div class="summary-card"><h3>Critical</h3><div class="value">{critical_count}</div></div>
        <div class="summary-card"><h3>High</h3><div class="value">{high_count}</div></div>
        <div class="summary-card"><h3>Medium</h3><div class="value">{medium_count}</div></div>
        <div class="summary-card"><h3>Low</h3><div class="value">{low_count}</div></div>
    </div>
    <h2>Violations</h2>
    {violations_html}
</body>
</html>
"""