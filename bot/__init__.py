"""
Try-Harder-AI Discord Bot
=========================

A comprehensive Discord bot for OffSec certification guidance powered by Google Gemini AI.

This package contains all the core modules for the bot:
- main.py: Bot initialization and entry point
- commands.py: Discord command handlers
- assessment.py: Skill assessment logic
- roadmap.py: AI-powered study plan generation
- gemini_engine.py: Google Gemini AI integration (1.5 Flash/Pro)
- user_manager.py: User state and progress tracking

Author: Try-Harder-AI Team
Version: 2.0.0 (Gemini Edition)
License: MIT
"""

__version__ = "2.0.0-gemini"
__author__ = "Try-Harder-AI Team"
__license__ = "MIT"

# Package-level imports for easier access
from .gemini_engine import GeminiAI
from .assessment import AssessmentManager
from .roadmap import RoadmapGenerator
from .user_manager import UserManager
from .commands import setup_commands

__all__ = [
    "GeminiAI",
    "AssessmentManager",
    "RoadmapGenerator",
    "UserManager",
    "setup_commands",
]

# Bot metadata
BOT_NAME = "Try-Harder-AI"
BOT_DESCRIPTION = "Your personal OffSec certification mentor powered by Google Gemini AI"
SUPPORTED_CERTS = [
    "OSCP",   # Offensive Security Certified Professional
    "OSEP",   # Offensive Security Experienced Penetration Tester
    "OSWE",   # Offensive Security Web Expert
    "OSED",   # Offensive Security Exploit Developer
    "OSWP",   # Offensive Security Wireless Professional
    "OSWA",   # OffSec Web Assessor
    "OSMR",   # OffSec macOS Researcher
    "OSDA",   # OffSec Defense Analyst
    "KLCP",   # Kali Linux Certified Professional
    "OSCC",   # OffSec CyberCore Certified (NEW - Beginner)
    "OSEE",   # OffSec Exploitation Expert (NEW - Expert)
    "OSIR"    # OffSec Incident Responder (NEW - Foundational)
]

# Google Gemini supported models
SUPPORTED_MODELS = {
    "flash": "gemini-1.5-flash",      # Fast, cost-effective (FREE - 15 RPM)
    "pro": "gemini-1.5-pro",          # Best quality (FREE - 2 RPM)
    "flash-8b": "gemini-1.5-flash-8b" # Ultra fast (FREE - 15 RPM)
}

# Default model selection (RECOMMENDED for speed + quality)
DEFAULT_MODEL = "gemini-1.5-flash"  # Best for technical content + speed


def get_version() -> str:
    """
    Return the current bot version.
    
    Returns:
        Version string
    """
    return __version__


def get_supported_certifications() -> list:
    """
    Return list of supported OffSec certifications.
    
    Returns:
        List of certification codes
    """
    return SUPPORTED_CERTS.copy()


def get_bot_info() -> dict:
    """
    Return comprehensive bot information.
    
    Returns:
        Dictionary with bot metadata
    """
    return {
        "name": BOT_NAME,
        "version": __version__,
        "description": BOT_DESCRIPTION,
        "supported_certifications": len(SUPPORTED_CERTS),
        "ai_provider": "Google Gemini",
        "default_model": DEFAULT_MODEL,
        "author": __author__,
        "license": __license__,
        "api_features": "2M token context, multimodal support, fast inference"
    }


def get_available_models() -> dict:
    """
    Return available AI models through Google Gemini.
    
    Returns:
        Dictionary of model shortcuts and their full IDs
    """
    return SUPPORTED_MODELS.copy()


# Initialize logging for the package
import logging

# Create package logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Log package initialization
logger.info(f"{BOT_NAME} v{__version__} package initialized")
logger.info(f"AI Provider: Google Gemini (Flash/Pro models)")
logger.info(f"Supported certifications: {', '.join(SUPPORTED_CERTS)}")
logger.info(f"Default AI model: {DEFAULT_MODEL}")


# Package-level constants
class BotConstants:
    """Constants used throughout the bot."""
    
    # Command prefix
    PREFIX = "/"
    
    # Embed colors (Discord color codes)
    COLOR_SUCCESS = 0x2ecc71    # Green
    COLOR_ERROR = 0xe74c3c      # Red
    COLOR_INFO = 0x3498db       # Blue
    COLOR_WARNING = 0xf39c12    # Orange
    COLOR_OFFSEC = 0xc0392b     # OffSec Red
    COLOR_GOLD = 0xf1c40f       # Gold (for achievements)
    
    # Assessment settings
    ASSESSMENT_TIMEOUT = 60.0   # Seconds per question
    MAX_QUESTIONS = 10          # Maximum questions per assessment
    
    # Gemini AI settings
    AI_MAX_TOKENS = 8192        # Maximum tokens per response (Gemini supports up to 8192)
    AI_TEMPERATURE = 0.7        # Response creativity (0.0-2.0 for Gemini)
    AI_TIMEOUT = 60             # API request timeout (seconds)
    AI_TOP_P = 0.95             # Nucleus sampling
    AI_TOP_K = 40               # Top-K sampling
    
    # Rate limiting (FREE tier)
    MAX_CONCURRENT_REQUESTS = 2  # Conservative for free tier
    COOLDOWN_SECONDS = 4         # Cooldown between commands (FREE: 15 RPM for Flash)
    
    # Roadmap settings
    DEFAULT_ROADMAP_WEEKS = 12   # Default study plan duration
    MIN_ROADMAP_WEEKS = 6        # Minimum weeks
    MAX_ROADMAP_WEEKS = 24       # Maximum weeks
    
    # Gemini-specific settings
    GEMINI_SAFETY_SETTINGS = {
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",  # Allow security content
        "HARM_CATEGORY_HARASSMENT": "BLOCK_ONLY_HIGH",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_ONLY_HIGH",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_ONLY_HIGH"
    }


# Export constants
__all__.append("BotConstants")


# Version check utility
def check_compatibility(python_version: tuple) -> bool:
    """
    Check if the current Python version is compatible.
    
    Args:
        python_version: Tuple of (major, minor, patch)
        
    Returns:
        True if compatible, False otherwise
    """
    required_version = (3, 10)
    current_version = python_version[:2]
    
    if current_version < required_version:
        logger.error(
            f"Python {required_version[0]}.{required_version[1]}+ required, "
            f"but running {current_version[0]}.{current_version[1]}"
        )
        return False
    
    return True


# Startup banner
def print_startup_banner():
    """Print a cool startup banner for the bot."""
    banner = f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║              🎯 TRY-HARDER-AI BOT v{__version__}        ║
║                                                          ║
║        Your Personal OffSec Certification Mentor         ║
║             Powered by Google Gemini AI 🤖               ║
║                                                          ║
║  Supported Certifications: {len(SUPPORTED_CERTS)}        ║
║  AI Model: {DEFAULT_MODEL}                               ║
║  Context Window: 1M tokens (Flash) / 2M (Pro)            ║
║  Status: Ready to Help You Try Harder! 💪                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

🔥 FREE Tier Active:
   • Gemini 1.5 Flash: 15 requests/minute
   • Gemini 1.5 Pro: 2 requests/minute
   • No credit card required!
    """
    print(banner)


# Initialize package on import
import sys

# Check Python version
if not check_compatibility(sys.version_info):
    raise RuntimeError(
        f"Try-Harder-AI requires Python 3.10 or higher. "
        f"Current version: {sys.version_info.major}.{sys.version_info.minor}"
    )

# Log successful initialization
logger.debug(f"Package initialization complete - {len(__all__)} exports available")
logger.debug(f"Gemini AI engine ready with {len(SUPPORTED_MODELS)} models")