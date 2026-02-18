"""
Bot Settings and Configuration
===============================

Centralized configuration management for the Try-Harder-AI bot.

Features:
- Environment variable management
- Bot configuration constants
- Feature flags
- Rate limiting settings
- API configurations
- Discord settings
- File paths
- Google Gemini model selection
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==================== PATHS ====================

# Base directory (project root)
BASE_DIR = Path(__file__).parent.parent

# Data directories
DATA_DIR = BASE_DIR / 'data'
PROMPTS_DIR = BASE_DIR / 'prompts'
LOGS_DIR = BASE_DIR / 'logs'
CONFIG_DIR = BASE_DIR / 'config'
TESTS_DIR = BASE_DIR / 'tests'
UTILS_DIR = BASE_DIR / 'utils'
DOCS_DIR = BASE_DIR / 'docs'

# Data files
CERTIFICATIONS_FILE = DATA_DIR / 'certifications.yaml'
QUESTIONS_FILE = DATA_DIR / 'questions.yaml'
RESOURCES_FILE = DATA_DIR / 'resources.yaml'
USER_DATA_FILE = DATA_DIR / 'user_data.json'

# Ensure directories exist
for directory in [DATA_DIR, PROMPTS_DIR, LOGS_DIR, UTILS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


# ==================== ENVIRONMENT VARIABLES ====================

# Discord Configuration
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
BOT_PREFIX = os.getenv('BOT_PREFIX', '/')
BOT_OWNER_ID = os.getenv('BOT_OWNER_ID')  # Optional: Owner Discord ID

# Google Gemini AI Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
AI_MODEL = os.getenv('DEFAULT_AI_MODEL', 'gemini-1.5-flash')
AI_MAX_TOKENS = int(os.getenv('AI_MAX_TOKENS', '8192'))
AI_TEMPERATURE = float(os.getenv('AI_TEMPERATURE', '0.7'))

# Bot Environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')  # development, production, testing
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_TO_FILE = os.getenv('LOG_TO_FILE', 'true').lower() == 'true'
LOG_TO_CONSOLE = os.getenv('LOG_TO_CONSOLE', 'true').lower() == 'true'


# ==================== BOT CONFIGURATION ====================

class BotConfig:
    """Bot configuration constants."""
    
    # Bot Information
    NAME = "Try-Harder-AI"
    VERSION = "2.0.0-gemini"
    DESCRIPTION = "Your personal OffSec certification mentor powered by Google Gemini AI"
    AUTHOR = "Try-Harder-AI Team"
    
    # Bot Prefix (for slash commands)
    PREFIX = BOT_PREFIX
    
    # Supported Certifications
    SUPPORTED_CERTS = [
        'OSCP',   # Offensive Security Certified Professional
        'OSEP',   # Offensive Security Experienced Penetration Tester
        'OSWE',   # Offensive Security Web Expert
        'OSED',   # Offensive Security Exploit Developer
        'OSWP',   # Offensive Security Wireless Professional
        'OSWA',   # OffSec Web Assessor
        'OSMR',   # OffSec macOS Researcher
        'OSDA',   # OffSec Defense Analyst
        'KLCP',    # Kali Linux Certified Professional
        'OSCC',   # OffSec CyberCore Certified
        'OSEE',   # OffSec Exploitation Expert
        'OSIR'    # OffSec Incident Responder
    ]
    
    # Bot Colors (for embeds) - Discord color codes
    COLOR_PRIMARY = 0x3498db      # Blue
    COLOR_SUCCESS = 0x2ecc71      # Green
    COLOR_WARNING = 0xf39c12      # Orange
    COLOR_ERROR = 0xe74c3c        # Red
    COLOR_INFO = 0x9b59b6         # Purple
    COLOR_GOLD = 0xf1c40f         # Gold
    COLOR_OFFSEC = 0xc0392b       # OffSec Red
    
    # Embed Settings
    EMBED_THUMBNAIL = None  # Optional: Bot logo URL
    FOOTER_TEXT = "Try Harder! • Powered by Google Gemini AI 🤖"
    FOOTER_ICON = None  # Optional: Footer icon URL
    
    # Bot Status
    STATUS_TEXT = "you Try Harder! | /start"
    STATUS_TYPE = "watching"  # playing, watching, listening, competing
    
    # Command Cooldowns (seconds)
    COOLDOWN_ASSESS = 60        # 1 minute
    COOLDOWN_ROADMAP = 30       # 30 seconds
    COOLDOWN_RESOURCES = 10     # 10 seconds
    COOLDOWN_TIPS = 10          # 10 seconds
    COOLDOWN_ASK = 5            # 5 seconds


# ==================== DISCORD SETTINGS ====================

class DiscordConfig:
    """Discord-specific settings."""
    
    # Intents
    REQUIRE_MESSAGE_CONTENT = True
    REQUIRE_MEMBERS = True
    REQUIRE_GUILDS = True
    REQUIRE_PRESENCES = False  # Usually not needed
    
    # Message Settings
    MAX_MESSAGE_LENGTH = 2000
    MAX_EMBED_DESCRIPTION = 4096
    MAX_EMBED_FIELDS = 25
    MAX_EMBED_FIELD_NAME = 256
    MAX_EMBED_FIELD_VALUE = 1024
    MAX_EMBED_TITLE = 256
    
    # Rate Limiting
    MAX_MESSAGES_PER_MINUTE = 60
    MAX_EMBEDS_PER_MESSAGE = 10
    
    # Permissions
    REQUIRED_PERMISSIONS = [
        'send_messages',
        'embed_links',
        'attach_files',
        'read_message_history',
        'add_reactions',
        'use_external_emojis',
        'use_application_commands'  # Required for slash commands
    ]
    
    # Auto-delete Settings
    AUTO_DELETE_ERRORS = False
    ERROR_DELETE_DELAY = 10  # seconds


# ==================== AI CONFIGURATION ====================

class AIConfig:
    """AI engine configuration for Google Gemini."""
    
    # Model Settings
    MODEL = AI_MODEL
    MAX_TOKENS = AI_MAX_TOKENS
    TEMPERATURE = AI_TEMPERATURE
    
    # Available Models (Google Gemini)
    AVAILABLE_MODELS = {
        'flash': 'gemini-1.5-flash',           # Fast, cost-effective (FREE - 15 RPM)
        'pro': 'gemini-1.5-pro',               # Best quality (FREE - 2 RPM)
        'flash-8b': 'gemini-1.5-flash-8b'      # Ultra fast (FREE - 15 RPM)
    }
    
    # Default Model
    DEFAULT_MODEL = 'gemini-1.5-flash'
    
    # Timeout Settings
    API_TIMEOUT = 60  # seconds
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds (exponential backoff)
    
    # Rate Limiting (FREE tier)
    REQUESTS_PER_MINUTE = 15  # Gemini 1.5 Flash free tier
    REQUESTS_PER_HOUR = 1000
    MAX_CONCURRENT_REQUESTS = 2  # Conservative for free tier
    
    # Response Settings
    MAX_CONVERSATION_HISTORY = 10  # messages
    ENABLE_STREAMING = False
    
    # Roadmap Generation
    ROADMAP_DEFAULT_WEEKS = 12
    ROADMAP_MIN_WEEKS = 6
    ROADMAP_MAX_WEEKS = 24
    
    # Cache Settings
    ENABLE_RESPONSE_CACHE = False
    CACHE_TTL = 3600  # seconds


# ==================== ASSESSMENT SETTINGS ====================

class AssessmentConfig:
    """Assessment system configuration."""
    
    # Question Settings
    MIN_QUESTIONS = 5
    MAX_QUESTIONS = 10
    DEFAULT_QUESTIONS = 5
    
    # Scoring
    MIN_SCORE = 0
    MAX_SCORE = 100
    
    # Skill Level Thresholds (based on percentage)
    BEGINNER_THRESHOLD = 40      # 0-39 = Beginner
    INTERMEDIATE_THRESHOLD = 65  # 40-64 = Intermediate
    ADVANCED_THRESHOLD = 85      # 65-84 = Advanced
                                 # 85-100 = Expert
    
    # Timeout Settings
    QUESTION_TIMEOUT = 60  # seconds per question
    SESSION_TIMEOUT = 1800  # seconds (30 minutes total)
    
    # Answer Validation
    ALLOW_SKIP = False
    ALLOW_BACK = False
    
    # Progress Tracking
    TRACK_TIME_PER_QUESTION = True
    SAVE_INTERMEDIATE_RESULTS = True


# ==================== USER MANAGEMENT ====================

class UserConfig:
    """User management configuration."""
    
    # Storage
    STORAGE_FILE = USER_DATA_FILE
    AUTO_SAVE = True
    BACKUP_ENABLED = True
    BACKUP_INTERVAL = 86400  # seconds (24 hours)
    
    # Session Management
    SESSION_TIMEOUT = 3600  # seconds (1 hour)
    MAX_CONCURRENT_SESSIONS = 1
    
    # Data Retention
    KEEP_HISTORY = True
    MAX_HISTORY_ENTRIES = 50
    INACTIVE_USER_DAYS = 90  # days before cleanup
    
    # Progress Tracking
    TRACK_MACHINES = True
    TRACK_HOURS = True
    TRACK_MILESTONES = True
    
    # Preferences
    DEFAULT_STUDY_HOURS = 15  # hours per week
    DEFAULT_NOTIFICATIONS = True


# ==================== FEATURE FLAGS ====================

class FeatureFlags:
    """Feature toggle flags."""
    
    # Core Features
    ENABLE_ASSESSMENTS = True
    ENABLE_ROADMAPS = True
    ENABLE_AI_GENERATION = True
    ENABLE_ASK_COMMAND = True
    
    # Additional Features
    ENABLE_PROGRESS_TRACKING = True
    ENABLE_LEADERBOARDS = True
    ENABLE_STATISTICS = True
    ENABLE_EXPORT_IMPORT = True
    
    # Experimental Features
    ENABLE_VOICE_COMMANDS = False
    ENABLE_SLASH_COMMANDS = True  # Discord slash commands enabled
    ENABLE_WEB_DASHBOARD = False
    ENABLE_NOTIFICATIONS = False
    ENABLE_MULTI_LANGUAGE = False
    
    # Admin Features
    ENABLE_ADMIN_COMMANDS = True
    ENABLE_DEBUG_COMMANDS = DEBUG_MODE
    ENABLE_METRICS = True


# ==================== RESOURCE LIMITS ====================

class ResourceLimits:
    """Resource usage limits."""
    
    # Memory
    MAX_MEMORY_MB = 512
    WARNING_MEMORY_MB = 400
    
    # Storage
    MAX_USER_DATA_SIZE_MB = 100
    MAX_LOG_SIZE_MB = 50
    MAX_CACHE_SIZE_MB = 20
    
    # Concurrent Operations
    MAX_CONCURRENT_ASSESSMENTS = 100
    MAX_CONCURRENT_AI_REQUESTS = 10
    MAX_CONCURRENT_ROADMAPS = 5
    
    # Rate Limiting
    USER_COMMANDS_PER_MINUTE = 10
    USER_COMMANDS_PER_HOUR = 100
    GLOBAL_COMMANDS_PER_MINUTE = 1000


# ==================== ERROR MESSAGES ====================

class ErrorMessages:
    """Standard error messages."""
    
    GENERIC_ERROR = "⚠️ An error occurred. Please try again."
    COMMAND_NOT_FOUND = "❌ Command not found! Use `/help` to see available commands."
    MISSING_ARGUMENT = "❌ Missing required argument: {arg}"
    INVALID_ARGUMENT = "❌ Invalid argument provided."
    PERMISSION_DENIED = "❌ You don't have permission to use this command."
    BOT_PERMISSION_DENIED = "❌ I don't have the required permissions."
    COOLDOWN_ACTIVE = "⏰ This command is on cooldown. Try again in {time} seconds."
    
    # Assessment Errors
    NO_ACTIVE_ASSESSMENT = "❌ No active assessment found. Use `/skillcheck` to start."
    ASSESSMENT_TIMEOUT = "⏰ Assessment timed out. Please start again."
    INVALID_ANSWER = "❌ Invalid answer. Please enter a number between {min} and {max}."
    
    # AI Errors
    AI_ERROR = "⚠️ AI service error. Please try again later."
    AI_RATE_LIMIT = "⚠️ Rate limit exceeded. Please wait a moment."
    AI_TIMEOUT = "⏰ AI request timed out. Please try again."
    
    # Data Errors
    CERT_NOT_FOUND = "❌ Certification '{cert}' not found! Use `/certs` to see available options."
    USER_NOT_FOUND = "❌ User data not found. Please start with `/skillcheck`."
    DATA_LOAD_ERROR = "❌ Failed to load data. Please contact support."


# ==================== SUCCESS MESSAGES ====================

class SuccessMessages:
    """Standard success messages."""
    
    ASSESSMENT_STARTED = "🎯 Assessment started for {cert}!"
    ASSESSMENT_COMPLETED = "🎉 Assessment complete! Your score: {score}%"
    ROADMAP_GENERATED = "✅ Roadmap generated successfully!"
    PROGRESS_UPDATED = "✅ Progress updated!"
    DATA_SAVED = "💾 Data saved successfully!"
    DATA_EXPORTED = "📤 Data exported successfully!"
    DATA_IMPORTED = "📥 Data imported successfully!"


# ==================== HELP TEXT ====================

class HelpText:
    """Help text for commands."""
    
    START = "🎯 Display welcome message and introduction"
    CERTS = "📚 List all available OffSec certifications"
    ASSESS = "📝 Start skill assessment for a certification (e.g., `/skillcheck`)"
    ROADMAP = "🗺️ View your personalized study roadmap"
    ASK = "💡 Ask any cybersecurity question with emoji-rich formatting"
    RESOURCES = "📖 Get resources for a specific certification"
    TIPS = "⚡ Get exam tips and strategies for a certification"
    PROGRESS = "📊 View your current progress"
    CANCEL = "❌ Cancel current assessment"
    STATS = "📈 Show bot statistics"
    HELP = "❓ Show this help message"


# ==================== URLS ====================

class URLs:
    """External URLs and links."""
    
    # OffSec
    OFFSEC_WEBSITE = "https://www.offsec.com"
    OFFSEC_LEARN = "https://learn.offsec.com"
    OFFSEC_DISCORD = "https://discord.gg/offsec"
    
    # Community
    GITHUB_REPO = "https://github.com/try-harder-ai/bot"  # Update with actual repo
    DOCUMENTATION = "https://docs.try-harder-ai.com"  # Update with actual docs
    
    # Practice Platforms
    HACKTHEBOX = "https://www.hackthebox.com"
    TRYHACKME = "https://tryhackme.com"
    PROVING_GROUNDS = "https://www.offsec.com/labs/individual/"
    VULNHUB = "https://www.vulnhub.com"
    
    # Resources
    HACKTRICKS = "https://book.hacktricks.xyz"
    PAYLOADS_ALL_THE_THINGS = "https://github.com/swisskyrepo/PayloadsAllTheThings"
    GTFOBINS = "https://gtfobins.github.io"
    LOLBAS = "https://lolbas-project.github.io"
    
    # Google Gemini
    GEMINI_WEBSITE = "https://ai.google.dev/"
    GEMINI_DOCS = "https://ai.google.dev/docs"


# ==================== EMOJI CONSTANTS ====================

class Emojis:
    """Emoji constants used throughout the bot."""
    
    # General
    SUCCESS = "✅"
    ERROR = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"
    LOADING = "⏳"
    
    # Certifications
    CERT = "🎯"
    BOOK = "📚"
    EXAM = "📝"
    
    # Progress
    FIRE = "🔥"
    STAR = "⭐"
    TROPHY = "🏆"
    ROCKET = "🚀"
    
    # Skills
    BEGINNER = "🌱"
    INTERMEDIATE = "⚡"
    ADVANCED = "🔥"
    EXPERT = "👑"
    
    # Activities
    STUDYING = "📖"
    PRACTICING = "🎮"
    TESTING = "🧪"
    CELEBRATING = "🎉"


# ==================== UTILITY FUNCTIONS ====================

def get_config() -> Dict[str, Any]:
    """
    Get all configuration as a dictionary.
    
    Returns:
        Configuration dictionary
    """
    return {
        'bot': {
            'name': BotConfig.NAME,
            'version': BotConfig.VERSION,
            'description': BotConfig.DESCRIPTION,
            'prefix': BotConfig.PREFIX,
            'supported_certs': BotConfig.SUPPORTED_CERTS
        },
        'discord': {
            'token': DISCORD_BOT_TOKEN is not None,
            'prefix': BOT_PREFIX,
            'owner_id': BOT_OWNER_ID
        },
        'ai': {
            'provider': 'Google Gemini',
            'model': AIConfig.MODEL,
            'max_tokens': AIConfig.MAX_TOKENS,
            'enabled': GEMINI_API_KEY is not None
        },
        'environment': {
            'env': ENVIRONMENT,
            'debug': DEBUG_MODE,
            'log_level': LOG_LEVEL
        },
        'features': {
            'assessments': FeatureFlags.ENABLE_ASSESSMENTS,
            'roadmaps': FeatureFlags.ENABLE_ROADMAPS,
            'ai_generation': FeatureFlags.ENABLE_AI_GENERATION,
            'ask_command': FeatureFlags.ENABLE_ASK_COMMAND,
            'progress_tracking': FeatureFlags.ENABLE_PROGRESS_TRACKING,
            'slash_commands': FeatureFlags.ENABLE_SLASH_COMMANDS
        }
    }


def validate_config() -> tuple[bool, list[str]]:
    """
    Validate configuration and check for required settings.
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check required environment variables
    if not DISCORD_BOT_TOKEN:
        errors.append("❌ DISCORD_BOT_TOKEN is not set in .env file")
    
    if not GEMINI_API_KEY:
        errors.append("❌ GEMINI_API_KEY is not set in .env file")
    
    # Check required files
    if not CERTIFICATIONS_FILE.exists():
        errors.append(f"⚠️ Certifications file not found: {CERTIFICATIONS_FILE}")
    
    if not QUESTIONS_FILE.exists():
        errors.append(f"⚠️ Questions file not found: {QUESTIONS_FILE}")
    
    # Check data directory permissions
    if not DATA_DIR.exists():
        try:
            DATA_DIR.mkdir(parents=True)
        except Exception as e:
            errors.append(f"❌ Cannot create data directory: {e}")
    
    # Validate AI model
    if AIConfig.MODEL not in AIConfig.AVAILABLE_MODELS.values():
        errors.append(f"⚠️ Unknown AI model: {AIConfig.MODEL}")
    
    is_valid = len(errors) == 0
    return is_valid, errors


def print_config():
    """Print configuration for debugging."""
    config = get_config()
    
    print("="*60)
    print("🤖 BOT CONFIGURATION")
    print("="*60)
    
    for section, values in config.items():
        print(f"\n📋 {section.upper()}:")
        for key, value in values.items():
            # Mask sensitive values
            if key in ['token', 'api_key'] and value:
                value = '***HIDDEN***'
            print(f"  {key}: {value}")
    
    print("\n" + "="*60)
    
    # Validate
    is_valid, errors = validate_config()
    if is_valid:
        print("✅ Configuration is valid")
    else:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"  {error}")
    
    print("="*60)


# ==================== EXPORTS ====================

__all__ = [
    # Paths
    'BASE_DIR',
    'DATA_DIR',
    'PROMPTS_DIR',
    'LOGS_DIR',
    'CERTIFICATIONS_FILE',
    'QUESTIONS_FILE',
    'USER_DATA_FILE',
    
    # Environment
    'DISCORD_BOT_TOKEN',
    'GEMINI_API_KEY',
    'BOT_PREFIX',
    'ENVIRONMENT',
    'DEBUG_MODE',
    'LOG_LEVEL',
    
    # Classes
    'BotConfig',
    'DiscordConfig',
    'AIConfig',
    'AssessmentConfig',
    'UserConfig',
    'FeatureFlags',
    'ResourceLimits',
    'ErrorMessages',
    'SuccessMessages',
    'HelpText',
    'URLs',
    'Emojis',
    
    # Functions
    'get_config',
    'validate_config',
    'print_config'
]


# ==================== TESTING ====================

if __name__ == "__main__":
    print_config()