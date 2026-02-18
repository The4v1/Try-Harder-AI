# 🚀 QUICKSTART GUIDE - Try-Harder-AI Discord Bot

Get your OffSec certification mentor bot running in **5 minutes**!

---

## ⚡ Quick Setup (5 Minutes)

### **Step 1: Prerequisites Check** ✅

Before starting, make sure you have:

- [x] **Python 3.10+** installed ([Download here](https://www.python.org/downloads/))
- [x] **Discord Account** ([Sign up](https://discord.com))
- [x] **Google Account** (for Gemini API - FREE tier available!)
- [x] **Git** installed ([Download here](https://git-scm.com/downloads))

---

### **Step 2: Get Your API Keys** 🔑

#### **A) Discord Bot Token**

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** → Name it "Try-Harder-AI"
3. Go to **"Bot"** tab → Click **"Add Bot"**
4. Under **"Token"** section → Click **"Reset Token"** → **Copy it**
5. Enable these **Privileged Gateway Intents**:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent
6. Go to **"OAuth2"** → **"URL Generator"**
   - Select scopes: `bot`, `applications.commands`
   - Select permissions: `Administrator` (or minimum: Send Messages, Embed Links, Add Reactions)
   - Copy the generated URL and open it to invite bot to your server

#### **B) Google Gemini API Key** (FREE!)

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your **Google Account**
3. Click **"Create API key"**
4. Choose **"Create API key in new project"** (or select existing project)
5. **Copy the API key** (starts with `AIzaSy...`)
6. **No credit card required!** - Generous free tier included

**FREE Tier Limits:**
- ✅ Gemini 1.5 Flash: **15 requests/minute** (1M requests/day)
- ✅ Gemini 1.5 Pro: **2 requests/minute** (50 requests/day)
- ✅ No expiration - FREE forever!

---

### **Step 3: Get the Project** 💻

**Option A: Clone with Git** (Recommended)
```bash
# Clone the repository
git clone https://github.com/The4v1/Try-Harder-AI.git
cd try-harder-ai
```

**Option B: Download ZIP**
1. Visit [https://github.com/The4v1/Try-Harder-AI](https://github.com/The4v1/Try-Harder-AI)
2. Click **"Code"** → **"Download ZIP"**
3. Extract the ZIP file to your desired location
4. Navigate to the extracted folder:
   ```bash
   cd try-harder-ai-main  # or wherever you extracted it
   ```

**Then continue with:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### **Step 4: Configure Environment** ⚙️

1. Open the `.env` file in the root directory
2. Add your API keys:

```env
# Discord Bot Token
DISCORD_BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE

# Google Gemini API Key (FREE!)
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE

# Bot Command Prefix (using / instead of !)
BOT_PREFIX=/

# AI Model (recommended: gemini-1.5-flash)
DEFAULT_AI_MODEL=gemini-1.5-flash
```

**Example:**
```env
DISCORD_BOT_TOKEN=MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.GhIjKl.MnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUv
GEMINI_API_KEY=AIzaSyD-abc123def456ghi789jkl012mno345pqr678stu901vwx234
BOT_PREFIX=/
DEFAULT_AI_MODEL=gemini-1.5-flash
```

---

### **Step 5: Run the Bot** 🎯

```bash
# Make sure you're in the project directory
cd try-harder-ai

# Activate virtual environment (if not already active)
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Run the bot
python main.py
```

**You should see:**
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

[INFO] Bot logged in as: Try-Harder-AI#1234
[INFO] Connected to 1 server(s)
[INFO] Bot is ready! 🚀
```

---

## 🎮 First Commands to Try

Open Discord and go to your server where the bot is invited:

### **1. Get Help**
```
/help
```
See all available commands

### **2. Welcome & Introduction**
```
/start
```
Get started with the bot

### **3. View Certifications**
```
/certs
```
See all 9 supported OffSec certifications

### **4. Take a Skill Assessment**
```
/assess OSCP
```
Get a 10-question quiz to gauge your current level

### **5. Ask AI Questions**
```
/ask What is privilege escalation?
```
Get AI-powered answers with emojis and step-by-step guidance

### **6. Generate Study Roadmap**
```
/roadmap
```
Get a personalized 12-week study plan based on your assessment

### **7. Get Resources**
```
/resources OSCP
```
View recommended learning materials

### **8. Get Exam Tips**
```
/tips OSCP
```
AI-generated exam strategies and tips

### **9. Check Your Progress**
```
/progress
```
View your learning statistics and achievements

---

## 📋 Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Welcome message & intro | `/start` |
| `/help` | Show all commands | `/help` |
| `/certs` | List all certifications | `/certs` |
| `/assess <cert>` | Take skill assessment | `/assess OSCP` |
| `/roadmap` | Generate study plan | `/roadmap` |
| `/ask <question>` | Ask AI anything | `/ask How to enumerate SMB?` |
| `/resources <cert>` | Get learning resources | `/resources OSCP` |
| `/tips <cert>` | Get exam tips | `/tips OSCP` |
| `/progress` | View your progress | `/progress` |
| `/cancel` | Cancel current assessment | `/cancel` |
| `/stats` | View bot statistics | `/stats` |

---

## 🎓 Supported Certifications

- **OSCP** - Offensive Security Certified Professional
- **OSEP** - Offensive Security Experienced Penetration Tester
- **OSWE** - Offensive Security Web Expert
- **OSED** - Offensive Security Exploit Developer
- **OSWP** - Offensive Security Wireless Professional
- **OSWA** - OffSec Web Assessor
- **OSMR** - OffSec macOS Researcher
- **OSDA** - OffSec Defense Analyst
- **KLCP** - Kali Linux Certified Professional

---

## 🤖 Available AI Models (Google Gemini)

| Model | Best For | Speed | Context | Free Tier |
|-------|----------|-------|---------|-----------|
| **Gemini 1.5 Flash** ⭐ | Technical content, fast responses | ⚡⚡⚡ | 1M tokens | 15 RPM |
| **Gemini 1.5 Pro** | Complex reasoning, long roadmaps | ⚡⚡ | 2M tokens | 2 RPM |
| **Gemini 1.5 Flash-8B** | Ultra-fast, simple queries | ⚡⚡⚡⚡ | 1M tokens | 15 RPM |

**All models are FREE!** No credit card required! 🎉

**Default Model:** `gemini-1.5-flash` (Recommended - Best balance of speed & quality)

---

## 🔧 Troubleshooting

### **Bot Won't Start**

**Error: "discord.errors.LoginFailure: Improper token"**
- ✅ Check your `DISCORD_BOT_TOKEN` in `.env`
- ✅ Make sure you copied the full token
- ✅ Reset token in Discord Developer Portal if needed

**Error: "ModuleNotFoundError: No module named 'discord'"**
- ✅ Make sure virtual environment is activated
- ✅ Run `pip install -r requirements.txt` again

**Error: "GEMINI_API_KEY not found in environment variables"**
- ✅ Check `.env` file has `GEMINI_API_KEY=...`
- ✅ Verify API key starts with `AIzaSy`
- ✅ Make sure `.env` file is in project root directory

**Error: "FileNotFoundError: .env file not found"**
- ✅ Make sure `.env` file exists in root directory
- ✅ Check file name is exactly `.env` (not `.env.txt`)

### **Bot is Online But Not Responding**

**Commands don't work:**
- ✅ Check bot has `Message Content Intent` enabled
- ✅ Verify bot has proper permissions in your Discord server
- ✅ Make sure you're using correct prefix (default: `/`)
- ✅ Try `/help` to verify bot is responding

**AI responses fail:**
- ✅ Check your `GEMINI_API_KEY` in `.env`
- ✅ Verify API key is valid at https://aistudio.google.com
- ✅ Check you haven't exceeded free tier rate limits (15 RPM for Flash)
- ✅ Look at logs in `logs/bot.log` for error details

**Error: "API key invalid"**
- ✅ Regenerate API key at https://aistudio.google.com/app/apikey
- ✅ Copy the new key to `.env` file
- ✅ Restart the bot

**Error: "Rate limit exceeded"**
- ✅ Wait 1 minute before trying again
- ✅ Free tier limits: 15 requests/min (Flash), 2 requests/min (Pro)
- ✅ Reduce `MAX_CONCURRENT_AI_REQUESTS` in `.env` to 1 or 2

### **Assessment or Roadmap Not Working**

**"Data file not found" error:**
- ✅ Make sure `data/` folder exists
- ✅ Check `certifications.yaml` and `questions.yaml` are present
- ✅ Verify file permissions

**Assessment questions don't appear:**
- ✅ Check `data/questions.yaml` exists
- ✅ Verify YAML syntax is correct
- ✅ Restart bot after making data file changes

### **Still Having Issues?**

1. Check logs in `logs/bot.log`
2. Enable debug mode in `.env`:
   ```env
   DEBUG_MODE=true
   LOG_LEVEL=DEBUG
   ```
3. Restart the bot
4. Check [GitHub Issues](https://github.com/The4v1/Try-Harder-AI/issues)

---

## 📚 Next Steps

1. **Read Full Documentation**: Check `README.md` for detailed features
2. **Customize Settings**: Edit `.env` file for your preferences
3. **Join Community**: Share feedback and get help
4. **Take Assessment**: Run `/assess OSCP` to get started
5. **Study Consistently**: Use `/roadmap` to stay on track

---

## 🎯 Example Workflow

Here's a typical user journey:

```bash
# 1. Get started
/start

# 2. View available certifications
/certs

# 3. Take skill assessment
/assess OSCP
# Answer 10 questions to gauge your level

# 4. Generate personalized roadmap
/roadmap
# Get a 12-week study plan based on your assessment

# 5. Ask questions while studying
/ask How do I exploit SUID binaries?
/ask Explain buffer overflow step by step
/ask What tools are best for Active Directory?

# 6. Get exam tips
/tips OSCP
# AI-generated strategies for exam day

# 7. Check progress regularly
/progress
# See your achievements and statistics

# 8. Get additional resources
/resources OSCP
# Access curated learning materials
```

---

## 💡 Pro Tips

- ⭐ **Start with `/start`**: Get an introduction to the bot
- ⭐ **Take assessment first**: This gives you a personalized baseline
- ⭐ **Use `/ask` liberally**: The AI is your 24/7 mentor (FREE!)
- ⭐ **Follow the roadmap**: Structured learning beats random studying
- ⭐ **Ask specific questions**: Better questions = better answers
- ⭐ **Track progress**: Use `/progress` to stay motivated
- ⭐ **Get exam tips**: Use `/tips` before your exam
- ⭐ **Study consistently**: Daily practice beats cramming
- ⭐ **Use Flash model**: Fast & free, perfect for most queries
- ⭐ **No rate limit worries**: 15 requests/minute is plenty for learning!

---

## 🆓 FREE Tier Benefits

**Google Gemini FREE tier is incredibly generous:**

✅ **15 requests/minute** (Gemini 1.5 Flash)
✅ **1 million requests/day**
✅ **1M token context** (Flash) / **2M tokens** (Pro)
✅ **No credit card** required
✅ **No expiration** - FREE forever!

**Perfect for:**
- Daily study sessions
- Quick questions during practice
- Generating roadmaps
- Getting exam tips
- Learning OffSec concepts

---

## 🔒 Security Notes

- ✅ **Never share** your `.env` file
- ✅ **Never commit** API keys to Git
- ✅ **Keep tokens secret**: Treat them like passwords
- ✅ **Regenerate keys** if accidentally exposed
- ✅ **Use `.gitignore`**: Already configured to protect secrets

---

## 📖 Additional Documentation

- **[README.md](README.md)** - Full project overview
- **[SETUP.md](SETUP.md)** - Detailed setup instructions
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design
- **[API_INTEGRATION.md](docs/API_INTEGRATION.md)** - Gemini integration details
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Production deployment guide

---

## 🆘 Need Help?

- 💬 **Discord**: [Join our server](https://discord.gg/tryharderai)
- 🐛 **Issues**: [GitHub Issues](https://github.com/The4v1/Try-Harder-AI/issues)
- 📖 **Docs**: [Full Documentation](https://docs.tryharderai.com)
- 🤖 **Google AI**: [Gemini Documentation](https://ai.google.dev/docs)

---

## 🎉 You're All Set!

Your Try-Harder-AI bot is now running with **Google Gemini AI (FREE!)**

Start your certification journey:

```
/start
/certs
/assess OSCP
/roadmap
```

**Try Harder! 💪🔥**

---

*Last Updated: 2026-02-14*
*Version: 2.0.0-gemini*
*Powered by: Google Gemini 1.5 Flash (FREE Tier)*