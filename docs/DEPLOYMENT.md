# 🚀 Deployment Guide - Try-Harder-AI Bot

## Overview

This document provides comprehensive instructions for deploying the Try-Harder-AI Discord bot to production environments, including cloud platforms, VPS servers, and containerized deployments.

---

## Table of Contents

1. [Deployment Options](#deployment-options)
2. [Pre-Deployment Checklist](#pre-deployment-checklist)
3. [Local Development](#local-development)
4. [VPS Deployment (Ubuntu)](#vps-deployment-ubuntu)
5. [Docker Deployment](#docker-deployment)
6. [Cloud Platform Deployments](#cloud-platform-deployments)
7. [Environment Configuration](#environment-configuration)
8. [Database & Storage](#database--storage)
9. [Monitoring & Logging](#monitoring--logging)
10. [Backup & Recovery](#backup--recovery)
11. [Security Hardening](#security-hardening)
12. [Scaling & Performance](#scaling--performance)
13. [CI/CD Pipeline](#cicd-pipeline)
14. [Troubleshooting](#troubleshooting)
15. [Maintenance](#maintenance)

---

## 🎯 Deployment Options

### Comparison Table

| Option | Difficulty | Cost | Scalability | Best For |
|--------|-----------|------|-------------|----------|
| **Local** | Easy | Free | Low | Development/Testing |
| **VPS** | Medium | $5-20/mo | Medium | Small-Medium servers |
| **Docker** | Medium | Varies | High | Any environment |
| **Railway** | Easy | $5+/mo | High | Quick deployment |
| **Heroku** | Easy | $7+/mo | High | Quick deployment |
| **AWS** | Hard | $10+/mo | Very High | Enterprise |
| **DigitalOcean** | Medium | $6+/mo | High | Cost-effective |
| **Google Cloud** | Hard | $10+/mo | Very High | Enterprise |

### Recommended Deployment Path

```
Development → Local Testing → Docker → VPS/Cloud
```

---

## ✅ Pre-Deployment Checklist

### Required Accounts & Keys

- [ ] **Discord Developer Account**
  - Bot application created
  - Bot token obtained
  - Bot invited to server with `applications.commands` scope
  - Necessary permissions enabled

- [ ] **Google Gemini API Key**
  - Google account ready
  - API key generated at https://aistudio.google.com/apikey
  - Free tier active (1,500 requests/day at no cost)
  - Paid billing enabled (optional — for higher rate limits)
  - Rate limits reviewed at https://ai.google.dev/pricing

- [ ] **Hosting Platform** (choose one)
  - VPS access (DigitalOcean, Linode, etc.)
  - Cloud platform account (AWS, GCP, Azure)
  - PaaS account (Railway, Heroku)

### System Requirements

**Minimum:**
- CPU: 1 core
- RAM: 512 MB
- Storage: 5 GB
- OS: Ubuntu 20.04+ / Debian 11+

**Recommended:**
- CPU: 2 cores
- RAM: 2 GB
- Storage: 10 GB
- OS: Ubuntu 22.04 LTS

**For 100+ concurrent users:**
- CPU: 4 cores
- RAM: 4 GB
- Storage: 20 GB

### Software Requirements

```bash
# Required
- Python 3.10 or higher
- pip (Python package manager)
- Git

# Recommended
- Docker & Docker Compose
- systemd (for service management)
- nginx (for reverse proxy if needed)
```

---

## 💻 Local Development

### Quick Setup

```bash
# Clone repository
git clone https://github.com/The4v1/Try-Harder-AI.git
cd try-harder-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your tokens

# Run bot
python bot/main.py
```

### Development Environment Variables

```bash
# .env for development
DISCORD_BOT_TOKEN=your_dev_bot_token
GEMINI_API_KEY=your_gemini_api_key_here
DEFAULT_AI_MODEL=gemini-1.5-flash

# Development settings
DEBUG=true
LOG_LEVEL=DEBUG
ENVIRONMENT=development

# Optional
APP_NAME=Try-Harder-AI-Dev
```

---

## 🖥️ VPS Deployment (Ubuntu)

### Step 1: Server Setup

```bash
# Connect to your VPS
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install required packages
apt install -y python3.10 python3-pip python3-venv git nginx

# Create bot user (security best practice)
adduser --disabled-password --gecos "" botuser
usermod -aG sudo botuser
su - botuser
```

### Step 2: Clone and Configure

```bash
# Clone repository
cd /home/botuser
git clone https://github.com/The4v1/Try-Harder-AI.git
cd try-harder-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env
```

### Step 3: Production Environment

```bash
# .env for production
DISCORD_BOT_TOKEN=your_production_bot_token
GEMINI_API_KEY=your_gemini_api_key_here
DEFAULT_AI_MODEL=gemini-1.5-flash

# Production settings
DEBUG=false
LOG_LEVEL=INFO
ENVIRONMENT=production

# Application info
APP_NAME=Try-Harder-AI
APP_URL=https://your-domain.com
```

### Step 4: Create Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/try-harder-ai.service
```

**Service configuration:**

```ini
[Unit]
Description=Try-Harder-AI Discord Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/try-harder-ai
Environment="PATH=/home/botuser/try-harder-ai/venv/bin"
ExecStart=/home/botuser/try-harder-ai/venv/bin/python bot/main.py
Restart=always
RestartSec=10

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/botuser/try-harder-ai/data /home/botuser/try-harder-ai/logs

# Logging
StandardOutput=append:/home/botuser/try-harder-ai/logs/bot.log
StandardError=append:/home/botuser/try-harder-ai/logs/error.log

[Install]
WantedBy=multi-user.target
```

### Step 5: Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable try-harder-ai

# Start service
sudo systemctl start try-harder-ai

# Check status
sudo systemctl status try-harder-ai

# View logs
sudo journalctl -u try-harder-ai -f
```

### Step 6: Monitoring Commands

```bash
# Check if running
sudo systemctl is-active try-harder-ai

# Restart bot
sudo systemctl restart try-harder-ai

# Stop bot
sudo systemctl stop try-harder-ai

# View recent logs
sudo journalctl -u try-harder-ai -n 100

# Follow logs in real-time
sudo journalctl -u try-harder-ai -f
```

---

## 🐳 Docker Deployment

### Dockerfile

Create `Dockerfile` in project root:

```dockerfile
# Use official Python runtime
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs

# Create non-root user
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

# Switch to non-root user
USER botuser

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Run bot
CMD ["python", "bot/main.py"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  bot:
    build: .
    container_name: try-harder-ai
    restart: unless-stopped
    
    # Environment variables
    env_file:
      - .env
    
    # Volumes for data persistence
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./prompts:/app/prompts:ro
    
    # Resource limits
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 512M
    
    # Logging
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    
    # Network
    networks:
      - bot-network

networks:
  bot-network:
    driver: bridge
```

### Docker Commands

```bash
# Build image
docker-compose build

# Start container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop container
docker-compose down

# Restart
docker-compose restart

# Check status
docker-compose ps

# Execute commands in container
docker-compose exec bot bash

# Update and restart
git pull
docker-compose build
docker-compose up -d
```

### Docker Production Setup

```bash
# 1. Clone repository on server
ssh user@server
git clone https://github.com/The4v1/Try-Harder-AI.git
cd try-harder-ai

# 2. Configure environment
cp .env.example .env
nano .env

# 3. Build and run
docker-compose up -d

# 4. Verify
docker-compose logs -f

# 5. Enable auto-restart
# Add to crontab for server reboot
crontab -e
# Add: @reboot cd /path/to/try-harder-ai && docker-compose up -d
```

---

## ☁️ Cloud Platform Deployments

### Railway Deployment

**1. Prepare for Railway:**

Create `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python bot/main.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Create `Procfile`:

```
worker: python bot/main.py
```

**2. Deploy to Railway:**

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add environment variables via dashboard:
# DISCORD_BOT_TOKEN=your_token
# GEMINI_API_KEY=your_gemini_api_key
# DEFAULT_AI_MODEL=gemini-1.5-flash

# Deploy
railway up

# View logs
railway logs
```

**3. Railway Dashboard Setup:**

- Go to https://railway.app
- Create new project
- Connect GitHub repo
- Add environment variables (`DISCORD_BOT_TOKEN`, `GEMINI_API_KEY`, `DEFAULT_AI_MODEL`)
- Deploy automatically on push

---

### Heroku Deployment

**1. Prepare for Heroku:**

Create `Procfile`:

```
worker: python bot/main.py
```

Create `runtime.txt`:

```
python-3.10.11
```

**2. Deploy to Heroku:**

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create try-harder-ai-bot

# Set environment variables
heroku config:set DISCORD_BOT_TOKEN=your_token
heroku config:set GEMINI_API_KEY=your_gemini_api_key
heroku config:set DEFAULT_AI_MODEL=gemini-1.5-flash

# Deploy
git push heroku main

# Scale worker
heroku ps:scale worker=1

# View logs
heroku logs --tail

# Restart
heroku restart
```

---

### AWS EC2 Deployment

**1. Launch EC2 Instance:**

```bash
# Instance type: t2.micro (free tier) or t2.small
# OS: Ubuntu 22.04 LTS
# Storage: 10 GB
# Security Group: Allow SSH (22)
```

**2. Connect and Setup:**

```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.10 python3-pip python3-venv git

# Clone and setup (same as VPS deployment)
git clone https://github.com/The4v1/Try-Harder-AI.git
cd try-harder-ai
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env

# Create systemd service (same as VPS)
sudo nano /etc/systemd/system/try-harder-ai.service
# [Copy service configuration from VPS section]

# Start service
sudo systemctl enable try-harder-ai
sudo systemctl start try-harder-ai
```

**3. AWS-Specific Configuration:**

```bash
# Set up CloudWatch for logs (optional)
sudo apt install -y amazon-cloudwatch-agent

# Configure auto-scaling (advanced)
# Use AWS Auto Scaling Groups

# Set up EBS snapshots for backups
aws ec2 create-snapshot --volume-id vol-xxxxx
```

---

### DigitalOcean Droplet

**1. Create Droplet:**

- Go to https://digitalocean.com
- Create Droplet
- Choose: Ubuntu 22.04 LTS
- Plan: Basic ($6/month)
- Add SSH key

**2. Deploy (Same as VPS):**

```bash
# SSH to droplet
ssh root@your-droplet-ip

# Follow VPS deployment steps
# (Same as VPS Deployment section)
```

**3. DigitalOcean Extras:**

```bash
# Enable firewall
ufw allow OpenSSH
ufw enable

# Set up monitoring
# Use DigitalOcean dashboard → Monitoring

# Create snapshots for backup
# Dashboard → Droplet → Snapshots → Take Snapshot
```

---

## ⚙️ Environment Configuration

### Production .env Template

```bash
# ==========================================
# Try-Harder-AI Production Configuration
# ==========================================

# Discord Configuration
DISCORD_BOT_TOKEN=your_production_bot_token_here

# Google Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here
DEFAULT_AI_MODEL=gemini-1.5-flash
AI_MAX_TOKENS=4096
AI_TEMPERATURE=0.7
AI_TIMEOUT=60

# Application Settings
APP_NAME=Try-Harder-AI
APP_URL=https://your-domain.com
ENVIRONMENT=production
DEBUG=false

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
LOG_MAX_SIZE=10485760  # 10MB
LOG_BACKUP_COUNT=5

# Database
DATA_DIR=data
USER_DATA_FILE=data/user_data.json

# Rate Limiting
MAX_CONCURRENT_REQUESTS=10
COOLDOWN_SECONDS=5

# Assessment Settings
ASSESSMENT_TIMEOUT=60
MAX_QUESTIONS=10

# Optional: Sentry Error Tracking
# SENTRY_DSN=your_sentry_dsn_here

# Optional: Custom Domain
# CUSTOM_DOMAIN=bot.your-domain.com
```

### Environment-Specific Configs

**Development:**
```bash
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
```

**Staging:**
```bash
ENVIRONMENT=staging
DEBUG=false
LOG_LEVEL=INFO
```

**Production:**
```bash
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
```

---

## 💾 Database & Storage

### Data Directory Structure

```
data/
├── certifications.yaml      # Read-only (version controlled)
├── questions.yaml           # Read-only (version controlled)
├── resources.yaml           # Read-only (version controlled)
└── user_data.json          # Writable (needs backup)

logs/
├── bot.log                  # Application logs
├── api.log                  # Gemini API request logs
└── errors.log              # Error logs
```

### Backup Strategy

**Automated Daily Backups:**

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/home/botuser/backups"
DATA_DIR="/home/botuser/try-harder-ai/data"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup user data
cp $DATA_DIR/user_data.json $BACKUP_DIR/user_data_$TIMESTAMP.json

# Compress old backups
gzip $BACKUP_DIR/user_data_*.json 2>/dev/null

# Keep only last 30 days
find $BACKUP_DIR -name "user_data_*.json.gz" -mtime +30 -delete

echo "Backup completed: $TIMESTAMP"
```

**Add to crontab:**

```bash
crontab -e

# Daily backup at 2 AM
0 2 * * * /home/botuser/try-harder-ai/backup.sh
```

### Cloud Storage Backup

**AWS S3 Backup:**

```bash
#!/bin/bash
# backup-s3.sh

BUCKET_NAME="try-harder-ai-backups"
DATA_FILE="/home/botuser/try-harder-ai/data/user_data.json"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Upload to S3
aws s3 cp $DATA_FILE s3://$BUCKET_NAME/user_data_$TIMESTAMP.json

echo "Uploaded to S3: $TIMESTAMP"
```

---

## 📊 Monitoring & Logging

### Log Rotation

**Configure logrotate:**

```bash
sudo nano /etc/logrotate.d/try-harder-ai
```

```
/home/botuser/try-harder-ai/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0644 botuser botuser
    sharedscripts
    postrotate
        systemctl reload try-harder-ai > /dev/null 2>&1 || true
    endscript
}
```

### Health Check Script

```python
# health_check.py

import sys
import json
from datetime import datetime

def check_bot_health():
    """Simple health check"""
    try:
        # Check if user_data.json is accessible
        with open('data/user_data.json', 'r') as f:
            data = json.load(f)
        
        # Check if logs are being written
        with open('logs/bot.log', 'r') as f:
            last_line = f.readlines()[-1]
            
        print(f"✅ Health check passed - {datetime.now()}")
        return 0
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(check_bot_health())
```

**Add to crontab for monitoring:**

```bash
# Health check every 15 minutes
*/15 * * * * cd /home/botuser/try-harder-ai && python health_check.py >> logs/health.log 2>&1
```

### Monitoring Tools

**1. System Monitoring:**

```bash
# Install htop
sudo apt install htop

# Monitor bot process
htop -p $(pgrep -f "python bot/main.py")
```

**2. Application Monitoring:**

```bash
# Real-time log monitoring
tail -f logs/bot.log

# Error monitoring
grep -i error logs/bot.log | tail -20

# Gemini API request monitoring
tail -f logs/api.log
```

**3. Advanced Monitoring (Optional):**

- **Prometheus + Grafana**: Metrics dashboard
- **Sentry**: Error tracking
- **DataDog**: Full-stack monitoring
- **UptimeRobot**: Uptime monitoring

---

## 🔒 Security Hardening

### Firewall Configuration

```bash
# Install UFW
sudo apt install ufw

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH
sudo ufw allow OpenSSH

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### Secure Environment Variables

**Never commit .env to Git:**

```bash
# .gitignore
.env
.env.local
.env.production
*.log
data/user_data.json
```

**Use encryption for sensitive data:**

```bash
# Install git-crypt
sudo apt install git-crypt

# Initialize encryption
git-crypt init

# Add to .gitattributes
echo ".env filter=git-crypt diff=git-crypt" >> .gitattributes
```

### API Key Rotation

```bash
# 1. Generate new Gemini API key at https://aistudio.google.com/apikey
# 2. Update .env file
# 3. Restart bot
# 4. Delete old API key in Google AI Studio

# Script for zero-downtime rotation
#!/bin/bash
# rotate-keys.sh

NEW_KEY="new_gemini_api_key_here"

# Update .env
sed -i "s/GEMINI_API_KEY=.*/GEMINI_API_KEY=$NEW_KEY/" .env

# Restart bot
sudo systemctl restart try-harder-ai

echo "Gemini API key rotated successfully"
```

### Security Best Practices

✅ **Do:**
- Use non-root user for bot
- Enable firewall
- Keep system updated
- Use strong passwords
- Enable 2FA on accounts
- Regular security audits
- Monitor logs for suspicious activity

❌ **Don't:**
- Commit secrets to Git
- Run as root
- Use default passwords
- Expose unnecessary ports
- Ignore security updates
- Share API keys

---

## 📈 Scaling & Performance

### Vertical Scaling

**Upgrade server resources:**

```bash
# Monitor resource usage
htop
df -h
free -m

# If needed, upgrade:
# - CPU cores
# - RAM
# - Storage
```

### Horizontal Scaling (Advanced)

**Multiple bot instances with sharding:**

```python
# bot/main.py (sharding example)

import discord
from discord.ext import commands

# Enable sharding for large servers
bot = commands.AutoShardedBot(
    shard_count=2,  # Number of shards
    intents=discord.Intents.all()
)

# Sync slash commands on ready
@bot.event
async def on_ready():
    await bot.tree.sync()

# Rest of bot code...
```

### Performance Optimization

**1. Database Optimization:**

```python
# Use caching for frequently accessed data
from functools import lru_cache

@lru_cache(maxsize=128)
def get_certification_data(cert_code):
    """Cached certification data"""
    # Load from YAML (expensive operation)
    return load_yaml(f"data/{cert_code}.yaml")
```

**2. Gemini SDK Model Reuse:**

```python
# Initialize GenerativeModel once per variant — reuse across requests
import google.generativeai as genai

_model_cache = {}

def get_model(model_name: str = "gemini-1.5-flash"):
    """Return a cached GenerativeModel instance"""
    if model_name not in _model_cache:
        _model_cache[model_name] = genai.GenerativeModel(model_name)
    return _model_cache[model_name]
```

**3. Async Optimization:**

```python
# Process multiple requests concurrently
import asyncio

async def process_multiple_users(user_ids):
    tasks = [process_user(uid) for uid in user_ids]
    results = await asyncio.gather(*tasks)
    return results
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/
    
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        script: |
          cd /home/botuser/try-harder-ai
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          sudo systemctl restart try-harder-ai
```

### Automated Testing

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Lint
      run: |
        flake8 bot/
        black --check bot/
    
    - name: Type check
      run: |
        mypy bot/
    
    - name: Run tests
      run: |
        pytest --cov=bot tests/
```

---

## 🔧 Troubleshooting

### Common Issues

**1. Bot won't start:**

```bash
# Check logs
sudo journalctl -u try-harder-ai -n 100

# Common causes:
# - Missing .env file
# - Invalid GEMINI_API_KEY
# - Port conflicts
# - Permission issues

# Fix permissions
sudo chown -R botuser:botuser /home/botuser/try-harder-ai
```

**2. Slash commands not appearing in Discord:**

```bash
# Ensure bot was invited with applications.commands scope
# Re-invite with correct URL:
# https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=8&scope=bot%20applications.commands

# Force re-sync on next startup by checking on_ready:
# await bot.tree.sync()
```

**3. Gemini API errors:**

```bash
# Test API key is valid
python3 -c "
import google.generativeai as genai
import os
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')
r = model.generate_content('hello')
print('API OK:', r.text[:50])
"

# Check rate limits — free tier: 15 RPM, 1500 RPD
# If hitting limits, either reduce request frequency
# or enable billing at https://console.cloud.google.com

# Increase timeout in .env if needed
AI_TIMEOUT=120
```

**4. Memory issues:**

```bash
# Check memory usage
free -m

# Restart bot
sudo systemctl restart try-harder-ai

# Increase swap if needed
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**5. Disk space:**

```bash
# Check disk usage
df -h

# Clean old logs
sudo journalctl --vacuum-time=7d

# Clean old backups
find ~/backups -mtime +30 -delete
```

### Debug Mode

```bash
# Enable debug logging
nano .env
# Set: LOG_LEVEL=DEBUG

# Restart
sudo systemctl restart try-harder-ai

# Watch debug logs
sudo journalctl -u try-harder-ai -f
```

---

## 🔄 Maintenance

### Regular Maintenance Tasks

**Daily:**
- Check bot status: `systemctl status try-harder-ai`
- Monitor error logs: `tail -f logs/error.log`

**Weekly:**
- Review disk usage: `df -h`
- Check backup integrity
- Review Gemini API token usage at https://aistudio.google.com

**Monthly:**
- Update system packages: `apt update && apt upgrade`
- Update Python dependencies: `pip install -r requirements.txt --upgrade`
- Rotate Gemini API keys (recommended)
- Review and clean old logs

**Quarterly:**
- Security audit
- Performance review
- Cost optimization
- Backup recovery test

### Update Procedure

```bash
# 1. Backup current state
cp -r /home/botuser/try-harder-ai /home/botuser/try-harder-ai.backup

# 2. Pull latest changes
cd /home/botuser/try-harder-ai
git pull origin main

# 3. Update dependencies
source venv/bin/activate
pip install -r requirements.txt --upgrade

# 4. Test changes
python -m pytest tests/

# 5. Restart bot
sudo systemctl restart try-harder-ai

# 6. Monitor logs
sudo journalctl -u try-harder-ai -f

# 7. If issues occur, rollback
# sudo systemctl stop try-harder-ai
# cd /home/botuser
# rm -rf try-harder-ai
# mv try-harder-ai.backup try-harder-ai
# sudo systemctl start try-harder-ai
```

---

## 📝 Deployment Checklist

### Pre-Deployment

- [ ] Create Discord bot application
- [ ] Get Discord bot token
- [ ] Invite bot with `bot` + `applications.commands` scopes
- [ ] Get Google Gemini API key at https://aistudio.google.com/apikey
- [ ] Confirm free tier is active (or enable billing for higher limits)
- [ ] Choose hosting platform
- [ ] Set up server/container
- [ ] Configure domain (if applicable)

### During Deployment

- [ ] Clone repository
- [ ] Configure .env file (`GEMINI_API_KEY`, `DISCORD_BOT_TOKEN`, `DEFAULT_AI_MODEL`)
- [ ] Install dependencies
- [ ] Set up systemd service / Docker
- [ ] Start bot
- [ ] Verify bot is online in Discord
- [ ] Verify slash commands appear (type `/` in Discord)
- [ ] Test all slash commands (`/start`, `/assess`, `/ask`, `/roadmap`, `/progress`)
- [ ] Set up logging
- [ ] Configure backups
- [ ] Set up monitoring

### Post-Deployment

- [ ] Monitor logs for errors
- [ ] Test with real users
- [ ] Set up automated backups
- [ ] Configure alerts
- [ ] Document any custom configurations
- [ ] Share bot invite link
- [ ] Monitor Gemini API usage at https://aistudio.google.com

---

## 📞 Support & Resources

**Documentation:**
- GitHub: https://github.com/The4v1/Try-Harder-AI
- Docs: See /docs folder
- Wiki: Project wiki

**Community:**
- Discord: https://discord.gg/try-harder-ai
- Issues: GitHub Issues

**Gemini API Resources:**
- Google AI Studio: https://aistudio.google.com
- API Docs: https://ai.google.dev/gemini-api/docs
- Pricing & Rate Limits: https://ai.google.dev/pricing
- API Status: https://status.cloud.google.com

**Hosting Providers:**
- DigitalOcean: https://digitalocean.com
- Railway: https://railway.app
- Heroku: https://heroku.com
- AWS: https://aws.amazon.com

---

## 🎯 Quick Reference

### Essential Commands

```bash
# Start bot
sudo systemctl start try-harder-ai

# Stop bot
sudo systemctl stop try-harder-ai

# Restart bot
sudo systemctl restart try-harder-ai

# Check status
sudo systemctl status try-harder-ai

# View logs
sudo journalctl -u try-harder-ai -f

# Update bot
cd /home/botuser/try-harder-ai
git pull
pip install -r requirements.txt
sudo systemctl restart try-harder-ai
```

### Deployment Paths Summary

```
🏠 Local:     git clone → pip install → python bot/main.py
🖥️  VPS:      SSH → clone → systemd service → start
🐳 Docker:    Dockerfile → docker-compose up -d
☁️  Railway:  railway init → railway up
☁️  Heroku:   heroku create → git push heroku main
```

---

*Last Updated: February 2026*
*Version: 3.0.0*
*Happy Deploying! 🚀*