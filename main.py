from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import random
import time
from datetime import datetime
import os
from ml_model import detector

app = FastAPI(title="Log Anomaly Detector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directory exists
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

def generate_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

def generate_path():
    paths = ["/api/v1/users", "/login", "/dashboard", "/api/v1/data", "/images/logo.png", "/wp-admin", "/admin", "/.env", "/index.html"]
    return random.choice(paths)

def generate_method():
    return random.choices(["GET", "POST", "PUT", "DELETE"], weights=[0.7, 0.2, 0.05, 0.05])[0]

@app.get("/api/logs/stream")
def stream_log():
    """Generates a single log entry, analyzes it, and returns the result."""
    # Determine if we force an anomaly based on random chance
    force_anomaly = random.random() < 0.1
    
    if force_anomaly:
        anomaly_type = random.choice(["ddos", "exfil", "server_error", "bruteforce"])
        if anomaly_type == "ddos":
            status = 429
            bytes_sent = int(random.gauss(500, 50))
            response_time = int(random.gauss(500, 100))
        elif anomaly_type == "exfil":
            status = 200
            bytes_sent = int(random.gauss(50000, 5000))
            response_time = int(random.gauss(100, 20))
        elif anomaly_type == "server_error":
            status = 500
            bytes_sent = int(random.gauss(100, 10))
            response_time = int(random.gauss(2000, 500))
        else: # bruteforce
            status = 401
            bytes_sent = int(random.gauss(300, 20))
            response_time = int(random.gauss(20, 5))
            
        ip = generate_ip()
        path = "/login" if anomaly_type == "bruteforce" else generate_path()
        method = "POST" if anomaly_type == "bruteforce" else generate_method()
        
    else:
        status = random.choices([200, 201, 301, 302, 304, 404], weights=[0.6, 0.1, 0.05, 0.05, 0.15, 0.05])[0]
        bytes_sent = int(random.gauss(1500, 300))
        response_time = int(random.gauss(50, 15))
        ip = generate_ip()
        path = generate_path()
        method = generate_method()

    bytes_sent = max(10, bytes_sent)
    response_time = max(1, response_time)

    features = {
        "status": status,
        "bytes": bytes_sent,
        "response_time": response_time
    }
    
    analysis = detector.predict(features)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "ip": ip,
        "method": method,
        "path": path,
        "status": status,
        "bytes": bytes_sent,
        "response_time": response_time,
        "is_anomaly": analysis["is_anomaly"],
        "anomaly_score": analysis["anomaly_score"]
    }
    
    return JSONResponse(content=log_entry)

@app.get("/")
def read_root():
    return {"message": "Go to /static/index.html to view the dashboard."}
