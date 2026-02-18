# 🎥 Demo Script - Try-Harder-AI Bot

## Overview

This document provides a comprehensive script for demonstrating the Try-Harder-AI Discord bot, perfect for creating video tutorials, presentations, or live demonstrations.

---

## Table of Contents

1. [Pre-Demo Setup](#pre-demo-setup)
2. [Demo Flow Overview](#demo-flow-overview)
3. [Introduction (2 minutes)](#introduction-2-minutes)
4. [Bot Setup Demo (3 minutes)](#bot-setup-demo-3-minutes)
5. [Core Features Demo (10 minutes)](#core-features-demo-10-minutes)
6. [Advanced Features (5 minutes)](#advanced-features-5-minutes)
7. [Closing (2 minutes)](#closing-2-minutes)
8. [Talking Points](#talking-points)
9. [Troubleshooting During Demo](#troubleshooting-during-demo)
10. [B-Roll Suggestions](#b-roll-suggestions)

**Total Demo Time:** ~20-25 minutes

---

## 📋 Pre-Demo Setup

### Required Tools

```
✅ Discord account with server admin permissions
✅ Screen recording software (OBS, Loom, etc.)
✅ Code editor (VS Code recommended)
✅ Terminal access
✅ Google Gemini API key (free at aistudio.google.com/apikey)
✅ Bot already running (for seamless demo)
```

### Discord Server Setup

**Create test server with:**
- Channel: `#bot-testing`
- Channel: `#commands`
- Role: `Student` (for permission demo)
- 2-3 test accounts (to show multi-user support)

### Test Data Preparation

**Before demo, prepare:**
```bash
# Clean user data for fresh start
cp data/user_data.json data/user_data.backup.json
echo '{"users": {}, "global_statistics": {}}' > data/user_data.json

# Verify bot is running
python bot/main.py
```

### Recording Settings

```
Resolution: 1920x1080 (Full HD)
Frame Rate: 30 FPS
Audio: Clear microphone, no background noise
Zoom: Increase Discord font size for visibility
```

---

## 🎬 Demo Flow Overview

```
┌─────────────────────────────────────────────────────┐
│ INTRODUCTION (2 min)                                │
│ - Welcome & overview                                │
│ - What is Try-Harder-AI                             │
│ - Key features                                      │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ SETUP DEMONSTRATION (3 min)                         │
│ - Installation                                      │
│ - Configuration                                     │
│ - First launch                                      │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ CORE FEATURES (10 min)                              │
│ 1. User registration (/start)                       │
│ 2. Skill assessment (/assess)                       │
│ 3. Roadmap generation (/roadmap)                    │
│ 4. AI Q&A (/ask)                                    │
│ 5. Progress tracking (/progress)                    │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ ADVANCED FEATURES (5 min)                           │
│ - AI model switching                                │
│ - Certification switching                           │
│ - Multi-user support                                │
│ - Data persistence                                  │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ CLOSING (2 min)                                     │
│ - Summary                                           │
│ - Resources                                         │
│ - Call to action                                    │
└─────────────────────────────────────────────────────┘
```

---

## 🎤 Introduction (2 minutes)

### Opening Hook (15 seconds)

**[Screen shows Discord server]**

> "Are you studying for OSCP, OSEP, or any OffSec certification? Tired of generic study plans that don't fit your specific needs? Let me show you something game-changing."

### Problem Statement (30 seconds)

**[Show frustrated student meme or graphic]**

> "Here's the problem: Everyone learns differently. Some people need more time on Active Directory, others struggle with buffer overflows. Traditional study plans treat everyone the same. And let's be honest - figuring out WHAT to study and WHEN can be just as hard as the actual studying."

### Solution Introduction (45 seconds)

**[Show bot avatar and name]**

> "Meet Try-Harder-AI - your personal OffSec certification mentor powered by Google Gemini AI. This isn't just another Discord bot. It's a comprehensive learning companion that:"

**[Show bullet points on screen]**

- 🎯 **Assesses your current skill level** through interactive quizzes
- 🗺️ **Creates personalized roadmaps** tailored to YOUR strengths and weaknesses
- 🤖 **Answers your questions 24/7** with AI-powered guidance
- 📊 **Tracks your progress** across multiple certifications
- 🔄 **Adapts as you learn** with continuous updates

### Value Proposition (30 seconds)

**[Show supported certifications graphic]**

> "Currently supports 9 OffSec certifications: OSCP, OSEP, OSWE, OSED, OSWP, OSWA, OSMR, OSDA, and KLCP. And here's the best part - it's completely FREE and open-source. Let me show you how it works."

---

## 🔧 Bot Setup Demo (3 minutes)

### Prerequisites Check (30 seconds)

**[Screen: Terminal with Python version]**

```bash
# Show Python version
python --version
# Output: Python 3.10.8

# Show Git
git --version
# Output: git version 2.40.0
```

> "First, make sure you have Python 3.10 or higher and Git installed. Quick version check shows we're all set."

### Installation (1 minute)

**[Screen: Terminal showing git clone]**

```bash
# Clone repository
git clone https://github.com/The4v1/Try-Harder-AI.git
cd try-harder-ai

# Show directory structure
ls -la
```

> "Installation is straightforward. Clone the repo, and you'll see our clean project structure. Everything's organized into modules - bot code, data files, prompts, and configuration."

**[Screen: Show directory tree]**

```bash
tree -L 1
```

> "Notice the data folder with our comprehensive certification information, the bot folder with all the core logic, and the prompts folder containing AI instructions for each certification."

### Configuration (1 minute 30 seconds)

**[Screen: VS Code showing .env.example]**

```bash
# Copy environment template
cp .env.example .env
```

> "Configuration is simple. Copy the example environment file and add your credentials."

**[Screen: Show .env file being edited]**

```bash
# .env file
DISCORD_BOT_TOKEN=your_discord_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
DEFAULT_AI_MODEL=gemini-1.5-flash
```

> "You'll need two things: a Discord bot token - which you get from the Discord Developer Portal - and a Google Gemini API key. I'll put links in the description."

**[Screen: Show Discord Developer Portal quickly]**

> "Creating a Discord bot takes about 2 minutes - create an application, add a bot, copy the token. Simple."

**[Screen: Show Google AI Studio dashboard]**

> "For the Gemini API key, head to aistudio.google.com, sign in with your Google account, and click 'Get API key'. It's completely free to get started - Google provides a generous free tier with 1,500 requests per day at no cost."

**[Screen: Back to terminal]**

```bash
# Install dependencies
pip install -r requirements.txt
```

> "Install the dependencies - takes about 30 seconds - and we're ready to launch."

---

## 🚀 Core Features Demo (10 minutes)

### 1. First Launch (30 seconds)

**[Screen: Terminal]**

```bash
python bot/main.py
```

**[Show startup banner]**

```
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              🎯 TRY-HARDER-AI BOT v3.0.0                 ║
║                                                          ║
║        Your Personal OffSec Certification Mentor        ║
║           Powered by Google Gemini AI ✨                 ║
║                                                          ║
║  Supported Certifications: 9                            ║
║  AI Models Available: 5                                 ║
║  Status: Ready to Help You Try Harder! 💪               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

[2025-01-15 10:30:00] INFO: Bot logged in as Try-Harder-AI#1234
[2025-01-15 10:30:00] INFO: Connected to 1 server(s)
[2025-01-15 10:30:00] INFO: Loaded 9 certifications
[2025-01-15 10:30:00] INFO: Slash commands synced: 8 commands registered
[2025-01-15 10:30:00] INFO: AI Engine ready - Model: gemini-1.5-flash
```

> "The bot is online. Notice it's using Gemini 1.5 Flash - fast, powerful, and free to start. Also notice our slash commands are synced and ready. Now let's switch to Discord."

### 2. User Registration (/start) (1 minute)

**[Screen: Discord #bot-testing channel]**

```
You: /help
```

**[Bot responds with help embed]**

> "First, let's see what commands are available. With Discord slash commands, just type `/` and all available commands appear instantly - no need to memorize anything."

**[Screen: Discord]**

```
You: /start
```

**[Bot responds]**

```
🎯 Welcome to Try-Harder-AI!

I'm your personal OffSec certification mentor, powered by Google Gemini AI.
I'll help you prepare for your certification through:

✅ Personalized skill assessments
✅ Custom study roadmaps
✅ 24/7 AI-powered Q&A
✅ Progress tracking and motivation

📚 Supported Certifications:
🔴 OSCP - Offensive Security Certified Professional
🔴 OSEP - Experienced Penetration Tester  
🔴 OSWE - Web Expert
🔴 OSED - Exploit Developer
🔴 OSWP - Wireless Professional
🔴 OSWA - Web Assessor
🔴 OSMR - macOS Researcher
🔴 OSDA - Defense Analyst
🔴 KLCP - Kubernetes & Linux Container Professional

📝 Your profile has been created!

🚀 Next Steps:
1️⃣ Run /assess to take a skill assessment
2️⃣ Run /roadmap to generate your study plan
3️⃣ Run /ask anytime you need help

Let's get started! 💪
```

> "Perfect! The bot welcomes me, explains what it does, shows all supported certifications, and gives me clear next steps. Notice how it automatically created my user profile."

### 3. Skill Assessment (/assess) (3 minutes)

**[Screen: Discord]**

```
You: /assess
```

**[Bot responds with certification selection]**

```
🎯 SKILL ASSESSMENT

Please select the certification you want to assess for:

🔴 OSCP - Penetration Testing
🔴 OSEP - Advanced Pentesting & Evasion
🔴 OSWE - Web Application Security
🔴 OSED - Exploit Development
🔴 OSWP - Wireless Security
🔴 OSWA - Web Assessment
🔴 OSMR - macOS Security
🔴 OSDA - Security Defense
🔴 KLCP - Container Security

React with the corresponding emoji to select your certification.
You have 60 seconds to choose.
```

> "I'm going to select OSCP by clicking the red circle emoji."

**[Click OSCP emoji]**

**[Bot responds]**

```
✅ OSCP selected!

📝 ASSESSMENT STRUCTURE:
• 5 Beginner questions (1 point each)
• 3 Intermediate questions (2 points each)
• 2 Advanced questions (3 points each)
• Total: 30 points possible
• Pass: 21+ points (70%)
• Time per question: 60 seconds

This assessment will help me understand your current skill level and 
identify areas for improvement.

Starting in 3... 2... 1... Let's go! 🚀
```

**[Bot shows first question]**

```
📝 QUESTION 1/10 [Beginner]

What is the primary purpose of the Nmap -sV flag?

🅰️ Perform a SYN scan
🅱️ Detect service versions running on open ports
🅲 Enable verbose output
🅳 Scan for vulnerabilities

React with A, B, C, or D
⏱️ Time remaining: 60 seconds
```

> "Great! Real-time interactive questions with a countdown timer. Let me answer this - I know it's B."

**[Click B emoji]**

**[Bot responds]**

```
✅ Correct! 

The -sV flag enables version detection in Nmap.

📊 Progress: 1/10 questions | Score: 1/30 points

Next question in 3 seconds...
```

> "Excellent! Immediate feedback. Let me speed through a few more questions to show the variety."

**[Show 2-3 more questions quickly, with mix of correct/incorrect answers]**

**[Show final results]**

```
🎯 ASSESSMENT COMPLETE!

═══════════════════════════════════════
              FINAL RESULTS
═══════════════════════════════════════

📊 OVERALL SCORE: 18/30 points (60%)

📈 BREAKDOWN BY DIFFICULTY:
┌─────────────────┬──────────┬────────┬────────┐
│   Difficulty    │ Correct  │ Total  │ Points │
├─────────────────┼──────────┼────────┼────────┤
│ 🟢 Beginner     │   4/5    │   5    │   4    │
│ 🟡 Intermediate │   2/3    │   3    │   4    │
│ 🔴 Advanced     │   1/2    │   2    │   3    │
└─────────────────┴──────────┴────────┴────────┘

═══════════════════════════════════════

🔍 AI ANALYSIS (Powered by Gemini 1.5 Flash):

📍 Current Level: INTERMEDIATE
You have a solid foundation but need to strengthen advanced 
concepts before attempting the OSCP exam.

💪 STRONG AREAS:
✅ Network Enumeration
✅ Basic Exploitation
✅ Linux Fundamentals

⚠️ WEAK AREAS:
❌ Active Directory Attacks
❌ Buffer Overflow Exploitation  
❌ Advanced Privilege Escalation

📚 RECOMMENDATIONS:
1️⃣ Focus heavily on Active Directory - this is critical for OSCP
2️⃣ Practice buffer overflow with Dostackbufferoverflowgood
3️⃣ Complete 10-15 medium-difficulty HTB/THM machines
4️⃣ Join a study group for accountability

🗺️ Ready to create your personalized roadmap? Run /roadmap

═══════════════════════════════════════
```

> "Wow! Look at this detailed analysis. The AI identified my weak areas - Active Directory and Buffer Overflow - and gave me specific recommendations. This is exactly what I needed to know before starting my study plan."

### 4. Roadmap Generation (/roadmap) (3 minutes)

**[Screen: Discord]**

```
You: /roadmap
```

**[Bot responds]**

```
🗺️ PERSONALIZED ROADMAP GENERATOR

Based on your recent assessment:
📊 Skill Level: Intermediate
📉 Weak Areas: Active Directory, Buffer Overflow, Privilege Escalation

I'll create a customized study plan for you!

⏱️ How many weeks do you want to study?
React with the number:
6️⃣ 6 weeks (Intensive)
1️⃣2️⃣ 12 weeks (Balanced - Recommended)
2️⃣4️⃣ 24 weeks (Thorough)

You have 60 seconds to choose.
```

> "I'll select 12 weeks - that's the recommended balanced approach."

**[Click 12 emoji]**

**[Bot shows thinking message]**

```
🤖 Generating your personalized roadmap...

✨ Analyzing your assessment results
✨ Consulting Gemini AI for optimal learning path
✨ Selecting practice resources
✨ Structuring weekly milestones

This may take 10-15 seconds...
```

> "The bot is now using Gemini AI to create a completely personalized study plan based on my assessment results. Watch this..."

**[Bot responds with roadmap]**

```
🗺️ YOUR 12-WEEK OSCP ROADMAP

═══════════════════════════════════════════
          🎯 PERSONALIZED FOR YOU
═══════════════════════════════════════════

📊 Skill Level: Intermediate
🎯 Target: OSCP Certification
⏱️ Duration: 12 Weeks (20 hrs/week recommended)
🎪 Focus Areas: Active Directory, Buffer Overflow, Priv Esc

───────────────────────────────────────────

📅 WEEK 1-2: ENUMERATION MASTERY
Topics:
  • Advanced Nmap techniques
  • SMB/LDAP enumeration
  • Web application reconnaissance
  
Practice Machines:
  🎯 HTB - Lame
  🎯 HTB - Legacy  
  🎯 THM - Relevant

Resources:
  📖 HackTricks - Enumeration
  🎥 IppSec - Enumeration techniques

Milestone: Complete 5 easy boxes

───────────────────────────────────────────

📅 WEEK 3-5: ACTIVE DIRECTORY DEEP DIVE
⚡ PRIORITY AREA - Your weak point!

Topics:
  • Kerberoasting & AS-REP Roasting
  • Pass-the-Hash attacks
  • BloodHound analysis
  • Domain privilege escalation
  
Practice Machines:
  🎯 HTB - Forest
  🎯 HTB - Active
  🎯 PG Practice - Hutch

Resources:
  📖 WADComs - AD Attack Cheatsheet
  📖 ired.team - AD Exploitation
  🎥 TCM Security - AD Course

Milestone: Compromise 3 AD environments

───────────────────────────────────────────

📅 WEEK 6-7: BUFFER OVERFLOW MASTERY
⚡ PRIORITY AREA - Your weak point!

Topics:
  • Stack-based buffer overflows
  • EIP control & bad characters
  • Shellcode generation
  • ASLR & DEP bypass basics
  
Practice:
  🎯 Dostackbufferoverflowgood
  🎯 THM - Buffer Overflow Prep
  🎯 VulnServer practice

Resources:
  📖 Corelan tutorials
  🎥 LiveOverflow - Binary Exploitation

Milestone: Exploit 5 different buffer overflows

───────────────────────────────────────────

📅 WEEK 8-9: PRIVILEGE ESCALATION INTENSIVE

Topics:
  • Linux: SUID, sudo, kernel exploits
  • Windows: SeImpersonate, unquoted paths
  • Automated enumeration tools
  
Practice Machines:
  🎯 HTB - Optimum (Windows)
  🎯 HTB - Cronos (Linux)
  🎯 PG Practice - Vault

Resources:
  📖 GTFOBins & LOLBAS
  📖 PayloadsAllTheThings
  🛠️ LinPEAS / WinPEAS

Milestone: Root/SYSTEM on 10 machines

───────────────────────────────────────────

📅 WEEK 10-11: EXAM PREPARATION

Topics:
  • Time management strategies
  • Report writing practice
  • Enumeration methodology review
  • Mock exam attempts
  
Practice:
  🎯 PG Practice - OSCP-like machines
  🎯 HTB - Pro Lab (if accessible)
  🎯 Timed challenge boxes

Activities:
  ✍️ Write 2 practice reports
  ⏱️ Complete 3 timed mock exams
  📝 Create personal cheatsheet

Milestone: Successfully complete mock exam

───────────────────────────────────────────

📅 WEEK 12: FINAL REVIEW & EXAM

Topics:
  • Quick review of weak areas
  • Cheatsheet refinement
  • Mental preparation
  • Rest before exam
  
Activities:
  📚 Review all notes
  🔄 Practice 2-3 easy boxes daily
  💤 Get proper sleep
  🧘 Manage stress

🎯 SCHEDULE YOUR EXAM!

═══════════════════════════════════════════

💡 STUDY TIPS:
• Take breaks every 90 minutes
• Document everything you learn
• Join OSCP study groups
• Ask questions using /ask anytime
• Update progress with /progress

🚀 Ready to begin? Start Week 1 today!
Track progress: /progress
Need help? Ask me: /ask

Good luck! You've got this! 💪
```

> "This is incredible! A fully personalized 12-week roadmap that focuses heavily on my weak areas - Active Directory and Buffer Overflow. Notice how it suggests specific machines, resources, and sets clear milestones for each week. This is exactly what I need."

### 5. AI Q&A (/ask) (2 minutes)

**[Screen: Discord]**

```
You: /ask How do I find SUID binaries for privilege escalation?
```

**[Bot shows thinking indicator — Discord "Bot is thinking..." message]**

**[Bot responds]**

```
🎯 LINUX SUID PRIVILEGE ESCALATION

Here's how to find and exploit SUID binaries:

═══════════════════════════════════════

1️⃣ FINDING SUID BINARIES

🔍 Basic Command:
```bash
find / -perm -4000 2>/dev/null
```

🔍 More Detailed Search:
```bash
find / -type f -perm -4000 -ls 2>/dev/null
```

What this does:
• `/` - Search entire filesystem
• `-perm -4000` - Files with SUID bit set
• `2>/dev/null` - Hide error messages

═══════════════════════════════════════

2️⃣ IDENTIFYING EXPLOITABLE BINARIES

✅ Check against GTFOBins:
   → https://gtfobins.github.io

⚡ Common exploitable SUID binaries:
   • find
   • vim
   • nmap (old versions)
   • bash
   • python
   • perl

═══════════════════════════════════════

3️⃣ EXPLOITATION EXAMPLE

🎯 If you find `/usr/bin/find` with SUID:

```bash
/usr/bin/find . -exec /bin/bash -p \; -quit
```

This spawns a privileged bash shell!

═══════════════════════════════════════

4️⃣ VERIFICATION

Check if exploit worked:
```bash
id
# Should show uid=0 (root)

whoami
# Should show root
```

═══════════════════════════════════════

⚠️ COMMON PITFALLS:
❌ Forgetting the -p flag in bash (drops privileges)
❌ Not checking file permissions carefully
❌ Missing obvious SUID binaries in /usr/bin

💡 PRO TIP:
Create a script to auto-check found binaries against GTFOBins!

═══════════════════════════════════════

Need more help? Ask me another question! 🚀
```

> "Perfect! Look at this response - clear step-by-step instructions with actual commands I can copy-paste, common pitfalls to avoid, and even a pro tip. The emoji structure makes it super easy to read. And notice it's concise - no lengthy theory, just actionable information."

**[Screen: Discord - Show another quick example]**

```
You: /ask What's the difference between Kerberoasting and AS-REP Roasting?
```

**[Bot responds with structured comparison]**

> "Let me ask one more question to show versatility... Beautiful! It even handles comparison questions with clear side-by-side explanations."

### 6. Progress Tracking (/progress) (1 minute)

**[Screen: Discord]**

```
You: /progress
```

**[Bot responds]**

```
📊 YOUR LEARNING PROGRESS

═══════════════════════════════════════════

👤 User: YourUsername#1234
🎯 Current Cert: OSCP
📅 Studying Since: Jan 15, 2025 (1 day)
⏰ Study Time: 2.5 hours

───────────────────────────────────────────

📈 SKILL LEVELS:
Enumeration:            ████████░░ 75%
Exploitation:           ██████░░░░ 60%
Privilege Escalation:   ████░░░░░░ 45%
Active Directory:       ███░░░░░░░ 30%
Web Exploitation:       █████░░░░░ 55%
Buffer Overflow:        ██░░░░░░░░ 20%
Reporting:              ████░░░░░░ 40%

───────────────────────────────────────────

🎮 MACHINES COMPLETED:
✅ HackTheBox:        6
✅ TryHackMe:         8
✅ VulnHub:           3
✅ Proving Grounds:   0
✅ PWK Labs:          0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Total:             17 machines

───────────────────────────────────────────

🗺️ CURRENT ROADMAP: Week 1/12
Status: In Progress

✅ Week 1: Enumeration Mastery (Completed)
🔄 Week 2: Advanced Enumeration (In Progress)
⏸️ Week 3-12: Upcoming

Next Milestone: Complete 5 machines (3/5 done)

───────────────────────────────────────────

🏆 ACHIEVEMENTS UNLOCKED:
🎯 First Steps - Completed first assessment
🗺️ Plan of Attack - Generated first roadmap  
🏆 Machine Hunter - Completed 5 machines
📚 Knowledge Seeker - Asked 10 questions

───────────────────────────────────────────

📊 STATISTICS:
Commands Used:      47
AI Queries:         23
Favorite Command:   /ask
Study Sessions:     12
Current Streak:     3 days 🔥
Longest Streak:     7 days

───────────────────────────────────────────

💡 NEXT STEPS:
1️⃣ Complete 2 more machines for Week 2 milestone
2️⃣ Focus on Active Directory (weak area)
3️⃣ Review Buffer Overflow basics

Keep trying harder! 💪
```

> "Awesome! Complete progress overview with skill percentages, machine counts, roadmap status, achievements, and statistics. This gamification keeps you motivated!"

---

## 🎨 Advanced Features (5 minutes)

### 1. AI Model Switching (1 minute)

**[Screen: Discord]**

```
You: /model
```

**[Bot responds]**

```
🤖 AI MODEL SELECTION

Current Model: gemini-1.5-flash ✨

Available Gemini Models:
⚡ Gemini 1.5 Flash (DEFAULT — RECOMMENDED)
   Best for: Fast Discord responses, general Q&A, all daily commands
   Context: 1M tokens | Free tier: 1,500 req/day

🧠 Gemini 1.5 Pro
   Best for: Complex roadmaps, deep reasoning, long-form analysis
   Context: 2M tokens | Best quality

🪶 Gemini 1.5 Flash-8B
   Best for: Simple queries, fastest responses, lowest cost
   Context: 1M tokens | Lightest model

🚀 Gemini 2.0 Flash
   Best for: Cutting-edge tasks, latest capabilities
   Context: 1M tokens | Next-gen model

📘 Gemini 1.0 Pro
   Best for: Stable, reliable fallback
   Context: 32K tokens | Legacy model

React to switch models:
⚡ Flash | 🧠 Pro | 🪶 Flash-8B | 🚀 Flash 2.0 | 📘 1.0 Pro
```

> "You can switch between 5 Gemini model variants depending on your needs. Flash is the default - it's fast, free, and great for everyday questions. If you're generating a complex roadmap and want the deepest analysis, switch to Gemini 1.5 Pro. Let me show you."

**[Click Pro emoji]**

```
✅ Model switched to Gemini 1.5 Pro

This model offers the deepest reasoning and a 2M token context window -
perfect for generating detailed, long-form roadmaps!
Your preference has been saved.
```

### 2. Certification Switching (1 minute)

**[Screen: Discord]**

```
You: /cert
```

**[Bot responds with cert selection menu]**

```
🎯 CERTIFICATION SELECTION

Current: OSCP

Select your certification focus:
🔴 OSCP - Penetration Testing
🔴 OSEP - Advanced Pentesting
🔴 OSWE - Web Application Security
🔴 OSED - Exploit Development
...
```

> "You can switch between any of the 9 supported certifications. Each one has its own specialized AI prompts, resources, and assessment questions."

**[Select OSWE]**

```
✅ Certification changed to OSWE!

Now focusing on web application security.
Your AI guidance will be specialized for OSWE topics.

Try asking: /ask How do I test for SQL injection?
```

### 3. Multi-User Support (1 minute 30 seconds)

**[Screen: Show second test account]**

```
TestUser2: /start
```

**[Bot responds]**

```
🎯 Welcome TestUser2 to Try-Harder-AI!
...
```

> "Each user gets their own completely separate profile, progress tracking, and roadmap. The bot remembers everyone individually."

**[Switch back to main account]**

```
You: /progress
```

> "See? My progress is still here, completely separate from other users. All data is isolated and private."

### 4. Data Persistence (1 minute 30 seconds)

**[Screen: Terminal - Show stopping bot]**

```bash
# Stop the bot (Ctrl+C)
^C
[2025-01-15 11:00:00] INFO: Saving user data...
[2025-01-15 11:00:00] INFO: Shutting down gracefully...
```

> "When we stop the bot, it automatically saves all user data. Let's restart and verify nothing was lost."

**[Restart bot]**

```bash
python bot/main.py
```

**[Screen: Discord]**

```
You: /progress
```

**[Bot shows same progress as before]**

> "Perfect! All my progress, roadmap, assessment history - everything is preserved. The bot uses JSON storage for persistence, so your data is always safe."

---

## 🎬 Closing (2 minutes)

### Feature Summary (45 seconds)

**[Screen: Show feature list graphic]**

> "Let's recap what we've seen today:"

**[Show animated bullets]**

- ✅ **Smart Assessments** - AI analyzes your skills and identifies weak areas
- ✅ **Personalized Roadmaps** - 6-24 week plans tailored to YOU
- ✅ **24/7 AI Mentor** - Get answers instantly with the `/ask` command
- ✅ **Progress Tracking** - Gamified system with achievements and stats
- ✅ **Multi-Model AI** - Switch between 5 Gemini model variants
- ✅ **9 Certifications** - Full OffSec certification suite support
- ✅ **100% Free** - Open-source, no subscriptions, no ads

### Getting Started (30 seconds)

**[Screen: Show GitHub repo]**

> "Ready to get started? Here's what you need to do:"

1. **Star the repo** on GitHub (link in description)
2. **Follow the setup guide** - takes 5 minutes
3. **Get your API keys** - Discord + Google AI Studio (free!)
4. **Launch and start learning!**

**[Show links on screen]**

```
📦 GitHub: github.com/The4v1/Try-Harder-AI
📖 Docs: Full setup guide in README.md
🔑 Discord Bot: discord.com/developers
🤖 Gemini API Key: aistudio.google.com/apikey
💬 Community: discord.gg/try-harder-ai
```

### Call to Action (30 seconds)

> "If you found this helpful:"
- 👍 **Like this video**
- 🔔 **Subscribe** for more OffSec content
- 💬 **Comment** which certification you're studying for
- ⭐ **Star the GitHub repo** to support the project
- 🔗 **Share** with your study group

### Final Message (15 seconds)

**[Screen: Show "Try Harder" graphic]**

> "Remember - the OSCP motto is 'Try Harder', but you don't have to try alone. Let AI help you work smarter, not just harder. Good luck with your certification journey, and I'll see you in the next video!"

**[Fade to outro with links]**

---

## 💬 Talking Points

### Key Messages to Emphasize

1. **Personalization**
   - "This isn't a generic study plan - it adapts to YOUR needs"
   - "The AI analyzes YOUR weak areas and focuses there"

2. **Comprehensiveness**
   - "2500+ lines of certification data"
   - "180 assessment questions across 9 certifications"
   - "1000+ resources with real links"

3. **AI Power**
   - "Powered by Google Gemini AI - fast, capable, and free to start"
   - "Gemini 1.5 Flash gives near-instant responses right in Discord"
   - "Step-by-step, actionable responses - no fluff"

4. **Open Source**
   - "Completely free and open-source"
   - "No subscriptions, no ads, no paywalls"
   - "Google's free tier covers up to 1,500 requests per day"
   - "Community-driven development"

5. **Ease of Use**
   - "5-minute setup"
   - "Native Discord slash commands - just type `/` and go"
   - "Works 24/7 on your server"

### Phrases to Avoid

❌ "This is perfect" - Nothing is perfect
❌ "Guaranteed to pass" - No guarantees in certification
❌ "Replace studying" - It's a supplement, not replacement
❌ "No effort needed" - Still requires work

### Phrases to Use

✅ "This helps you study smarter"
✅ "Personalized to your learning style"
✅ "Complements your existing study plan"
✅ "Identifies areas needing focus"

---

## 🔧 Troubleshooting During Demo

### Common Issues & Fixes

**Bot doesn't respond:**
```
Quick Fix: Check bot is online (green status)
Backup: Restart bot quickly
Fallback: "Looks like a temporary glitch - this rarely happens"
```

**Slash commands don't appear:**
```
Quick Fix: Re-invite bot with applications.commands scope
Backup: Wait 1-2 minutes for Discord to sync
Fallback: "Slash commands sync on startup - let me restart"
```

**API timeout:**
```
Quick Fix: "Gemini is thinking hard on this one..."
Backup: Ask simpler question
Fallback: "This shows how complex the AI analysis is!"
```

**Assessment freezes:**
```
Quick Fix: Have backup assessment ready
Backup: Restart assessment with /assess
Fallback: Skip to results screenshot
```

**Roadmap takes long:**
```
Quick Fix: "While Gemini generates the roadmap, let me show you..."
Backup: Use pre-generated roadmap screenshot
Fallback: Fast-forward with editing
```

### Emergency Backup Plan

**If bot completely fails:**
1. Have screenshots ready
2. Switch to showing code
3. Focus on architecture explanation
4. Use backup recording clips

---

## 🎨 B-Roll Suggestions

### Visual Elements

1. **Code Editor Shots**
   - Scrolling through bot/main.py
   - Showing data YAML files
   - Configuration files

2. **Terminal Activity**
   - Bot startup logs
   - Gemini API requests logging
   - Database operations

3. **Graphics/Animations**
   - Certification logos
   - Feature icons
   - Architecture diagrams

4. **Screenshots**
   - Discord embeds
   - Assessment results
   - Roadmap examples

5. **Screen Recordings**
   - Typing `/` in Discord to reveal slash commands
   - Bot responding
   - Progress bars filling

### Music Suggestions

- **Intro:** Upbeat, energetic (30 sec)
- **Demo:** Focus music, tech vibes (18 min)
- **Outro:** Motivational, inspiring (30 sec)

### On-Screen Text

**Use text overlays for:**
- Key features
- Slash command syntax (e.g., `/ask [question]`)
- Links and resources
- Statistics and numbers
- Emphasis on important points

---

## 📝 Script Variations

### Quick Demo (5 minutes)

Focus on:
1. What is Try-Harder-AI (30 sec)
2. Quick setup montage (1 min)
3. One assessment question (1 min)
4. Show roadmap result (1 min 30 sec)
5. One `/ask` example (1 min)

### Deep Dive (45 minutes)

Include:
1. Full installation process
2. Complete assessment (all questions)
3. Roadmap generation explanation
4. Multiple `/ask` examples
5. Architecture walkthrough
6. Code explanation
7. Contribution guide
8. Community showcase

### Tutorial Series

**Episode 1:** Setup & Installation
**Episode 2:** Skill Assessment Deep Dive
**Episode 3:** Creating Perfect Roadmaps
**Episode 4:** Mastering the `/ask` Command
**Episode 5:** Tracking Progress & Achievements
**Episode 6:** Advanced Features & Customization

---

## 🎯 Target Audience Notes

### For Beginners

- Emphasize ease of use
- Show simple slash commands (highlight the `/` autocomplete UI)
- Explain what certifications are
- Focus on learning path guidance

### For Intermediate

- Show assessment accuracy
- Emphasize roadmap customization
- Demonstrate AI quality
- Focus on time-saving features

### For Advanced

- Show technical architecture
- Discuss Gemini model options and when to use each
- Mention contribution opportunities
- Focus on customization potential

---

## 📊 Metrics to Track

**During Demo, showcase:**
- Number of certifications (9)
- Questions in database (180+)
- Lines of code (5000+)
- Resources available (200+)
- Response time (<3 seconds with Gemini Flash)
- Setup time (5 minutes)
- Free tier: 1,500 requests/day at no cost

---

## 🎬 Production Checklist

**Before Recording:**
- [ ] Clean Discord history
- [ ] Reset user data
- [ ] Check bot status and slash commands are synced
- [ ] Test all slash commands
- [ ] Prepare backup screenshots
- [ ] Charge devices
- [ ] Test audio levels
- [ ] Close unnecessary apps

**During Recording:**
- [ ] Speak clearly and slowly
- [ ] Show excitement/enthusiasm
- [ ] Pause between major sections
- [ ] Check time periodically
- [ ] Note any mistakes for editing
- [ ] Stay hydrated

**After Recording:**
- [ ] Review footage
- [ ] Note edit points
- [ ] Export in high quality
- [ ] Create thumbnail
- [ ] Write description
- [ ] Add timestamps
- [ ] Upload unlisted for review

---

**Good luck with your demo! Try Harder! 🚀💪**

*Last Updated: February 2026*
*Version: 3.0.0*