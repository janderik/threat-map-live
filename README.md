# Threat Map Live

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![WebSocket](https://img.shields.io/badge/WebSocket-real--time-blue)]()

A real-time threat visualization dashboard that displays live cyber attacks on an interactive world map using D3.js and Leaflet.

## Architecture

```
threat-map-live/
├── src/
│   ├── server/          # Flask + WebSocket backend
│   ├── static/          # Frontend (HTML/JS/CSS)
│   │   ├── index.html
│   │   ├── js/
│   │   └── css/
│   └── data/            # Threat data feeders
├── app.py               # Application entry point
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── setup.py
```

## Features

- **Real-Time Updates**: WebSocket-based live threat feed
- **Interactive Map**: Leaflet.js world map with attack visualization
- **Attack Animations**: Animated attack lines between source and destination
- **Statistics Dashboard**: Live counters and charts
- **Multiple Data Sources**: Integration with threat intelligence feeds
- **Geolocation**: IP to geolocation mapping
- **Filtering**: Filter by attack type, severity, country
- **Responsive Design**: Works on desktop and mobile

## Live Map Architecture

```
┌──────────────────────────────────────────────────────┐
│                    Frontend                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │   Leaflet    │  │   D3.js      │  │ Stats      │  │
│  │    Map       │  │   Charts     │  │ Dashboard  │  │
│  └─────────────┘  └──────────────┘  └────────────┘  │
│                       │                              │
│                  WebSocket Client                    │
└───────────────────────┬──────────────────────────────┘
                        │
              ┌─────────┴─────────┐
              │    WebSocket      │
              │     Server       │
              └─────────┬─────────┘
                        │
┌───────────────────────┴──────────────────────────────┐
│                    Backend                           │
│  ┌──────────────┐  ┌────────────┐  ┌──────────────┐ │
│  │ Threat Feed   │  │  GeoIP     │  │  WebSocket   │ │
│  │  Engine      │  │  Resolver  │  │   Handler    │ │
│  └──────────────┘  └────────────┘  └──────────────┘ │
└──────────────────────────────────────────────────────┘
```

## Installation

```bash
git clone https://github.com/janderik/threat-map-live.git
cd threat-map-live
pip install -r requirements.txt
```

## Usage

```bash
# Start the server
python app.py

# Access the dashboard
open http://localhost:5000
```

## Python API

```python
from src.server.engine import ThreatMapServer

server = ThreatMapServer(port=5000)
server.add_threat_source("custom", lambda: get_threats())
server.start()
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.
