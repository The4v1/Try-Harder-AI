"""
Discord Embed Formatters
=========================

Utility functions for creating beautiful, consistent Discord embeds
and formatting messages for the Try-Harder-AI bot.

Features:
- Standardized embed creation
- Color coding by message type
- Field formatting and truncation
- Code block formatting
- Progress bar generation
- Certification-specific styling
- Error message formatting
- Success message formatting

Author: Try-Harder-AI Team
"""

import discord
from datetime import datetime
from typing import List, Dict, Optional, Union


# =============================================================================
# COLOR CONSTANTS
# =============================================================================

class Colors:
    """Discord embed color constants"""
    SUCCESS = 0x2ecc71      # Green
    ERROR = 0xe74c3c        # Red
    INFO = 0x3498db         # Blue
    WARNING = 0xf39c12      # Orange
    OFFSEC = 0xc0392b       # OffSec Red
    GOLD = 0xf1c40f         # Gold (achievements)
    PURPLE = 0x9b59b6       # Purple
    DARK = 0x2c3e50         # Dark Gray


# =============================================================================
# CERTIFICATION COLORS
# =============================================================================

CERTIFICATION_COLORS = {
    'OSCP': 0xc0392b,    # OffSec Red
    'OSEP': 0xe74c3c,    # Bright Red
    'OSWE': 0x3498db,    # Blue
    'OSED': 0x9b59b6,    # Purple
    'OSWP': 0x1abc9c,    # Turquoise
    'OSWA': 0x3498db,    # Blue
    'OSMR': 0x95a5a6,    # Gray (macOS)
    'OSDA': 0x2ecc71,    # Green (Defense)
    'KLCP': 0x00ff00,    # Green (Kali Linux)
}


# =============================================================================
# CERTIFICATION EMOJIS
# =============================================================================

CERTIFICATION_EMOJIS = {
    'OSCP': '🎯',
    'OSEP': '🔥',
    'OSWE': '🌐',
    'OSED': '💾',
    'OSWP': '📡',
    'OSWA': '🕸️',
    'OSMR': '🍎',
    'OSDA': '🛡️',
    'KLCP': '🐉',
}


# =============================================================================
# BASIC EMBED CREATION
# =============================================================================

def create_embed(
    title: str,
    description: str = None,
    color: int = Colors.INFO,
    thumbnail: str = None,
    image: str = None,
    footer: str = None,
    timestamp: bool = True
) -> discord.Embed:
    """
    Create a basic Discord embed with standard formatting.
    
    Args:
        title: Embed title
        description: Embed description
        color: Embed color (hex)
        thumbnail: URL for thumbnail image
        image: URL for main image
        footer: Footer text
        timestamp: Whether to add timestamp
        
    Returns:
        Configured Discord embed
    """
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    
    if image:
        embed.set_image(url=image)
    
    if footer:
        embed.set_footer(text=footer)
    elif timestamp:
        embed.set_footer(text="Try-Harder-AI")
    
    if timestamp:
        embed.timestamp = datetime.utcnow()
    
    return embed


# =============================================================================
# SUCCESS/ERROR/INFO EMBEDS
# =============================================================================

def success_embed(title: str, description: str, **kwargs) -> discord.Embed:
    """Create a success embed (green)"""
    return create_embed(
        title=f"✅ {title}",
        description=description,
        color=Colors.SUCCESS,
        **kwargs
    )


def error_embed(title: str, description: str, **kwargs) -> discord.Embed:
    """Create an error embed (red)"""
    return create_embed(
        title=f"❌ {title}",
        description=description,
        color=Colors.ERROR,
        **kwargs
    )


def info_embed(title: str, description: str, **kwargs) -> discord.Embed:
    """Create an info embed (blue)"""
    return create_embed(
        title=f"ℹ️ {title}",
        description=description,
        color=Colors.INFO,
        **kwargs
    )


def warning_embed(title: str, description: str, **kwargs) -> discord.Embed:
    """Create a warning embed (orange)"""
    return create_embed(
        title=f"⚠️ {title}",
        description=description,
        color=Colors.WARNING,
        **kwargs
    )


# =============================================================================
# CERTIFICATION-SPECIFIC EMBEDS
# =============================================================================

def certification_embed(
    certification: str,
    title: str,
    description: str = None,
    **kwargs
) -> discord.Embed:
    """
    Create a certification-specific embed with appropriate color and emoji.
    
    Args:
        certification: Certification code (OSCP, OSEP, etc.)
        title: Embed title
        description: Embed description
        
    Returns:
        Formatted embed
    """
    cert_upper = certification.upper()
    color = CERTIFICATION_COLORS.get(cert_upper, Colors.OFFSEC)
    emoji = CERTIFICATION_EMOJIS.get(cert_upper, '🎯')
    
    return create_embed(
        title=f"{emoji} {title}",
        description=description,
        color=color,
        **kwargs
    )


# =============================================================================
# FIELD FORMATTING
# =============================================================================

def add_field(
    embed: discord.Embed,
    name: str,
    value: str,
    inline: bool = False,
    max_length: int = 1024
) -> discord.Embed:
    """
    Add a field to embed with automatic truncation.
    
    Args:
        embed: Discord embed to modify
        name: Field name
        value: Field value
        inline: Whether field should be inline
        max_length: Maximum field value length
        
    Returns:
        Modified embed
    """
    # Truncate if necessary
    if len(value) > max_length:
        value = value[:max_length-3] + "..."
    
    # Ensure value is not empty
    if not value or value.isspace():
        value = "N/A"
    
    embed.add_field(name=name, value=value, inline=inline)
    return embed


def add_fields(
    embed: discord.Embed,
    fields: List[Dict[str, Union[str, bool]]],
    max_fields: int = 25
) -> discord.Embed:
    """
    Add multiple fields to embed.
    
    Args:
        embed: Discord embed to modify
        fields: List of field dictionaries with 'name', 'value', 'inline'
        max_fields: Maximum number of fields to add
        
    Returns:
        Modified embed
    """
    for i, field in enumerate(fields[:max_fields]):
        add_field(
            embed,
            name=field.get('name', 'Field'),
            value=field.get('value', 'N/A'),
            inline=field.get('inline', False)
        )
    
    return embed


# =============================================================================
# CODE BLOCK FORMATTING
# =============================================================================

def code_block(content: str, language: str = "") -> str:
    """
    Format content as Discord code block.
    
    Args:
        content: Code content
        language: Syntax highlighting language
        
    Returns:
        Formatted code block
    """
    return f"```{language}\n{content}\n```"


def inline_code(content: str) -> str:
    """Format content as inline code"""
    return f"`{content}`"


# =============================================================================
# PROGRESS BAR GENERATION
# =============================================================================

def progress_bar(
    value: int,
    max_value: int,
    length: int = 10,
    fill: str = "█",
    empty: str = "░"
) -> str:
    """
    Generate a visual progress bar.
    
    Args:
        value: Current value
        max_value: Maximum value
        length: Bar length in characters
        fill: Character for filled portion
        empty: Character for empty portion
        
    Returns:
        Progress bar string
    """
    if max_value == 0:
        percentage = 0
    else:
        percentage = min(100, int((value / max_value) * 100))
    
    filled = int((percentage / 100) * length)
    bar = fill * filled + empty * (length - filled)
    
    return f"{bar} {percentage}%"


def skill_progress_bar(skill_name: str, value: int) -> str:
    """
    Generate a labeled skill progress bar.
    
    Args:
        skill_name: Name of the skill
        value: Skill level (0-100)
        
    Returns:
        Formatted progress bar with label
    """
    bar = progress_bar(value, 100, length=15)
    return f"**{skill_name}**\n{bar}"


# =============================================================================
# LIST FORMATTING
# =============================================================================

def bullet_list(items: List[str], emoji: str = "•") -> str:
    """
    Format items as bulleted list.
    
    Args:
        items: List of items
        emoji: Bullet character/emoji
        
    Returns:
        Formatted list
    """
    if not items:
        return "None"
    
    return "\n".join([f"{emoji} {item}" for item in items])


def numbered_list(items: List[str]) -> str:
    """
    Format items as numbered list.
    
    Args:
        items: List of items
        
    Returns:
        Formatted numbered list
    """
    if not items:
        return "None"
    
    return "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])


# =============================================================================
# ASSESSMENT RESULT FORMATTING
# =============================================================================

def format_assessment_results(results: Dict) -> discord.Embed:
    """
    Format assessment results as embed.
    
    Args:
        results: Assessment results dictionary
        
    Returns:
        Formatted embed
    """
    certification = results.get('certification', 'Assessment')
    score = results.get('score', 0)
    max_score = results.get('max_score', 0)
    percentage = results.get('percentage', 0)
    skill_level = results.get('skill_level', 'Unknown')
    
    # Determine color based on score
    if percentage >= 70:
        color = Colors.SUCCESS
        icon = "🎉"
    elif percentage >= 50:
        color = Colors.WARNING
        icon = "⚡"
    else:
        color = Colors.ERROR
        icon = "📚"
    
    embed = certification_embed(
        certification,
        f"{icon} Assessment Complete!",
        f"You scored **{score}/{max_score}** ({percentage}%)"
    )
    
    # Skill level
    embed.add_field(
        name="📊 Skill Level",
        value=f"**{skill_level.upper()}**",
        inline=True
    )
    
    # Score breakdown
    breakdown = results.get('breakdown', {})
    if breakdown:
        breakdown_text = ""
        for difficulty, stats in breakdown.items():
            correct = stats.get('correct', 0)
            total = stats.get('total', 0)
            breakdown_text += f"**{difficulty.capitalize()}:** {correct}/{total}\n"
        
        embed.add_field(
            name="📈 Score Breakdown",
            value=breakdown_text,
            inline=True
        )
    
    # Weak areas
    weak_areas = results.get('weak_areas', [])
    if weak_areas:
        embed.add_field(
            name="⚠️ Areas to Improve",
            value=bullet_list(weak_areas[:5], "🔸"),
            inline=False
        )
    
    # Strong areas
    strong_areas = results.get('strong_areas', [])
    if strong_areas:
        embed.add_field(
            name="✅ Strong Areas",
            value=bullet_list(strong_areas[:5], "✨"),
            inline=False
        )
    
    return embed


# =============================================================================
# ROADMAP FORMATTING
# =============================================================================

def format_roadmap_week(week: Dict) -> discord.Embed:
    """
    Format a single week from roadmap as embed.
    
    Args:
        week: Week dictionary from roadmap
        
    Returns:
        Formatted embed
    """
    week_number = week.get('week_number', 1)
    title = week.get('title', f'Week {week_number}')
    status = week.get('status', 'not_started')
    
    # Status emoji
    status_emoji = {
        'completed': '✅',
        'in_progress': '⚡',
        'not_started': '⏳',
        'paused': '⏸️'
    }.get(status, '📅')
    
    embed = create_embed(
        title=f"{status_emoji} Week {week_number}: {title}",
        color=Colors.INFO
    )
    
    # Topics
    topics = week.get('topics', [])
    if topics:
        embed.add_field(
            name="📚 Topics",
            value=bullet_list(topics, "▫️"),
            inline=False
        )
    
    # Tasks progress
    tasks_completed = week.get('tasks_completed', 0)
    tasks_total = week.get('tasks_total', 0)
    if tasks_total > 0:
        progress = progress_bar(tasks_completed, tasks_total)
        embed.add_field(
            name="✓ Tasks Progress",
            value=progress,
            inline=False
        )
    
    # Machines completed
    machines = week.get('machines_completed', [])
    if machines:
        embed.add_field(
            name="💻 Machines Completed",
            value=bullet_list(machines, "🎯"),
            inline=False
        )
    
    # Current machine
    current_machine = week.get('current_machine')
    if current_machine:
        embed.add_field(
            name="🔄 Currently Working On",
            value=current_machine,
            inline=False
        )
    
    # Notes
    notes = week.get('notes')
    if notes:
        embed.add_field(
            name="📝 Notes",
            value=notes[:500],  # Limit length
            inline=False
        )
    
    return embed


# =============================================================================
# PROGRESS FORMATTING
# =============================================================================

def format_user_progress(progress: Dict) -> discord.Embed:
    """
    Format user progress as embed.
    
    Args:
        progress: User progress dictionary
        
    Returns:
        Formatted embed
    """
    embed = create_embed(
        title="📊 Your Learning Progress",
        description="Here's your current progress across all areas",
        color=Colors.INFO
    )
    
    # Machines completed
    machines = progress.get('machines_completed', {})
    if machines:
        machines_text = ""
        total_machines = 0
        for platform, count in machines.items():
            machines_text += f"**{platform.capitalize()}:** {count}\n"
            total_machines += count
        
        embed.add_field(
            name=f"💻 Machines Completed ({total_machines} total)",
            value=machines_text,
            inline=True
        )
    
    # Skills
    skills = progress.get('skills', {})
    if skills:
        skills_text = ""
        for skill, level in list(skills.items())[:5]:  # Top 5 skills
            skills_text += f"{skill_progress_bar(skill.replace('_', ' ').title(), level)}\n\n"
        
        embed.add_field(
            name="🎯 Skills Progress",
            value=skills_text,
            inline=False
        )
    
    # Topics mastered
    topics_mastered = progress.get('topics_mastered', [])
    if topics_mastered:
        embed.add_field(
            name="✅ Topics Mastered",
            value=bullet_list(topics_mastered[:8], "✨"),
            inline=True
        )
    
    # Topics in progress
    topics_in_progress = progress.get('topics_in_progress', [])
    if topics_in_progress:
        embed.add_field(
            name="⚡ Currently Learning",
            value=bullet_list(topics_in_progress[:5], "🔸"),
            inline=True
        )
    
    return embed


# =============================================================================
# HELP COMMAND FORMATTING
# =============================================================================

def format_command_help(
    command: str,
    description: str,
    usage: str,
    examples: List[str]
) -> discord.Embed:
    """
    Format help information for a command.
    
    Args:
        command: Command name
        description: Command description
        usage: Usage syntax
        examples: List of example usages
        
    Returns:
        Formatted embed
    """
    embed = create_embed(
        title=f"📖 Command: {command}",
        description=description,
        color=Colors.INFO
    )
    
    embed.add_field(
        name="📝 Usage",
        value=code_block(usage, ""),
        inline=False
    )
    
    if examples:
        examples_text = "\n".join([code_block(ex, "") for ex in examples])
        embed.add_field(
            name="💡 Examples",
            value=examples_text,
            inline=False
        )
    
    return embed


# =============================================================================
# STATISTICS FORMATTING
# =============================================================================

def format_statistics(stats: Dict) -> discord.Embed:
    """
    Format user statistics as embed.
    
    Args:
        stats: Statistics dictionary
        
    Returns:
        Formatted embed
    """
    embed = create_embed(
        title="📈 Your Statistics",
        description="Your activity and progress metrics",
        color=Colors.GOLD
    )
    
    # Commands used
    total_commands = stats.get('total_commands_used', 0)
    embed.add_field(
        name="⌨️ Commands Used",
        value=f"**{total_commands}** commands",
        inline=True
    )
    
    # AI queries
    ai_queries = stats.get('total_ai_queries', 0)
    embed.add_field(
        name="🤖 AI Questions Asked",
        value=f"**{ai_queries}** questions",
        inline=True
    )
    
    # Study sessions
    study_sessions = stats.get('total_study_sessions', 0)
    embed.add_field(
        name="📚 Study Sessions",
        value=f"**{study_sessions}** sessions",
        inline=True
    )
    
    # Current streak
    current_streak = stats.get('current_streak_days', 0)
    longest_streak = stats.get('longest_streak_days', 0)
    
    streak_text = f"**Current:** {current_streak} days\n**Longest:** {longest_streak} days"
    embed.add_field(
        name="🔥 Study Streak",
        value=streak_text,
        inline=True
    )
    
    # Study time
    study_time_hours = stats.get('total_study_time_hours', 0)
    embed.add_field(
        name="⏱️ Total Study Time",
        value=f"**{study_time_hours}** hours",
        inline=True
    )
    
    # Favorite command
    favorite_command = stats.get('favorite_command', 'N/A')
    embed.add_field(
        name="⭐ Favorite Command",
        value=inline_code(favorite_command),
        inline=True
    )
    
    return embed


# =============================================================================
# ACHIEVEMENT FORMATTING
# =============================================================================

def format_achievement(achievement: Dict) -> discord.Embed:
    """
    Format achievement unlock as embed.
    
    Args:
        achievement: Achievement dictionary
        
    Returns:
        Formatted embed
    """
    name = achievement.get('name', 'Achievement')
    description = achievement.get('description', '')
    icon = achievement.get('icon', '🏆')
    
    embed = create_embed(
        title=f"{icon} Achievement Unlocked!",
        description=f"**{name}**\n\n{description}",
        color=Colors.GOLD
    )
    
    return embed


# =============================================================================
# TRUNCATION UTILITIES
# =============================================================================

def truncate_text(text: str, max_length: int = 2000, suffix: str = "...") -> str:
    """
    Truncate text to Discord's message limit.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def split_message(text: str, max_length: int = 2000) -> List[str]:
    """
    Split long message into multiple parts.
    
    Args:
        text: Text to split
        max_length: Maximum length per message
        
    Returns:
        List of message parts
    """
    if len(text) <= max_length:
        return [text]
    
    parts = []
    current = ""
    
    for line in text.split('\n'):
        if len(current) + len(line) + 1 > max_length:
            parts.append(current)
            current = line
        else:
            current += ('\n' if current else '') + line
    
    if current:
        parts.append(current)
    
    return parts


# =============================================================================
# TIME FORMATTING
# =============================================================================

def format_duration(seconds: int) -> str:
    """
    Format duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def format_timestamp(dt: datetime) -> str:
    """
    Format datetime as Discord timestamp.
    
    Args:
        dt: Datetime object
        
    Returns:
        Formatted timestamp
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


# =============================================================================
# CERTIFICATION INFO
# =============================================================================

def get_certification_info(certification: str) -> Dict:
    """
    Get certification display information.
    
    Args:
        certification: Certification code
        
    Returns:
        Dictionary with color and emoji
    """
    cert_upper = certification.upper()
    return {
        'color': CERTIFICATION_COLORS.get(cert_upper, Colors.OFFSEC),
        'emoji': CERTIFICATION_EMOJIS.get(cert_upper, '🎯'),
        'name': cert_upper
    }