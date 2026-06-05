# Calculator App — Live Deployed & Tested

A Calculator web application with a **live testing dashboard**, REST API, and tests across multiple Python testing frameworks.

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask dev server
python app.py
```

Open your browser to **http://localhost:5000**

> **macOS note:** Port 5000 is used by macOS Control Center's **AirPlay Receiver**,
> which responds with `HTTP ERROR 403 (Access to localhost was denied)`. Either turn it
> off (System Settings → General → AirDrop & Handoff → AirPlay Receiver) or run the app
> on a different port via the `PORT` env var:
>
> ```bash
> PORT=5001 python app.py   # then open http://localhost:5001
> ```

Dev-server environment variables (all optional):

| Var | Default | Purpose |
|-----|---------|---------|
| `PORT` | `5000` | Port to bind |
| `HOST` | `127.0.0.1` | Interface to bind (use `0.0.0.0` to expose externally) |
| `FLASK_DEBUG` | `0` | Set to `1` to enable debug/auto-reload |

### Production Deployment

```bash
# With Gunicorn
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5000
```

## 📐 Deployment Options

### Option 1: Heroku (Easiest)

```bash
# Install Heroku CLI, then:
heroku create your-app-name
git push heroku main
heroku open
```

### Option 2: Docker

```bash
docker build -t calculator-app .
docker run -p 5000:5000 calculator-app
```

### Option 3: Railway / Render / Fly.io

Push to GitHub → connect your repo → auto-deploy.

### Option 4: AWS EC2 / Lightsail

```bash
# On the server
sudo apt update && sudo apt install python3-pip docker.io -y
sudo systemctl start docker
sudo usermod -aG docker $USER
newgrp docker
docker build -t calculator-app .
docker run -d -p 5000:5000 --name calculator calculator-app
```

## 🌐 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET/POST | `/api/add?a=5&b=3` | Add |
| GET/POST | `/api/subtract?a=10&b=4` | Subtract |
| GET/POST | `/api/multiply?a=6&b=7` | Multiply |
| GET/POST | `/api/divide?a=15&b=3` | Divide |
| GET/POST | `/api/power?a=2&b=8` | Power |
| GET/POST | `/api/factorial?n=10` | Factorial |
| GET/POST | `/api/is_palindrome?text=racecar` | Palindrome check |
| GET/POST | `/api/fizz_buzz?n=15` | FizzBuzz |
| POST | `/api/calculate` | Unified (JSON body) |
| GET | `/api/health` | Health check |

### Unified API Example

```bash
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 5, "b": 3}'
```

## 🧪 Testing

### Run All Tests

```bash
# Unit tests (Python built-in)
python -m unittest test_calculator_unittest -v

# Pytest
pytest test_calculator_pytest.py -v

# Doctest
python -m doctest test_calculator_doctest.py -v
```

### Live Test Runner

Visit **http://localhost:5000** and click **"Run All Tests"** on the dashboard.
The dashboard runs unittest, pytest, doctest, and functional tests in real-time
and shows results with pass/fail counts.

## 📁 Project Structure

```
├── app.py                  # Flask server + API + test runner
├── calculator.py           # Application logic
├── templates/
│   └── dashboard.html      # Live testing UI
├── test_calculator_unittest.py   # unittest framework tests
├── test_calculator_pytest.py     # pytest framework tests
├── test_calculator_doctest.py    # Doctest tests
├── requirements.txt        # Python dependencies
├── Procfile                # Heroku deployment config
├── Dockerfile              # Container deployment config
└── README.md               # This file
```

## 🏗 Architecture

```
Browser (Dashboard UI)
    │
    ├──→ Flask API Server (app.py)
    │       ├── REST endpoints (/api/*)
    │       ├── Health check (/api/health)
    │       └── Live test runner (/api/run-tests)
    │               ├── unittest suite
    │               ├── pytest suite
    │               ├── doctest suite
    │               └── functional smoke tests
    │
    └──→ Calculator Module (calculator.py)
            ├── add, subtract, multiply, divide
            ├── power, factorial
            ├── is_palindrome, fizz_buzz
```
