"""
Try-Harder-AI Discord Bot - Main Entry Point
=============================================

A comprehensive Discord bot for OffSec certification guidance powered by Google Gemini AI.

Features:
- Multi-certification support (OSCP, OSEP, OSWE, OSED, OSWP, OSWA, OSMR, OSDA, KLCP, OSCC, OSIR, OSEE)
- AI-powered question answering with Google Gemini (FREE tier!)
- Skill assessments and personalized roadmaps
- Progress tracking and achievements
- Slash commands support for modern Discord UI

Author: Try-Harder-AI Team
Version: 2.0.0-gemini
License: MIT
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import bot modules
from bot.gemini_engine import GeminiAI
from bot.assessment import AssessmentManager
from bot.roadmap import RoadmapGenerator
from bot.user_manager import UserManager
from bot.commands import setup_commands

# Import config and utils
from config.logging_config import setup_logging
from utils.formatters import success_embed, error_embed, Colors


# =============================================================================
# CONFIGURATION
# =============================================================================

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
COMMAND_PREFIX = os.getenv('BOT_PREFIX', '/')
DEFAULT_MODEL = os.getenv('DEFAULT_AI_MODEL', 'gemini-1.5-flash')

# Data paths
DATA_DIR = Path(__file__).parent / 'data'
PROMPTS_DIR = Path(__file__).parent / 'prompts'

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)


# =============================================================================
# LOGGING SETUP
# =============================================================================

logger = setup_logging()


# =============================================================================
# BOT INITIALIZATION
# =============================================================================

class TryHarderAI(commands.Bot):
    """
    Try-Harder-AI Discord Bot
    
    A comprehensive bot for OffSec certification preparation with AI-powered
    guidance, assessments, and personalized study roadmaps using Google Gemini.
    """
    
    def __init__(self):
        """Initialize the bot with required intents and configuration"""
        
        # Configure intents
        intents = discord.Intents.default()
        intents.message_content = True  # Required for reading message content
        intents.members = True  # Required for member information
        intents.reactions = True  # Required for reaction-based interactions
        
        # Initialize bot
        super().__init__(
            command_prefix=COMMAND_PREFIX,
            intents=intents,
            help_command=None,  # We'll create custom help
            case_insensitive=True,
            description="Your personal OffSec certification mentor powered by Google Gemini AI"
        )
        
        # Bot metadata
        self.version = "2.0.0-gemini"
        self.author = "Try-Harder-AI Team"
        
        # Initialize components
        self.ai_engine: Optional[GeminiAI] = None
        self.assessment_manager: Optional[AssessmentManager] = None
        self.roadmap_generator: Optional[RoadmapGenerator] = None
        self.user_manager: Optional[UserManager] = None
        
        # Statistics
        self.total_commands_executed = 0
        self.total_ai_queries = 0
        self.uptime_start = None
        
        logger.info(f"🤖 Initializing Try-Harder-AI Bot v{self.version}")
    
    async def setup_hook(self):
        """
        Setup hook called during bot initialization.
        
        Initialize all bot components:
        - AI Engine (Google Gemini)
        - Assessment Manager
        - Roadmap Generator
        - User Manager
        - Slash Commands
        """
        try:
            logger.info("⚙️ Setting up bot components...")
            
            # Initialize AI Engine (Google Gemini)
            logger.info("🧠 Initializing AI Engine (Google Gemini)...")
            if not GEMINI_API_KEY:
                logger.error("❌ GEMINI_API_KEY not found in environment variables")
                raise ValueError("Missing GEMINI_API_KEY")
            
            self.ai_engine = GeminiAI(
                api_key=GEMINI_API_KEY,
                model=DEFAULT_MODEL
            )
            logger.info(f"✅ Gemini AI engine initialized with model: {DEFAULT_MODEL}")
            
            # Load questions data
            logger.info("📚 Loading assessment questions...")
            import yaml
            questions_file = DATA_DIR / 'questions.yaml'
            with open(questions_file, 'r', encoding='utf-8') as f:
                questions_data = yaml.safe_load(f)
            logger.info("✅ Questions loaded")
            
            # Initialize User Manager FIRST
            logger.info("👥 Initializing User Manager...")
            self.user_manager = UserManager()
            logger.info("✅ User Manager initialized")
            
            # Initialize Assessment Manager with user_manager reference
            logger.info("📝 Initializing Assessment Manager...")
            self.assessment_manager = AssessmentManager(questions_data=questions_data, user_manager=self.user_manager)
            logger.info("✅ Assessment Manager initialized")
            
            # Initialize Roadmap Generator
            logger.info("🗺️ Initializing Roadmap Generator...")
            self.roadmap_generator = RoadmapGenerator(ai_engine=self.ai_engine)
            logger.info("✅ Roadmap Generator initialized")
            
            # Load certifications data
            logger.info("📚 Loading certifications data...")
            cert_file = DATA_DIR / 'certifications.yaml'
            with open(cert_file, 'r', encoding='utf-8') as f:
                cert_data = yaml.safe_load(f)
            logger.info("✅ Certifications loaded")
            
            # Setup commands (MUST USE AWAIT - setup_commands is async)
            logger.info("🔧 Setting up slash commands...")
            await setup_commands(
                bot=self,
                cert_data=cert_data,
                assessment_manager=self.assessment_manager,
                roadmap_generator=self.roadmap_generator,
                gemini_engine=self.ai_engine,
                user_manager=self.user_manager
            )
            logger.info("✅ Slash commands registered")
            
            logger.info("🎉 All components initialized successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error during setup: {e}", exc_info=True)
            raise
    
    async def on_ready(self):
        """
        Event handler for when the bot is ready.
        
        Called when the bot has successfully connected to Discord.
        """
        self.uptime_start = datetime.now(timezone.utc)
        
        # Print startup banner
        print("\n" + "="*70)
        print("║" + " "*68 + "║")
        print("║" + "           🎯 TRY-HARDER-AI BOT ONLINE 🎯".center(66) + "║")
        print("║" + " "*68 + "║")
        print("="*70)
        print(f"║ Bot User:        {str(self.user).ljust(49)} ║")
        print(f"║ Bot ID:          {str(self.user.id).ljust(49)} ║")
        print(f"║ Version:         {self.version.ljust(49)} ║")
        print(f"║ Prefix:          {COMMAND_PREFIX.ljust(49)} ║")
        print(f"║ Guilds:          {str(len(self.guilds)).ljust(49)} ║")
        print(f"║ AI Provider:     Google Gemini".ljust(69) + "║")
        print(f"║ AI Model:        {DEFAULT_MODEL.ljust(49)} ║")
        print("="*70)
        print(f"║ Status:          READY ✅".ljust(68) + "║")
        print("="*70)
        print(f"║ FREE Tier:       15 requests/min (Flash)".ljust(69) + "║")
        print(f"║                  2 requests/min (Pro)".ljust(69) + "║")
        print("="*70 + "\n")
        
        logger.info(f"🚀 Bot is ready! Logged in as {self.user.name} (ID: {self.user.id})")
        logger.info(f"📊 Connected to {len(self.guilds)} guild(s)")
        logger.info(f"🤖 AI Provider: Google Gemini")
        logger.info(f"🤖 AI Model: {DEFAULT_MODEL}")
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"you Try Harder! | /help"
            ),
            status=discord.Status.online
        )
        
        logger.info("✅ Bot status set")
        
        # Sync slash commands globally
        try:
            logger.info("🔄 Syncing slash commands globally...")
            synced = await self.tree.sync()
            logger.info(f"✅ Synced {len(synced)} slash command(s)")
        except Exception as e:
            logger.error(f"❌ Failed to sync commands: {e}")
    
    async def on_guild_join(self, guild: discord.Guild):
        """
        Event handler for when the bot joins a new guild.
        
        Args:
            guild: The guild that was joined
        """
        logger.info(f"📥 Joined new guild: {guild.name} (ID: {guild.id}, Members: {guild.member_count})")
        
        # Send welcome message to the first available text channel
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = success_embed(
                    "Welcome to Try-Harder-AI! 🎯",
                    f"Thanks for adding me to **{guild.name}**!\n\n"
                    f"I'm your personal OffSec certification mentor powered by **Google Gemini AI (100% FREE!)**\n\n"
                    f"**Get Started:**\n"
                    f"• Use `/start` to begin your journey\n"
                    f"• Use `/help` to see all commands\n"
                    f"• Use `/skillcheck OSCP` to check your skills\n"
                    f"• Use `/ask` to get AI-powered answers\n\n"
                    f"**Supported Certifications:**\n"
                    f"OSCP • OSEP • OSWE • OSED • OSWP • OSWA • OSMR • OSDA • KLCP • OSCC • OSIR • OSEE\n\n"
                    f"**AI Powered by:**\n"
                    f"🤖 Google Gemini 1.5 Flash (15 req/min FREE!)\n\n"
                    f"Let's Try Harder! 💪"
                )
                embed.set_footer(text=f"Try-Harder-AI v{self.version} • Powered by Google Gemini")
                
                try:
                    await channel.send(embed=embed)
                    logger.info(f"✅ Sent welcome message to {guild.name}")
                except Exception as e:
                    logger.error(f"❌ Failed to send welcome message: {e}")
                
                break
    
    async def on_guild_remove(self, guild: discord.Guild):
        """
        Event handler for when the bot is removed from a guild.
        
        Args:
            guild: The guild that was left
        """
        logger.info(f"📤 Removed from guild: {guild.name} (ID: {guild.id})")
    
    async def on_command(self, ctx: commands.Context):
        """
        Event handler for when a command is invoked.
        
        Args:
            ctx: Command context
        """
        self.total_commands_executed += 1
        
        logger.info(
            f"📝 Command executed: {ctx.command.name} | "
            f"User: {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) | "
            f"Guild: {ctx.guild.name if ctx.guild else 'DM'}"
        )
    
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """
        Global error handler for command errors.
        
        Args:
            ctx: Command context
            error: The error that occurred
        """
        # Ignore command not found errors
        if isinstance(error, commands.CommandNotFound):
            return
        
        # Handle cooldown errors
        if isinstance(error, commands.CommandOnCooldown):
            embed = error_embed(
                "Command on Cooldown ⏰",
                f"Please wait **{error.retry_after:.1f}s** before using this command again.\n\n"
                f"💡 This helps us stay within Google Gemini's FREE tier limits (15 requests/minute)."
            )
            await ctx.send(embed=embed, delete_after=10)
            return
        
        # Handle missing permissions
        if isinstance(error, commands.MissingPermissions):
            embed = error_embed(
                "Missing Permissions 🔒",
                f"You need the following permissions: {', '.join(error.missing_permissions)}"
            )
            await ctx.send(embed=embed, delete_after=10)
            return
        
        # Handle bot missing permissions
        if isinstance(error, commands.BotMissingPermissions):
            embed = error_embed(
                "Bot Missing Permissions 🔒",
                f"I need the following permissions: {', '.join(error.missing_permissions)}"
            )
            await ctx.send(embed=embed, delete_after=10)
            return
        
        # Handle missing required argument
        if isinstance(error, commands.MissingRequiredArgument):
            embed = error_embed(
                "Missing Argument ❓",
                f"Missing required argument: `{error.param.name}`\n\n"
                f"Use `/help {ctx.command.name}` for usage information."
            )
            await ctx.send(embed=embed, delete_after=15)
            return
        
        # Handle bad argument
        if isinstance(error, commands.BadArgument):
            embed = error_embed(
                "Invalid Argument ❌",
                f"{str(error)}\n\n"
                f"Use `/help {ctx.command.name}` for usage information."
            )
            await ctx.send(embed=embed, delete_after=15)
            return
        
        # Handle generic command invoke error
        if isinstance(error, commands.CommandInvokeError):
            logger.error(f"❌ Command error in {ctx.command.name}: {error.original}", exc_info=True)
            
            embed = error_embed(
                "Command Error ⚠️",
                "An error occurred while executing the command.\n"
                "The error has been logged and will be investigated.\n\n"
                "Please try again later or contact support if the issue persists."
            )
            await ctx.send(embed=embed, delete_after=20)
            return
        
        # Log unexpected errors
        logger.error(f"❌ Unexpected command error: {type(error).__name__}: {error}", exc_info=True)
        
        embed = error_embed(
            "Unexpected Error 🐛",
            "An unexpected error occurred.\n"
            "The error has been logged for investigation.\n\n"
            "Please try again later."
        )
        await ctx.send(embed=embed, delete_after=20)
    
    async def on_error(self, event_method: str, *args, **kwargs):
        """
        Global error handler for non-command errors.
        
        Args:
            event_method: Name of the event that raised the error
        """
        logger.error(f"❌ Error in event {event_method}", exc_info=True)
    
    async def close(self):
        """
        Cleanup when bot is shutting down.
        """
        logger.info("👋 Shutting down bot...")
        
        # Close AI engine session
        if self.ai_engine:
            logger.info("🔒 Closing Gemini AI session...")
            await self.ai_engine.close()
        
        # Save any pending data
        if self.user_manager:
            logger.info("💾 Saving user data...")
            self.user_manager.save_all_users()
        
        logger.info("✅ Cleanup complete")
        
        await super().close()


# =============================================================================
# MAIN FUNCTION
# =============================================================================

def validate_configuration():
    """
    Validate required configuration before starting the bot.
    
    Raises:
        ValueError: If required configuration is missing
    """
    logger.info("🔍 Validating configuration...")
    
    if not BOT_TOKEN:
        logger.error("❌ DISCORD_BOT_TOKEN not found in environment variables")
        raise ValueError(
            "Missing DISCORD_BOT_TOKEN.\n"
            "Please set it in your .env file:\n"
            "DISCORD_BOT_TOKEN=your_token_here\n\n"
            "Get your token from: https://discord.com/developers/applications"
        )
    
    if not GEMINI_API_KEY:
        logger.error("❌ GEMINI_API_KEY not found in environment variables")
        raise ValueError(
            "Missing GEMINI_API_KEY.\n"
            "Please set it in your .env file:\n"
            "GEMINI_API_KEY=your_api_key_here\n\n"
            "Get your FREE API key from: https://aistudio.google.com/app/apikey\n"
            "No credit card required!"
        )
    
    # Validate API key format
    if not GEMINI_API_KEY.startswith('AIzaSy'):
        logger.warning("⚠️ GEMINI_API_KEY doesn't look like a valid Gemini key (should start with 'AIzaSy')")
    
    logger.info("✅ Configuration validated")


def check_data_files():
    """
    Check for required data files and log warnings if missing.
    """
    logger.info("📂 Checking data files...")
    
    required_files = [
        ('certifications.yaml', 'Certification information'),
        ('questions.yaml', 'Assessment questions'),
        ('resources.yaml', 'Learning resources'),
    ]
    
    missing_files = []
    for filename, description in required_files:
        file_path = DATA_DIR / filename
        if not file_path.exists():
            missing_files.append(f"{filename} ({description})")
            logger.warning(f"⚠️ Missing data file: {filename}")
        else:
            logger.info(f"✅ Found: {filename}")
    
    if missing_files:
        logger.warning(
            f"⚠️ Some data files are missing:\n" + 
            "\n".join([f"   - {f}" for f in missing_files]) +
            "\nThe bot may have limited functionality."
        )
    else:
        logger.info("✅ All data files present")


def check_prompt_files():
    """
    Check for required prompt files and log warnings if missing.
    """
    logger.info("📝 Checking prompt files...")
    
    required_prompts = [
        'system_prompt.txt',
        'oscp_prompt.txt',
        'osep_prompt.txt',
        'oswe_prompt.txt',
        'osed_prompt.txt',
        'oswp_prompt.txt',
        'oswa_prompt.txt',
        'osmr_prompt.txt',
        'osda_prompt.txt',
        'klcp_prompt.txt',
        'oscc_prompt.txt',
        'osir_prompt.txt',
        'osee_prompt.txt',
    ]
    
    if not PROMPTS_DIR.exists():
        logger.warning(f"⚠️ Prompts directory not found: {PROMPTS_DIR}")
        return
    
    missing_prompts = []
    for prompt_file in required_prompts:
        file_path = PROMPTS_DIR / prompt_file
        if not file_path.exists():
            missing_prompts.append(prompt_file)
            logger.warning(f"⚠️ Missing prompt file: {prompt_file}")
        else:
            logger.info(f"✅ Found: {prompt_file}")
    
    if missing_prompts:
        logger.warning(
            f"⚠️ Some prompt files are missing: {', '.join(missing_prompts)}\n"
            "Default prompts will be used for AI responses."
        )
    else:
        logger.info("✅ All prompt files present")


def print_startup_info():
    """
    Print startup information to console.
    """
    print("\n" + "="*70)
    print("║" + " "*68 + "║")
    print("║" + "🎯 TRY-HARDER-AI DISCORD BOT 🎯".center(66) + "║")
    print("║" + " "*68 + "║")
    print("║" + "Your Personal OffSec Certification Mentor".center(68) + "║")
    print("║" + "Powered by Google Gemini AI (FREE!)".center(68) + "║")
    print("║" + " "*68 + "║")
    print("="*70)
    print(f"║ Version:         2.0.0-gemini".ljust(69) + "║")
    print(f"║ Author:          Try-Harder-AI Team".ljust(69) + "║")
    print(f"║ Prefix:          {COMMAND_PREFIX} (slash commands)".ljust(69) + "║")
    print(f"║ AI Provider:     Google Gemini".ljust(69) + "║")
    print(f"║ AI Model:        {DEFAULT_MODEL}".ljust(69) + "║")
    print(f"║ FREE Tier:       15 requests/min".ljust(69) + "║")
    print("="*70)
    print("\n🚀 Starting bot...\n")


async def main():
    """
    Main entry point for the bot.
    
    Handles initialization, validation, and startup.
    """
    try:
        # Print startup info
        print_startup_info()
        
        # Validate configuration
        validate_configuration()
        
        # Check data files
        check_data_files()
        
        # Check prompt files
        check_prompt_files()
        
        # Create and start bot
        logger.info("🤖 Creating bot instance...")
        bot = TryHarderAI()
        
        logger.info("🔌 Connecting to Discord...")
        await bot.start(BOT_TOKEN)
        
    except KeyboardInterrupt:
        logger.info("⌨️ Keyboard interrupt received")
        print("\n👋 Shutting down gracefully...")
    
    except ValueError as e:
        # Configuration errors
        logger.error(f"❌ Configuration error: {e}")
        print(f"\n❌ Configuration Error:\n{e}\n")
        sys.exit(1)
    
    except FileNotFoundError as e:
        # Missing required files
        logger.error(f"❌ Required file not found: {e}")
        print(f"\n❌ Missing Required File:\n{e}\n")
        print("Please ensure all data files are present in the 'data/' directory.")
        sys.exit(1)
    
    except Exception as e:
        logger.critical(f"💥 Critical error during startup: {e}", exc_info=True)
        print(f"\n❌ Failed to start bot: {e}")
        print("\nCheck logs/bot.log for detailed error information.")
        sys.exit(1)


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    """
    Script entry point.
    
    Run the bot using asyncio.
    """
    try:
        # Check Python version
        if sys.version_info < (3, 10):
            print("❌ Python 3.10 or higher is required!")
            print(f"Current version: {sys.version_info.major}.{sys.version_info.minor}")
            sys.exit(1)
        
        # Run the bot
        asyncio.run(main())
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Stay safe and Try Harder! 💪")
    
    except Exception as e:
        logger.critical(f"💥 Fatal error: {e}", exc_info=True)
        print(f"\n💥 Fatal error: {e}")
        print("\nPlease check:")
        print("  1. Your .env file is configured correctly")
        print("  2. All required files are present")
        print("  3. You have Python 3.10+ installed")
        print("  4. All dependencies are installed (pip install -r requirements.txt)")
        print(f"\nFor help, see: SETUP.md or QUICKSTART.md")
        sys.exit(1)