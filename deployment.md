# 🚀 Azure VM Deployment Guide — Docker & Port 8080

This guide provides step-by-step instructions to build, push to **Docker Hub**, and run the **Django 8-Puzzle Game** on your **Azure Virtual Machine (VM)** on port **8080**.

---

## 📋 Overview of Workflow

```text
[Local Machine]
  │
  ├── 1. Build Docker Image  ──> `docker build -t <your-dockerhub-username>/puzzle-game:latest .`
  └── 2. Push to Docker Hub  ──> `docker push <your-dockerhub-username>/puzzle-game:latest`

[Azure Portal]
  └── 3. Open Inbound Port 8080 in Network Security Group (NSG)

[Azure VM via SSH]
  ├── 4. Pull Image from Docker Hub ──> `docker pull <your-dockerhub-username>/puzzle-game:latest`
  └── 5. Run Container on Port 8080 ──> `docker run -d -p 8080:8080 ...`
```

---

## 🛠️ Step 1: Build & Push Image to Docker Hub (From Local Machine)

### 1.1 Log in to Docker Hub

```bash
docker login
```
*(Enter your Docker Hub username and password/access token when prompted)*

### 1.2 Using the Makefile (Quick Shortcuts)

You can use the provided `Makefile` to quickly build, push, and test:

```bash
# Build Docker image
make build

# Build and push to Docker Hub
make push

# Run locally on port 8080
make run

# Stop local container
make stop

# View live logs
make logs
```

### 1.3 Manual Build & Push (Alternative)

Replace `<your-dockerhub-username>` with your actual Docker Hub username:

```bash
docker build -t <your-dockerhub-username>/puzzle-game:latest .
```

> **Tip for Multi-Arch (e.g. M1/M2/M3 Mac to x86_64 Azure VM):**  
> If you are building on ARM64 and your Azure VM is x86_64/amd64:
> ```bash
> docker buildx build --platform linux/amd64 -t <your-dockerhub-username>/puzzle-game:latest --push .
> ```

### 1.3 Push Image to Docker Hub

```bash
docker push <your-dockerhub-username>/puzzle-game:latest
```

---

## ☁️ Step 2: Open Port 8080 on Azure VM (Network Security Group)

To allow web traffic to reach port 8080 on your Azure VM:

1. Log in to the **[Azure Portal](https://portal.azure.com/)**.
2. Navigate to **Virtual Machines** and select your VM.
3. In the left menu under **Settings**, click on **Networking** (or **Network settings**).
4. Click **"Add inbound port rule"** (or **"Create port rule"**).
5. Fill in the following details:
   - **Source**: `Any`
   - **Source port ranges**: `*`
   - **Destination**: `Any`
   - **Destination port ranges**: `8080`
   - **Protocol**: `TCP`
   - **Action**: `Allow`
   - **Priority**: `310` (or any available priority number, e.g., 300–400)
   - **Name**: `Allow-Port-8080`
6. Click **Add**.

---

## 💻 Step 3: Connect to your Azure VM

Open PowerShell, Command Prompt, or Terminal and SSH into your Azure VM:

```bash
ssh azureuser@<YOUR_AZURE_VM_PUBLIC_IP>
```
*(Replace `azureuser` and `<YOUR_AZURE_VM_PUBLIC_IP>` with your VM credentials and public IP address)*

---

## 🐳 Step 4: Install Docker on Azure VM (If Not Already Installed)

If Docker is not yet installed on your Azure Ubuntu/Debian VM, run this quick script:

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Allow running docker without sudo
sudo usermod -aG docker $USER
newgrp docker

# Verify Docker installation
docker --version
```

---

## 🚀 Step 5: Pull & Run the Container on Port 8080

### Option A: Standard `docker run` Command (Recommended)

Run the container in detached background mode with port forwarding `8080:8080` and persistent volume mounts for uploaded images and data:

```bash
# Pull the latest image
docker pull <your-dockerhub-username>/puzzle-game:latest

# Run the container
docker run -d \
  --name puzzle-web \
  --restart unless-stopped \
  -p 8080:8080 \
  -e PORT=8080 \
  -e DEBUG=False \
  -e ALLOWED_HOSTS="*" \
  -v puzzle_media:/app/media \
  -v puzzle_db:/app/data \
  <your-dockerhub-username>/puzzle-game:latest
```

---

### Option B: Using `docker-compose`

If you prefer using `docker-compose`:

1. Create a `docker-compose.yml` on the VM:
```bash
cat << 'EOF' > docker-compose.yml
services:
  web:
    image: <your-dockerhub-username>/puzzle-game:latest
    container_name: puzzle_web
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
      - DEBUG=False
      - ALLOWED_HOSTS=*
    volumes:
      - puzzle_media:/app/media
      - puzzle_db:/app/data

volumes:
  puzzle_media:
    driver: local
  puzzle_db:
    driver: local
EOF
```

2. Replace `<your-dockerhub-username>` with your Docker Hub username.
3. Start the application:
```bash
docker compose up -d
```

---

## 🌐 Step 6: Verify Deployment

Open your web browser and navigate to:

👉 **`http://<YOUR_AZURE_VM_PUBLIC_IP>:8080/`**

You should see the 8-Puzzle game running live in Light Theme with full functionality (sliding tiles, preset gallery, photo upload, and instant dark mode switch)!

---

## 🔍 Useful Management & Maintenance Commands

### View Live Container Logs
```bash
docker logs -f puzzle-web
```

### Check Container Status
```bash
docker ps
```

### Stop / Restart Container
```bash
docker stop puzzle-web
docker restart puzzle-web
```

### Update to a Newer Image Version
When you push a new version to Docker Hub, simply run:
```bash
docker pull <your-dockerhub-username>/puzzle-game:latest
docker stop puzzle-web
docker rm puzzle-web
docker run -d \
  --name puzzle-web \
  --restart unless-stopped \
  -p 8080:8080 \
  -e PORT=8080 \
  -e DEBUG=False \
  -e ALLOWED_HOSTS="*" \
  -v puzzle_media:/app/media \
  -v puzzle_db:/app/data \
  <your-dockerhub-username>/puzzle-game:latest
```
*(Your custom uploaded photos in `puzzle_media` volume will remain safely preserved across updates!)*

---

## 🛡️ Security Best Practices for Production

1. **Secret Key**: When deploying to production, pass a custom random secret key:
   ```bash
   -e SECRET_KEY="your-super-secret-random-key-here"
   ```
2. **Specific Allowed Hosts**: Set `ALLOWED_HOSTS` to your VM's public IP or domain name:
   ```bash
   -e ALLOWED_HOSTS="<YOUR_VM_IP>,yourdomain.com"
   ```
3. **Nginx Reverse Proxy & SSL Configuration**:
   When using Nginx as a reverse proxy for your domain (`bxng.khakse.dev`), configure your `/etc/nginx/sites-available/default` (or custom site file) with `client_max_body_size 25M;` and proper proxy headers:

   ```nginx
   server {
       listen 80;
       server_name bxng.khakse.dev;

       # Max upload file size (prevents 413 Request Entity Too Large)
       client_max_body_size 25M;

       location / {
           proxy_pass http://127.0.0.1:8080;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

   After editing, test and reload Nginx:
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```
