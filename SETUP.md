# 📚 SETUP GUIDE - Try-Harder-AI Discord Bot

Complete setup instructions for installing and configuring the Try-Harder-AI Discord bot.

---

## 📋 Table of Contents

- [System Requirements](#-system-requirements)
- [Pre-Installation Checklist](#-pre-installation-checklist)
- [Step-by-Step Installation](#-step-by-step-installation)
- [Discord Bot Setup](#-discord-bot-setup)
- [Google Gemini API Setup](#-google-gemini-api-setup)
- [Environment Configuration](#-environment-configuration)
- [Directory Structure](#-directory-structure)
- [First Run](#-first-run)
- [Verification](#-verification)
- [Post-Installation](#-post-installation)
- [Advanced Configuration](#-advanced-configuration)
- [Troubleshooting](#-troubleshooting)
- [Security Best Practices](#-security-best-practices)
- [Maintenance](#-maintenance)

---

## 💻 System Requirements

### **Minimum Requirements**

- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 20.04+)
- **Python**: 3.10 or higher
- **RAM**: 512 MB minimum, 1 GB recommended
- **Storage**: 500 MB free space
- **Internet**: Stable internet connection

### **Software Requirements**

- Python 3.10+ with pip
- Git (for cloning repository)
- Text editor (VS Code, Sublime, Notepad++, etc.)
- Discord account
- Google account (for FREE Gemini API)

### **Optional Requirements**

- Virtual environment tool (venv, conda)
- PostgreSQL (for future database features)
- Redis (for advanced caching)

---

## ✅ Pre-Installation Checklist

Before you begin, ensure you have:

- [ ] Python 3.10+ installed and added to PATH
- [ ] pip package manager working
- [ ] Git installed
- [ ] Discord account created
- [ ] Google account (for FREE Gemini API - no credit card!)
- [ ] Basic command line knowledge
- [ ] Text editor installed
- [ ] Admin/sudo access (for some installations)

### **Verify Python Installation**

```bash
# Check Python version
python --version
# or
python3 --version

# Should output: Python 3.10.x or higher

# Check pip
pip --version
# or
pip3 --version
```

If Python is not installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: `brew install python@3.10` or download from python.org
- **Linux**: `sudo apt install python3.10 python3-pip`

---

## 🚀 Step-by-Step Installation

### **Step 1: Get the Repository**

You have two options to get the project files:

#### **Option A: Clone with Git** (Recommended)

```bash
# Navigate to your desired directory
cd ~/projects  # or C:\Users\YourName\projects on Windows

# Clone the repository
git clone https://github.com/The4v1/Try-Harder-AI.git

# Navigate into the directory
cd try-harder-ai

# Verify files are present
ls -la  # On Windows: dir
```

#### **Option B: Download ZIP File**

1. Go to [https://github.com/The4v1/Try-Harder-AI](https://github.com/The4v1/Try-Harder-AI)
2. Click the green **"Code"** button
3. Select **"Download ZIP"**
4. Save the ZIP file to your desired location (e.g., `~/projects` or `C:\Users\YourName\projects`)
5. Extract the ZIP file:
   - **Windows**: Right-click → **"Extract All..."** → Choose destination
   - **macOS**: Double-click the ZIP file
   - **Linux**: `unzip try-harder-ai-main.zip`
6. Navigate into the extracted directory:
   ```bash
   cd try-harder-ai-main  # Note: ZIP downloads often add "-main" suffix
   ```

**Expected output (for both options):**
```
.env
.gitignore
LICENSE
README.md
QUICKSTART.md
SETUP.md
requirements.txt
main.py
bot/
data/
prompts/
config/
utils/
docs/
tests/
```

### **Step 2: Create Virtual Environment**

**Why use virtual environment?**
- Isolates dependencies
- Prevents conflicts with other Python projects
- Makes deployment easier
- Recommended best practice

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# You should see (venv) in your prompt
```

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in your prompt
```

**Verify activation:**
```bash
which python  # Should show path to venv/bin/python
# On Windows: where python
```

### **Step 3: Install Dependencies**

```bash
# Make sure virtual environment is activated
# You should see (venv) in your prompt

# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# This will take 2-5 minutes depending on your internet speed
```

**Verify installation:**
```bash
# Check if discord.py is installed
pip show discord.py

# Check if google-generativeai is installed
pip show google-generativeai

# List all installed packages
pip list
```

**Expected packages:**
- discord.py >= 2.3.0
- google-generativeai >= 0.3.0
- python-dotenv
- aiohttp
- PyYAML
- asyncio

**Common installation issues:**

If you get SSL errors:
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

If you get permission errors:
```bash
pip install --user -r requirements.txt
```

If you get compiler errors (Windows):
```bash
# Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

---

## 🤖 Discord Bot Setup

### **Step 1: Create Discord Application**

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Name it **"Try-Harder-AI"** (or your preferred name)
4. Click **"Create"**
5. Read and accept Discord's Developer Terms of Service

### **Step 2: Configure Bot Settings**

1. Click on your application
2. Go to **"Bot"** tab in the left sidebar
3. Click **"Add Bot"** → Confirm with **"Yes, do it!"**
4. **Customize your bot:**
   - **Username**: Try-Harder-AI
   - **Icon**: Upload a logo (optional - use a hacker/security themed icon)
   - **Public Bot**: Toggle OFF (unless you want others to invite it)
   - **Require OAuth2 Code Grant**: Leave OFF

### **Step 3: Get Bot Token**

1. Under **"Token"** section
2. Click **"Reset Token"** → Confirm
3. **COPY THE TOKEN** - You won't see it again!
4. **IMPORTANT**: Never share this token publicly
5. Store it securely (password manager recommended)

**Token format example:**
```
MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.GhIjKl.MnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUv
```

### **Step 4: Enable Privileged Intents**

Scroll down to **"Privileged Gateway Intents"** and enable:

- [x] **Presence Intent** (Optional - for seeing online status)
- [x] **Server Members Intent** (Recommended - for member tracking)
- [x] **Message Content Intent** ⚠️ **CRITICAL - Bot won't work without this**

**Why these are needed:**
- **Message Content**: Required to read message content and respond to commands
- **Server Members**: Helpful for tracking user progress across servers
- **Presence**: Nice to have but not critical

Click **"Save Changes"**

### **Step 5: Generate Bot Invite URL**

1. Go to **"OAuth2"** → **"URL Generator"** tab
2. Under **SCOPES**, select:
   - [x] `bot` (Required)
   - [x] `applications.commands` ⚠️ **REQUIRED for slash commands**

3. Under **BOT PERMISSIONS**, select:
   - [x] `Administrator` (easiest option - gives all permissions)
   
   **OR** select specific permissions (recommended for production):
   - [x] **Read Messages/View Channels**
   - [x] **Send Messages**
   - [x] **Send Messages in Threads**
   - [x] **Embed Links**
   - [x] **Attach Files**
   - [x] **Read Message History**
   - [x] **Add Reactions**
   - [x] **Use Slash Commands** ⚠️ **REQUIRED**
   - [x] **Use Application Commands** ⚠️ **REQUIRED**
   - [x] **Manage Messages** (for cleanup - optional)
   - [x] **Use External Emojis** (optional)

4. **Copy the generated URL** at the bottom
5. Open URL in browser
6. Select your Discord server from dropdown
7. Click **"Authorize"**
8. Complete CAPTCHA verification

**Verify bot is in server:**
- Bot should appear in member list (offline until you run it)
- Check server settings → Members to see bot
- Bot will have a "BOT" tag next to its name

---

## 🔑 Google Gemini API Setup

### **Step 1: Get FREE Google Gemini API Key**

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your **Google Account** (any Gmail account works)
3. Click **"Create API key"**
4. Choose one of these options:
   - **"Create API key in new project"** (recommended for beginners)
   - **"Create API key in existing project"** (if you have Google Cloud project)
5. **COPY THE API KEY** immediately
6. **IMPORTANT**: Store it securely - you can view it later but it's best to save it now

**API Key format:**
```
AIzaSyD-abc123def456ghi789jkl012mno345pqr678stu901vwx234
```

**🎉 NO CREDIT CARD REQUIRED! Completely FREE!**

### **Step 2: Understand FREE Tier Limits**

Google Gemini offers an extremely generous FREE tier perfect for learning and development:

| Model | Speed | Context Window | Free Tier Limit | Best For |
|-------|-------|----------------|-----------------|----------|
| **Gemini 1.5 Flash** ⭐ | ⚡⚡⚡ | 1M tokens | **15 requests/minute** | Daily use, fast responses |
| **Gemini 1.5 Pro** | ⚡⚡ | 2M tokens | **2 requests/minute** | Complex reasoning, long roadmaps |
| **Gemini 1.5 Flash-8B** | ⚡⚡⚡⚡ | 1M tokens | **15 requests/minute** | Ultra-fast, simple queries |

**Additional FREE Tier Benefits:**
- ✅ **1 million requests per day** (Flash/Flash-8B)
- ✅ **50 requests per day** (Pro)
- ✅ **No expiration** - FREE forever!
- ✅ **No credit card required** - ever
- ✅ **Perfect for learning and development**
- ✅ **More than enough for daily study sessions**

**Typical Usage Examples:**
- 1-hour study session: ~30-50 requests
- Daily usage: ~100-200 requests
- Weekly usage: ~500-1000 requests
- **All well within FREE limits!** 🎉

### **Step 3: Test Your API Key (Optional)**

**Option A: Using curl (Linux/Mac/Windows with Git Bash):**
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_API_KEY"
```

**Expected response:**
```json
{
  "models": [
    {
      "name": "models/gemini-1.5-flash",
      "displayName": "Gemini 1.5 Flash",
      ...
    }
  ]
}
```

**Option B: Using Python:**
```python
import requests

api_key = "YOUR_API_KEY"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

response = requests.get(url)
if response.status_code == 200:
    print("✅ API key is valid!")
    models = response.json().get('models', [])
    print(f"Available models: {len(models)}")
    for model in models:
        print(f"  - {model.get('displayName')}")
else:
    print(f"❌ API key is invalid: {response.status_code}")
    print(response.text)
```

**Option C: Quick test with Google AI Studio:**
1. Go back to [Google AI Studio](https://aistudio.google.com)
2. Try the chat interface
3. If it works there, your API key is valid

### **Step 4: Monitor Usage (Optional)**

**Via Google Cloud Console:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or the one where API key was created)
3. Navigate to **"APIs & Services"** → **"Dashboard"**
4. Click on **"Generative Language API"**
5. View usage statistics:
   - Requests per day
   - Success/error rates
   - Quota usage

**Via Bot Logs:**
The bot automatically logs all API calls:
```bash
# View API usage
grep "Gemini API" logs/bot.log | tail -n 50

# Count requests today
grep "$(date +%Y-%m-%d)" logs/bot.log | grep "Gemini API response" | wc -l
```

---

## ⚙️ Environment Configuration

### **Step 1: Locate .env File**

The `.env` file should already exist in your project root directory:
```bash
cd try-harder-ai
ls -la | grep .env
```

If it doesn't exist:
```bash
# Copy from example (if you have .env.example)
cp .env.example .env

# Or create new one
touch .env  # Linux/Mac
type nul > .env  # Windows
```

### **Step 2: Edit .env File**

Open `.env` with your preferred editor:

```bash
# Linux/Mac
nano .env          # Simple editor
vim .env           # Advanced editor
code .env          # VS Code

# Windows
notepad .env       # Notepad
code .env          # VS Code
```

### **Step 3: Configure Required Settings**

Replace placeholder values with your actual keys:

```env
# ============================================================================
# TRY-HARDER-AI DISCORD BOT - ENVIRONMENT CONFIGURATION
# ============================================================================
#
# IMPORTANT: This is your actual .env file
# NEVER commit this file to version control
# Keep all API keys and tokens SECRET
#
# ============================================================================

# ============================================================================
# DISCORD BOT CONFIGURATION (REQUIRED)
# ============================================================================

# Discord Bot Token - Get from: https://discord.com/developers/applications
# Example: MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.GhIjKl.MnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUv
DISCORD_BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE

# Bot Command Prefix (Using / for slash commands)
BOT_PREFIX=/

# Bot Status Message (shown in Discord)
BOT_STATUS=Try Harder! 💪 | Use /help

# Bot Owner ID (Optional - your Discord user ID)
# Right-click your username in Discord (with Developer Mode on) → Copy ID
BOT_OWNER_ID=

# ============================================================================
# GOOGLE GEMINI API CONFIGURATION (REQUIRED)
# ============================================================================

# Google Gemini API Key - Get from: https://aistudio.google.com/app/apikey
# Example: AIzaSyD-abc123def456ghi789jkl012mno345pqr678
# FREE Tier: 15 requests/min (Flash), 2 requests/min (Pro)
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE

# ============================================================================
# AI MODEL CONFIGURATION
# ============================================================================

# Default AI Model - Gemini 1.5 Flash (Recommended - Fast & Free)
# Options:
#   - gemini-1.5-flash (RECOMMENDED - Fast, 1M context, FREE: 15 RPM)
#   - gemini-1.5-pro (Best quality, 2M context, FREE: 2 RPM)
#   - gemini-1.5-flash-8b (Ultra fast, FREE: 15 RPM)
DEFAULT_AI_MODEL=gemini-1.5-flash

# Fallback Model (if primary fails)
FALLBACK_AI_MODEL=gemini-1.5-flash-8b

# AI Generation Settings
AI_MAX_TOKENS=8192
AI_TEMPERATURE=0.7
AI_TIMEOUT=60
AI_TOP_P=0.95
AI_TOP_K=40

# ============================================================================
# BOT SETTINGS
# ============================================================================

# Feature Toggles
ENABLE_ASSESSMENTS=true
ENABLE_ROADMAPS=true
ENABLE_AI_QUERIES=true
ENABLE_PROGRESS_TRACKING=true
ENABLE_SLASH_COMMANDS=true

# Rate Limiting (Conservative for FREE tier)
MAX_CONCURRENT_AI_REQUESTS=2
COMMAND_COOLDOWN_SECONDS=4
USER_DAILY_AI_LIMIT=100

# Assessment Configuration
ASSESSMENT_QUESTIONS_PER_TEST=10
ASSESSMENT_TIMEOUT_SECONDS=60
ASSESSMENT_PASS_PERCENTAGE=70

# Roadmap Configuration
DEFAULT_ROADMAP_DURATION_WEEKS=12
MIN_ROADMAP_WEEKS=6
MAX_ROADMAP_WEEKS=24

# ============================================================================
# DATA FILES
# ============================================================================

USER_DATA_FILE=data/user_data.json
CERTIFICATIONS_FILE=data/certifications.yaml
QUESTIONS_FILE=data/questions.yaml
RESOURCES_FILE=data/resources.yaml

# Auto-save Settings
AUTO_SAVE_INTERVAL=300

# Backup Settings
ENABLE_AUTO_BACKUP=true
BACKUP_INTERVAL_HOURS=24
BACKUP_DIRECTORY=backups/
MAX_BACKUP_FILES=7

# ============================================================================
# LOGGING
# ============================================================================

LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
MAX_LOG_SIZE_MB=10
LOG_BACKUP_COUNT=5
ENABLE_CONSOLE_LOGGING=true
LOG_FORMAT=detailed

# ============================================================================
# DISCORD EMBED COLORS (Hex codes without #)
# ============================================================================

COLOR_SUCCESS=2ecc71
COLOR_ERROR=e74c3c
COLOR_INFO=3498db
COLOR_WARNING=f39c12
COLOR_OFFSEC=c0392b
COLOR_GOLD=f1c40f

# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

DEBUG_MODE=false
VERBOSE_LOGGING=false
ENABLE_RESPONSE_CACHE=true
CACHE_TTL_SECONDS=3600

# Environment (development, production, testing)
ENVIRONMENT=development

# ============================================================================
# GOOGLE GEMINI SPECIFIC SETTINGS
# ============================================================================

# Safety Settings (Allow cybersecurity content)
# Options: BLOCK_NONE, BLOCK_ONLY_HIGH, BLOCK_MEDIUM_AND_ABOVE, BLOCK_LOW_AND_ABOVE
GEMINI_BLOCK_DANGEROUS=BLOCK_NONE
GEMINI_BLOCK_HARASSMENT=BLOCK_ONLY_HIGH
GEMINI_BLOCK_HATE=BLOCK_ONLY_HIGH
GEMINI_BLOCK_SEXUAL=BLOCK_ONLY_HIGH

# ============================================================================
# USAGE INSTRUCTIONS
# ============================================================================
#
# 1. Get your Google Gemini API key:
#    - Visit: https://aistudio.google.com/app/apikey
#    - Sign in with Google account
#    - Click "Create API key"
#    - Copy the key (starts with AIzaSy...)
#
# 2. Get your Discord Bot Token:
#    - Visit: https://discord.com/developers/applications
#    - Create new application or select existing
#    - Go to "Bot" section
#    - Reset token and copy it
#
# 3. Fill in the values above:
#    DISCORD_BOT_TOKEN=your_discord_token_here
#    GEMINI_API_KEY=your_gemini_api_key_here
#
# 4. Save this file as .env in your project root
#
# 5. NEVER commit this file to GitHub!
#    (Already in .gitignore)
#
# ============================================================================

# ============================================================================
# FREE TIER LIMITS (Google Gemini)
# ============================================================================
#
# Gemini 1.5 Flash:
#   - 15 requests per minute (RPM)
#   - 1 million requests per day (RPD)
#   - 1M token context window
#   - FREE forever
#
# Gemini 1.5 Pro:
#   - 2 requests per minute (RPM)
#   - 50 requests per day (RPD)
#   - 2M token context window
#   - FREE forever
#
# No credit card required!
#
# ============================================================================
```

### **Step 4: Verify Configuration**

```bash
# Check if .env file is properly formatted
cat .env  # Linux/Mac
type .env  # Windows

# Test loading .env
python -c "from dotenv import load_dotenv; load_dotenv(); print('✅ .env loaded successfully')"

# Check specific variables (without exposing keys)
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Discord Token:', 'SET' if os.getenv('DISCORD_BOT_TOKEN') else 'NOT SET'); print('Gemini Key:', 'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET')"
```

**Expected output:**
```
✅ .env loaded successfully
Discord Token: SET
Gemini Key: SET
```

---

## 📁 Directory Structure

### **Verify Directory Structure**

```bash
# Check if all directories exist
ls -R  # Linux/Mac basic listing
tree   # If tree is installed (detailed)
dir /s # Windows

# Quick check for required directories
ls -d bot/ data/ prompts/ logs/ 2>/dev/null || echo "Some directories missing"
```

### **Required Directory Structure**

```
try-harder-ai/
├── .env                  ✅ Environment variables (YOU CREATE THIS)
├── .gitignore            ✅ Git ignore rules
├── LICENSE               ✅ MIT License
├── README.md             ✅ Project overview
├── QUICKSTART.md         ✅ Quick 5-minute setup
├── SETUP.md              ✅ This file - detailed setup
├── requirements.txt      ✅ Python dependencies
├── main.py               ✅ Bot entry point
│
├── bot/                  ✅ Core bot code
│   ├── __init__.py
│   ├── commands.py       # Discord slash command handlers
│   ├── assessment.py     # Skill assessment logic
│   ├── roadmap.py        # AI-powered roadmap generation
│   ├── gemini_engine.py  # Google Gemini AI integration
│   ├── user_manager.py   # User state and progress tracking
│   └── logging_config.py # Logging configuration
│
├── data/                 ✅ Data files (YAML, JSON)
│   ├── certifications.yaml  # 9 OffSec certifications
│   ├── questions.yaml       # 90+ assessment questions
│   ├── resources.yaml       # 150+ learning resources
│   └── user_data.json       # User progress (auto-generated)
│
├── image and logo/       ✅ Logo and Banner image for discord bot
│   ├── Banner.png
│   └── Logo.png
|
├── prompts/              ✅ AI system prompts
│   ├── system_prompt.txt    # Base system instruction
│   ├── oscp_prompt.txt      # OSCP-specific guidance
│   ├── osep_prompt.txt      # OSEP-specific guidance
│   └── ...                  # Other certification prompts
│
├── config/               ✅ Configuration files
│   └── settings.py          # Centralized settings
│
├── utils/                ✅ Utility functions
│   ├── formatters.py        # Discord embed formatting
│   ├── helpers.py           # Helper functions
│   └── validators.py        # Input validation
│
├── docs/                 ✅ Documentation
│   ├── API_INTEGRATION.md   # Gemini API details
│   ├── ARCHITECTURE.md      # System architecture
│   ├── DEPLOYMENT.md        # Production deployment
│   └── CONTRIBUTING.md      # Contribution guidelines
│
├── tests/                ✅ Unit tests
│   ├── test_ai_engine.py
│   ├── test_assessment.py
│   └── test_commands.py
│
├── logs/                 ⚠️ Auto-created on first run
│   └── bot.log              # Main log file
│
└── backups/              ⚠️ Auto-created on first backup
    └── backup_YYYYMMDD/     # Timestamped backups
```

### **Create Missing Directories**

If any directories are missing, create them:

```bash
# Create all required directories at once
mkdir -p logs backups data prompts config utils docs tests

# Linux/Mac - verify permissions
chmod 755 logs backups data

# Verify all directories exist
ls -d bot/ data/ prompts/ logs/ backups/ config/ utils/ docs/ tests/
```

**Expected output:**
```
bot/  config/  data/  docs/  logs/  prompts/  tests/  utils/  backups/
```

### **File Permissions (Linux/Mac Only)**

```bash
# Make main.py executable
chmod +x main.py

# Secure .env file (only owner can read/write)
chmod 600 .env

# Verify permissions
ls -l .env main.py

# Expected for .env:
# -rw------- 1 user user ... .env

# Expected for main.py:
# -rwxr-xr-x 1 user user ... main.py
```

---

## 🎯 First Run

### **Step 1: Pre-flight Check**

Before running the bot, verify everything is ready:

```bash
# 1. Check you're in the project directory
pwd  # Should show: /path/to/try-harder-ai

# 2. Virtual environment activated?
which python  # Should show venv/bin/python
# Windows: where python  # Should show venv\Scripts\python.exe

# 3. Dependencies installed?
pip list | grep discord  # Should show discord.py
pip list | grep google   # Should show google-generativeai

# 4. .env file exists and configured?
test -f .env && echo "✅ .env exists" || echo "❌ .env missing"

# 5. Data files exist?
test -f data/certifications.yaml && echo "✅ Certifications OK"
test -f data/questions.yaml && echo "✅ Questions OK"
test -f data/resources.yaml && echo "✅ Resources OK"

# 6. Directories exist?
test -d logs && echo "✅ Logs directory OK" || mkdir logs
test -d backups && echo "✅ Backups directory OK" || mkdir backups
```

### **Step 2: Test Bot Startup**

```bash
# Make sure you're in project directory
cd try-harder-ai

# Activate virtual environment if not already active
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run the bot
python main.py

# Alternative if main.py is not at root:
python bot/main.py
```

### **Step 3: Expected Startup Output**

You should see this beautiful banner:

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              🎯 TRY-HARDER-AI BOT v2.0.0-gemini      ║
║                                                          ║
║        Your Personal OffSec Certification Mentor        ║
║             Powered by Google Gemini AI 🤖              ║
║                                                          ║
║  Supported Certifications: 9                          ║
║  AI Model: gemini-1.5-flash                 ║
║  Context Window: 1M tokens (Flash) / 2M (Pro)           ║
║  Status: Ready to Help You Try Harder! 💪               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

🔥 FREE Tier Active:
   • Gemini 1.5 Flash: 15 requests/minute
   • Gemini 1.5 Pro: 2 requests/minute
   • No credit card required!

[2026-02-14 10:30:45] [INFO] Loading configuration...
[2026-02-14 10:30:45] [INFO] Configuration loaded successfully
[2026-02-14 10:30:45] [INFO] Loading data files...
[2026-02-14 10:30:46] [INFO] ✅ Loaded 9 certifications
[2026-02-14 10:30:46] [INFO] ✅ Loaded 90 questions
[2026-02-14 10:30:46] [INFO] ✅ Loaded 150+ resources
[2026-02-14 10:30:46] [INFO] Initializing Gemini AI...
[2026-02-14 10:30:46] [INFO] ✅ Gemini AI engine initialized with model: gemini-1.5-flash
[2026-02-14 10:30:46] [INFO] Connecting to Discord...
[2026-02-14 10:30:47] [SUCCESS] Bot logged in as: Try-Harder-AI#1234
[2026-02-14 10:30:47] [INFO] Connected to 1 server(s)
[2026-02-14 10:30:47] [INFO] Registering slash commands...
[2026-02-14 10:30:48] [SUCCESS] 15 commands registered
[2026-02-14 10:30:48] [SUCCESS] ✅ Bot is ready! 🚀
[2026-02-14 10:30:48] [INFO] Serving 0 users across 1 servers
[2026-02-14 10:30:48] [INFO] Press Ctrl+C to stop
```

**Bot status in Discord should change to: 🟢 Online**

### **Step 4: Common Startup Errors**

#### **Error: "discord.errors.LoginFailure: Improper token"**

```
❌ Problem: Invalid Discord bot token
✅ Solution: 
   1. Check DISCORD_BOT_TOKEN in .env
   2. Make sure you copied the FULL token (no spaces)
   3. Token should start with M or N and be very long
   4. Reset token in Discord Developer Portal if needed
   5. Restart bot after updating .env
```

#### **Error: "FileNotFoundError: .env file not found"**

```
❌ Problem: .env file missing or in wrong location
✅ Solution:
   1. Make sure .env exists in root directory
   2. Check you're in correct directory: pwd (should show try-harder-ai/)
   3. Create .env if missing: touch .env (Linux/Mac) or type nul > .env (Windows)
   4. Copy template from SETUP.md and fill in values
```

#### **Error: "GEMINI_API_KEY not found in environment variables"**

```
❌ Problem: Gemini API key not set in .env
✅ Solution:
   1. Check GEMINI_API_KEY in .env file
   2. Verify API key starts with AIzaSy...
   3. Make sure no quotes around the key
   4. Restart bot after adding key
   5. Test key at https://aistudio.google.com
```

#### **Error: "yaml.scanner.ScannerError"**

```
❌ Problem: Malformed YAML file
✅ Solution:
   1. Check data/certifications.yaml syntax
   2. Ensure proper indentation (spaces, not tabs)
   3. Validate YAML online: yamllint.com
   4. Look for missing colons, quotes, or brackets
   5. Compare with working YAML examples
```

#### **Error: "ModuleNotFoundError: No module named 'discord'"**

```
❌ Problem: Dependencies not installed
✅ Solution:
   1. Activate virtual environment: source venv/bin/activate
   2. Verify activation: which python (should show venv path)
   3. Install dependencies: pip install -r requirements.txt
   4. Check installation: pip show discord.py
```

#### **Error: "Gemini API error: 403 Forbidden"**

```
❌ Problem: Invalid API key or API not enabled
✅ Solution:
   1. Verify API key at https://aistudio.google.com/app/apikey
   2. Regenerate API key if needed
   3. Check you're not rate limited
   4. Ensure Generative Language API is enabled
   5. Wait a few minutes and try again
```

#### **Error: "Port already in use" or "Address already in use"**

```
❌ Problem: Another instance of bot is running
✅ Solution:
   1. Check for running instances: ps aux | grep python (Linux/Mac)
   2. Kill old instance: pkill -f "python main.py"
   3. Or on Windows: tasklist | findstr python
   4. Kill process: taskkill /F /PID <process_id>
   5. Start bot again
```

---

## ✔️ Verification

### **Step 1: Check Bot Status in Discord**

1. Open Discord
2. Go to your server where you invited the bot
3. Check member list on the right side
4. Bot should show **🟢 Online** status
5. Bot should have "BOT" tag next to name
6. Bot's status should show your configured message (e.g., "Try Harder! 💪")

### **Step 2: Test Basic Slash Commands**

Open Discord and go to your server. **Note: Slash commands may take up to 1 hour to register globally. For instant testing, test in your server where bot was first invited.**

Type `/` in any channel and you should see Try-Harder-AI commands appear.

**Test Help Command:**
```
/help
```

**Expected response:**
```
📚 Try-Harder-AI Bot Commands

🎯 Getting Started:
• /start - Welcome message and introduction
• /help - Show this help message
• /certs - List all supported certifications

📝 Assessments & Learning:
• /assess <cert> - Start skill assessment
• /roadmap - Generate personalized study plan
• /ask <question> - Ask any cybersecurity question

📊 Progress Tracking:
• /progress - View your progress and statistics
• /stats - Show bot statistics

... (more commands)

💡 Tip: All commands use / prefix (slash commands)
```

### **Step 3: Test Certification Commands**

```
/certs
```

**Expected response:**
```
🎯 Supported OffSec Certifications

1️⃣ OSCP - Offensive Security Certified Professional
2️⃣ OSEP - Offensive Security Experienced Penetration Tester
3️⃣ OSWE - Offensive Security Web Expert
4️⃣ OSED - Offensive Security Exploit Developer
5️⃣ OSWP - Offensive Security Wireless Professional
6️⃣ OSWA - OffSec Web Assessor
7️⃣ OSMR - OffSec macOS Researcher
8️⃣ OSDA - OffSec Defense Analyst
9️⃣ KLCP - Kali Linux Certified Professional

Use /assess <cert> to start an assessment!
```

### **Step 4: Test AI Integration**

This is the most important test - verifying Google Gemini integration works:

```
/ask What is Nmap and why is it important for penetration testing?
```

**Expected response (from Google Gemini):**
```
🔍 Nmap (Network Mapper)

Nmap is a powerful open-source network scanning tool used for:

✅ **Key Features:**
• Port scanning - Discover open ports on target systems
• Service detection - Identify running services and versions
• OS fingerprinting - Determine target operating system
• Network mapping - Map network topology

⚡ **Why Important for PenTesting:**
1️⃣ **Reconnaissance** - First step in penetration testing
2️⃣ **Attack Surface** - Identify potential entry points
3️⃣ **Vulnerability Detection** - Find outdated services
4️⃣ **Network Understanding** - Understand target infrastructure

💡 **Common Nmap Commands:**
• Basic scan: `nmap target.com`
• Service version: `nmap -sV target.com`
• Aggressive scan: `nmap -A target.com`
• All ports: `nmap -p- target.com`

🎯 Nmap is essential for OSCP, OSEP, and all penetration testing certifications!
```

**If you see response with emojis and formatting like above:** ✅ **Gemini integration is working!**

### **Step 5: Test Assessment System**

```
/assess OSCP
```

**Expected response:**
```
📝 OSCP Skill Assessment

Welcome to the OSCP skill assessment! This quiz will help evaluate your current knowledge level.

⏱️ You'll have 60 seconds per question
📊 10 questions covering beginner to advanced topics
🎯 Answer carefully - this determines your personalized roadmap!

Ready to begin? React with ✅ to start!
```

Then bot will ask 10 questions one by one. Example:

```
Question 1/10 (Beginner)

What port does HTTP typically use?

A) 80
B) 443
C) 22
D) 3389

Reply with A, B, C, or D
```

### **Step 6: Test Roadmap Generation**

After completing assessment:

```
/roadmap
```

**Expected response (AI-generated):**
```
🗺️ Your Personalized OSCP Study Roadmap

Based on your assessment results (Score: 65%), here's your 12-week study plan:

📊 Current Level: Intermediate
🎯 Target: OSCP Certification
⏰ Study Time: 15 hours/week

**Week 1-2: Enumeration Fundamentals**
...

(AI generates detailed week-by-week plan using Google Gemini)
```

### **Step 7: Check Logs**

Verify everything is being logged properly:

```bash
# View recent logs
tail -n 50 logs/bot.log

# Linux/Mac - follow logs in real-time
tail -f logs/bot.log

# Windows PowerShell - follow logs
Get-Content logs\bot.log -Wait -Tail 50

# Search for errors
grep -i "error" logs/bot.log
grep -i "exception" logs/bot.log

# Check Gemini API calls
grep "Gemini API" logs/bot.log | tail -n 10
```

**Look for these log entries:**
```
[INFO] ✅ Gemini AI engine initialized
[INFO] Model: gemini-1.5-flash
[SUCCESS] AI response received (Attempt 1)
[INFO] Command used: /ask by User#1234
[INFO] Gemini API response received
```

**No errors should appear for:**
- Configuration loading
- Data file loading
- Gemini initialization
- Command registration

---

## 🎓 Post-Installation

### **Step 1: Customize Bot Behavior**

Edit `.env` to customize bot behavior:

```env
# Change bot status message
BOT_STATUS=Learning OffSec! | /help

# Change default AI model
DEFAULT_AI_MODEL=gemini-1.5-pro  # For better quality
# or
DEFAULT_AI_MODEL=gemini-1.5-flash-8b  # For faster responses

# Adjust command cooldowns
COMMAND_COOLDOWN_SECONDS=3  # Faster
# or
COMMAND_COOLDOWN_SECONDS=10  # More conservative

# Change assessment difficulty
ASSESSMENT_QUESTIONS_PER_TEST=15  # More questions
ASSESSMENT_PASS_PERCENTAGE=75  # Higher passing grade

# Adjust roadmap length
DEFAULT_ROADMAP_DURATION_WEEKS=8  # Shorter plan
# or
DEFAULT_ROADMAP_DURATION_WEEKS=16  # Longer plan
```

### **Step 2: Add Custom AI Prompts**

Customize how AI responds for each certification:

```bash
# Edit OSCP-specific prompt
nano prompts/oscp_prompt.txt
# or
code prompts/oscp_prompt.txt
```

**Example custom prompt:**
```
You are an elite OSCP mentor specializing in Active Directory attacks.

**Your Communication Style:**
- Use emojis liberally (🎯 💡 ✅ 🔥 ⚡)
- Format answers in clear numbered steps
- Provide specific command examples
- Reference GTFOBins, PayloadsAllTheThings, HackTricks

**Your Expertise:**
- Active Directory enumeration and exploitation
- Kerberos attacks (Kerberoasting, AS-REP roasting)
- NTLM relay and hash manipulation
- BloodHound analysis
- Lateral movement techniques
- Privilege escalation (Windows & Linux)

**When answering questions:**
1️⃣ Start with a clear definition
2️⃣ Explain why it's important for OSCP
3️⃣ Provide specific tool commands
4️⃣ Give practical examples
5️⃣ Link to relevant resources

Always be encouraging and remind users to "Try Harder!"
```

### **Step 3: Add Custom Resources**

Edit `data/resources.yaml` to add your favorite resources:

```yaml
OSCP:
  books:
    - name: "Penetration Testing: A Hands-On Introduction"
      url: "https://www.amazon.com/..."
      cost: "paid"
      priority: "high"
      
    - name: "YOUR FAVORITE BOOK"
      url: "https://..."
      cost: "free"
      priority: "high"
      notes: "Excellent for beginners"
  
  practice_platforms:
    - name: "HackTheBox"
      url: "https://hackthebox.com"
      cost: "freemium"
      priority: "essential"
      
    - name: "YOUR CUSTOM LAB"
      url: "https://..."
      cost: "free"
      priority: "recommended"
```

### **Step 4: Create Backups**

Set up automated backups:

```bash
# Manual backup
cp -r data/ backups/data_$(date +%Y%m%d)/  # Linux/Mac
xcopy data backups\data_%date%\ /E /I  # Windows

# Create backup script
nano scripts/backup.sh
```

**Backup script example:**
```bash
#!/bin/bash
# Save as scripts/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/backup_$DATE"

mkdir -p $BACKUP_DIR
cp -r data/ $BACKUP_DIR/
cp .env $BACKUP_DIR/.env.backup
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR/
rm -rf $BACKUP_DIR

# Keep only last 7 backups
ls -t backups/*.tar.gz | tail -n +8 | xargs rm -f

echo "✅ Backup complete: $BACKUP_DIR.tar.gz"
```

**Make executable and run:**
```bash
chmod +x scripts/backup.sh
./scripts/backup.sh
```

### **Step 5: Monitor Performance**

Keep an eye on resource usage:

```bash
# Check bot resource usage (Linux/Mac)
ps aux | grep python
top | grep python

# Windows
tasklist | findstr python
wmic process where name="python.exe" get ProcessId,WorkingSetSize

# Check disk usage
du -sh data/ logs/ backups/  # Linux/Mac
dir data logs backups  # Windows

# Monitor API usage
grep "Gemini API" logs/bot.log | wc -l  # Total calls
grep "$(date +%Y-%m-%d)" logs/bot.log | grep "Gemini API" | wc -l  # Today
```

**Expected resource usage:**
- **CPU**: 1-5% idle, 10-30% during AI requests
- **RAM**: 50-200 MB
- **Disk**: <100 MB (plus logs)
- **Network**: Minimal when idle, spikes during AI requests

---

## 🔧 Advanced Configuration

### **1. Custom AI Model Selection**

You can dynamically switch between Gemini models:

```env
# For everyday use (RECOMMENDED)
DEFAULT_AI_MODEL=gemini-1.5-flash
# Pros: Fast (⚡⚡⚡), 15 RPM free, 1M context
# Best for: Quick questions, assessments, daily study

# For complex roadmaps and detailed explanations
DEFAULT_AI_MODEL=gemini-1.5-pro
# Pros: Best quality (⚡⚡), 2M context
# Cons: Only 2 RPM free
# Best for: Roadmap generation, complex topics

# For ultra-fast simple queries
DEFAULT_AI_MODEL=gemini-1.5-flash-8b
# Pros: Fastest (⚡⚡⚡⚡), 15 RPM free
# Best for: Quick definitions, simple questions
```

### **2. Adjust Safety Settings**

For cybersecurity content, you may want to adjust safety:

```env
# Very permissive (recommended for security content)
GEMINI_BLOCK_DANGEROUS=BLOCK_NONE  # Allow security tools/exploits
GEMINI_BLOCK_HARASSMENT=BLOCK_ONLY_HIGH
GEMINI_BLOCK_HATE=BLOCK_ONLY_HIGH
GEMINI_BLOCK_SEXUAL=BLOCK_ONLY_HIGH

# Moderate (balanced)
GEMINI_BLOCK_DANGEROUS=BLOCK_ONLY_HIGH
GEMINI_BLOCK_HARASSMENT=BLOCK_ONLY_HIGH
GEMINI_BLOCK_HATE=BLOCK_MEDIUM_AND_ABOVE
GEMINI_BLOCK_SEXUAL=BLOCK_MEDIUM_AND_ABOVE

# Strict (most restrictive)
GEMINI_BLOCK_DANGEROUS=BLOCK_MEDIUM_AND_ABOVE
GEMINI_BLOCK_HARASSMENT=BLOCK_MEDIUM_AND_ABOVE
GEMINI_BLOCK_HATE=BLOCK_LOW_AND_ABOVE
GEMINI_BLOCK_SEXUAL=BLOCK_LOW_AND_ABOVE
```

### **3. Database Integration (Future)**

For PostgreSQL integration (not yet implemented):

```bash
# Install PostgreSQL
# Ubuntu
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql

# Install Python adapter
pip install asyncpg

# Create database
sudo -u postgres createdb tryharderai

# Configure in .env
DATABASE_URL=postgresql://username:password@localhost/tryharderai
ENABLE_DATABASE=true
```

### **4. Redis Caching (Optional)**

For advanced caching to reduce API calls:

```bash
# Install Redis
# Ubuntu
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis

# macOS
brew install redis
brew services start redis

# Install Python client
pip install redis aioredis

# Configure in .env
REDIS_URL=redis://localhost:6379
ENABLE_REDIS_CACHE=true
CACHE_TTL_SECONDS=3600
```

**Benefits:**
- Reduces duplicate AI API calls
- Faster responses for repeated questions
- Lower API usage

### **5. Monitoring & Metrics (Advanced)**

Set up Prometheus metrics:

```bash
# Install prometheus client
pip install prometheus-client

# Configure in .env
ENABLE_METRICS=true
METRICS_PORT=9090

# Access metrics at:
# http://localhost:9090/metrics
```

**Metrics tracked:**
- Total commands executed
- AI API calls and response times
- Error rates
- User activity
- Memory and CPU usage

### **6. Multi-Server Support**

To run bot across multiple Discord servers:

```env
# No special configuration needed!
# Bot automatically works on all servers where it's invited

# Optional: Set different behavior per server
ENABLE_PER_SERVER_SETTINGS=true

# Optional: Restrict to specific servers
ALLOWED_SERVER_IDS=123456789,987654321
```

---

## 🔧 Troubleshooting

### **Section 1: Bot Won't Start**

#### **Problem: Bot starts then immediately crashes**

**Symptoms:**
```
[INFO] Bot is ready!
[ERROR] Task exception was never retrieved
Traceback (most recent call last):
...
```

**Solutions:**
1. **Check Python version:**
   ```bash
   python --version  # Must be 3.10+
   ```

2. **Reinstall dependencies:**
   ```bash
   pip install --force-reinstall -r requirements.txt
   ```

3. **Check for conflicting packages:**
   ```bash
   pip list | grep discord
   # Should only show discord.py, not discord (old package)
   
   # If old discord package exists, remove it:
   pip uninstall discord  # Old package
   pip install discord.py  # Correct package
   ```

4. **Enable debug mode:**
   ```env
   DEBUG_MODE=true
   LOG_LEVEL=DEBUG
   ```

#### **Problem: Bot goes offline after few minutes**

**Symptoms:**
- Bot shows online, then goes offline
- No errors in logs
- Happens randomly

**Solutions:**
1. **Check network stability:**
   ```bash
   ping discord.com  # Should show consistent response times
   ```

2. **Increase timeout:**
   ```env
   AI_TIMEOUT=120  # Increase from 60 to 120 seconds
   ```

3. **Check system resources:**
   ```bash
   # Linux/Mac
   free -h  # Check available RAM
   df -h    # Check disk space
   
   # Windows
   systeminfo | find "Available Physical Memory"
   ```

4. **Run bot with nohup (Linux/Mac):**
   ```bash
   nohup python main.py > /dev/null 2>&1 &
   ```

### **Section 2: Slash Commands Not Working**

#### **Problem: Slash commands don't appear in Discord**

**Symptoms:**
- Type `/` and bot commands don't show up
- Bot is online but no slash commands

**Solutions:**
1. **Check bot permissions:**
   - Go to Discord Developer Portal
   - Your Application → OAuth2 → URL Generator
   - Verify `applications.commands` scope is selected
   - Re-invite bot using new URL if needed

2. **Wait for global sync:**
   ```
   ⏰ Slash commands can take up to 1 hour to sync globally
   ```
   - Test in your original server first
   - Guild (server) commands sync instantly
   - Global commands sync slowly

3. **Force command sync (for testing):**
   Add to main.py temporarily:
   ```python
   @bot.event
   async def on_ready():
       print(f'{bot.user} has connected to Discord!')
       await bot.tree.sync()  # Force sync
       print('Commands synced!')
   ```

4. **Check Discord Developer Mode:**
   - Discord Settings → Advanced → Developer Mode → ON
   - This helps see command IDs and debug issues

#### **Problem: Commands work but bot doesn't respond**

**Symptoms:**
- Commands appear when typing `/`
- Bot shows "Bot is thinking..."
- Then times out with no response

**Solutions:**
1. **Check Message Content Intent:**
   - Discord Developer Portal → Your Bot → Bot tab
   - Scroll to "Privileged Gateway Intents"
   - ✅ Enable "Message Content Intent"

2. **Check for errors in logs:**
   ```bash
   grep -i "error" logs/bot.log
   tail -n 100 logs/bot.log
   ```

3. **Test AI connection:**
   ```bash
   # Run Gemini test
   python -c "from bot.gemini_engine import test_connection; import asyncio; asyncio.run(test_connection())"
   ```

4. **Increase timeout in code:**
   Edit `bot/gemini_engine.py` if needed:
   ```python
   timeout=aiohttp.ClientTimeout(total=120)  # Increase from 60
   ```

### **Section 3: AI Responses Failing**

#### **Problem: "Gemini API error" messages**

**Symptoms:**
```
⚠️ AI service error. Please try again later.
```

**Solutions:**
1. **Verify API key:**
   ```bash
   # Test API key directly
   curl "https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_KEY"
   ```

2. **Check rate limits:**
   ```bash
   # Count recent API calls
   grep "Gemini API" logs/bot.log | grep "$(date +%Y-%m-%d)" | wc -l
   
   # If > 900 calls today, you might be hitting daily limit
   ```

3. **Check Gemini service status:**
   - Visit https://status.cloud.google.com/
   - Look for Generative Language API status

4. **Regenerate API key:**
   - Go to https://aistudio.google.com/app/apikey
   - Create new key
   - Update .env with new key
   - Restart bot

#### **Problem: "Rate limit exceeded" errors**

**Symptoms:**
```
⚠️ Rate limit exceeded. Please wait a moment.
```

**Solutions:**
1. **Reduce concurrent requests:**
   ```env
   MAX_CONCURRENT_AI_REQUESTS=1  # Down from 2
   ```

2. **Increase cooldown:**
   ```env
   COMMAND_COOLDOWN_SECONDS=10  # Up from 4
   ```

3. **Switch to Flash-8B for simple queries:**
   ```env
   DEFAULT_AI_MODEL=gemini-1.5-flash-8b
   ```

4. **Monitor usage:**
   ```bash
   # Check calls per minute
   grep "Gemini API" logs/bot.log | tail -n 20 | awk '{print $1" "$2}'
   ```

5. **Wait before retrying:**
   - Flash: Wait 1 minute (15 RPM limit)
   - Pro: Wait 1 minute (2 RPM limit)

### **Section 4: Data and File Issues**

#### **Problem: "YAML file error" or "Failed to load data"**

**Symptoms:**
```
[ERROR] Error parsing YAML file data/certifications.yaml
yaml.scanner.ScannerError: ...
```

**Solutions:**
1. **Validate YAML syntax:**
   - Visit https://www.yamllint.com/
   - Paste your YAML content
   - Fix any syntax errors

2. **Check file encoding:**
   ```bash
   file -i data/certifications.yaml
   # Should show: charset=utf-8
   ```

3. **Look for common YAML mistakes:**
   - Tabs instead of spaces (use spaces only!)
   - Missing colons after keys
   - Incorrect indentation
   - Unescaped special characters

4. **Restore from backup:**
   ```bash
   cp backups/latest/data/certifications.yaml data/
   ```

#### **Problem: User data not saving**

**Symptoms:**
- Progress not tracked
- Assessments don't save results
- `user_data.json` not updating

**Solutions:**
1. **Check file permissions:**
   ```bash
   ls -l data/user_data.json
   # Should be writable by bot user
   
   chmod 644 data/user_data.json
   ```

2. **Verify AUTO_SAVE enabled:**
   ```env
   AUTO_SAVE_INTERVAL=300
   ```

3. **Check disk space:**
   ```bash
   df -h  # Linux/Mac
   dir    # Windows
   ```

4. **Check logs for save errors:**
   ```bash
   grep -i "save" logs/bot.log | grep -i "error"
   ```

### **Section 5: Performance Issues**

#### **Problem: Bot is slow to respond**

**Solutions:**
1. **Use faster AI model:**
   ```env
   DEFAULT_AI_MODEL=gemini-1.5-flash-8b  # Fastest
   ```

2. **Enable response caching:**
   ```env
   ENABLE_RESPONSE_CACHE=true
   CACHE_TTL_SECONDS=3600
   ```

3. **Reduce max tokens:**
   ```env
   AI_MAX_TOKENS=4096  # Down from 8192
   ```

4. **Check server resources:**
   ```bash
   top  # Check CPU/RAM usage
   ```

#### **Problem: High memory usage**

**Solutions:**
1. **Restart bot periodically:**
   ```bash
   # Use cron job (Linux/Mac)
   0 3 * * * pkill -f "python main.py" && cd /path/to/bot && python main.py
   ```

2. **Disable caching:**
   ```env
   ENABLE_RESPONSE_CACHE=false
   ```

3. **Reduce concurrent requests:**
   ```env
   MAX_CONCURRENT_AI_REQUESTS=1
   ```

### **Section 6: Discord-Specific Issues**

#### **Problem: Bot can't see messages**

**Solutions:**
1. **Enable Message Content Intent** (most common fix)
2. **Check channel permissions:**
   - Bot needs "View Channel" permission
   - Bot needs "Read Message History"

3. **Verify bot role hierarchy:**
   - Server Settings → Roles
   - Bot's role should be high enough

#### **Problem: Bot can't send embeds**

**Solutions:**
1. **Check "Embed Links" permission**
2. **Verify Discord isn't blocking embeds:**
   - User Settings → Text & Images → Show website preview info from links

---

## 🔒 Security Best Practices

### **1. Protect Your API Keys**

```bash
# ✅ DO:
# Store keys in .env (already in .gitignore)
# Use environment variables
# Rotate keys monthly

# ❌ DON'T:
# Hardcode keys in source code
# Share keys publicly
# Commit .env to Git
# Screenshot with visible keys
```

**Check if .env is in gitignore:**
```bash
cat .gitignore | grep .env
# Should show: .env
```

**If accidentally committed:**
```bash
# Remove from Git history
git rm --cached .env
git commit -m "Remove .env from tracking"

# Rotate all keys immediately!
# 1. Generate new Discord bot token
# 2. Generate new Gemini API key
# 3. Update .env
# 4. Restart bot
```

### **2. Secure File Permissions**

```bash
# Linux/Mac only
chmod 600 .env  # Only owner can read/write
chmod 700 logs/  # Only owner can access logs
chmod 700 backups/  # Only owner can access backups

# Verify
ls -l .env
# Should show: -rw------- (600)
```

### **3. Regular Updates**

```bash
# Update dependencies monthly
pip install --upgrade -r requirements.txt

# Check for security vulnerabilities
pip install safety
safety check

# Update specific packages
pip install --upgrade discord.py
pip install --upgrade google-generativeai
pip install --upgrade aiohttp
```

**Create update script:**
```bash
#!/bin/bash
# Save as scripts/update.sh

echo "🔄 Updating Try-Harder-AI Bot..."

# Activate venv
source venv/bin/activate

# Update pip
pip install --upgrade pip

# Update all packages
pip install --upgrade -r requirements.txt

# Run security check
pip install safety
safety check

# Show what changed
pip list --outdated

echo "✅ Update complete!"
```

### **4. Rate Limiting Protection**

Protect against abuse:

```env
# Per-user limits
USER_DAILY_AI_LIMIT=100
COMMAND_COOLDOWN_SECONDS=4

# Global limits
MAX_CONCURRENT_AI_REQUESTS=2
```

**Add IP-based rate limiting (advanced):**
```python
# In bot/commands.py
from collections import defaultdict
from datetime import datetime, timedelta

user_requests = defaultdict(list)

def check_rate_limit(user_id: int, max_requests: int = 10) -> bool:
    now = datetime.utcnow()
    cutoff = now - timedelta(minutes=1)
    
    # Remove old requests
    user_requests[user_id] = [
        req for req in user_requests[user_id] 
        if req > cutoff
    ]
    
    # Check limit
    if len(user_requests[user_id]) >= max_requests:
        return False
    
    # Add current request
    user_requests[user_id].append(now)
    return True
```

### **5. Input Validation**

Always validate user input:

```python
# Already implemented in bot/validators.py
from bot.validators import (
    sanitize_user_input,
    validate_certification,
    validate_question_text
)

# Example usage in commands
@app_commands.command()
async def ask(interaction: discord.Interaction, question: str):
    # Sanitize input
    clean_question = sanitize_user_input(question, max_length=500)
    
    # Validate
    is_valid, error = validate_question_text(clean_question)
    if not is_valid:
        return await interaction.response.send_message(
            f"❌ {error}",
            ephemeral=True
        )
    
    # Process...
```

### **6. Logging and Monitoring**

Monitor for suspicious activity:

```bash
# Check for unusual patterns
grep -i "error" logs/bot.log | tail -n 50
grep -i "exception" logs/bot.log | tail -n 50
grep -i "rate limit" logs/bot.log | tail -n 50

# Monitor API usage
grep "Gemini API" logs/bot.log | wc -l

# Check for repeated failures from same user
grep "User:" logs/bot.log | sort | uniq -c | sort -nr | head -n 10
```

### **7. Secure Deployment**

For production deployment:

```bash
# Use systemd service (Linux)
sudo nano /etc/systemd/system/try-harder-ai.service
```

```ini
[Unit]
Description=Try-Harder-AI Discord Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/try-harder-ai
ExecStart=/home/botuser/try-harder-ai/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable try-harder-ai
sudo systemctl start try-harder-ai

# Check status
sudo systemctl status try-harder-ai

# View logs
sudo journalctl -u try-harder-ai -f
```

---

## 🛠️ Maintenance

### **Daily Tasks**

```bash
# Check bot status
ps aux | grep python | grep main.py  # Linux/Mac
tasklist | findstr python  # Windows

# Check for errors
tail -n 100 logs/bot.log | grep -i "error"

# Monitor API usage
grep "$(date +%Y-%m-%d)" logs/bot.log | grep "Gemini API" | wc -l
```

### **Weekly Tasks**

```bash
# Clean old logs
find logs/ -name "*.log.*" -mtime +7 -delete  # Linux/Mac

# Check disk usage
du -sh data/ logs/ backups/

# Review user activity
grep "Command used:" logs/bot.log | tail -n 100

# Test critical commands
# In Discord: /help, /ask, /assess
```

### **Monthly Tasks**

**1. Update Dependencies:**
```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
safety check
```

**2. Security Audit:**
```bash
# Check for exposed secrets
grep -r "AIzaSy" . --exclude-dir=venv --exclude-dir=.git
grep -r "sk-or-v1" . --exclude-dir=venv --exclude-dir=.git

# Should only find them in .env (which is gitignored)
```

**3. Backup Data:**
```bash
# Create monthly backup
DATE=$(date +%Y%m)
tar -czf backups/monthly_backup_$DATE.tar.gz data/ .env prompts/

# Keep last 6 months of backups
ls -t backups/monthly_backup_*.tar.gz | tail -n +7 | xargs rm -f
```

**4. Review Logs:**
```bash
# Generate monthly report
echo "📊 Monthly Report - $(date +%B %Y)"
echo "================================"
echo "Total commands: $(grep 'Command used:' logs/bot.log | wc -l)"
echo "AI queries: $(grep 'Gemini API' logs/bot.log | wc -l)"
echo "Errors: $(grep -i 'error' logs/bot.log | wc -l)"
echo "Active users: $(grep 'User:' logs/bot.log | awk '{print $NF}' | sort -u | wc -l)"
```

**5. Rotate API Keys:**
```bash
# Every 3-6 months:
# 1. Generate new Gemini API key
# 2. Update .env
# 3. Restart bot
# 4. Delete old key from Google AI Studio
```

### **Log Rotation**

Set up automatic log rotation:

**Create logrotate config (Linux):**
```bash
sudo nano /etc/logrotate.d/try-harder-ai
```

```
/path/to/try-harder-ai/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 botuser botuser
}
```

### **Automated Maintenance Script**

```bash
#!/bin/bash
# Save as scripts/maintenance.sh

echo "🔧 Running maintenance tasks..."

# 1. Clean old logs
echo "📝 Cleaning logs..."
find logs/ -name "*.log.*" -mtime +7 -delete
find logs/ -name "*.log" -mtime +1 -exec gzip {} \;

# 2. Backup data
echo "💾 Creating backup..."
DATE=$(date +%Y%m%d)
tar -czf backups/auto_backup_$DATE.tar.gz data/

# 3. Keep only recent backups
ls -t backups/auto_backup_*.tar.gz | tail -n +8 | xargs rm -f

# 4. Check disk usage
echo "💿 Disk usage:"
du -sh data/ logs/ backups/

# 5. Check bot status
if pgrep -f "python main.py" > /dev/null; then
    echo "✅ Bot is running"
else
    echo "❌ Bot is not running!"
fi

echo "✅ Maintenance complete!"
```

**Schedule with cron:**
```bash
# Edit crontab
crontab -e

# Run maintenance daily at 3 AM
0 3 * * * /path/to/try-harder-ai/scripts/maintenance.sh
```

---

## 📞 Getting Help

If you're still having issues after following this guide:

### **1. Check Documentation**

- **README.md** - Project overview and features
- **QUICKSTART.md** - 5-minute quick setup
- **This SETUP.md** - Comprehensive setup guide
- **ANALYSIS_REPORT.md** - Technical architecture details

### **2. Search Logs**

```bash
# Find recent errors
tail -n 200 logs/bot.log | grep -i "error"

# Find exceptions
grep -i "exception" logs/bot.log | tail -n 20

# Find Gemini API issues
grep "Gemini" logs/bot.log | grep -i "error"
```

### **3. Enable Debug Mode**

```env
# In .env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
VERBOSE_LOGGING=true
```

Restart bot and reproduce the issue. Logs will have much more detail.

### **4. Test Components Individually**

```bash
# Test Gemini connection
python -c "from bot.gemini_engine import test_connection; import asyncio; asyncio.run(test_connection())"

# Test Discord connection
python -c "import discord; print(discord.__version__)"

# Test data loading
python -c "from bot.user_manager import UserManager; um = UserManager(); print('✅ Data loaded')"
```

### **5. Community Support**

- **GitHub Issues**: [Report bugs](https://github.com/The4v1/Try-Harder-AI/issues)
- **Discord Server**: [Get help from community](https://discord.gg/tryharderai)
- **Email Support**: support@tryharderai.com

### **6. Open New Issue**

When reporting issues, include:

```
**Environment:**
- OS: Ubuntu 22.04
- Python: 3.11.2
- discord.py: 2.3.2
- google-generativeai: 0.3.1

**Problem:**
[Clear description of the issue]

**Steps to Reproduce:**
1. Run command /ask What is Nmap?
2. Bot shows "thinking" but times out
3. Error in logs: [paste relevant log lines]

**Expected Behavior:**
Bot should respond with AI-generated answer

**Actual Behavior:**
Bot times out after 30 seconds

**Configuration:**
DEFAULT_AI_MODEL=gemini-1.5-flash
AI_TIMEOUT=60

**Logs:**
[Paste relevant logs - remove any API keys!]
```

---

## 🎉 Success!

If you've made it here and followed all steps, your Try-Harder-AI bot should be:

- ✅ Running smoothly with Google Gemini AI (100% FREE!)
- ✅ Responding to slash commands (`/`)
- ✅ Providing AI-powered answers with emojis and formatting
- ✅ Tracking user progress across certifications
- ✅ Generating personalized study roadmaps
- ✅ Conducting skill assessments
- ✅ Logging all activity properly
- ✅ Secured with best practices

### **Next Steps:**

**For Users:**
1. **Take assessment**: `/assess OSCP`
2. **Ask questions**: `/ask What is privilege escalation?`
3. **Generate roadmap**: `/roadmap`
4. **Track progress**: `/progress`
5. **Get exam tips**: `/tips OSCP`
6. **View resources**: `/resources OSCP`

**For Admins:**
1. **Monitor logs**: `tail -f logs/bot.log`
2. **Check API usage**: Monitor Gemini requests
3. **Backup data**: Run backup script weekly
4. **Update regularly**: Monthly dependency updates
5. **Customize prompts**: Edit prompts/ directory

### **Pro Tips:**

💡 **Use Gemini Flash** (default) for everyday questions - it's fast and free (15 RPM)!

💡 **Use Gemini Pro** for complex roadmap generation - better quality for detailed plans (2 RPM)

💡 **Enable caching** to reduce duplicate API calls:
```env
ENABLE_RESPONSE_CACHE=true
```

💡 **Monitor API usage** to stay within free tier:
```bash
grep "Gemini API" logs/bot.log | wc -l
```

💡 **Customize prompts** for better answers specific to your needs

💡 **Backup regularly** - user progress is valuable!

💡 **Join Discord** to share tips with other users

---

## 🌟 What Makes This Special?

**100% FREE Setup:**
- ✅ Google Gemini API - FREE forever (no credit card!)
- ✅ Discord bot - FREE
- ✅ Unlimited certifications - FREE
- ✅ Open source code - FREE
- ✅ No subscriptions - FREE

**Powerful Features:**
- ✅ AI-powered study plans (personalized for YOU)
- ✅ Skill assessments (gauge your level)
- ✅ Progress tracking (stay motivated)
- ✅ 9 OffSec certifications supported
- ✅ 90+ assessment questions
- ✅ 150+ curated resources
- ✅ Modern slash commands

**Developer Friendly:**
- ✅ Well-documented code
- ✅ Modular architecture
- ✅ Easy to customize
- ✅ Active development
- ✅ Community-driven

---

## 🙏 Acknowledgments

- **OffSec** - For amazing certifications and training
- **Google AI** - For FREE Gemini API access
- **Discord.py** - For excellent Discord bot framework
- **The Community** - For support and feedback
- **You** - For using Try-Harder-AI!

---

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

**Try Harder! 💪🔥**

*Last Updated: February 14, 2026*  
*Version: 2.0.0-gemini*  
*Powered by: Google Gemini 1.5 Flash (FREE Tier)*

*For quick 5-minute setup, see [QUICKSTART.md](QUICKSTART.md)*  
*For technical details, see [ARCHITECTURE.md](docs/ARCHITECTURE.md)*  

*For API integration, see [API_INTEGRATION.md](docs/API_INTEGRATION.md)*
