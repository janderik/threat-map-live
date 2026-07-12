"""Threat Data Feeders - Generate and consume threat data."""

import random
import time
from datetime import datetime, timezone
from typing import Dict, List


class SimulatedThreatFeeder:
    """Generates simulated threat data for demonstration."""

    def __init__(self, rate: float = 1.0):
        self.rate = rate
        self.running = False
        self.threats = []

    def start_feeding(self, callback):
        self.running = True
        while self.running:
            threat = self._generate_threat()
            self.threats.append(threat)
            callback(threat)
            time.sleep(random.uniform(0.5 / self.rate, 2.0 / self.rate))

    def stop(self):
        self.running = False

    def _generate_threat(self) -> Dict:
        return {
            "id": f"sim-{int(time.time() * 1000)}-{random.randint(1000, 9999)}",
            "type": random.choice(["DDoS", "Brute Force", "SQL Injection", "Malware", "Phishing"]),
            "severity": random.choice(["low", "medium", "high", "critical"]),
            "source_ip": f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
            "dest_ip": f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
            "source_country": random.choice(["US", "CN", "RU", "DE", "BR", "IN"]),
            "dest_country": random.choice(["US", "UK", "FR", "JP", "AU"]),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


class LogFileFeeder:
    """Reads threat data from log files."""

    def __init__(self, log_path: str):
        self.log_path = log_path
        self.running = False

    def start_feeding(self, callback):
        self.running = True
        try:
            with open(self.log_path, "r") as f:
                f.seek(0, 2)
                while self.running:
                    line = f.readline()
                    if line:
                        threat = self._parse_line(line.strip())
                        if threat:
                            callback(threat)
                    else:
                        time.sleep(0.1)
        except FileNotFoundError:
            print(f"[!] Log file not found: {self.log_path}")

    def stop(self):
        self.running = False

    def _parse_line(self, line: str) -> Dict:
        if not line:
            return None
        return {
            "id": f"log-{hash(line) % 100000}",
            "raw": line,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
