const logBody = document.getElementById('logBody');
const totalLogsEl = document.getElementById('totalLogs');
const totalAnomaliesEl = document.getElementById('totalAnomalies');
const threatLevelEl = document.getElementById('threatLevel');

let totalLogs = 0;
let totalAnomalies = 0;
const MAX_LOGS_DISPLAYED = 50;

async function fetchLog() {
    try {
        const response = await fetch('/api/logs/stream');
        const data = await response.json();
        addLogToTable(data);
        updateStats(data.is_anomaly);
    } catch (error) {
        console.error("Error fetching log:", error);
    }
}

function addLogToTable(log) {
    const row = document.createElement('tr');
    if (log.is_anomaly) {
        row.className = 'is-anomaly';
    }

    const time = new Date(log.timestamp).toLocaleTimeString();
    
    row.innerHTML = `
        <td>${time}</td>
        <td>${log.ip}</td>
        <td>${log.method}</td>
        <td>${log.path}</td>
        <td>${log.status}</td>
        <td>${log.bytes}</td>
        <td>${log.response_time}ms</td>
        <td>
            <span class="status-label ${log.is_anomaly ? 'status-anomaly' : 'status-normal'}">
                ${log.is_anomaly ? 'ANOMALY DETECTED' : 'NORMAL'}
            </span>
        </td>
    `;

    logBody.insertBefore(row, logBody.firstChild);

    // Keep table from growing infinitely
    if (logBody.children.length > MAX_LOGS_DISPLAYED) {
        logBody.removeChild(logBody.lastChild);
    }
}

function updateStats(isAnomaly) {
    totalLogs++;
    if (isAnomaly) {
        totalAnomalies++;
    }

    totalLogsEl.textContent = totalLogs;
    totalAnomaliesEl.textContent = totalAnomalies;

    // Calculate threat level based on recent anomaly rate
    const anomalyRate = totalAnomalies / totalLogs;
    if (totalLogs > 10) {
        if (anomalyRate > 0.2) {
            threatLevelEl.textContent = "CRITICAL";
            threatLevelEl.style.color = "var(--accent-red)";
        } else if (anomalyRate > 0.05) {
            threatLevelEl.textContent = "ELEVATED";
            threatLevelEl.style.color = "orange";
        } else {
            threatLevelEl.textContent = "LOW";
            threatLevelEl.style.color = "var(--text-primary)";
        }
    }
}

// Fetch a new log every 800ms to simulate live traffic
setInterval(fetchLog, 800);
