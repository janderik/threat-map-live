"""Threat Map Live Server - Flask + WebSocket backend for real-time threat visualization."""

import json
import random
import time
import threading
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

try:
    from flask import Flask, render_template, send_from_directory
except ImportError:
    Flask = None

try:
    from flask_socketio import SocketIO, emit
except ImportError:
    SocketIO = None


# Simulated attack sources and destinations
ATTACK_TYPES = [
    "DDoS", "Brute Force", "SQL Injection", "XSS", "Ransomware",
    "Phishing", "C2 Communication", "Data Exfiltration", "Port Scan",
    "Malware Download", "APT", "Zero-Day Exploit",
]

COUNTRIES = [
    {"name": "United States", "code": "US", "lat": 39.8, "lon": -98.5},
    {"name": "China", "code": "CN", "lat": 35.8, "lon": 104.2},
    {"name": "Russia", "code": "RU", "lat": 61.5, "lon": 105.3},
    {"name": "Germany", "code": "DE", "lat": 51.2, "lon": 10.4},
    {"name": "United Kingdom", "code": "GB", "lat": 55.4, "lon": -3.4},
    {"name": "Brazil", "code": "BR", "lat": -14.2, "lon": -51.9},
    {"name": "India", "code": "IN", "lat": 20.6, "lon": 78.9},
    {"name": "Japan", "code": "JP", "lat": 36.2, "lon": 138.3},
    {"name": "South Korea", "code": "KR", "lat": 35.9, "lon": 127.8},
    {"name": "Netherlands", "code": "NL", "lat": 52.1, "lon": 5.3},
    {"name": "France", "code": "FR", "lat": 46.2, "lon": 2.2},
    {"name": "Canada", "code": "CA", "lat": 56.1, "lon": -106.3},
    {"name": "Australia", "code": "AU", "lat": -25.3, "lon": 133.8},
    {"name": "Iran", "code": "IR", "lat": 32.4, "lon": 53.7},
    {"name": "North Korea", "code": "KP", "lat": 40.3, "lon": 127.5},
    {"name": "Israel", "code": "IL", "lat": 31.0, "lon": 34.9},
    {"name": "Ukraine", "code": "UA", "lat": 48.4, "lon": 31.2},
    {"name": "Turkey", "code": "TR", "lat": 38.9, "lon": 35.2},
    {"name": "Vietnam", "code": "VN", "lat": 14.1, "lon": 108.3},
    {"name": "Indonesia", "code": "ID", "lat": -0.8, "lon": 113.9},
]


def generate_threat_event() -> Dict:
    """Generate a simulated threat event."""
    source = random.choice(COUNTRIES)
    dest = random.choice(COUNTRIES)
    while dest["code"] == source["code"]:
        dest = random.choice(COUNTRIES)

    return {
        "id": f"threat-{int(time.time() * 1000)}-{random.randint(1000, 9999)}",
        "type": random.choice(ATTACK_TYPES),
        "severity": random.choice(["low", "medium", "high", "critical"]),
        "source": {
            "country": source["name"],
            "code": source["code"],
            "lat": source["lat"] + random.uniform(-5, 5),
            "lon": source["lon"] + random.uniform(-5, 5),
            "ip": f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
        },
        "destination": {
            "country": dest["name"],
            "code": dest["code"],
            "lat": dest["lat"] + random.uniform(-3, 3),
            "lon": dest["lon"] + random.uniform(-3, 3),
            "ip": f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "confidence": random.randint(40, 100),
    }


class ThreatMapServer:
    """Flask + WebSocket server for real-time threat visualization."""

    def __init__(self, port: int = 5000, debug: bool = False):
        self.port = port
        self.debug = debug
        self.app = None
        self.socketio = None
        self.threat_sources: List[Callable] = []
        self.threat_history: List[Dict] = []
        self.stats = {
            "total_attacks": 0,
            "attacks_by_type": {},
            "attacks_by_country": {},
        }
        self._running = False

        if Flask and SocketIO:
            self._init_flask()
        else:
            print("[!] Flask or flask-socketio not installed. Running in simulation mode.")

    def _init_flask(self):
        self.app = Flask(__name__, template_folder="../static",
                         static_folder="../static")
        self.app.config["SECRET_KEY"] = "threat-map-secret"
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        @self.app.route("/")
        def index():
            return render_template("index.html")

        @self.app.route("/api/threats")
        def get_threats():
            return {"threats": self.threat_history[-100:], "stats": self.stats}

        @self.app.route("/api/stats")
        def get_stats():
            return self.stats

        @self.socketio.on("connect")
        def handle_connect():
            print("[+] Client connected")

        @self.socketio.on("request_threats")
        def handle_request():
            emit("threat_history", self.threat_history[-50:])

    def add_threat_source(self, name: str, source_func: Callable):
        self.threat_sources.append(source_func)

    def start(self):
        self._running = True

        feed_thread = threading.Thread(target=self._feed_threats, daemon=True)
        feed_thread.start()

        if self.app:
            print(f"[*] Starting Threat Map on port {self.port}")
            self.socketio.run(self.app, host="0.0.0.0", port=self.port,
                            debug=self.debug)
        else:
            print("[*] Running in simulation mode (no Flask)")
            try:
                while self._running:
                    self._feed_threats()
                    time.sleep(5)
            except KeyboardInterrupt:
                self._running = False

    def _feed_threats(self):
        while self._running:
            if self.threat_sources:
                for source in self.threat_sources:
                    try:
                        threats = source()
                        for threat in threats:
                            self._process_threat(threat)
                    except Exception:
                        pass
            else:
                threat = generate_threat_event()
                self._process_threat(threat)

            time.sleep(random.uniform(0.5, 3.0))

    def _process_threat(self, threat: Dict):
        self.threat_history.append(threat)
        if len(self.threat_history) > 10000:
            self.threat_history = self.threat_history[-5000:]

        self.stats["total_attacks"] += 1
        attack_type = threat.get("type", "unknown")
        self.stats["attacks_by_type"][attack_type] = \
            self.stats["attacks_by_type"].get(attack_type, 0) + 1
        country = threat.get("source", {}).get("country", "Unknown")
        self.stats["attacks_by_country"][country] = \
            self.stats["attacks_by_country"].get(country, 0) + 1

        if self.socketio:
            self.socketio.emit("new_threat", threat)

    def stop(self):
        self._running = False
