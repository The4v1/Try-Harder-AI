# 🏗️ System Architecture - Try-Harder-AI Bot

## Overview

This document provides a comprehensive overview of the Try-Harder-AI Discord bot architecture, including system design, component interactions, data flow, and technical implementation details.

---

## Table of Contents

1. [High-Level Architecture](#high-level-architecture)
2. [System Components](#system-components)
3. [Directory Structure](#directory-structure)
4. [Data Flow](#data-flow)
5. [Module Dependencies](#module-dependencies)
6. [Database Design](#database-design)
7. [AI Integration Architecture](#ai-integration-architecture)
8. [Discord Bot Architecture](#discord-bot-architecture)
9. [Security Architecture](#security-architecture)
10. [Scalability Considerations](#scalability-considerations)
11. [Deployment Architecture](#deployment-architecture)

---

## 🎯 High-Level Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         DISCORD PLATFORM                         │
│                     (User Interaction Layer)                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Discord API
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    TRY-HARDER-AI BOT                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Slash Cmd  │  │  Assessment  │  │   Roadmap    │          │
│  │   Handler    │  │    Engine    │  │  Generator   │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                  │
│         └──────────────────┼──────────────────┘                  │
│                            │                                     │
│                  ┌─────────▼─────────┐                          │
│                  │   User Manager    │                          │
│                  │ (State & Progress)│                          │
│                  └─────────┬─────────┘                          │
│                            │                                     │
│                  ┌─────────▼─────────┐                          │
│                  │    AI Engine      │                          │
│                  │  (Gemini API)     │                          │
│                  └─────────┬─────────┘                          │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                             │ HTTPS API Calls
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    GOOGLE GEMINI API                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐  │
│  │ Gemini 1.5 │  │ Gemini 1.5 │  │ Gemini 1.5 │  │Gemini 2.0│  │
│  │   Flash    │  │  Flash-8B  │  │    Pro     │  │  Flash   │  │
│  └────────────┘  └────────────┘  └────────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         DATA STORAGE                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │Certifications│  │  Questions   │  │  Resources   │          │
│  │     YAML     │  │     YAML     │  │     YAML     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
│  ┌──────────────────────────────────────────────────┐          │
│  │         User Progress & State (JSON)             │          │
│  │  • Assessment History  • Roadmaps  • Settings    │          │
│  └──────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **Modularity**: Each component has a single responsibility
2. **Async-First**: All I/O operations are asynchronous
3. **Stateful**: User progress and context are preserved
4. **Scalable**: Designed to handle multiple concurrent users
5. **Configurable**: Environment-based configuration
6. **Extensible**: Easy to add new certifications or features

---

## 🧩 System Components

### 1. **Slash Command Handler** (`commands.py`)
**Responsibility:** Process Discord slash commands and route to appropriate handlers

**Key Functions:**
- Slash command parsing and validation
- Permission checking
- Error handling and user feedback
- Rate limiting enforcement
- Command help generation

**Commands Supported:**
```python
/start          # Initialize user profile
/assess         # Begin skill assessment
/roadmap        # Generate study plan
/ask            # AI-powered Q&A
/progress       # View learning progress
/help           # Display help information
/model          # Switch AI model
/cert           # Change certification focus
```

### 2. **Assessment Engine** (`assessment.py`)
**Responsibility:** Conduct skill assessments and analyze results

**Features:**
- Question selection based on difficulty
- Interactive quiz flow with timeout
- Score calculation and analysis
- Weak area identification
- Skill level determination
- Recommendation generation

**Assessment Flow:**
```
User -> /assess -> Select Certification
                        ↓
                Load Questions (YAML)
                        ↓
                Present Questions
                   (Interactive)
                        ↓
                Collect Responses
                        ↓
                Calculate Score
                        ↓
                AI Analysis (Gemini API)
                        ↓
                Store Results (JSON)
                        ↓
                Display Feedback
```

### 3. **Roadmap Generator** (`roadmap.py`)
**Responsibility:** Create personalized study plans

**Features:**
- AI-powered roadmap generation
- Customizable duration (6-24 weeks)
- Skill-level adaptation
- Resource integration
- Milestone tracking
- Progress monitoring

**Generation Process:**
```
Assessment Results + User Preferences
              ↓
    Load Certification Data
              ↓
    AI Prompt Construction
              ↓
    Gemini API Call
              ↓
    Parse & Structure Roadmap
              ↓
    Save to User Data
              ↓
    Format for Discord Display
```

### 4. **AI Engine** (`ai_engine.py`)
**Responsibility:** Interface with Google Gemini API

**Core Capabilities:**
- Multi-model support (Gemini 1.5 Flash, Flash-8B, Pro, 2.0 Flash, 1.0 Pro)
- Async request handling
- Error handling and retries
- Token usage tracking
- Response formatting
- Prompt management

**Request Pipeline:**
```
User Input
    ↓
System Instruction + User Prompt
    ↓
Rate Limiter Check
    ↓
Gemini API Request (with retries)
    ↓
Response Validation
    ↓
Token Usage Tracking
    ↓
Format Response
    ↓
Return to Slash Command Handler
```

### 5. **User Manager** (`user_manager.py`)
**Responsibility:** Manage user state and progress

**Data Managed:**
- User profiles
- Assessment history
- Active roadmaps
- Progress tracking
- Achievements
- Settings and preferences

**Operations:**
```python
- create_user()           # Initialize new user
- get_user()              # Retrieve user data
- update_progress()       # Update learning progress
- save_assessment()       # Store assessment results
- save_roadmap()          # Store study plan
- get_statistics()        # Retrieve user stats
- update_settings()       # Modify preferences
```

### 6. **Configuration Module** (`config/settings.py`)
**Responsibility:** Central configuration management

**Configuration Categories:**
- Discord bot settings
- Google Gemini API configuration
- Database paths
- Logging configuration
- Command settings
- Rate limiting rules

### 7. **Logging System** (`config/logging_config.py`)
**Responsibility:** Structured logging for debugging and monitoring

**Log Levels:**
- DEBUG: Detailed diagnostic information
- INFO: General informational messages
- WARNING: Warning messages
- ERROR: Error events
- CRITICAL: Critical failures

---

## 📁 Directory Structure

```
try-harder-ai-complete/
│
├── 📂 bot/                          # Core bot modules
│   ├── __init__.py                  # Package initialization
│   ├── main.py                      # Bot entry point & event handlers
│   ├── commands.py                  # Discord slash command handlers (600+ lines)
│   ├── assessment.py                # Assessment logic & flow (500+ lines)
│   ├── roadmap.py                   # Study plan generation (450+ lines)
│   ├── ai_engine.py                 # Gemini API integration (650+ lines)
│   └── user_manager.py              # User data management (400+ lines)
│
├── 📂 data/                         # Data storage
│   ├── certifications.yaml          # Cert details (2550+ lines)
│   ├── questions.yaml               # Assessment questions (1150+ lines)
│   ├── resources.yaml               # Learning resources (1000+ lines)
│   └── user_data.json               # User progress (auto-generated)
│
├── 📂 prompts/                      # AI system prompts
│   ├── system_prompt.txt            # Base AI instructions
│   ├── oscp_prompt.txt              # OSCP-specific guidance
│   ├── osep_prompt.txt              # OSEP-specific guidance
│   ├── oswe_prompt.txt              # OSWE-specific guidance
│   ├── osed_prompt.txt              # OSED-specific guidance
│   ├── oswp_prompt.txt              # OSWP-specific guidance
│   ├── oswa_prompt.txt              # OSWA-specific guidance
│   ├── osmr_prompt.txt              # OSMR-specific guidance
│   ├── osda_prompt.txt              # OSDA-specific guidance
│   └── klcp_prompt.txt              # KLCP-specific guidance
│
├── 📂 config/                       # Configuration
│   ├── settings.py                  # Bot constants & config (300+ lines)
│   └── logging_config.py            # Logging setup (250+ lines)
│
├── 📂 utils/                        # Utility functions
│   ├── helpers.py                   # Common helper functions
│   ├── validators.py                # Input validation
│   └── formatters.py                # Discord embed formatting
│
├── 📂 docs/                         # Documentation
│   ├── ARCHITECTURE.md              # This file
│   ├── API_INTEGRATION.md           # API integration details
│   ├── DEMO_SCRIPT.md               # Video demo guide
│   ├── DEPLOYMENT.md                # Production deployment
│   └── CONTRIBUTING.md              # Contribution guidelines
│
├── 📂 tests/                        # Unit tests
│   ├── test_assessment.py           # Assessment tests
│   ├── test_ai_engine.py            # AI integration tests
│   └── test_commands.py             # Slash command handler tests
│
├── 📂 logs/                         # Log files (auto-generated)
│   ├── bot.log                      # Main bot log
│   ├── api.log                      # API request log
│   └── errors.log                   # Error log
│
├── 📄 .env                          # Environment variables (not in git)
├── 📄 .env.example                  # Environment template
├── 📄 .gitignore                    # Git ignore rules
├── 📄 requirements.txt              # Python dependencies
├── 📄 README.md                     # Main documentation
├── 📄 SETUP.md                      # Setup instructions
├── 📄 QUICKSTART.md                 # 5-minute quickstart
└── 📄 LICENSE                       # MIT License
```

---

## 🔄 Data Flow

### Slash Command Processing Flow

```
Discord User Input (Slash Command)
       ↓
┌──────────────────────────────────────┐
│  1. Discord.py Interaction Handler   │
│     - on_interaction                 │
│     - app_commands tree dispatch     │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│  2. Slash Command Parser             │
│     - Validate parameters            │
│     - Check permissions              │
│     - Rate limit check               │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│  3. Command Handler                  │
│     - Route to specific function     │
│     - Load user data                 │
│     - Defer interaction response     │
└──────┬───────────────────────────────┘
       ↓
       ├─→ /assess Command
       │        ↓
       │   Load Questions
       │        ↓
       │   Interactive Quiz
       │        ↓
       │   Calculate Score
       │        ↓
       │   AI Analysis
       │        ↓
       │   Save Results
       │
       ├─→ /roadmap Command
       │        ↓
       │   Get User Preferences
       │        ↓
       │   AI Generation
       │        ↓
       │   Parse & Format
       │        ↓
       │   Save Roadmap
       │
       └─→ /ask Command
                ↓
           Load Cert Context
                ↓
           Build AI Prompt
                ↓
           Gemini API Call
                ↓
           Format Response
       ↓
┌──────────────────────────────────────┐
│  4. Response Formatter               │
│     - Discord embed creation         │
│     - Message chunking (2000 chars)  │
│     - Emoji formatting               │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│  5. Discord Interaction Followup     │
│     - Send response via followup     │
│     - Update user last_active        │
└──────────────────────────────────────┘
```

### Assessment Flow (Detailed)

```
/assess command received
         ↓
┌─────────────────────────────────────────┐
│ 1. Certification Selection              │
│    - Display 9 cert options             │
│    - Wait for user reaction (emoji)     │
│    - Timeout: 60 seconds                │
└────┬────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────┐
│ 2. Load Questions                       │
│    - Read questions.yaml                │
│    - Filter by certification            │
│    - Select mix of difficulty levels    │
│      • 5 beginner                       │
│      • 3 intermediate                   │
│      • 2 advanced                       │
└────┬────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────┐
│ 3. Present Questions                    │
│    - For each question:                 │
│      • Display question + options       │
│      • Add reaction emojis (A/B/C/D)    │
│      • Wait for answer (60s timeout)    │
│      • Record response                  │
└────┬────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────┐
│ 4. Calculate Score                      │
│    - Beginner: 1 point each             │
│    - Intermediate: 2 points each        │
│    - Advanced: 3 points each            │
│    - Total: /30 points                  │
│    - Percentage calculation             │
└────┬────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────┐
│ 5. Analyze Results (AI)                 │
│    - Send results to Gemini API         │
│    - AI identifies:                     │
│      • Weak areas                       │
│      • Strong areas                     │
│      • Recommended level                │
│      • Study suggestions                │
└────┬────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────┐
│ 6. Save to User Data                    │
│    - Add to assessment_history[]        │
│    - Update user skill_level            │
│    - Save to user_data.json             │
└────┬────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────┐
│ 7. Display Results                      │
│    - Score breakdown                    │
│    - Visual progress bar                │
│    - Weak/strong areas                  │
│    - Next step recommendations          │
└─────────────────────────────────────────┘
```

### AI Request Flow

```
User Query
    ↓
┌──────────────────────────────┐
│ 1. Prompt Construction       │
│    - Load system instruction │
│    - Load cert-specific      │
│    - Add user context        │
│    - Format question         │
└────┬─────────────────────────┘
     ↓
┌──────────────────────────────┐
│ 2. Rate Limit Check          │
│    - Check request queue     │
│    - Apply backoff if needed │
│    - Acquire semaphore       │
└────┬─────────────────────────┘
     ↓
┌──────────────────────────────┐
│ 3. Gemini API Request        │
│    - Build GenerativeModel   │
│    - Set generation config   │
│    - Set timeout (60s)       │
│    - Call generate_content() │
└────┬─────────────────────────┘
     ↓
┌──────────────────────────────┐
│ 4. Error Handling            │
│    - Success  → Continue     │
│    - 400/403: Auth → Raise   │
│    - 429: Rate limit → Retry │
│    - 500/503: Server → Retry │
│    - Timeout → Retry         │
└────┬─────────────────────────┘
     ↓
┌──────────────────────────────┐
│ 5. Response Processing       │
│    - Extract response.text   │
│    - Track token usage       │
│    - Estimate cost           │
│    - Log request             │
└────┬─────────────────────────┘
     ↓
┌──────────────────────────────┐
│ 6. Format for Discord        │
│    - Add emojis              │
│    - Format code blocks      │
│    - Split if >2000 chars    │
│    - Create embeds           │
└────┬─────────────────────────┘
     ↓
Return to Slash Command Handler
```

---

## 🔗 Module Dependencies

### Dependency Graph

```
main.py
  │
  ├─→ commands.py
  │     ├─→ assessment.py
  │     │     ├─→ ai_engine.py
  │     │     ├─→ user_manager.py
  │     │     └─→ data/questions.yaml
  │     │
  │     ├─→ roadmap.py
  │     │     ├─→ ai_engine.py
  │     │     ├─→ user_manager.py
  │     │     ├─→ data/certifications.yaml
  │     │     └─→ data/resources.yaml
  │     │
  │     └─→ user_manager.py
  │           └─→ data/user_data.json
  │
  ├─→ ai_engine.py
  │     ├─→ config/settings.py
  │     └─→ prompts/*.txt
  │
  ├─→ config/settings.py
  │     └─→ .env
  │
  └─→ config/logging_config.py
        └─→ logs/
```

### External Dependencies

```python
# requirements.txt

# Discord Integration
discord.py>=2.3.0           # Discord bot framework (slash command support)
python-dotenv>=1.0.0        # Environment variable management

# Google Gemini AI
google-generativeai>=0.5.0  # Official Gemini API Python SDK

# Data Processing
pyyaml>=6.0                 # YAML file parsing
orjson>=3.9.0               # Fast JSON serialization

# Utilities
python-dateutil>=2.8.0      # Date/time utilities
colorama>=0.4.6             # Colored terminal output

# Optional - Development
pytest>=7.4.0               # Testing framework
black>=23.0.0               # Code formatting
flake8>=6.0.0               # Linting
```

---

## 🗄️ Database Design

### User Data Schema (JSON)

```json
{
  "user_id": {
    "user_id": "string",
    "username": "string",
    "registered_at": "ISO8601 datetime",
    "last_active": "ISO8601 datetime",
    "selected_certification": "OSCP|OSEP|OSWE|etc",
    "ai_model_preference": "gemini-1.5-flash|gemini-1.5-pro|etc",
    
    "profile": {
      "experience_level": "beginner|intermediate|advanced",
      "current_goal": "string",
      "study_hours_per_week": "integer",
      "preferred_learning_style": "hands-on|theoretical|mixed",
      "timezone": "string",
      "total_study_time_hours": "integer"
    },
    
    "assessment_history": [
      {
        "assessment_id": "string",
        "certification": "string",
        "date": "ISO8601 datetime",
        "questions_asked": "integer",
        "questions_answered": "integer",
        "score": {
          "total_points": "integer",
          "max_points": "integer",
          "percentage": "integer",
          "passed": "boolean"
        },
        "breakdown": {
          "beginner": {"correct": "int", "total": "int", "points": "int"},
          "intermediate": {"correct": "int", "total": "int", "points": "int"},
          "advanced": {"correct": "int", "total": "int", "points": "int"}
        },
        "recommended_level": "string",
        "weak_areas": ["string"],
        "strong_areas": ["string"]
      }
    ],
    
    "roadmap": {
      "roadmap_id": "string",
      "created_at": "ISO8601 datetime",
      "certification": "string",
      "duration_weeks": "integer",
      "skill_level": "string",
      "focus_areas": ["string"],
      "current_week": "integer",
      "weeks": [
        {
          "week_number": "integer",
          "title": "string",
          "status": "not_started|in_progress|completed|paused",
          "completed_at": "ISO8601 datetime|null",
          "topics": ["string"],
          "tasks_completed": "integer",
          "tasks_total": "integer",
          "machines_completed": ["string"],
          "current_machine": "string|null",
          "notes": "string"
        }
      ],
      "milestones": [
        {
          "name": "string",
          "target_date": "ISO8601 date",
          "status": "not_started|in_progress|completed",
          "progress": "integer",
          "total": "integer"
        }
      ]
    },
    
    "progress": {
      "machines_completed": {
        "hackthebox": "integer",
        "tryhackme": "integer",
        "vulnhub": "integer",
        "proving_grounds": "integer",
        "pwk_labs": "integer"
      },
      "topics_mastered": ["string"],
      "topics_in_progress": ["string"],
      "topics_to_learn": ["string"],
      "skills": {
        "enumeration": "0-100",
        "exploitation": "0-100",
        "privilege_escalation": "0-100",
        "active_directory": "0-100",
        "web_exploitation": "0-100",
        "buffer_overflow": "0-100",
        "reporting": "0-100"
      },
      "certifications": {
        "completed": ["string"],
        "in_progress": ["string"],
        "planned": ["string"]
      }
    },
    
    "achievements": [
      {
        "id": "string",
        "name": "string",
        "description": "string",
        "earned_at": "ISO8601 datetime",
        "icon": "emoji"
      }
    ],
    
    "statistics": {
      "total_commands_used": "integer",
      "total_ai_queries": "integer",
      "favorite_command": "string",
      "total_study_sessions": "integer",
      "longest_streak_days": "integer",
      "current_streak_days": "integer",
      "total_messages": "integer"
    },
    
    "settings": {
      "notifications": "boolean",
      "daily_reminders": "boolean",
      "weekly_summary": "boolean",
      "ai_model": "gemini-1.5-flash|gemini-1.5-pro|gemini-2.0-flash|etc",
      "response_style": "concise|detailed|technical",
      "emoji_enabled": "boolean",
      "theme": "offsec_red|hacker_green|blue"
    },
    
    "notes": [
      {
        "id": "string",
        "created_at": "ISO8601 datetime",
        "title": "string",
        "content": "string",
        "tags": ["string"]
      }
    ],
    
    "bookmarks": {
      "favorite_resources": ["string"],
      "saved_machines": ["string"]
    }
  }
}
```

### Data Access Patterns

```python
# Read Operations
- get_user(user_id)                    # O(1) - Direct access
- get_assessment_history(user_id)     # O(1) - Direct access
- get_active_roadmap(user_id)         # O(1) - Direct access
- get_user_progress(user_id)          # O(1) - Direct access

# Write Operations
- create_user(user_data)              # O(1) - Insert
- update_user(user_id, data)          # O(1) - Update
- append_assessment(user_id, result)  # O(1) - Append to array
- save_roadmap(user_id, roadmap)      # O(1) - Replace object

# Aggregate Operations
- get_global_statistics()             # O(n) - Iterate all users
- get_leaderboard()                   # O(n log n) - Sort users
```

---

## 🤖 AI Integration Architecture

### Prompt Engineering System

```
prompts/
  ├── system_prompt.txt          # Base personality & guidelines
  ├── oscp_prompt.txt            # OSCP-specific expertise
  ├── osep_prompt.txt            # OSEP-specific expertise
  └── ...                        # Other certification prompts

Prompt Construction:
  Base System Instruction
       +
  Certification-Specific Prompt
       +
  User Context (skill level, weak areas)
       +
  User Question
       =
  Final Prompt sent to Gemini API
```

### Multi-Model Strategy

```python
# Model Selection Logic

def select_model(task_type: str, user_preference: str = None) -> str:
    """
    Select appropriate Gemini model based on task type
    """
    if user_preference:
        return user_preference

    # Task-specific model selection
    model_map = {
        "roadmap":      "gemini-1.5-pro",       # Long-form, 2M context window
        "assessment":   "gemini-1.5-pro",       # Deep analysis & reasoning
        "quick_answer": "gemini-1.5-flash",     # Fast, cost-effective responses
        "code_review":  "gemini-1.5-pro",       # Technical accuracy
        "simple_query": "gemini-1.5-flash-8b",  # Lightweight, lowest cost
        "latest":       "gemini-2.0-flash",     # Next-gen cutting-edge tasks
    }

    return model_map.get(task_type, "gemini-1.5-flash")  # Default: Flash
```

---

## 🤖 Discord Bot Architecture

### Event Handling

```python
# Bot Event Flow

@bot.event
async def on_ready():
    """Bot startup event"""
    - Load data files (YAML, JSON)
    - Initialize Gemini AI engine
    - Setup logging
    - Print startup banner
    - Sync slash commands via bot.tree.sync()

@bot.event
async def on_interaction(interaction):
    """Every slash command interaction received"""
    - Ignore bot interactions
    - Route to app_commands tree
    - Process slash command
    - Update last_active

@bot.event
async def on_app_command_error(interaction, error):
    """Slash command error handling"""
    - Log error
    - Send user-friendly followup message
    - Update error statistics

@bot.event
async def on_reaction_add(reaction, user):
    """Interactive elements (assessment answers, cert selection)"""
    - Assessment questions
    - Certification selection
    - Multi-choice interactions
```

### Slash Command Architecture

```python
# Slash Command Pattern using discord.app_commands

from discord import app_commands

@app_commands.command(name="assess", description="Start a skill assessment")
@app_commands.describe(certification="The certification to assess (e.g. OSCP)")
@app_commands.checks.cooldown(1, 300, key=lambda i: i.user.id)  # 5 min per user
async def assess_command(interaction: discord.Interaction, certification: str = None):
    """
    Slash command structure:
    1. Defer the interaction response (shows "Bot is thinking...")
    2. Validation
    3. User data loading
    4. Core logic execution
    5. Response formatting
    6. Data persistence
    7. Send followup to user
    """
    await interaction.response.defer()  # Required for long-running tasks
    # ... implementation ...
    await interaction.followup.send(embed=result_embed)
```

---

## 🔒 Security Architecture

### API Key Management

```python
# Environment-based secrets
GEMINI_API_KEY       # Never hardcoded — stored in .env only
DISCORD_BOT_TOKEN    # Stored in .env

# Security measures:
- Keys in environment variables only
- .env file in .gitignore
- API key rotation capability
- Rate limiting per user
- Slash command cooldowns
- Permission checking
```

### Data Security

```python
# User Data Protection
- Local storage only (no cloud by default)
- No PII collection (Discord IDs only)
- User data export capability
- Data deletion on request
- No sharing between users
- Audit logging
```

### Input Validation

```python
# All user inputs validated
- Slash command parameter type enforcement (Discord handles this)
- User ID verification
- Permission checks
- Rate limit enforcement
- XSS prevention in embeds
- Prompt injection mitigation via system instructions
```

---

## 📈 Scalability Considerations

### Current Capacity

```
Concurrent Users:        100-500
Requests per Minute:     Up to 14 (Gemini Flash free tier, safely under 15 RPM)
Database Size:           <100MB for 10,000 users
API Rate Limits:         Gemini Flash: 15 RPM / 1M TPM / 1500 RPD (free tier)
Memory Usage:            ~200MB baseline
CPU Usage:               Low (async I/O bound)
```

### Horizontal Scaling

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Bot Shard  │    │  Bot Shard  │    │  Bot Shard  │
│     #1      │    │     #2      │    │     #3      │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                  ┌───────▼────────┐
                  │ Shared Storage │
                  │  (Redis/DB)    │
                  └────────────────┘
```

### Optimization Strategies

1. **Caching**
   ```python
   # Cache frequently accessed data
   - Certification data (YAML)
   - System prompts
   - User profiles (with TTL)
   ```

2. **Gemini SDK Connection Reuse**
   ```python
   # Initialize GenerativeModel once per model variant
   # Reuse across requests — avoid re-configuring per call
   model = genai.GenerativeModel("gemini-1.5-flash")
   ```

3. **Async Operations**
   ```python
   # Non-blocking I/O via run_in_executor
   - All Gemini API calls wrapped in asyncio.get_event_loop().run_in_executor()
   - Concurrent request handling
   - Background task processing
   ```

4. **Rate Limiting**
   ```python
   # Protect against abuse and API quota overrun
   - Per-user slash command cooldowns
   - Global rate limiter (14 RPM for Gemini Flash free tier)
   - Exponential backoff on 429 errors
   ```

---

## 🚀 Deployment Architecture

### Production Deployment

```
┌─────────────────────────────────────────┐
│         Cloud Platform (VPS/Cloud)      │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │      Docker Container             │ │
│  │                                   │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │   Try-Harder-AI Bot         │ │ │
│  │  │   - Discord.py (slash cmds) │ │ │
│  │  │   - Google Gemini Client    │ │ │
│  │  │   - Data Storage            │ │ │
│  │  └─────────────────────────────┘ │ │
│  │                                   │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │   Persistent Volumes        │ │ │
│  │  │   - /data (user_data.json)  │ │ │
│  │  │   - /logs                   │ │ │
│  │  └─────────────────────────────┘ │ │
│  └───────────────────────────────────┘ │
│                                         │
│  Process Manager: systemd or Docker     │
│  Auto-restart: Yes                      │
│  Logging: File + stdout                 │
└─────────────────────────────────────────┘
```

### Monitoring & Logging

```python
# Structured Logging
logs/
  ├── bot.log          # General bot activity
  ├── api.log          # Gemini API requests/responses
  ├── errors.log       # Error events
  └── audit.log        # User slash command actions

# Metrics Tracked
- Total slash commands executed
- Gemini API response times
- Error rates
- Active users
- Token usage (prompt + completion)
- Estimated cost tracking
```

---

## 📊 Performance Metrics

### Response Time Targets

```
Slash Command Processing:    < 100ms (defer immediately)
AI Response (cached):        < 500ms
AI Response (fresh):         1-4 seconds (Gemini Flash is fast)
Assessment (10 questions):   5-10 minutes
Roadmap Generation:          5-15 seconds (Gemini Flash)
```

### Resource Usage

```
Memory:
  - Baseline: ~200MB
  - Per concurrent user: +10MB
  - Peak: ~500MB (50 concurrent users)

CPU:
  - Idle: 1-5%
  - Active: 10-30%
  - Spike: 50% (mass commands)

Network:
  - Outbound Gemini API: ~50-150KB per request (avg)
  - Discord messages: ~5KB per message
  - Data files: One-time load (~4MB)
```

---

## 🔄 System Lifecycle

### Startup Sequence

```
1. Load environment variables (.env)
2. Initialize logging system
3. Configure Gemini SDK (genai.configure)
4. Connect to Discord API
5. Load data files (YAML)
6. Initialize AI engine (GeminiAI)
7. Setup slash command handlers (app_commands tree)
8. Register event listeners
9. Sync slash commands (bot.tree.sync)
10. Print startup banner
11. Set bot status (Ready)
```

### Shutdown Sequence

```
1. Stop accepting new slash command interactions
2. Complete in-progress requests
3. Save pending user data
4. Close Discord connection
5. Flush logs
6. Exit gracefully
```

---

## 📚 Technical Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Platform** | Discord | User interface & interaction |
| **Language** | Python 3.10+ | Core implementation |
| **Framework** | Discord.py | Discord bot framework (slash commands) |
| **AI Provider** | Google Gemini API | Direct AI model access |
| **AI Models** | Gemini 1.5 Flash, Flash-8B, Pro, 2.0 Flash | Natural language processing |
| **Data Format** | YAML, JSON | Data storage |
| **Async** | asyncio, run_in_executor | Concurrency handling |
| **Config** | python-dotenv | Environment management |
| **Logging** | Python logging | Monitoring & debugging |

---

## 🎯 Design Patterns Used

1. **Command Pattern**: Slash command handlers
2. **Factory Pattern**: Gemini model selection
3. **Singleton Pattern**: Configuration, logging, Gemini client
4. **Strategy Pattern**: Multiple Gemini model variants
5. **Repository Pattern**: User data management
6. **Observer Pattern**: Discord events
7. **Template Method**: Assessment flow

---

## 📝 Future Enhancements

### Planned Improvements

1. **Database Migration**
   - Move from JSON to PostgreSQL/MongoDB
   - Better concurrent access
   - Advanced querying

2. **Caching Layer**
   - Redis for frequent data
   - Reduce Gemini API calls
   - Faster response times

3. **Message Queue**
   - RabbitMQ/Kafka for async tasks
   - Background job processing
   - Better scalability

4. **Analytics Dashboard**
   - Web dashboard for statistics
   - Usage insights
   - Gemini token cost tracking

5. **Multi-Server Support**
   - Server-specific configurations
   - Leaderboards per server
   - Custom branding

6. **Gemini Multimodal Support**
   - Image analysis via Gemini Vision
   - Screenshot-based help for CTF challenges
   - PDF/document ingestion for study materials

---

*Last Updated: February 2026*
*Version: 3.0.0*
*Maintained by: Try-Harder-AI Team*