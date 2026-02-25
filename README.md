# 🎯 Try-Harder-AI Discord Bot

> **Your Personal OffSec Certification Mentor - Powered by Google Gemini AI (100% FREE!)**

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.3+-blue.svg)](https://github.com/Rapptz/discord.py)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-AI-blue.svg)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

An advanced Discord bot that serves as your **24/7 AI-powered mentor** for OffSec certifications. Get personalized study roadmaps, take skill assessments, ask technical questions, and track your progress - all powered by **Google Gemini AI (100% FREE tier available!)**.

---

## ✨ Features

### 🧠 **AI-Powered Intelligence**

- **Google Gemini AI**: Powered by Google's latest AI (Gemini 3 Flash & 2.5 Flash Lite)
- **100% FREE Tier**: 15 requests/minute - No credit card required!
- **Context-aware responses**: Remembers your certification and skill level
- **Emoji-rich formatting**: Visual, step-by-step answers (not lengthy theory)

### 📚 **Smart Assessments**

- **Skill-level evaluation**: 10-question quizzes for each certification
- **Instant analysis**: Get categorized as Beginner, Intermediate, Advanced, or Expert
- **Personalized feedback**: Identify your strengths and weak areas
- **Progress tracking**: Watch your improvement over time

### 🗺️ **Personalized Study Roadmaps**

- **AI-generated plans**: Customized 8-24 week study roadmaps
- **Machine progression**: Specific HTB/PG/THM machine lists
- **GitHub tool integration**: Direct links to SecLists, LinPEAS, Impacket, etc.
- **Time estimates**: Daily and weekly hour breakdowns
- **Adaptive difficulty**: Adjusts based on your skill assessment

### 💬 **24/7 AI Mentor**

- **Ask anything**: Technical questions answered instantly
- **Concise explanations**: Step-by-step guidance with emojis
- **Multiple certifications**: Support for all 12 OffSec certs
- **No judgment**: Learn at your own pace

### 📊 **Progress Tracking**

- **Assessment history**: All past results saved
- **Skill evolution**: Track improvement over time
- **Achievement system**: Milestones and statistics
- **Study analytics**: See your learning journey

### 📦 **40+ Free Resources**

- **GitHub repositories**: SecLists, PEASS-ng, AutoRecon, BloodHound, Impacket, etc.
- **Free platforms**: Root-Me, OverTheWire, PicoCTF, PortSwigger Academy, etc.
- **Practice machines**: TJNull's OSCP list with OS-specific recommendations
- **Study techniques**: Pomodoro, spaced repetition, active recall tips

---

## 🤖 Google Gemini AI Models (All 100% FREE!)

The bot uses **Google Gemini AI** - completely FREE with generous quotas!

| Model                   | Best For                          | Speed    | Context Window | Free Tier  |
| ----------------------- | --------------------------------- | -------- | -------------- | ---------- |
| **Gemini 3 Flash (Preview)** 🚀 | Default Model (Fastest)           | ⚡⚡⚡⚡ | 1M tokens      | **Preview** |
| **Gemini 2.5 Flash Lite** 🛡️ | Fallback Model (Reliable)         | ⚡⚡⚡   | 1M tokens      | **Preview** |
| **Gemini 1.5 Flash**          | Legacy / Stable                   | ⚡⚡⚡   | 1M tokens      | **15 RPM** |
| **Gemini 1.5 Pro**      | Complex reasoning, long roadmaps  | ⚡⚡     | 2M tokens      | **2 RPM**  |
| **Gemini 1.5 Flash-8B** | Ultra-fast, simple queries        | ⚡⚡⚡⚡ | 1M tokens      | **15 RPM** |

**Default Model**: Gemini 3 Flash Preview (with automatic fallback to Gemini 2.5 Flash Lite)

### 🆓 FREE Tier Benefits:

- ✅ **No credit card required** - FREE forever!
- ✅ **15 requests/minute** (Flash model)
- ✅ **1 million requests/day**
- ✅ **1M-2M token context** window
- ✅ **Perfect for daily study sessions**

**Get your FREE API key**: [Google AI Studio](https://aistudio.google.com/app/apikey)

---

## 🎥 Video Tutorial

Prefer watching instead of reading?  
Watch full setup guide here:  
👉 [Full Setup Guide](https://youtu.be/oRFpiGiHWl8)

---

## ⚡ Quick Start (5 Minutes)

```bash
# 1. Clone repository
git clone https://github.com/The4v1/Try-Harder-AI.git
cd Try-Harder-AI

# 2. Update PIP & Install Dependencies
python.exe -m pip install --upgrade pip
pip install -r requirements.txt

# 3. Get FREE Gemini API key
# Visit: https://aistudio.google.com/app/apikey
# No credit card needed!

# 4. Add to .env file
# GEMINI_API_KEY=your_key_here
# DISCORD_BOT_TOKEN=your_discord_token

# 5. Run the bot
python main.py
```

**🚀 For detailed setup**: See [QUICKSTART.md](QUICKSTART.md)

---

## 🎯 Supported Certifications

- **OSCP** - Offensive Security Certified Professional
- **OSEP** - Offensive Security Experienced Penetration Tester  
- **OSWE** - Offensive Security Web Expert
- **OSED** - Offensive Security Exploit Developer
- **OSWP** - Offensive Security Wireless Professional
- **OSWA** - OffSec Web Assessor
- **OSMR** - OffSec macOS Researcher
- **OSDA** - OffSec Defense Analyst
- **KLCP** - Kali Linux Certified Professional
- **OSCC** - OffSec Certified Cloud Practitioner
- **OSIR** - OffSec Security Incident Responder
- **OSEE** - OffSec Exploit Expert

---

## 📋 Commands

| Command              | Description                      | Example                       |
| -------------------- | -------------------------------- | ----------------------------- |
| `/start`             | Welcome message & intro          | `/start`                      |
| `/help`              | Show all commands                | `/help`                       |
| `/certs`             | List certifications              | `/certs`                      |
| `/assess <cert>`     | Start skill assessment           | `/assess OSCP`                |
| `/roadmap`           | Generate study plan              | `/roadmap`                    |
| `/ask <question>`    | Ask AI anything                  | `/ask What is SQLi?`          |
| `/resources <cert>`  | Get learning resources           | `/resources OSCP`             |
| `/machines <cert> [difficulty] [os]` | Get practice machine lists | `/machines OSCP easy linux` |
| `/tips <cert>`       | Get exam strategies              | `/tips OSCP`                  |
| `/progress`          | View your progress               | `/progress`                   |
| `/cancel`            | Cancel current assessment        | `/cancel`                     |
| `/stats`             | View bot statistics              | `/stats`                      |

---

## 🛠️ Installation

### **Prerequisites**

- Python 3.10 or higher
- Discord account
- Google Account (for FREE Gemini API - no credit card!)
- Git

### **Setup Steps**

#### **1. Clone Repository**

```bash
git clone https://github.com/The4v1/Try-Harder-AI.git
cd Try-Harder-AI
```

#### **2. Install Dependencies**

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install requirements
pip install -r requirements.txt
```

#### **3. Get API Keys**

**Discord Bot Token:**

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create new application
3. Go to "Bot" tab → Create bot
4. Copy token
5. Enable "Message Content Intent"

**Google Gemini API Key** (100% FREE!):

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your **Google Account**
3. Click **"Create API key"**
4. Choose **"Create API key in new project"**
5. Copy the API key (starts with `AIzaSy...`)
6. **No credit card required!** - FREE tier forever!

**FREE Tier Limits:**

- Gemini 1.5 Flash: 15 requests/minute, 1M requests/day
- Gemini 1.5 Pro: 2 requests/minute, 50 requests/day

#### **4. Configure Environment**

Edit the `.env` file:

```env
# Discord Bot Token
DISCORD_BOT_TOKEN=your_discord_token_here

# Google Gemini API Key (FREE!)
GEMINI_API_KEY=your_gemini_api_key_here

# OPTIONAL
# Secondary API Keys for Failover/Rotation (Optional)
# If the primary key is rate-limited (429), the bot will automatically try these:
GEMINI_API_KEY_2=your_gemini_api_key_here
GEMINI_API_KEY_3=your_gemini_api_key_here

# Bot Command Prefix (using / for slash commands)
BOT_PREFIX=/

# AI Model (Default: gemini-3-flash-preview)
DEFAULT_AI_MODEL=gemini-3-flash-preview
```

#### **5. Run the Bot**

```bash
python main.py
```

**You should see:**

```
╔═══════════════════════════════════════════════════════════════╗
║                  🎯 TRY-HARDER-AI BOT v2.0.0-gemini          ║
║             Your Personal OffSec Certification Mentor         ║
║               Powered by Google Gemini AI 🤖                 ║
║                                                               ║
║  Supported Certifications : 12                                ║
║  AI Model                 : gemini-1.5-flash                  ║
║  Context Window           : 1M tokens                         ║
║  Status                   : Ready to Help You Try Harder! 💪 ║
╚═══════════════════════════════════════════════════════════════╝

🔥 FREE Tier Active:
   • Gemini 1.5 Flash : 15 requests/minute
   • No credit card required!

[INFO] Bot is ready! 🚀
```

---

## 💡 Usage Examples

### **Example Workflow:**

```
/start
# Get introduction

/certs
# View all certifications

/assess OSCP
# Take 10-question quiz

/roadmap
# Get personalized 12-week plan with HTB machines

/ask How do I exploit SUID binaries?
# Get step-by-step answer with emojis

/resources OSCP
# See 40+ GitHub repos and free platforms

/tips OSCP
# Get exam day strategies

/progress
# Track your improvement
```

---

## 🔧 Configuration

Optional settings in `.env`:

```env
# Required
DISCORD_BOT_TOKEN=your_token
GEMINI_API_KEY=your_gemini_key

# Optional - AI Settings
DEFAULT_AI_MODEL=gemini-2.5-flash-lite-preview-09-2025
AI_MAX_TOKENS=8192
AI_TEMPERATURE=0.7
AI_TIMEOUT=60

# Optional - Bot Behavior
BOT_PREFIX=/
ASSESSMENT_QUESTIONS_PER_TEST=15
DEFAULT_ROADMAP_DURATION_WEEKS=12

# Optional - Rate Limiting (Conservative for FREE tier)
MAX_CONCURRENT_AI_REQUESTS=2
COMMAND_COOLDOWN_SECONDS=5
USER_DAILY_AI_LIMIT=200
```

---

## 📂 Project Structure

```
try-harder-ai/
│
├── bot/
│   ├── __init__.py
│   ├── assessment.py
│   ├── commands.py
│   ├── gemini_engine.py
│   ├── roadmap.py
│   └── user_manager.py
│
├── config/
│   ├── logging_config.py
│   └── settings.py
│
├── data/
│   ├── certifications.yaml
│   ├── questions.yaml
│   └── resources.yaml
|   └── user_data.json
│
├── docs/
│   ├── API_INTEGRATION.md
│   ├── ARCHITECTURE.md
│   ├── CONTRIBUTING.md
│   ├── DEMO_SCRIPT.md
│   └── DEVELOPMENT.md
│
├── image and logo/
│   ├── Banner.png
│   └── Logo.png
|
├── prompts/
│   ├── klcp_prompt.txt
│   ├── oscc_prompt.txt
│   ├── oscp_romp.txt
│   ├── osda_prompt.txt
│   ├── osed_romp.txt
│   ├── osee_prompt.txt
│   ├── osep_romp.txt
│   ├── osir_prompt.txt
│   ├── osmr_romp.txt
│   ├── oswa_prompt.txt
│   ├── oswe_romp.txt
│   ├── oswp_prompt.txt
│   └── system_prompt.txt
│
├── scripts/
│   └── validate_data.py
│
├── tests/
│   ├── test_ai_engine.py
│   ├── test_all_certs.py
│   ├── test_assessment.py
│   ├── test_commands.py
│   ├── test_thresholds.py
│   └── validate_questions.py
│
├── utils/
│   ├── formatters.py
│   ├── helpers.py
│   └── validators.py
│
├── .env
├── .gitignore
├── LICENSE
├── main.py
├── QUICKSTART.md
├── README.md
├── requirements.txt
└── SETUP.md

```
---

## 🐛 Troubleshooting

**AI responses fail:**

```
Error: Gemini API error
Solution:
1. Verify GEMINI_API_KEY in .env file
2. Check key is valid at https://aistudio.google.com
3. Ensure you haven't exceeded rate limits (15 RPM for Flash)
4. Look at logs/bot.log for details
```

**Error: "API key invalid"**

```
Solution: Regenerate at https://aistudio.google.com/app/apikey
```

**Error: "Rate limit exceeded"**

```
Solution:
- Wait 1 minute before trying again
- FREE tier: 15 requests/min (Flash), 2 requests/min (Pro)
- Reduce MAX_CONCURRENT_AI_REQUESTS to 1 or 2
```

**See [QUICKSTART.md](QUICKSTART.md) for more troubleshooting**

---

## ❓ FAQ

**Q: Is this free to use?**  
A: Yes! The bot is 100% open-source and Google Gemini offers a generous FREE tier with no credit card required!

**Q: Do I need to pay for AI?**  
A: No! Google Gemini provides 15 requests/minute FREE forever. Perfect for daily study sessions.

**Q: Which AI model is used?**  
A: Gemini 1.5 Flash (default) - fast, free, and excellent for technical content.

**Q: What are the rate limits?**  
A: FREE tier gives you:

- Gemini 1.5 Flash: 15 requests/minute, 1M requests/day
- Gemini 1.5 Pro: 2 requests/minute, 50 requests/day

**Q: How much does this cost?**  
A: $0! Everything is FREE:

- ✅ Bot is open-source (free)
- ✅ Google Gemini API (free tier)
- ✅ No credit card needed

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OffSec** - For amazing certifications and training
- **Google AI** - For FREE Gemini API access
- **Discord** - For excellent Discord bot framework
- **The Community** - For support and feedback
- **TJNull** - For the amazing OSCP machine list
- **HackTricks** - For comprehensive pentesting methodology

---

## 📞 Support

- **Documentation**: [QUICKSTART.md](QUICKSTART.md) | [SETUP.md](SETUP.md)
- **Gemini API**: [Google AI Docs](https://ai.google.dev/docs)

---

## 🚀 Roadmap

- [ ] Add machine completion tracking
- [ ] Community machine recommendations
- [ ] Multi-cert learning paths
- [ ] Study streak gamification
- [ ] PDF report generation
- [ ] Discord role integration

---

**Try Harder! 💪🔥**

_Last Updated: February 16, 2026_  
_Version: 2.0.0-gemini_  
_Powered by: Google Gemini AI (FREE Tier)_







