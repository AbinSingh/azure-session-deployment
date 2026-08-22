# ⚡ From Electromagnetic Waves to AKS

## Understanding What Actually Happens When a Web Request Reaches an Application

This project started with a simple question:

> **How do sessions and authentication actually work?**

Instead of starting with a framework tutorial, I decided to understand the journey from the bottom up — from physical signals and networking concepts to HTTP, FastAPI, Redis, containers, Kubernetes, and a distributed application running on Azure AKS.

The goal was not just to make the application work, but to understand **why each layer exists, what problem it solves, and how to debug it when something goes wrong.**

---

## 🧭 The Journey

```text
⚡ Electromagnetic Waves
        ↓
🔌 Voltage Levels
        ↓
🔢 Bits
        ↓
🧩 OSI / Networking Layers
        ↓
🌐 DNS
        ↓
📦 TCP/IP
        ↓
🔗 Sockets & Ports
        ↓
🔐 TLS
        ↓
🌍 HTTP
        ↓
🚀 Uvicorn → ASGI → FastAPI
        ↓
🔐 Sessions
        ↓
🔴 Redis
        ↓
🐳 Docker
        ↓
☁️ Azure Container Registry
        ↓
☸️ Azure Kubernetes Service
        ↓
🔄 Distributed Application
```

This is the mental model behind the project.

---

# 🎯 What I Wanted to Understand

The project began with authentication and sessions.

But instead of treating FastAPI's authentication/session mechanisms as a black box, I wanted to answer questions such as:

* How does a user's request actually reach an application?
* How are bits transmitted across a network?
* How does DNS resolve a hostname?
* How does a TCP connection reach the correct process?
* What is a socket?
* What role does a port play?
* What happens during a TLS connection?
* What does an HTTP request actually contain?
* How does Uvicorn receive the request?
* How does ASGI connect the server to FastAPI?
* Where should session state live?
* What happens when there are multiple application processes?
* What happens when there are multiple Kubernetes replicas?
* Why should application pods be stateless?
* How does Redis solve the shared-state problem?

---

# 🏗️ Application Evolution

The application evolved incrementally.

### 1. Minimal FastAPI Application

Started with a simple FastAPI application and explored how HTTP requests reach application code.

```text
Client
  ↓
HTTP Request
  ↓
Uvicorn
  ↓
ASGI
  ↓
FastAPI
  ↓
Application
```

---

### 2. Authentication & Sessions

Added:

* Authentication
* Session generation
* Session storage
* HttpOnly cookies
* Session middleware
* Protected endpoints
* Logout
* Session expiration

Initially, session state was stored in a Python dictionary.

```text
Application Process
        ↓
Python Dictionary
        ↓
Session State
```

This worked for a single process, but introduced an important scalability problem.

---

# ⚠️ The Multiple-Process Problem

Consider:

```text
             Load Balancer
                  ↓
          ┌───────┴───────┐
          ↓               ↓
      Process 1        Process 2
          ↓               ↓
     Session Store 1  Session Store 2
```

A user might log in through Process 1:

```text
Login Request
     ↓
Process 1
     ↓
Session created
     ↓
Stored in Process 1 memory
```

The next request could reach Process 2:

```text
Authenticated Request
        ↓
    Process 2
        ↓
Session not found ❌
```

The application cannot rely on local process memory for shared session state.

This led to the next step.

---

# 🔴 Redis

I introduced Redis as an external session store.

```text
             ┌───────────────┐
             │    Redis      │
             │ Session Store │
             └───────┬───────┘
                     ↑
              ┌──────┴──────┐
              │             │
          Process 1      Process 2
```

Now both processes can access the same session state.

I also explored Redis directly using:

```bash
redis-cli
```

and investigated:

* Redis commands
* Key/value storage
* Session keys
* Expiration
* TTL
* RESP (Redis Serialization Protocol)

The goal was to understand Redis rather than simply configure it.

---

# 🐳 Docker

The application was then containerized.

```text
FastAPI Application
        ↓
      Docker
        ↓
   Container Image
```

This provided a consistent runtime environment and prepared the application for deployment to Kubernetes.

---

# ☁️ Azure Container Registry

The Docker image was pushed to Azure Container Registry.

```text
Developer Machine
       ↓
     Docker
       ↓
 Container Image
       ↓
Azure Container Registry
       ↓
      AKS
```

ACR acts as the image registry from which AKS can retrieve the application image.

---

# ☸️ Azure Kubernetes Service

The application was deployed to Azure Kubernetes Service.

The architecture became:

```text
                         Internet
                            ↓
                     Load Balancer
                            ↓
                  Kubernetes Service
                     ↙           ↘
              FastAPI Pod 1   FastAPI Pod 2
                     ↘           ↙
                    Azure Managed Redis
```

The application can now run with multiple replicas.

A request may reach Pod 1:

```text
Request → Pod 1 → Redis
```

while the next request may reach Pod 2:

```text
Request → Pod 2 → Redis
```

The session remains available because the state is stored externally.

---

# 🔄 Stateless Application Architecture

This led to one of the most important concepts in the project:

> **Application pods should be stateless. Shared state belongs in an external store.**

Instead of:

```text
Pod 1 → Local Session State
Pod 2 → Local Session State
Pod 3 → Local Session State
```

the architecture becomes:

```text
Pod 1 ──┐
Pod 2 ──┼──→ Azure Managed Redis
Pod 3 ──┘
```

This allows application replicas to be replaced, restarted, or scaled without losing shared session state.

---

# 🔍 Debugging & Investigation

I didn't want to treat the networking and infrastructure layers as black boxes.

I used different tools to investigate what was actually happening.

| Tool                        | What I Used It For                     |
| --------------------------- | -------------------------------------- |
| `nslookup`                  | DNS resolution                         |
| `ping` / connectivity tests | Network reachability                   |
| `curl`                      | HTTP requests and responses            |
| TLS/SSL verification        | Certificates and encrypted connections |
| `redis-cli`                 | Redis and session state                |
| `docker`                    | Containers and images                  |
| `az` CLI                    | Azure resources                        |
| `kubectl`                   | Kubernetes resources                   |
| AKS logs                    | Application and container debugging    |

The idea was:

> **Don't just make it work. Understand what is happening underneath and have the tools to prove where something is failing.**

---

# 🧰 Technologies Used

### Application

* Python
* FastAPI
* Uvicorn
* ASGI

### Authentication & State

* Sessions
* HttpOnly Cookies
* Redis
* Azure Managed Redis

### Containerization

* Docker

### Azure

* Azure Container Registry (ACR)
* Azure Kubernetes Service (AKS)
* Azure CLI

### Kubernetes

* Pods
* Deployments
* Services
* Replicas
* Logs

### Networking

* OSI model
* DNS
* TCP/IP
* Sockets
* Ports
* HTTP
* TLS/SSL

---

# 🚀 Running Locally

## Prerequisites

Install:

* Python
* Docker
* Redis

Optional tools for deeper investigation:

* `redis-cli`
* `curl`
* `nslookup`

---

## Clone the Repository

```bash
git clone https://github.com/AbinSingh/azure-session-deployment.git

cd azure-session-deployment
```

Checkout the project branch if required:

```bash
git checkout session-aks
```

---

## Create a Python Environment

```bash
python -m venv .venv
```

Activate it.

### Linux/macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔴 Run Redis Locally

Start Redis using Docker:

```bash
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis
```

Verify:

```bash
redis-cli ping
```

Expected:

```text
PONG
```

---

# 🚀 Run FastAPI

Start the application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The application should now be available locally.

You can test it using:

```bash
curl http://localhost:8000
```

---

# 🐳 Build the Docker Image

```bash
docker build -t fastapi-session-app .
```

Run:

```bash
docker run -p 8000:8000 fastapi-session-app
```

---

# ☁️ Azure Deployment

The deployment flow is:

```text
Source Code
    ↓
Docker Build
    ↓
Docker Image
    ↓
Azure Container Registry
    ↓
AKS
    ↓
FastAPI Pods
    ↓
Azure Managed Redis
```

Azure CLI is used to manage the Azure resources and deployment workflow.

---

# ☸️ AKS Deployment

The Kubernetes deployment consists of the application components required to run multiple FastAPI replicas.

Conceptually:

```text
                 Azure Load Balancer
                         ↓
                  Kubernetes Service
                         ↓
              ┌──────────┴──────────┐
              ↓                     ↓
         FastAPI Pod 1         FastAPI Pod 2
              │                     │
              └──────────┬──────────┘
                         ↓
                 Azure Managed Redis
```

The important architectural property is that **session state does not live inside the pods**.

---

# 🧠 Key Learnings

This project started as a question about authentication.

It eventually became a study of the entire request path.

The biggest lessons were:

### 1. Abstractions hide complexity

FastAPI makes HTTP application development easy, but underneath it are ASGI, sockets, TCP/IP, networking, TLS, and physical communication.

### 2. Local memory is not shared state

A Python dictionary is fine for a simple single-process application, but it doesn't provide shared state across replicas.

### 3. External state enables stateless application instances

Redis allows multiple application instances to share session state.

### 4. Containers provide packaging and consistency

Docker packages the application and its runtime dependencies into a deployable unit.

### 5. Kubernetes provides orchestration

AKS allows the application to run multiple replicas and provides mechanisms for networking, scaling, and managing those replicas.

### 6. Debugging requires understanding the layers

When something fails, the problem could be DNS, connectivity, TLS, HTTP, the application, Redis, Docker, Kubernetes, or Azure infrastructure.

Understanding the layers makes troubleshooting much more systematic.

---

# 🔬 The Mental Model

The most important outcome of this project is this mental model:

```text
Physical World
      ↓
Electromagnetic Signals
      ↓
Voltage Levels
      ↓
Bits
      ↓
Networking
      ↓
TCP/IP
      ↓
Sockets & Ports
      ↓
DNS / TLS / HTTP
      ↓
Uvicorn
      ↓
ASGI
      ↓
FastAPI
      ↓
Authentication / Sessions
      ↓
Redis
      ↓
Docker
      ↓
ACR
      ↓
AKS
      ↓
Multiple Application Replicas
      ↓
Distributed Application
```

The journey changed the question from:

> **How do I implement sessions?**

to:

> **What actually happens when a user's request reaches a distributed application?**

That shift in perspective is the main purpose of this project.

---

# 🚧 Next Steps

The next stage of the project is focused on further production hardening:

* Azure Key Vault
* AKS Workload Identity
* Secret management
* Identity-based access
* Further security hardening
* Production-oriented configuration

---

# 📌 Project

**GitHub:** https://github.com/AbinSingh/azure-session-deployment

Branch:

```text
session-aks
```

---

# 📚 Why This Project Exists

This is a learning-by-building project.

The objective is not to demonstrate a production-ready authentication framework.

The objective is to build a deeper mental model of:

**Networking → Web Applications → Authentication → State → Containers → Kubernetes → Distributed Systems**

and to understand the engineering problems that appear as a simple application evolves into a distributed application.

---

## ⚡ Final Takeaway

> **Don't just learn the framework. Learn the layers underneath the framework.**

> **Don't just make the deployment work. Understand why it works.**

> **And when it breaks, know which layer to investigate.**

#FastAPI #Redis #Azure #AKS #Docker #Kubernetes #Networking #SystemDesign #CloudComputing #SoftwareEngineering
