import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import random
import time
from datetime import datetime

class LogAnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
        self.is_trained = False
        
    def generate_synthetic_data(self, n_samples=1000):
        # Generate realistic-looking baseline data for training
        data = []
        for _ in range(n_samples):
            is_anomaly = random.random() < 0.05
            if not is_anomaly:
                status = random.choices([200, 201, 301, 302, 304], weights=[0.7, 0.1, 0.05, 0.05, 0.1])[0]
                bytes_sent = int(np.random.normal(1500, 300))
                response_time = int(np.random.normal(50, 15))
            else:
                # Anomalous profiles: e.g., DDoS, large payload exfiltration, server errors
                anomaly_type = random.choice(["ddos", "exfil", "server_error", "bruteforce"])
                if anomaly_type == "ddos":
                    status = 429
                    bytes_sent = int(np.random.normal(500, 50))
                    response_time = int(np.random.normal(500, 100))
                elif anomaly_type == "exfil":
                    status = 200
                    bytes_sent = int(np.random.normal(50000, 5000))
                    response_time = int(np.random.normal(100, 20))
                elif anomaly_type == "server_error":
                    status = 500
                    bytes_sent = int(np.random.normal(100, 10))
                    response_time = int(np.random.normal(2000, 500))
                else: # bruteforce
                    status = 401
                    bytes_sent = int(np.random.normal(300, 20))
                    response_time = int(np.random.normal(20, 5))
                    
            bytes_sent = max(10, bytes_sent)
            response_time = max(1, response_time)
            data.append([status, bytes_sent, response_time])
            
        return pd.DataFrame(data, columns=['status', 'bytes', 'response_time'])

    def train(self):
        df = self.generate_synthetic_data(2000)
        self.model.fit(df)
        self.is_trained = True
        print("Model trained successfully on synthetic realistic data.")

    def predict(self, log_features):
        """
        log_features: dict with keys 'status', 'bytes', 'response_time'
        Returns True if anomaly, False otherwise
        """
        if not self.is_trained:
            self.train()
            
        df = pd.DataFrame([log_features])
        # IsolationForest returns -1 for outliers and 1 for inliers.
        prediction = self.model.predict(df)[0]
        score = self.model.decision_function(df)[0]
        
        return {
            "is_anomaly": bool(prediction == -1),
            "anomaly_score": float(score)
        }

detector = LogAnomalyDetector()
detector.train()
