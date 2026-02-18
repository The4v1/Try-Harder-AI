"""
Discord Bot Commands
====================

All Discord slash command handlers for the Try-Harder-AI bot.

Commands (using slash /):
- /start - Welcome message and bot introduction
- /certs - List all available certifications
- /skillcheck <cert> - Start skill assessment
- /roadmap - View personalized study plan
- /resources <cert> - Get certification resources
- /tips <cert> - Get exam tips and strategies
- /ask <question> - Ask any cybersecurity question
- /progress - View your progress
- /help - Show all commands
- /stats - Show bot statistics
- /cancel - Cancel current assessment
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime
import discord
from discord import app_commands
from discord.ext import commands

from .assessment import AssessmentManager, AssessmentState
from .roadmap import RoadmapGenerator
from .gemini_engine import GeminiAI
from .user_manager import UserManager

# Setup logging
logger = logging.getLogger(__name__)


class BotCommands(commands.Cog):
    """Discord bot slash command handlers."""
    
    def __init__(
        self,
        bot: commands.Bot,
        cert_data: Dict[str, Any],
        assessment_manager: AssessmentManager,
        roadmap_generator: RoadmapGenerator,
        gemini_engine: GeminiAI,
        user_manager: UserManager
    ):
        """
        Initialize command handlers.
        
        Args:
            bot: Discord bot instance
            cert_data: Certification data from YAML
            assessment_manager: Assessment manager instance
            roadmap_generator: Roadmap generator instance
            gemini_engine: Gemini AI engine instance
            user_manager: User manager instance
        """
        self.bot = bot
        self.cert_data = cert_data
        self.assessment_manager = assessment_manager
        self.roadmap_generator = roadmap_generator
        self.gemini_engine = gemini_engine
        self.user_manager = user_manager
        
        # Rate limiting tracking
        self.ask_cooldowns = {}  # {user_id: last_ask_timestamp}
        self.ask_cooldown_seconds = 5  # 5 second cooldown between /ask commands
        
        # Setup logging
        logger.info("✅ Bot commands initialized (Slash Commands)")
    
    async def cert_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        """
        Autocomplete function for certification selection.
        Returns list of certifications matching the current input.
        """
        certs = self.cert_data.get('certifications', self.cert_data)
        exact_matches = []
        prefix_matches = []
        substring_matches = []
        
        current_lower = current.lower()
        
        for cert_code, cert_info in certs.items():
            # Get cert name for display
            if isinstance(cert_info, dict):
                cert_name = cert_info.get('name', cert_code)
            else:
                cert_name = cert_code
            
            cert_code_lower = cert_code.lower()
            cert_name_lower = cert_name.lower()
            
            # Create the choice
            choice = app_commands.Choice(
                name=f"{cert_code} - {cert_name}",
                value=cert_code
            )
            
            # Prioritize exact matches first
            if cert_code_lower == current_lower or cert_name_lower == current_lower:
                exact_matches.append(choice)
            # Then prefix matches
            elif cert_code_lower.startswith(current_lower) or cert_name_lower.startswith(current_lower):
                prefix_matches.append(choice)
            # Finally substring matches
            elif current_lower in cert_code_lower or current_lower in cert_name_lower:
                substring_matches.append(choice)
        
        # Combine in priority order: exact > prefix > substring
        choices = exact_matches + prefix_matches + substring_matches
        
        # Return top 25 matches (Discord limit)
        return choices[:25]
    
    async def machines_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        """
        Autocomplete for machines command - only shows certs with practice_by_os data.
        """
        # Load resources to check which certs have machines
        import yaml
        from pathlib import Path
        
        resources_file = Path(__file__).parent.parent / 'data' / 'resources.yaml'
        certs_with_machines = []
        
        try:
            with open(resources_file, 'r', encoding='utf-8') as f:
                all_resources = yaml.safe_load(f)
            
            # Find certs that have practice_by_os or practice_platforms with practice_by_os
            for cert_key, cert_data in all_resources.items():
                if isinstance(cert_data, dict):
                    has_machines = False
                    
                    # Check direct practice_by_os
                    if 'practice_by_os' in cert_data:
                        has_machines = True
                    # Check practice_platforms for practice_by_os
                    elif 'practice_platforms' in cert_data:
                        for platform in cert_data['practice_platforms']:
                            if isinstance(platform, dict) and 'practice_by_os' in platform:
                                has_machines = True
                                break
                    
                    if has_machines:
                        # Get cert name from certifications.yaml
                        cert_name = self.cert_data.get('certifications', {}).get(cert_key, {}).get('name', cert_key)
                        certs_with_machines.append((cert_key, cert_name))
        except:
            # Fallback - return empty to avoid errors
            return []
        
        # Filter based on user input
        exact_matches = []
        prefix_matches = []
        substring_matches = []
        
        current_lower = current.lower()
        
        for cert_code, cert_name in certs_with_machines:
            cert_code_lower = cert_code.lower()
            cert_name_lower = cert_name.lower() if isinstance(cert_name, str) else cert_code.lower()
            
            choice = app_commands.Choice(
                name=f"{cert_code} - {cert_name}",
                value=cert_code
            )
            
            # Exact match
            if cert_code_lower == current_lower or cert_name_lower == current_lower:
                exact_matches.append(choice)
            # Prefix match
            elif cert_code_lower.startswith(current_lower) or cert_name_lower.startswith(current_lower):
                prefix_matches.append(choice)
            # Substring match
            elif current_lower in cert_code_lower or current_lower in cert_name_lower:
                substring_matches.append(choice)
        
        return (exact_matches + prefix_matches + substring_matches)[:25]
    
    def _create_embed(
        self,
        title: str,
        description: str,
        color: discord.Color = discord.Color.blue(),
        fields: Optional[list] = None,
        footer: Optional[str] = None
    ) -> discord.Embed:
        """
        Create a formatted Discord embed.
        
        Args:
            title: Embed title
            description: Embed description
            color: Embed color
            fields: List of field dictionaries
            footer: Footer text
            
        Returns:
            Discord Embed object
        """
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )
        
        if fields:
            for field in fields:
                embed.add_field(
                    name=field.get('name', ''),
                    value=field.get('value', ''),
                    inline=field.get('inline', False)
                )
        
        if footer:
            embed.set_footer(text=footer)
        else:
            embed.set_footer(text="Try Harder! • Powered by Google Gemini AI 🤖")
        
        return embed
    
    @app_commands.command(name='start', description='Welcome message and bot introduction')
    async def start_command(self, interaction: discord.Interaction):
        """Welcome message and introduction."""
        try:
            embed = discord.Embed(
                title="🎯 Welcome to Try-Harder-AI!",
                description=(
                    "Your personal **OffSec certification mentor** powered by Google Gemini AI.\n\n"
                    "I'll help you create a personalized study plan based on your skill level "
                    "and provide curated resources for your certification journey.\n\n"
                    "**✨ What I Can Do:**\n"
                    "→ Assess your current skill level\n"
                    "→ Generate personalized study roadmaps\n"
                    "→ Answer cybersecurity questions with emoji-rich formatting\n"
                    "→ Provide exam tips and strategies\n"
                    "→ Track your progress"
                ),
                color=discord.Color.red()
            )
            
            # Available certifications
            cert_list = "**📚 Available Certifications:**\n"
            certs = self.cert_data.get('certifications', self.cert_data)
            
            for cert_code, cert_info in certs.items():
                if isinstance(cert_info, dict):
                    name = cert_info.get('name', cert_code)
                    level = cert_info.get('level', 'Unknown')
                else:
                    name = cert_code
                    level = 'Unknown'
                cert_list += f"• **{cert_code}** - {level}\n"
            
            embed.add_field(
                name="Certifications Supported:",
                value=cert_list,
                inline=False
            )
            
            # Quick start guide
            quick_start = (
                "**🚀 Quick Start Guide:**\n"
                "1️⃣ Use `/skillcheck <cert>` to check your skill level\n"
                "2️⃣ Get your personalized roadmap with `/roadmap`\n"
                "3️⃣ Ask questions with `/ask <question>`\n"
                "4️⃣ Get exam tips with `/tips <cert>`\n\n"
                "Type `/help` to see all available commands!"
            )
            
            embed.add_field(
                name="Getting Started:",
                value=quick_start,
                inline=False
            )
            
            # Set thumbnail if bot has avatar
            if self.bot.user.avatar:
                embed.set_thumbnail(url=self.bot.user.avatar.url)
            
            embed.set_footer(text="Try Harder! 💪 • Powered by Google Gemini AI")
            
            await interaction.response.send_message(embed=embed)
            logger.info(f"✅ Start command executed by {interaction.user}")
            
        except Exception as e:
            logger.error(f"❌ Error in start command: {e}", exc_info=True)
            await interaction.response.send_message("⚠️ An error occurred. Please try again.", ephemeral=True)
    
    @app_commands.command(name='certs', description='List all available certifications')
    async def certs_command(self, interaction: discord.Interaction):
        """List all available certifications."""
        try:
            embed = discord.Embed(
                title="📚 OffSec Certifications",
                description="Here are all the certifications I can help you with:\n━━━━━━━━━━━━━━━━━━━━━━",
                color=discord.Color.blue()
            )
            
            certs = self.cert_data.get('certifications', self.cert_data)
            
            for cert_code, cert_info in certs.items():
                if isinstance(cert_info, dict):
                    name = cert_info.get('name', cert_code)
                    level = cert_info.get('level', 'Unknown')
                else:
                    name = cert_code
                    level = 'Unknown'
                
                # Emoji based on level
                level_emoji = {
                    'Beginner': '🌱',
                    'Intermediate': '⚡',
                    'Advanced': '🔥',
                    'Expert': '👑'
                }.get(level, '📘')
                
                field_value = (
                    f"{level_emoji} {level}\n"
                    f"\n"
                    f"*Use `/skillcheck {cert_code}` to begin*"
                )
                
                embed.add_field(
                    name=f"**{cert_code}** • {name}",
                    value=field_value,
                    inline=True
                )
            
            embed.set_footer(text="Try Harder! 💪 • Use /skillcheck <cert> to begin")
            
            await interaction.response.send_message(embed=embed)
            logger.info(f"✅ Certs command executed by {interaction.user}")
            
        except Exception as e:
            logger.error(f"❌ Error in certs command: {e}", exc_info=True)
            await interaction.response.send_message("⚠️ An error occurred. Please try again.", ephemeral=True)
    
    @app_commands.command(name='skillcheck', description='Check your skill level for a certification')
    @app_commands.describe(cert='Choose certification')
    @app_commands.autocomplete(cert=cert_autocomplete)
    async def skillcheck_command(self, interaction: discord.Interaction, cert: str):
        """Check your skill level for a certification."""
        try:
            # Validate certification
            cert = cert.upper()
            certs = self.cert_data.get('certifications', self.cert_data)
            
            if cert not in certs:
                await interaction.response.send_message(
                    f"❌ Certification **{cert}** not found!\n"
                    f"Use `/certs` to see available certifications.",
                    ephemeral=True
                )
                return
            
            # Check for active session
            user_id = str(interaction.user.id)
            if self.assessment_manager.has_active_session(user_id):
                await interaction.response.send_message(
                    "⚠️ You already have an active assessment!\n"
                    "Use `/cancel` to cancel it, or continue answering questions.",
                    ephemeral=True
                )
                return
            
            # Start assessment
            session = self.assessment_manager.start_assessment(user_id, cert)
            
            if not session:
                await interaction.response.send_message(
                    "⚠️ Failed to start assessment. Please try again.",
                    ephemeral=True
                )
                return
            
            # Get cert info safely
            cert_info = certs[cert]
            if isinstance(cert_info, dict):
                cert_name = cert_info.get('name', cert)
            else:
                cert_name = cert
            
            # Welcome message
            welcome_embed = discord.Embed(
                title=f"🎯 {cert} Skill Assessment",
                description=(
                    f"Let's assess your readiness for **{cert_name}**!\n\n"
                    f"📝 I'll ask you **{len(session.questions)} questions** about various topics.\n"
                    f"💡 Answer honestly to get the most accurate study plan.\n\n"
                    f"**How to answer:**\n"
                    f"→ Click the **button** for your chosen answer\n"
                    f"→ You have 60 seconds per question\n\n"
                    f"Ready? Let's begin! 🚀"
                ),
                color=discord.Color.gold()
            )
            
            welcome_embed.set_footer(text="Try Harder! 💪")
            
            await interaction.response.send_message(embed=welcome_embed)
            
            # Send first question
            await self._send_question(interaction.channel, session)
            
            logger.info(f"✅ Skill check started for {interaction.user} - {cert}")
            
        except Exception as e:
            logger.error(f"❌ Error in skillcheck command: {e}", exc_info=True)
            await interaction.response.send_message("⚠️ An error occurred. Please try again.", ephemeral=True)
    
    async def _send_question(self, channel, session):
        """Send current question to user."""
        question = session.get_current_question()
        
        if not question:
            await self._finish_assessment_channel(channel, session)
            return
        
        current, total = session.get_progress()
        
        # Create question embed
        embed = self.assessment_manager.create_question_embed(
            question, current, total, session.certification
        )
        
        # Import button view
        from bot.assessment import AssessmentButtonView
        
        try:
            # Create clickable buttons
            view = AssessmentButtonView(self.assessment_manager, session.user_id, session, bot_commands=self)
            await channel.send(embed=embed, view=view)
            logger.info(f"✅ Question sent with buttons")
        except Exception as e:
            logger.error(f"❌ Error with button view: {e}", exc_info=True)
            # Fallback: send without buttons
            await channel.send(embed=embed)
    
    async def _finish_assessment_channel(self, channel, session):
        """Complete assessment and show results."""
        user_id = session.user_id
        results = self.assessment_manager.complete_session(user_id)
        
        if not results:
            await channel.send("⚠️ Failed to complete assessment.")
            return
        
        # Save user data
        self.user_manager.save_assessment_results(user_id, results)
        
        # Create results embed
        user = await self.bot.fetch_user(int(user_id))
        embed = self.assessment_manager.create_results_embed(results, user.name)
        
        await channel.send(embed=embed)
        
        # Generate roadmap in background
        await channel.send("⏳ Generating your personalized study plan with Gemini AI... This may take a moment.")
        
        try:
            roadmap = await self.roadmap_generator.generate_roadmap(
                user_id=user_id,
                certification=results['certification'],
                assessment_results=results
            )
            
            self.user_manager.save_roadmap_for_cert(user_id, results['certification'], roadmap)
            
            # Send roadmap
            await self._send_roadmap_channel(channel, roadmap)
            
        except Exception as e:
            logger.error(f"❌ Error generating roadmap: {e}", exc_info=True)
            await channel.send(
                "⚠️ Failed to generate roadmap automatically.\n"
                "Use `/roadmap` to try again."
            )
    
    @app_commands.command(name='roadmap', description='View or generate your personalized study roadmap')
    @app_commands.describe(cert='Choose certification')
    @app_commands.autocomplete(cert=cert_autocomplete)
    async def roadmap_command(self, interaction: discord.Interaction, cert: str):
        """View or generate your personalized study roadmap."""
        try:
            await interaction.response.defer()  # This might take a while
            
            user_id = str(interaction.user.id)
            user_data = self.user_manager.get_user_data(user_id)
            certification = cert.upper()
            
            # DEBUG: Log what cert was actually received
            logger.info(f"🔍 Roadmap requested by {interaction.user} - Input cert: '{cert}' -> Processed: '{certification}'")
            
            # Validate certification
            certs = self.cert_data.get('certifications', self.cert_data)
            if certification not in certs:
                await interaction.followup.send(
                    f"❌ Certification **{certification}** not found!\n"
                    f"Use `/certs` to see available certifications.",
                    ephemeral=True
                )
                return

            # Check if user already has a saved roadmap for THIS specific certification
            saved_roadmap_content = self.user_manager.get_roadmap_for_cert(user_id, certification)
            
            if saved_roadmap_content:
                await self._send_roadmap_interaction(interaction, saved_roadmap_content)
                logger.info(f"✅ Roadmap command (saved) executed by {interaction.user} - {certification}")
                return

            # Generate NEW roadmap (Default Intermediate)
            await interaction.followup.send(
                f"⏳ Generating **{certification}** roadmap with Gemini AI... ⚡\n"
                f"💡 **Tip:** Use `/skillcheck {certification}` for a personalized roadmap based on your skill level!"
            )
            
            # Create default assessment results for intermediate level
            default_assessment = {
                'certification': certification,
                'skill_level': 'Intermediate',
                'score': 50,
                'score_percentage': 50,
                'total_questions': 10,
                'correct_answers': 5,
                'strengths': ['General knowledge'],
                'weaknesses': ['Various areas'],
                'areas_to_focus': ['General preparation'],
                'timestamp': datetime.now().isoformat()
            }
            
            roadmap = await self.roadmap_generator.generate_roadmap(
                user_id=user_id,
                certification=certification,
                assessment_results=default_assessment
            )
            
            # Save roadmap keyed by certification so each cert has its own saved roadmap
            self.user_manager.save_roadmap_for_cert(user_id, certification, roadmap)
            
            await self._send_roadmap_interaction(interaction, roadmap)
            logger.info(f"✅ Roadmap command (new) executed by {interaction.user} - {certification}")
            return
            
    
            
        except Exception as e:
            logger.error(f"❌ Error in roadmap command: {e}", exc_info=True)
            await interaction.followup.send("⚠️ An error occurred. Please try again.")
    
    async def _send_roadmap_interaction(self, interaction: discord.Interaction, roadmap: str):
        """Send roadmap in chunks via interaction."""
        chunks = self._split_text(roadmap, 4000)
        
        for i, chunk in enumerate(chunks):
            if i == 0:
                embed = discord.Embed(
                    title="🗺️ Your Personalized Study Roadmap",
                    description=chunk,
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title=f"🗺️ Roadmap (continued {i+1}/{len(chunks)})",
                    description=chunk,
                    color=discord.Color.green()
                )
            
            embed.set_footer(text="Try Harder! 💪 • Use /progress to track your journey")
            
            if i == 0:
                await interaction.followup.send(embed=embed)
            else:
                await interaction.channel.send(embed=embed)
    
    async def _send_roadmap_channel(self, channel, roadmap: str):
        """Send roadmap in chunks via channel."""
        chunks = self._split_text(roadmap, 4000)
        
        for i, chunk in enumerate(chunks):
            if i == 0:
                embed = discord.Embed(
                    title="🗺️ Your Personalized Study Roadmap",
                    description=chunk,
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title=f"🗺️ Roadmap (continued {i+1}/{len(chunks)})",
                    description=chunk,
                    color=discord.Color.green()
                )
            
            embed.set_footer(text="Try Harder! 💪 • Use /progress to track your journey")
            
            await channel.send(embed=embed)
    
    @app_commands.command(name='ask', description='Ask any cybersecurity question')
    @app_commands.describe(question='Your cybersecurity question')
    async def ask_command(self, interaction: discord.Interaction, question: str):
        """Ask any cybersecurity question with emoji-rich formatting."""
        try:
            # Rate limiting check
            import time
            user_id = str(interaction.user.id)
            current_time = time.time()
            
            if user_id in self.ask_cooldowns:
                time_since_last = current_time - self.ask_cooldowns[user_id]
                if time_since_last < self.ask_cooldown_seconds:
                    remaining = int(self.ask_cooldown_seconds - time_since_last)
                    await interaction.response.send_message(
                        f"⏳ Please wait **{remaining} seconds** before asking another question.\n"
                        f"This cooldown prevents API rate limit issues.",
                        ephemeral=True
                    )
                    return
            
            # Update cooldown timestamp
            self.ask_cooldowns[user_id] = current_time
            
            await interaction.response.defer()  # AI might take time
            
            # Call Gemini AI with special emoji-rich formatting
            response = await self.gemini_engine.ask(question, use_emoji_format=True)
            
            # Split if too long
            chunks = self._split_text(response, 1900)
            
            for i, chunk in enumerate(chunks):
                if i == 0:
                    # First chunk with question as title
                    embed = discord.Embed(
                        title=f"💡 {question[:100]}{'...' if len(question) > 100 else ''}",
                        description=chunk,
                        color=discord.Color.blue()
                    )
                else:
                    # Continuation chunks
                    embed = discord.Embed(
                        description=chunk,
                        color=discord.Color.blue()
                    )
                
                embed.set_footer(text="Powered by Google Gemini AI 🤖")
                
                if i == 0:
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.channel.send(embed=embed)
            
            logger.info(f"✅ Ask command executed by {interaction.user}: {question[:50]}")
            
        except Exception as e:
            logger.error(f"❌ Error in ask command: {e}", exc_info=True)
            await interaction.followup.send("⚠️ An error occurred while processing your question. Please try again.")
    
    @app_commands.command(name='resources', description='Get certification resources')
    @app_commands.describe(cert='Choose certification')
    @app_commands.autocomplete(cert=cert_autocomplete)
    async def resources_command(self, interaction: discord.Interaction, cert: str):
        """Get certification resources."""
        try:
            cert = cert.upper()
            
            # Load resources from resources.yaml directly
            import yaml
            from pathlib import Path
            
            resources_file = Path(__file__).parent.parent / 'data' / 'resources.yaml'
            with open(resources_file, 'r', encoding='utf-8') as f:
                all_resources = yaml.safe_load(f)
            
            if cert not in all_resources:
                await interaction.response.send_message(
                    f"❌ Resources for **{cert}** not found!\n"
                    f"Try: `/resources OSCP`, `/resources OSWE`, or `/resources OSEP`\n"
                    f"Use `/certs` to see all certifications.",
                    ephemeral=True
                )
                return
            
            cert_resources = all_resources[cert]
            await interaction.response.defer()  # Resources may take time to format
            
            # 1. GitHub Resources Section
            github_resources = cert_resources.get('github_resources', [])
            if github_resources:
                desc = f"**🔧 Top GitHub tools for {cert}:**\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
                for i, repo in enumerate(github_resources[:20], 1):  # Show top 20
                    name = repo.get('name', 'Unknown')
                    url = repo.get('url', '')
                    description = repo.get('description', '')
                    stars = repo.get('stars', '')
                    
                    desc += f"**{i}. {name}** "
                    if stars:
                        desc += f"⭐ {stars}"
                    desc += f"\n   {description}\n"
                    if url:
                        desc += f"   🔗 {url}\n"
                    desc += "\n"
                
                if len(github_resources) > 20:
                    desc += f"_...and {len(github_resources) - 20} more_\n"
                
                embed = discord.Embed(
                    title=f"🔧 {cert} - GitHub Resources",
                    description=desc,
                    color=discord.Color.purple()
                )
                embed.set_footer(text=f"Install these tools for {cert} practice")
                await interaction.followup.send(embed=embed)
            
            # 2. Free Practice Platforms
            free_platforms = cert_resources.get('free_platforms', [])
            if free_platforms:
                desc = f"**🎮 Free practice platforms:**\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
                for i, platform in enumerate(free_platforms[:7], 1):  # Show 7
                    name = platform.get('name', 'Unknown')
                    url = platform.get('url', '')
                    cost = platform.get('cost', 'Free')
                    description = platform.get('description', '')
                    
                    desc += f"**{i}. {name}**\n"
                    desc += f"   💰 {cost}\n"
                    desc += f"   📝 {description}\n"
                    if url:
                        desc += f"   🔗 {url}\n"
                    desc += "\n"
                
                embed = discord.Embed(
                    title=f"🎮 {cert} - Free Platforms",
                    description=desc,
                    color=discord.Color.green()
                )
                embed.set_footer(text=f"Start practicing {cert} for free!")
                await interaction.followup.send(embed=embed)
            
            # 3. Practice Platforms (existing HTB, THM, etc.)
            practice_platforms = cert_resources.get('practice_platforms', [])
            if practice_platforms:
                desc = f"**🏆 Recommended practice platforms:**\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
                for platform in practice_platforms[:5]:
                    name = platform.get('name', 'Unknown')
                    # Skip TJNull here as it has its own dedicated section
                    if "TJNull" in name:
                        continue
                        
                    url = platform.get('url', '')
                    cost = platform.get('cost', 'Unknown')
                    description = platform.get('description', '')
                    
                    desc += f"**• {name}**\n"
                    desc += f"  💰 {cost}\n"
                    desc += f"  📝 {description}\n"
                    if url:
                        desc += f"  🔗 {url}\n"
                    desc += "\n"
                
                embed = discord.Embed(
                    title=f"🏆 {cert} - Practice Platforms",
                    description=desc,
                    color=discord.Color.blue()
                )
                await interaction.followup.send(embed=embed)
            
            # 3.5 Generic Practice Machines (Handles TJNull, OSEP, OSWE, etc.)
            machine_lists = []
            
            # Source 1: Root level practice_by_os
            if 'practice_by_os' in cert_resources:
                machine_lists.append({
                    "name": f"{cert} Recommended Machines", 
                    "data": cert_resources['practice_by_os']
                })
            
            # Source 2: Platform level practice_by_os
            for platform in practice_platforms:
                if 'practice_by_os' in platform:
                    list_name = platform.get('name', 'Practice List')
                    # If it's TJNull, we keep the special name
                    if "TJNull" in list_name:
                        list_name = f"TJNull's List"
                    
                    machine_lists.append({
                        "name": list_name,
                        "data": platform['practice_by_os']
                    })
            
            # Display all found machine lists
            for m_list in machine_lists:
                list_name = m_list['name']
                os_data = m_list['data']
                
                # Iterate through all categories (linux, windows, redteam, web, binary...)
                for category, levels in os_data.items():
                    if not levels: continue
                    
                    # Formatting matching the category
                    cat_icon = "🐧" if category == "linux" else \
                               "🪟" if category == "windows" else \
                               "🏢" if category == "active_directory" else \
                               "🌐" if category == "web" else \
                               "🔴" if category == "redteam" else \
                               "👾" if category == "binary" else "💻"
                               
                    cat_title = category.replace('_', ' ').title()
                    if category == "active_directory": cat_title = "Active Directory"
                    
                    desc = f"**🎯 {cert} - {list_name} ({cat_title}):**\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    desc += f"**{cat_icon} {cat_title} Machines:**\n"
                    
                    has_machines = False
                    
                    # Determine default platform based on list_name
                    default_platform_url = "https://app.hackthebox.com/machines"
                    if "Proving Grounds" in list_name or "OffSec" in list_name:
                        default_platform_url = "https://portal.offsec.com/labs/practice"
                    elif "TryHackMe" in list_name:
                        default_platform_url = "https://tryhackme.com/room"
                    
                    # Handle both dict (levels) and potential list (direct machines)
                    if isinstance(levels, dict):
                        for difficulty in ['easy', 'medium', 'hard', 'insane']:
                            machines = levels.get(difficulty, [])
                            if machines:
                                has_machines = True
                                desc += f"\n_{difficulty.capitalize()}:_ "
                                machine_links = []
                                for machine_entry in machines:
                                    # Parse machine entries that may contain:
                                    # - Simple names: "Poison"
                                    # - Prefixed lists: "HTB: Poison, Help, Networked"
                                    # - Already formatted links: "[Poison](url)"
                                    
                                    if "[" in machine_entry and "]" in machine_entry:
                                        # Already has markdown link format
                                        machine_links.append(machine_entry)
                                    elif ":" in machine_entry:
                                        # Format like "HTB: Poison, Help, Networked"
                                        parts = machine_entry.split(":", 1)
                                        platform = parts[0].strip()
                                        machines_str = parts[1].strip()
                                        
                                        # Split by comma and create individual links
                                        individual_machines = [m.strip() for m in machines_str.split(",")]
                                        
                                        for machine_name in individual_machines:
                                            # Determine URL based on platform
                                            if "HTB" in platform or "HackTheBox" in platform:
                                                url = f"https://app.hackthebox.com/machines/{machine_name}"
                                            elif "PG" in platform or "Proving Grounds" in platform:
                                                url = "https://portal.offsec.com/labs/practice"
                                            elif "THM" in platform or "TryHackMe" in platform:
                                                url = f"https://tryhackme.com/room/{machine_name.lower().replace(' ', '')}"
                                            elif "PortSwigger" in platform:
                                                url = "https://portswigger.net/web-security"
                                            else:
                                                url = f"https://app.hackthebox.com/machines/{machine_name}"
                                            
                                            machine_links.append(f"[{machine_name}]({url})")
                                    else:
                                        # Simple machine name - use platform from list_name
                                        if "Proving Grounds" in list_name or "OffSec" in list_name:
                                            url = "https://portal.offsec.com/labs/practice"
                                        elif "TryHackMe" in list_name:
                                            url = f"https://tryhackme.com/room/{machine_entry.lower().replace(' ', '')}"
                                        else:
                                            # Default to HTB
                                            url = f"https://app.hackthebox.com/machines/{machine_entry}"
                                        machine_links.append(f"[{machine_entry}]({url})")
                                
                                desc += ", ".join(machine_links)
                                desc += "\n"
                    elif isinstance(levels, list):
                        # Direct list of machines under category
                        has_machines = True
                        machine_links = []
                        for machine_entry in levels:
                            if "[" in machine_entry and "]" in machine_entry:
                                machine_links.append(machine_entry)
                            elif ":" in machine_entry:
                                # Format like "HTB: Poison, Help, Networked"
                                parts = machine_entry.split(":", 1)
                                platform = parts[0].strip()
                                machines_str = parts[1].strip()
                                
                                # Split by comma and create individual links
                                individual_machines = [m.strip() for m in machines_str.split(",")]
                                
                                for machine_name in individual_machines:
                                    # Determine URL based on platform
                                    if "HTB" in platform or "HackTheBox" in platform:
                                        url = f"https://app.hackthebox.com/machines/{machine_name}"
                                    elif "PG" in platform or "Proving Grounds" in platform:
                                        url = "https://portal.offsec.com/labs/practice"
                                    elif "THM" in platform or "TryHackMe" in platform:
                                        url = f"https://tryhackme.com/room/{machine_name.lower().replace(' ', '')}"
                                    elif "PortSwigger" in platform:
                                        url = "https://portswigger.net/web-security"
                                    else:
                                        url = f"https://app.hackthebox.com/machines/{machine_name}"
                                    
                                    machine_links.append(f"[{machine_name}]({url})")
                            else:
                                # Simple machine name - use platform from list_name
                                if "Proving Grounds" in list_name or "OffSec" in list_name:
                                    url = "https://portal.offsec.com/labs/practice"
                                elif "TryHackMe" in list_name:
                                    url = f"https://tryhackme.com/room/{machine_entry.lower().replace(' ', '')}"
                                else:
                                    # Default to HTB
                                    url = f"https://app.hackthebox.com/machines/{machine_entry}"
                                machine_links.append(f"[{machine_entry}]({url})")
                        desc += ", ".join(machine_links)
                        desc += "\n"

                    if has_machines:
                        embed = discord.Embed(
                            description=desc,
                            color=discord.Color.gold()
                        )
                        await interaction.followup.send(embed=embed)

            # 3.7 Tools Section (NEW)
            tools_list = cert_resources.get('tools', [])
            if tools_list:
                desc = f"**🧰 Essential Tools for {cert}:**\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
                
                # Handle dictionary of categories (e.g. OSCP) or list (e.g. OSEP)
                if isinstance(tools_list, dict):
                    for category, tools in tools_list.items():
                        desc += f"**{category.title()}:**\n"
                        for tool in tools:
                             desc += f"• {tool}\n"
                        desc += "\n"
                elif isinstance(tools_list, list):
                    for tool in tools_list[:15]: # Limit to 15 tools
                        if isinstance(tool, dict):
                            name = tool.get('name', 'Unknown')
                            t_desc = tool.get('description', '')
                            url = tool.get('url', '')
                            desc += f"**• {name}**"
                            if url: desc += f" ([Link]({url}))"
                            if t_desc: desc += f"\n  {t_desc}"
                            desc += "\n\n"
                        else:
                            desc += f"• {tool}\n"
                
                embed = discord.Embed(
                    title=f"🧰 {cert} - Arsenal",
                    description=desc,
                    color=discord.Color.teal()
                )
                await interaction.followup.send(embed=embed)
            
            
            # 4. Cheatsheets
            cheatsheets = cert_resources.get('cheatsheets', [])
            if cheatsheets:
                desc = "**📚 Essential cheatsheets:**\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
                for sheet in cheatsheets[:6]:
                    name = sheet.get('name', 'Unknown')
                    url = sheet.get('url', '')
                    description = sheet.get('description', '')
                    
                    desc += f"**• {name}**\n"
                    desc += f"  📝 {description}\n"
                    if url:
                        desc += f"  🔗 {url}\n"
                    desc += "\n"
                
                embed = discord.Embed(
                    title=f"📚 {cert} - Cheatsheets",
                    description=desc,
                    color=discord.Color.orange()
                )
                await interaction.followup.send(embed=embed)
            
            # If no resources found at all
            # Check for any type of resource content
            has_any_resources = any([
                cert_resources.get('github_resources'),
                cert_resources.get('free_platforms'),
                cert_resources.get('practice_platforms'),
                cert_resources.get('cheatsheets'),
                cert_resources.get('tools'),
                cert_resources.get('books'),
                cert_resources.get('videos'),
                cert_resources.get('writeups'),
                cert_resources.get('courses'),
                cert_resources.get('communities'),
                cert_resources.get('official'),
                cert_resources.get('practice_by_os')
            ])
            
            if not has_any_resources:
                await interaction.followup.send(
                    f"⚠️ Resources for {cert} are coming soon!\n"
                    f"Meanwhile, try `/resources OSCP`, `/resources OSWE`, or `/resources OSEP`",
                    ephemeral=True
                )
            
            logger.info(f"✅ Resources command executed by {interaction.user} - {cert}")
            
        except FileNotFoundError:
            logger.error(f"❌ resources.yaml file not found")
            await interaction.response.send_message(
                "⚠️ Resources data file not found. Please contact administrator.",
                ephemeral=True
            )
        except Exception as e:
            logger.error(f"❌ Error in resources command: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "⚠️ An error occurred while loading resources. Please try again.",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    "⚠️ An error occurred. Please try again.",
                    ephemeral=True
                )
    
    @app_commands.command(name='machines', description='Get practice machine recommendations')
    @app_commands.describe(
        cert='Choose certification',
        difficulty='Difficulty level (easy, medium, hard) - optional',
        os_type='Operating system (linux, windows, ad) - optional'
    )
    @app_commands.autocomplete(cert=machines_autocomplete)
    async def machines_command(
        self, 
        interaction: discord.Interaction, 
        cert: str,
        difficulty: str = None,
        os_type: str = None
    ):
        """Get practice machine recommendations by difficulty and OS."""
        try:
            cert = cert.upper()
            
            # Load resources dynamically
            import yaml
            from pathlib import Path
            
            resources_file = Path(__file__).parent.parent / 'data' / 'resources.yaml'
            machines_db = {}
            
            try:
                with open(resources_file, 'r', encoding='utf-8') as f:
                    all_resources = yaml.safe_load(f)
                    
                # Extract practice_by_os and TRANSFORM to [Level][OS] -> List
                for cert_key, cert_data in all_resources.items():
                    raw_os_data = {}
                    
                    if isinstance(cert_data, dict):
                        # direct practice_by_os
                        if 'practice_by_os' in cert_data:
                            raw_os_data = cert_data['practice_by_os']
                        
                        # check inside practice_platforms (legacy TJNull structure support)
                        elif 'practice_platforms' in cert_data: # Use elif to prioritize direct
                            for platform in cert_data['practice_platforms']:
                                if isinstance(platform, dict) and 'practice_by_os' in platform:
                                    raw_os_data = platform['practice_by_os']
                                    break
                    
                    if raw_os_data:
                        # 1. Transform: {os: {level: [machines]}} -> {level: {os: [machines]}}
                        transformed = {}
                        for os_name, levels in raw_os_data.items():
                            if isinstance(levels, dict):
                                for level, machines in levels.items():
                                    if level not in transformed:
                                        transformed[level] = {}
                                    
                                    # Ensure list exists
                                    if os_name not in transformed[level]:
                                        transformed[level][os_name] = []
                                        
                                    # Add machines (no prefix for main list)
                                    transformed[level][os_name].extend(machines)
                        
                        # Initialize or update machines_db for this cert
                        if cert_key.upper() not in machines_db:
                            machines_db[cert_key.upper()] = transformed
                        else:
                            # Merge into existing
                            for level, os_dict in transformed.items():
                                if level not in machines_db[cert_key.upper()]:
                                    machines_db[cert_key.upper()][level] = {}
                                for os_name, m_list in os_dict.items():
                                    if os_name not in machines_db[cert_key.upper()][level]:
                                        machines_db[cert_key.upper()][level][os_name] = []
                                    machines_db[cert_key.upper()][level][os_name].extend(m_list)

                    # 2. Check other platforms for MORE lists (Proving Grounds, etc.)
                    if 'practice_platforms' in cert_data:
                         for platform in cert_data['practice_platforms']:
                            if isinstance(platform, dict) and 'practice_by_os' in platform:
                                p_data = platform['practice_by_os']
                                p_name = platform.get('name', 'Other')
                                prefix = ""
                                if "Proving Grounds" in p_name: prefix = "PG: "
                                elif "HackTheBox" in p_name: prefix = "HTB: " # Only if explicit
                                
                                # Transform and Merge
                                for os_name, levels in p_data.items():
                                    if isinstance(levels, dict):
                                        for level, machines in levels.items():
                                            if level not in machines_db.get(cert_key.upper(), {}):
                                                 if cert_key.upper() not in machines_db: machines_db[cert_key.upper()] = {}
                                                 machines_db[cert_key.upper()][level] = {}
                                            
                                            if os_name not in machines_db[cert_key.upper()][level]:
                                                machines_db[cert_key.upper()][level][os_name] = []
                                            
                                            # Add with prefix
                                            for m in machines:
                                                machines_db[cert_key.upper()][level][os_name].append(f"{prefix}{m}")
            except Exception as e:
                logger.error(f"❌ Error loading dynamic machine data: {e}")
                # Fallback to empty if load fails
                machines_db = {}
            
            # Check if cert has machine data
            if cert not in machines_db:
                await interaction.response.send_message(
                    f"⚠️ Machine recommendations for **{cert}** coming soon!\n"
                    f"Try: `/machines OSCP`, `/machines OSWE`, or `/machines OSEP`",
                    ephemeral=True
                )
                return
            
            cert_machines = machines_db[cert]
            
            # Build description based on filters
            if difficulty and os_type:
                # Specific filter
                difficulty = difficulty.lower()
                os_type = os_type.lower()
                
                if difficulty not in cert_machines:
                    await interaction.response.send_message(
                        f"❌ Difficulty **{difficulty}** not found!\n"
                        f"Available: {', '.join(cert_machines.keys())}",
                        ephemeral=True
                    )
                    return
                
                if os_type not in cert_machines[difficulty]:
                    await interaction.response.send_message(
                        f"❌ OS type **{os_type}** not found for {difficulty}!\n"
                        f"Available: {', '.join(cert_machines[difficulty].keys())}",
                        ephemeral=True
                    )
                    return
                
                # Show specific filtered machines
                machines = cert_machines[difficulty][os_type]
                desc = f"**🗺️ Practice machine roadmap for {cert}:**\n" \
                       f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                
                desc += f"> **📊 {difficulty.upper()} Difficulty - {os_type.title()}**\n\n"
                for item in machines:
                    desc += f"• {item}\n"
                
                # TRUNCATION CHECK
                MAX_DESC_LENGTH = 3800  # Discord limit is 4096, leave buffer
                if len(desc) > MAX_DESC_LENGTH:
                    desc = desc[:MAX_DESC_LENGTH]
                    last_newline = desc.rfind('\n')
                    if last_newline > 0:
                        desc = desc[:last_newline]
                    desc += f"\n\n⚠️ **List truncated!** Use more specific filters.\n"
                
                embed = discord.Embed(
                    title=f"🎮 {cert} Machine Recommendations",
                    description=desc,
                    color=discord.Color.blue()
                )
                embed.set_footer(text=f"Use /resources {cert} for more practice platforms")
                await interaction.response.send_message(embed=embed)
                
            else:
                # Show all machines for the cert
                desc = f"**🗺️ Practice machine roadmap for {cert}:**\n" \
                       f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                
                for diff_level in ['easy', 'medium', 'hard']:
                    if diff_level in cert_machines:
                        # Difficulty Header with blockquote
                        desc += f"> **📊 {diff_level.upper()} Difficulty:**\n\n"
                        
                        for os_t, machines in cert_machines[diff_level].items():
                            icon = "🐧" if os_t == "linux" else "🪟" if os_t == "windows" else "🖥️" if os_t == "ad" else "🌐"
                            
                            desc += f"**{icon} {os_t.title()}:**\n"
                            
                            # Limit machines per category to avoid overflow
                            machine_count = 0
                            MAX_MACHINES_PER_CATEGORY = 25
                            
                            for item in machines:
                                if machine_count >= MAX_MACHINES_PER_CATEGORY:
                                    remaining = len(machines) - machine_count
                                    desc += f"• ... and {remaining} more (use filters)\n"
                                    break
                                    
                                # Parse each machine entry - keep it simple
                                if isinstance(item, str):
                                    desc += f"• {item}\n"
                                else:
                                    desc += f"• {item}\n"
                                
                                machine_count += 1
                            
                            desc += "\n" # Extra space between OS categories
                        
                        desc += "━━━━━━━━━━━━━━━━━━━━━━\n\n" # Separator
                
                desc += f"\n**💡 Filter your search:**\n" \
                        f"• `/machines {cert} easy linux` - Easy Linux boxes\n" \
                        f"• `/machines {cert} medium ad` - Medium AD labs\n" \
                        f"• `/machines {cert} hard windows` - Hard Windows boxes"
                
                # FINAL TRUNCATION CHECK - ensure we never exceed limit
                MAX_DESC_LENGTH = 3800  # Discord limit is 4096, leave safe buffer
                if len(desc) > MAX_DESC_LENGTH:
                    # Truncate and add warning
                    desc = desc[:MAX_DESC_LENGTH]
                    # Find last complete line to avoid cutting mid-line
                    last_newline = desc.rfind('\n')
                    if last_newline > 0:
                        desc = desc[:last_newline]
                    desc += f"\n\n⚠️ **Output truncated** - Too many machines!\n" \
                            f"**Use filters:** `/machines {cert} easy linux`"
                
                embed = discord.Embed(
                    title=f"🎮 {cert} - All Machine Recommendations",
                    description=desc,
                    color=discord.Color.gold()
                )
                embed.set_footer(text=f"Follow this progression for optimal learning | Based on TJNull's list")
                await interaction.response.send_message(embed=embed)
            
            logger.info(f"✅ Machines command executed by {interaction.user} - {cert} {difficulty or 'all'} {os_type or 'all'}")
            
        except Exception as e:
            logger.error(f"❌ Error in machines command: {e}", exc_info=True)
            await interaction.response.send_message(
                "⚠️ An error occurred while loading machine recommendations. Please try again.",
                ephemeral=True
            )
    
    @app_commands.command(name='tips', description='Get exam tips and strategies')
    @app_commands.describe(cert='Choose certification')
    @app_commands.autocomplete(cert=cert_autocomplete)
    async def tips_command(self, interaction: discord.Interaction, cert: str):
        """Get exam tips and strategies."""
        try:
            cert = cert.upper()
            certs = self.cert_data.get('certifications', self.cert_data)
            
            if cert not in certs:
                await interaction.response.send_message(
                    f"❌ Certification **{cert}** not found!\n"
                    f"Use `/certs` to see available certifications.",
                    ephemeral=True
                )
                return
            
            await interaction.response.defer()
            await interaction.followup.send(f"⏳ Generating exam tips for **{cert}** with Gemini AI... ⚡")
            
            cert_info = certs[cert]
            if not isinstance(cert_info, dict):
                cert_info = {}
            
            tips = await self.gemini_engine.get_exam_tips(cert, cert_info)
            
            # Split tips if too long
            chunks = self._split_text(tips, 4000)
            
            for i, chunk in enumerate(chunks):
                if i == 0:
                    embed = discord.Embed(
                        title=f"💡 {cert} - Exam Tips & Strategies",
                        description=chunk,
                        color=discord.Color.gold()
                    )
                else:
                    embed = discord.Embed(
                        title=f"💡 {cert} - Tips (continued {i+1}/{len(chunks)})",
                        description=chunk,
                        color=discord.Color.gold()
                    )
                
                embed.set_footer(text="Try Harder! 💪 • Good luck on your exam!")
                if i == 0:
                    await interaction.followup.send(embed=embed)
                else:
                    await interaction.channel.send(embed=embed)
            
            logger.info(f"✅ Tips command executed by {interaction.user} - {cert}")
            
        except Exception as e:
            logger.error(f"❌ Error in tips command: {e}", exc_info=True)
            await interaction.followup.send("⚠️ An error occurred. Please try again.")
    
    @app_commands.command(name='progress', description='View your progress dashboard')
    async def progress_command(self, interaction: discord.Interaction):
        """View your progress."""
        try:
            user_id = str(interaction.user.id)
            user_data = self.user_manager.get_user_data(user_id)
            
            if not user_data:
                await interaction.response.send_message(
                    "❌ No progress found!\n"
                    "Use `/skillcheck <cert>` to get started.",
                    ephemeral=True
                )
                return
            
            assessment = user_data.get('assessment_results', {})
            progress_data = user_data.get('progress', {})
            
            cert = assessment.get('certification', 'N/A')
            score = assessment.get('score_percentage', 0)
            skill_level = assessment.get('skill_level', 'Unknown')
            
            embed = discord.Embed(
                title="📊 Your Progress Dashboard",
                description=f"Here's your current progress, **{interaction.user.name}**!",
                color=discord.Color.blue()
            )
            
            # Certification info
            embed.add_field(
                name="🎯 Target Certification",
                value=f"**{cert}**",
                inline=True
            )
            
            embed.add_field(
                name="📈 Skill Level",
                value=f"**{skill_level}**",
                inline=True
            )
            
            embed.add_field(
                name="💯 Assessment Score",
                value=f"**{score}%**",
                inline=True
            )
            
            # Strengths and weaknesses
            strengths = assessment.get('strengths', [])
            if strengths:
                embed.add_field(
                    name="💪 Your Strengths",
                    value="\n".join(f"✅ {s}" for s in strengths[:5]),
                    inline=True
                )
            
            weaknesses = assessment.get('weaknesses', [])
            if weaknesses:
                embed.add_field(
                    name="📚 Focus Areas",
                    value="\n".join(f"📖 {w}" for w in weaknesses[:5]),
                    inline=True
                )
            
            # Next steps
            next_steps = (
                "**🚀 Next Steps:**\n"
                "→ Use `/roadmap` to view your study plan\n"
                "→ Use `/resources` for learning materials\n"
                "→ Use `/tips` for exam strategies"
            )
            
            embed.add_field(
                name="What's Next?",
                value=next_steps,
                inline=False
            )
            
            embed.set_footer(text="Keep going! You've got this! 💪")
            
            await interaction.response.send_message(embed=embed)
            
            logger.info(f"✅ Progress command executed by {interaction.user}")
            
        except Exception as e:
            logger.error(f"❌ Error in progress command: {e}", exc_info=True)
            await interaction.response.send_message("⚠️ An error occurred. Please try again.", ephemeral=True)
    
    @app_commands.command(name='cancel', description='Cancel your current assessment')
    async def cancel_command(self, interaction: discord.Interaction):
        """Cancel current assessment."""
        try:
            user_id = str(interaction.user.id)
            
            if not self.assessment_manager.has_active_session(user_id):
                await interaction.response.send_message(
                    "❌ You don't have an active assessment to cancel.",
                    ephemeral=True
                )
                return
            
            self.assessment_manager.abandon_session(user_id)
            
            embed = discord.Embed(
                title="✅ Assessment Cancelled",
                description=(
                    "Your current assessment has been cancelled.\n\n"
                    "Use `/skillcheck` to start a new assessment when you're ready!"
                ),
                color=discord.Color.orange()
            )
            
            await interaction.response.send_message(embed=embed)
            
            logger.info(f"✅ Assessment cancelled by {interaction.user}")
            
        except Exception as e:
            logger.error(f"❌ Error in cancel command: {e}", exc_info=True)
            await interaction.response.send_message("⚠️ An error occurred. Please try again.", ephemeral=True)
    
    @app_commands.command(name='stats', description='Show bot statistics')
    async def stats_command(self, interaction: discord.Interaction):
        """Show bot statistics."""
        try:
            stats = self.assessment_manager.get_statistics()
            
            embed = discord.Embed(
                title="📊 Bot Statistics",
                description="Here are the current bot statistics:\n━━━━━━━━━━━━━━━━━━━━━━",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="✅ Assessments Completed",
                value=f"**{stats['total_completed']}**",
                inline=True
            )
            
            embed.add_field(
                name="⏳ Active Sessions",
                value=f"**{stats['active_sessions']}**",
                inline=True
            )
            
            embed.add_field(
                name="📈 Average Score",
                value=f"**{stats['average_score']}%**",
                inline=True
            )
            
            distribution = stats.get('skill_distribution', {})
            if distribution:
                dist_text = ""
                emoji_map = {
                    'Beginner': '🌱',
                    'Intermediate': '⚡',
                    'Advanced': '🔥',
                    'Expert': '👑'
                }
                
                for level, count in distribution.items():
                    emoji = emoji_map.get(level, '📊')
                    dist_text += f"{emoji} **{level}:** {count}\n"
                
                embed.add_field(
                    name="🎯 Skill Level Distribution",
                    value=dist_text,
                    inline=False
                )
            
            # Gemini AI Model info
            model_info = self.gemini_engine.get_model_info()
            embed.add_field(
                name="🤖 AI Model",
                value=f"**{model_info['provider']}**\n{model_info['model']}",
                inline=True
            )
            
            embed.set_footer(text="Try Harder! 💪 • Join the journey!")
            
            await interaction.response.send_message(embed=embed)
            
            logger.info(f"✅ Stats command executed by {interaction.user}")
            
        except Exception as e:
            logger.error(f"❌ Error in stats command: {e}", exc_info=True)
            await interaction.response.send_message("⚠️ An error occurred. Please try again.", ephemeral=True)
    
    @app_commands.command(name='help', description='Show all available commands')
    async def help_command(self, interaction: discord.Interaction):
        """Show all available commands."""
        try:
            # Defer response to avoid timeout
            await interaction.response.defer()
            embed = discord.Embed(
                title="❓ Try-Harder-AI Commands",
                description="Here are all available slash commands:\n━━━━━━━━━━━━━━━━━━━━━━",
                color=discord.Color.blue()
            )
            
            commands_list = [
                ("/start", "🎯 Welcome message and introduction"),
                ("/certs", "📚 List all available certifications"),
                ("/skillcheck <cert>", "📝 Check your skill level (e.g., `/skillcheck OSCP`)"),
                ("/roadmap", "🗺️ View your personalized study plan"),
                ("/ask <question>", "💡 Ask any cybersecurity question with emoji-rich answers"),
                ("/resources <cert>", "📖 Get certification resources"),
                ("/machines <cert> [difficulty] [os]", "🎮 Get practice machine recommendations (e.g., `/machines OSCP easy linux`)"),
                ("/tips <cert>", "⚡ Get exam tips and strategies"),
                ("/progress", "📊 View your current progress"),
                ("/cancel", "❌ Cancel current assessment"),
                ("/stats", "📈 Show bot statistics"),
                ("/help", "❓ Show this help message")
            ]
            
            for cmd, desc in commands_list:
                embed.add_field(
                    name=f"`{cmd}`",
                    value=desc,
                    inline=False
                )
            
            quick_start = (
                "**💡 Quick Start:**\n"
                "1️⃣ Use `/skillcheck OSCP` to start\n"
                "2️⃣ Answer the questions honestly\n"
                "3️⃣ Get your personalized roadmap!\n"
                "4️⃣ Ask questions with `/ask`\n\n"
                "**Need help?** Just ask in the server! 🚀"
            )
            
            embed.add_field(
                name="Getting Started:",
                value=quick_start,
                inline=False
            )
            
            embed.set_footer(text="Try Harder! 💪 • Powered by Google Gemini AI")
            
            await interaction.followup.send(embed=embed)
            
            logger.info(f"✅ Help command executed by {interaction.user}")
            
        except Exception as e:
            logger.error(f"❌ Error in help command: {e}", exc_info=True)
            await interaction.followup.send("⚠️ An error occurred. Please try again.", ephemeral=True)
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Listen for assessment answers."""
        # Ignore bot messages
        if message.author.bot:
            return
        
        # Check if user has active assessment
        user_id = str(message.author.id)
        session = self.assessment_manager.get_session(user_id)
        
        if not session or session.state != AssessmentState.IN_PROGRESS:
            return
        
        # Try to process as answer
        content = message.content.strip()
        
        # Skip if it's a slash command
        if content.startswith('/'):
            return
        
        # Validate and submit answer
        success, error = self.assessment_manager.submit_answer(user_id, content)
        
        if not success:
            if error:
                await message.channel.send(error)
            return
        
        # Check if assessment is completed
        if session.state == AssessmentState.COMPLETED:
            await self._finish_assessment_channel(message.channel, session)
        else:
            # Send next question
            await self._send_question(message.channel, session)
    
    def _split_text(self, text: str, max_length: int = 4000) -> list:
        """
        Split text into chunks respecting Discord limits.
        
        Args:
            text: Text to split
            max_length: Maximum length per chunk
            
        Returns:
            List of text chunks
        """
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        for line in text.split('\n'):
            if len(current_chunk) + len(line) + 1 <= max_length:
                current_chunk += line + '\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = line + '\n'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks


async def setup_commands(
    bot: commands.Bot,
    cert_data: Dict[str, Any],
    assessment_manager: AssessmentManager,
    roadmap_generator: RoadmapGenerator,
    gemini_engine: GeminiAI,
    user_manager: UserManager
) -> BotCommands:
    """
    Setup and register all bot slash commands.
    
    Args:
        bot: Discord bot instance
        cert_data: Certification data
        assessment_manager: Assessment manager
        roadmap_generator: Roadmap generator
        gemini_engine: Gemini AI engine
        user_manager: User manager
        
    Returns:
        BotCommands cog instance
    """
    logger.info("Setting up bot slash commands...")
    
    cog = BotCommands(
        bot,
        cert_data,
        assessment_manager,
        roadmap_generator,
        gemini_engine,
        user_manager
    )
    
    # CRITICAL FIX: Must use await in discord.py 2.0+
    await bot.add_cog(cog)
    
    # Sync slash commands with Discord
    try:
        synced = await bot.tree.sync()
        logger.info(f"✅ Synced {len(synced)} slash commands with Discord")
    except Exception as e:
        logger.error(f"❌ Failed to sync commands: {e}")
    
    logger.info("✅ Bot commands registered successfully")
    logger.info(f"✅ Registered {len([cmd for cmd in bot.commands])} traditional commands")
    logger.info(f"✅ Registered {len(bot.tree.get_commands())} slash commands")
    
    return cog