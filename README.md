# 🚀 Flask App Deployment on Minikube using Kubernetes

This repository contains a simple Flask application containerized with Docker and deployed on **Minikube Kubernetes Cluster**.  
The application is exposed externally using a **NodePort Service**.

---

## 📌 Project Overview

This project demonstrates:

- Building a Docker image for a Flask app
- Loading the Docker image into Minikube
- Creating a Kubernetes Deployment (2 replicas)
- Exposing the Flask app using a NodePort service

---

## 📂 Project Structure

```
.
├── app.py
├── requirements.txt
├── Dockerfile
├── deployment.yml
└── service.yml
```

---

## ✅ Step 1: Install Docker, Kubectl & Minikube

```bash
sudo apt update
sudo apt install docker.io -y

sudo usermod -aG docker ubuntu
sudo systemctl status docker

# Remove wrong kubectl binary if exists
sudo rm -f /usr/local/bin/kubectl

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/kubectl
kubectl version --client --output=yaml

sudo apt install -y curl wget apt-transport-https ca-certificates conntrack

# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

minikube version
```

---

## 🧑‍💻 Step 2: Flask App Code

### **app.py**

```python
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    name = os.environ.get("GREETING_TARGET", "World")
    return f"Hello, {name}!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
```

### **requirements.txt**

```
flask
```

---

## 📦 Step 3: Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV GREETING_TARGET="Docker User"

CMD ["python", "app.py"]
```

---

## 🧱 Step 4: Build Image inside Minikube

```bash
eval $(minikube docker-env)
docker build -t ganesh/pythonapp .
```

---

## 🚀 Step 5: Kubernetes Deployment

### **deployment.yml**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
  labels:
    app: python-flask-label
spec:
  replicas: 2
  selector:
    matchLabels:
      app: python-flask-label
  template:
    metadata:
      labels:
        app: python-flask-label
    spec:
      containers:
      - name: flask-app
        image: ganesh/pythonapp
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
```

Apply deployment:

```bash
kubectl apply -f deployment.yml
kubectl get pods
```

---

## 🌐 Step 6: NodePort Service

### **service.yml**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
spec:
  type: NodePort
  selector:
    app: python-flask-label
  ports:
    - port: 80
      targetPort: 8000
      nodePort: 30007
```

Apply Service:

```bash
kubectl apply -f service.yml
kubectl get svc
```

---

## 🌍 Step 7: Access Application

```bash
minikube ip
```

Open in browser:

```
http://<minikube-ip>:30007
```

Example:

```
http://192.168.49.2:30007
```

---

## 🧹 Cleanup

```bash
kubectl delete -f service.yml
kubectl delete -f deployment.yml
```

---

## ⭐ Summary

| Step | Completed |
|------|------------|
| Dockerized Flask App | ✅ |
| Deployed on Kubernetes | ✅ |
| Exposed via NodePort | ✅ |
| Accessed on Browser | ✅ |

---

If this helped you, ⭐ star the project on GitHub!
