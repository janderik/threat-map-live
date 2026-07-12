"""Threat Map Live - Application Entry Point."""

import argparse
from src.server import ThreatMapServer


def main():
    parser = argparse.ArgumentParser(description="Threat Map Live - Real-time threat visualization")
    parser.add_argument("--port", type=int, default=5000, help="Server port")
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    args = parser.parse_args()

    server = ThreatMapServer(port=args.port, debug=args.debug)
    print("[*] Threat Map Live starting...")
    print(f"[*] Dashboard: http://localhost:{args.port}")
    server.start()


if __name__ == "__main__":
    main()
