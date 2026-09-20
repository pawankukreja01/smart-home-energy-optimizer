# 🏠 AI Smart Home Energy Optimizer

An AI-powered smart home energy management system that monitors device energy consumption, detects abnormal usage, generates recommendations, automatically responds to selected anomalies, and tracks energy and estimated cost savings.

The project combines **IoT simulation, Django REST APIs, machine learning, automation, energy analytics, and a Vue.js dashboard** into an end-to-end smart home energy optimization platform.

---

## 🚀 Overview

Smart home devices continuously consume energy, but unusual or excessive consumption can be difficult to identify manually.

This project demonstrates an intelligent energy-management workflow:

```text
IoT Device Simulator
        ↓
Django REST API
        ↓
Energy Readings
        ↓
AI Anomaly Detection
        ↓
Recommendation Engine
        ↓
Automation Engine
        ↓
Energy Savings Tracking
        ↓
Vue.js Dashboard
```

The system can detect unusual energy consumption, generate recommendations, automatically control selected simulated devices, and track the energy and estimated cost saved as a result.

---

## ✨ Features

### 📡 IoT Device Simulation

The project includes an IoT simulator that continuously generates energy readings for simulated smart-home devices.

Currently simulated devices include:

- 💡 Living Room Light
- ❄️ Living Room AC
- 📺 Bedroom TV
- 💡 Kitchen Light

The simulator generates power consumption based on the device type and current state.

---

### 🤖 AI-Powered Anomaly Detection

The system combines **device-specific energy ranges** with the **Isolation Forest** unsupervised machine-learning algorithm from Scikit-learn to identify unusual energy consumption.

Device-specific ranges provide domain knowledge about expected consumption, while Isolation Forest identifies statistically unusual observations within the available readings.

For example:

```text
Normal AC consumption:
700W - 1000W

Detected:
Living Room AC → 1741.66W

Result:
🚨 Abnormal energy consumption detected
```

---

### 💡 Recommendation Engine

After detecting an anomaly, the system generates an actionable recommendation.

Example:

```text
Abnormally high AC consumption detected.

Recommendation:
Reduce AC load or inspect the unit for abnormal power consumption.

Potential saving:
741.66W
```

---

### ⚡ Automated Device Control

For selected anomaly scenarios, the automation engine can automatically control the simulated device.

Example:

```text
AC consumption
1741.66W
      ↓
AI anomaly detection
      ↓
Recommendation
      ↓
Automation triggered
      ↓
AC switched OFF
      ↓
Power reduced to 0W
```

The system records the automation action together with:

- Reason for the action
- Power before the action
- Power after the action
- Potential power saving

---

### 💰 Energy Savings Tracking

The system tracks the duration of an automation intervention and calculates:

- Potential power avoided
- Duration of the intervention
- Energy saved in kWh
- Estimated electricity cost saved
- Start timestamp
- End timestamp
- Associated automation action

Example:

```text
Power avoided:       741.66W
Duration:            0.2287 hours
Energy saved:        0.1696 kWh
Estimated cost:      £0.0509
```

When an automated device is switched back on, the system closes the active saving period and calculates the actual energy and estimated cost savings based on the intervention duration.

---

### 📊 Interactive Energy Dashboard

The Vue.js dashboard provides a visual overview of the smart-home environment.

It includes:

- Current power consumption
- Active devices
- AI anomaly alerts
- Power avoided
- Energy consumption history
- Energy saved
- Estimated cost saved
- Automation actions
- Savings history
- Device status
- Device ON/OFF controls

---

## 🧠 Machine Learning

The project uses the **Isolation Forest** algorithm for anomaly detection.

Isolation Forest is an unsupervised learning technique that is useful for identifying unusual observations without requiring a large labelled anomaly dataset.

The detection workflow is:

```text
Energy Readings
      ↓
Group readings by device
      ↓
Check device-specific normal range
      ↓
Isolation Forest
      ↓
Identify unusual consumption
      ↓
Generate anomaly information
```

The project combines machine-learning detection with domain-specific energy ranges to make anomaly detection more suitable for the simulated smart-home environment.

---

## 🏗️ System Architecture

```text
                         SMART HOME
                             │
                             ▼
                     ┌─────────────────┐
                     │ IoT Simulator   │
                     │                 │
                     │ Simulated       │
                     │ Devices         │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Django REST API │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Energy Database │
                     │     SQLite      │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ AI Analytics    │
                     │                 │
                     │ IsolationForest │
                     └────────┬────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ Recommendation       │
                   │ Engine               │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ Automation Engine    │
                   │                      │
                   │ Device Control       │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ Energy Savings       │
                   │ Tracking             │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │ Vue.js Dashboard     │
                   └──────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend

- Python
- Django
- Django REST Framework
- SQLite
- Requests

### Machine Learning & Data

- Pandas
- Scikit-learn
- Isolation Forest

### Frontend

- Vue.js
- Vite
- Axios
- Chart.js
- Vue-Chartjs

### Architecture

- REST API
- IoT device simulation
- Machine-learning anomaly detection
- Recommendation engine
- Automated device control
- Energy savings analytics
- Interactive data visualization

---

## 📁 Project Structure

```text
smart-home-energy-optimizer/
│
├── automation/
│   ├── __init__.py
│   └── automation_engine.py
│
├── backend/
│   ├── manage.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   └── devices/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── admin.py
│       └── migrations/
│
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   ├── EnergyChart.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── ml/
│   └── anomaly_detector.py
│
├── recommendations/
│   ├── __init__.py
│   └── recommendation_engine.py
│
├── simulator/
│   └── simulator.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

Make sure you have:

- Python 3.13+
- Node.js
- npm
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/pawankukreja01/smart-home-energy-optimizer.git
```

Navigate into the project:

```bash
cd smart-home-energy-optimizer
```

---

### 2. Create a Python Virtual Environment

```bash
python3 -m venv .venv
```

Activate it.

#### macOS / Linux

```bash
source .venv/bin/activate
```

#### Windows

```powershell
.venv\Scripts\activate
```

---

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run Database Migrations

Navigate to the backend:

```bash
cd backend
```

Run:

```bash
python3 manage.py migrate
```

---

### 5. Create the Initial Devices

Start the Django development server:

```bash
python3 manage.py runserver
```

Open another terminal and activate the virtual environment.

From the project root:

```bash
source .venv/bin/activate
```

Navigate to the backend:

```bash
cd backend
```

Open the Django shell:

```bash
python3 manage.py shell
```

Create the initial simulated devices:

```python
from devices.models import Device

Device.objects.create(
    name="Living Room Light",
    device_type="light",
    room="Living Room",
    is_on=True,
    power_watts=40
)

Device.objects.create(
    name="Living Room AC",
    device_type="ac",
    room="Living Room",
    is_on=True,
    power_watts=850
)

Device.objects.create(
    name="Bedroom TV",
    device_type="tv",
    room="Bedroom",
    is_on=False,
    power_watts=0
)

Device.objects.create(
    name="Kitchen Light",
    device_type="light",
    room="Kitchen",
    is_on=False,
    power_watts=0
)
```

Exit the Django shell:

```python
exit()
```

---

## ▶️ Running the Backend

From the `backend` directory:

```bash
python3 manage.py runserver
```

The Django API will normally be available at:

```text
http://127.0.0.1:8000/
```

---

## 🌐 Running the Frontend

Open a new terminal and navigate to the frontend:

```bash
cd smart-home-energy-optimizer/frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The Vue dashboard will normally be available at:

```text
http://localhost:5173/
```

If port `5173` is already in use, Vite may automatically start on another available port, such as `5174`.

---

## 📡 Running the IoT Simulator

Open another terminal.

From the project root:

```bash
source .venv/bin/activate
```

Then run:

```bash
python3 simulator/simulator.py
```

The simulator will continuously send energy readings to the Django API.

Example:

```text
🏠 Smart Home IoT Simulator Started
------------------------------------
📡 Living Room Light: 42.31W
📡 Living Room AC: 847.26W
📡 Bedroom TV: 0W
📡 Kitchen Light: 0W
------------------------------------
```

---

## 🤖 Running AI Anomaly Detection

With the Django server running and the simulator generating readings, open another terminal.

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Then run:

```bash
python3 ml/anomaly_detector.py
```

The system analyses recent energy readings and identifies unusual consumption.

Example:

```text
🤖 AI ENERGY ANALYSIS
---------------------

🚨 Living Room AC: 1741.66W
💡 Recommendation: Reduce AC load or inspect the unit for abnormal power consumption.
⚡ Potential saving: 741.66W

🤖 Automation: Living Room AC switched OFF.
```

---

## 🎬 Controlled Demo Mode

The simulator supports a controlled demonstration mode that intentionally generates unusually high AC consumption.

### macOS / Linux

Run:

```bash
DEMO_MODE=1 python3 simulator/simulator.py
```

In demo mode, the simulated AC generates approximately:

```text
1500W - 1800W
```

instead of its normal consumption range.

This makes it possible to reliably demonstrate the complete workflow:

```text
Abnormal consumption
        ↓
AI detection
        ↓
Recommendation
        ↓
Automation
        ↓
Device switched OFF
        ↓
Energy saving tracked
```

---

## 🔌 API Endpoints

### Devices

```text
GET     /api/devices/
POST    /api/devices/
PATCH   /api/devices/{id}/
```

### Energy Readings

```text
GET     /api/energy-readings/
POST    /api/energy-readings/
```

### Analytics

```text
GET     /api/analytics/
GET     /api/energy-history/
```

### Automation

```text
GET     /api/automation-history/
```

### Energy Savings

```text
GET     /api/energy-savings/
GET     /api/energy-savings-analytics/
```

---

## 🔄 Example End-to-End Workflow

### 1. Normal Operation

The simulated AC operates within its normal range:

```text
Living Room AC
850W
```

No anomaly is detected.

---

### 2. Abnormal Consumption

The simulator generates an unusually high reading:

```text
Living Room AC
1741.66W
```

---

### 3. AI Detection

The anomaly detection system identifies the unusual consumption.

```text
🚨 AI anomaly detected
```

---

### 4. Recommendation

The recommendation engine evaluates the anomaly and calculates the potential saving:

```text
1741.66W - 1000W
= 741.66W potential saving
```

---

### 5. Automation

The automation engine switches the simulated AC OFF:

```text
1741.66W → 0W
```

---

### 6. Savings Tracking

The system records the intervention and starts tracking the saving period.

When the device is switched back ON, the system calculates:

```text
Duration
   ↓
Energy saved (kWh)
   ↓
Estimated electricity cost saved
```

---

## 📊 Example Result

A simulated intervention can produce a result such as:

```text
Device:
Living Room AC

Power before:
1741.66W

Power after:
0W

Potential power saving:
741.66W

Energy saved:
0.1696 kWh

Estimated cost saved:
£0.0509
```

The energy and cost figures depend on the actual duration of the intervention.

---

## 🎯 Engineering Concepts Demonstrated

This project demonstrates practical implementation of:

- Python software development
- Django REST API development
- RESTful architecture
- Database modelling
- Machine learning
- Unsupervised anomaly detection
- Data processing with Pandas
- Scikit-learn
- IoT device simulation
- Automated decision-making
- Device state management
- Energy analytics
- Vue.js frontend development
- Interactive data visualization
- Backend/frontend integration
- API-driven architecture

---

## 🎯 Why This Project?

This project explores the intersection of:

- Artificial intelligence
- Software engineering
- IoT and home automation
- Energy analytics
- Intelligent automation

It demonstrates how machine-learning insights can be connected to device control through a REST-based software architecture.

---

## 🔮 Future Improvements

The current project uses simulated IoT devices, but the architecture can be extended to physical smart-home hardware.

Potential improvements include:

- MQTT integration
- ESP32 integration
- Raspberry Pi integration
- Smart plug integration
- Real energy sensors
- Real-time WebSocket updates
- More advanced anomaly detection
- Device-specific machine-learning models
- Energy consumption forecasting
- Occupancy-aware automation
- Automated energy scheduling
- Dynamic electricity pricing
- Solar energy integration
- Cloud deployment
- Mobile application

The simulator can be replaced or extended with physical IoT devices while keeping the core backend, machine-learning, automation, and dashboard architecture.

---

## ⚠️ Project Scope

This project currently uses **simulated IoT devices** rather than physical smart-home hardware.

The purpose is to demonstrate an end-to-end software architecture for intelligent energy monitoring and automation.

The simulator can later be replaced or extended with real IoT devices and communication protocols such as MQTT.

---

## 🔐 Security & Configuration

The project is intended for local development and demonstration.

For production deployment, the following should be added:

- Environment variables for configuration
- Secure secret management
- Production database
- Authentication and authorization
- HTTPS
- API rate limiting
- Secure device communication
- Production deployment configuration

---


## 👨‍💻 Author

**Pawan Kukreja**

MSc Artificial Intelligence & Data Science  
University of Hull

Software Engineer | AI & Data Science | IoT & Home Automation

---

## ⭐ Project

**AI + IoT + Automation + Energy Analytics**

Built as a portfolio project to explore intelligent smart-home energy management and demonstrate the integration of machine learning, backend engineering, automation, and interactive data visualization.
