# 🤖 AI Self-Healing Infrastructure Platform

## 📌 Overview

This project is an **AI-powered self-healing system** designed to automatically detect, analyze, and fix issues in a Kubernetes-based application environment.

It integrates **monitoring, AI decision-making, and automated remediation** to reduce manual intervention in DevOps workflows.

---

## 🚀 Features

* 📊 **Real-time Monitoring**

  * Detects issues like pod crashes (CrashLoopBackOff)
* 🧠 **AI Decision Engine**

  * Analyzes alerts and determines corrective actions
* ⚙️ **Automated Remediation**

  * Executes fixes like restarting pods using Kubernetes API
* 🔔 **Notification System**

  * Sends alerts after action execution
* 🔁 **Feedback Loop (Future Scope)**

  * Learns from past incidents to improve decisions

---

## 🏗️ Architecture

```
Monitoring Service → AI Engine → Execution Service → Notification Service
```

---

## 🧩 Microservices

### 1. Monitoring Service

* Receives alerts
* Forwards to AI engine

### 2. AI Engine Service

* Analyzes alerts
* Decides action (rule-based for MVP)

### 3. Execution Service

* Executes actions (e.g., restart pod)

### 4. Notification Service

* Sends alerts/logs after execution

---

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI
* **DevOps:** Docker, Kubernetes
* **Monitoring:** Prometheus (planned)
* **AI:** OpenAI / LLM (planned)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/<your-username>/ai-self-healing-platform.git
cd ai-self-healing-platform
```

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```
cd monitoring-service && pip install -r requirements.txt
cd ../ai-engine-service && pip install -r requirements.txt
cd ../execution-service && pip install -r requirements.txt
cd ../notification-service && pip install -r requirements.txt
```

---

## ▶️ Run Services Locally

Open 4 terminals:

```
uvicorn app:app --port 8001   # monitoring-service
uvicorn app:app --port 8002   # ai-engine-service
uvicorn app:app --port 8003   # execution-service
uvicorn app:app --port 8004   # notification-service
```

---

## 🧪 Test the System

```
curl -X POST http://localhost:8001/alert \
-H "Content-Type: application/json" \
-d "{\"error\": \"CrashLoopBackOff\"}"
```

---

## 📈 Future Enhancements

* 🔥 Integrate Prometheus Alertmanager
* 🤖 Replace rule-based logic with LLM
* ☸️ Deploy on Kubernetes
* 📊 Add dashboard (Grafana / React)
* 🔐 Add RBAC for secure execution

---

## 🎯 Use Cases

* Automated incident response
* DevOps productivity improvement
* Self-healing cloud infrastructure

---

## 👨‍💻 Author

Vikrant Kumar

---

## ⭐ If you like this project

Give it a star ⭐ and feel free to contribute!
