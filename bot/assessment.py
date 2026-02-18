"""
Assessment Manager
==================

Handles skill assessment questionnaires for certification readiness evaluation.

Features:
- Interactive question flow
- Answer validation and scoring
- Skill level calculation
- Strength/weakness analysis
- Progress tracking
- Multi-certification support (12 OffSec certs)
- Professional Discord embeds
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import asyncio
from datetime import datetime
import discord

# Setup logging
logger = logging.getLogger(__name__)


class SkillLevel(Enum):
    """Skill level classifications."""
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"


class AssessmentState(Enum):
    """Assessment progress states."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class Question:
    """Represents a single assessment question."""
    
    def __init__(
        self,
        id: str,
        text: str,
        category: str,
        options: List[Dict[str, Any]],
        weight: float = 1.0
    ):
        """
        Initialize a question.
        
        Args:
            id: Unique question identifier
            text: Question text
            category: Topic category (e.g., "networking", "web_exploitation")
            options: List of answer options with scores
            weight: Question importance weight (default: 1.0)
        """
        self.id = id
        self.text = text
        self.category = category
        self.options = options
        self.weight = weight
    
    def get_formatted_options(self) -> str:
        """
        Format options for Discord display.
        
        Returns:
            Formatted options string
        """
        formatted = ""
        emoji_letters = [":regional_indicator_a:", ":regional_indicator_b:", ":regional_indicator_c:", ":regional_indicator_d:"]
        
        for i, option in enumerate(self.options):
            emoji = emoji_letters[i] if i < len(emoji_letters) else f"{chr(65+i)}."
            formatted += f"{emoji} {option['text']}\n"
        
        return formatted.strip()
    
    def validate_answer(self, answer: str) -> bool:
        """
        Validate if answer is in valid range.
        
        Args:
            answer: User's answer (numeric string)
            
        Returns:
            True if valid, False otherwise
        """
        try:
            answer_num = int(answer)
            return 1 <= answer_num <= len(self.options)
        except ValueError:
            return False
    
    def get_score(self, answer: str) -> int:
        """
        Get score for a given answer.
        
        Args:
            answer: User's answer (numeric string)
            
        Returns:
            Score for the answer (0-100)
        """
        try:
            answer_num = int(answer)
            if 1 <= answer_num <= len(self.options):
                return self.options[answer_num - 1].get('score', 0)
            return 0
        except (ValueError, IndexError):
            return 0



class AssessmentButtonView(discord.ui.View):
    """Clickable buttons for assessment answers - A, B, C, D"""
    
    def __init__(self, assessment_manager, user_id: str, session, bot_commands=None):
        super().__init__(timeout=60.0)
        self.assessment_manager = assessment_manager
        self.user_id = user_id
        self.session = session
        self.answered = False
        self.bot_commands = bot_commands  # Reference to BotCommands cog for roadmap generation
        question = session.get_current_question()
        if not question:
            return
        emojis = ["🇬", "🇧", "🇨", "🇩"]  # Regional indicators A, B, C, D
        button_styles = [discord.ButtonStyle.primary, discord.ButtonStyle.primary, 
                        discord.ButtonStyle.success, discord.ButtonStyle.danger]  # Blue, Blue, Green, Red
        for i, option in enumerate(question.options[:4]):
            button = discord.ui.Button(
                label=f"{chr(65+i)}.  {option['text']}",  # Show full text
                style=button_styles[i]
            )
            button.callback = self.create_callback(chr(65+i), i+1)
            self.add_item(button)
    
    def create_callback(self, letter, number):
        async def button_callback(interaction: discord.Interaction):
            if str(interaction.user.id) != self.user_id:
                await interaction.response.send_message(" Not your assessment!", ephemeral=True)
                return
            if self.answered:
                await interaction.response.send_message(" Already answered!", ephemeral=True)
                return
            self.answered = True
            for item in self.children:
                item.disabled = True
            await interaction.response.edit_message(view=self)
            success, error = self.assessment_manager.submit_answer(self.user_id, str(number))
            if not success:
                await interaction.followup.send(f" {error}")
                return
            await asyncio.sleep(0.5)
            
            next_q = self.session.get_current_question()
            if next_q:
                current, total = self.session.get_progress()
                embed = self.assessment_manager.create_question_embed(next_q, current, total, self.session.certification)
                new_view = AssessmentButtonView(self.assessment_manager, self.user_id, self.session, self.bot_commands)
                await interaction.channel.send(embed=embed, view=new_view)
            else:
                # Assessment complete — delegate to BotCommands._finish_assessment_channel
                # which handles results embed + roadmap generation
                if self.bot_commands:
                    await self.bot_commands._finish_assessment_channel(interaction.channel, self.session)
                else:
                    # Fallback: show basic results if bot_commands not available
                    results = self.assessment_manager.complete_session(self.user_id)
                    if results:
                        results_embed = discord.Embed(
                            title=f"🏆 {self.session.certification} Assessment Complete!",
                            description=f"**Skill Level:** {results['skill_level']}\n**Score:** {results['score']:.0f}%",
                            color=discord.Color.gold()
                        )
                        if results.get('strengths'):
                            strengths_text = "\n".join([f"✅ {s}" for s in results['strengths'][:3]])
                            results_embed.add_field(name="💪 Strengths", value=strengths_text, inline=False)
                        if results.get('weaknesses'):
                            weaknesses_text = "\n".join([f"📝 {w}" for w in results['weaknesses'][:3]])
                            results_embed.add_field(name="🎯 Areas to Focus", value=weaknesses_text, inline=False)
                        results_embed.set_footer(text="Use /roadmap to generate your personalized study plan!")
                        await interaction.channel.send(embed=results_embed)
        return button_callback
    
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

class AssessmentSession:
    """Manages an individual assessment session."""
    
    def __init__(
        self,
        user_id: str,
        certification: str,
        questions: List[Question]
    ):
        """
        Initialize assessment session.
        
        Args:
            user_id: Discord user ID
            certification: Certification code (e.g., "OSCP")
            questions: List of questions to ask
        """
        self.user_id = user_id
        self.certification = certification
        self.questions = questions
        self.current_question_idx = 0
        self.answers: Dict[str, str] = {}
        self.scores: Dict[str, int] = {}
        self.category_scores: Dict[str, List[int]] = {}
        self.state = AssessmentState.NOT_STARTED
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
    
    def start(self):
        """Start the assessment session."""
        self.state = AssessmentState.IN_PROGRESS
        self.started_at = datetime.now()
        logger.info(f"🎯 Assessment started for user {self.user_id} - {self.certification}")
    
    def get_current_question(self) -> Optional[Question]:
        """
        Get the current question.
        
        Returns:
            Current Question object or None if completed
        """
        if self.current_question_idx < len(self.questions):
            return self.questions[self.current_question_idx]
        return None
    
    def get_progress(self) -> Tuple[int, int]:
        """
        Get assessment progress.
        
        Returns:
            Tuple of (current_question, total_questions)
        """
        return (self.current_question_idx + 1, len(self.questions))
    
    def submit_answer(self, answer: str) -> bool:
        """
        Submit answer for current question.
        
        Args:
            answer: User's answer
            
        Returns:
            True if answer was valid and recorded, False otherwise
        """
        question = self.get_current_question()
        if not question:
            return False
        
        if not question.validate_answer(answer):
            return False
        
        # Record answer and score
        self.answers[question.id] = answer
        score = question.get_score(answer)
        self.scores[question.id] = score
        
        # Track category scores
        if question.category not in self.category_scores:
            self.category_scores[question.category] = []
        self.category_scores[question.category].append(score)
        
        # Move to next question
        self.current_question_idx += 1
        
        # Check if completed
        if self.current_question_idx >= len(self.questions):
            self.complete()
        
        logger.debug(f"✅ Answer recorded: Q{question.id} = {answer} (score: {score})")
        return True
    
    def complete(self):
        """Mark assessment as completed."""
        self.state = AssessmentState.COMPLETED
        self.completed_at = datetime.now()
        logger.info(f"✅ Assessment completed for user {self.user_id}")
    
    def abandon(self):
        """Mark assessment as abandoned."""
        self.state = AssessmentState.ABANDONED
        logger.info(f"⚠️ Assessment abandoned by user {self.user_id}")
    
    def calculate_total_score(self) -> float:
        """
        Calculate overall assessment score.
        
        Returns:
            Score as percentage (0-100)
        """
        if not self.scores:
            return 0.0
        
        total_score = 0.0
        max_possible = 0.0
        
        for question in self.questions:
            if question.id in self.scores:
                score = self.scores[question.id]
                total_score += score * question.weight
                
                # Get max score for this question
                max_score = max(opt.get('score', 0) for opt in question.options)
                max_possible += max_score * question.weight
        
        if max_possible == 0:
            return 0.0
        
        # Normalize to percentage (0-100)
        return (total_score / max_possible) * 100.0
    
    def determine_skill_level(self) -> SkillLevel:
        """
        Determine user's skill level based on score.
        
        Scoring Logic:
        - All A (0pts) = 0%   = Beginner
        - All B (1pt)  = 33%  = Beginner  
        - All C (2pts) = 67%  = Intermediate
        - All D (3pts) = 100% = Expert
        
        Returns:
            SkillLevel enum value
        """
        score = self.calculate_total_score()
        
        # Thresholds adjusted to match answer scoring
        if score >= 84:              # All D or mostly D
            return SkillLevel.EXPERT
        elif score >= 75:            # Mostly D with some C
            return SkillLevel.ADVANCED
        elif score >= 50:            # All C or C+B mix
            return SkillLevel.INTERMEDIATE
        else:                        # All A/B or low mix
            return SkillLevel.BEGINNER
    
    def analyze_strengths_weaknesses(self) -> Tuple[List[str], List[str]]:
        """
        Analyze strengths and weaknesses by category.
        
        Returns:
            Tuple of (strengths, weaknesses) as category lists
        """
        strengths = []
        weaknesses = []
        
        # Get overall score to adjust thresholds
        overall_score = self.calculate_total_score()
        
        for category, scores in self.category_scores.items():
            if not scores:
                continue
            
            # Calculate average raw score for this category
            avg_raw_score = sum(scores) / len(scores)
            
            # Normalize to percentage (assuming max score is 3)
            avg_percentage = (avg_raw_score / 3.0) * 100.0
            
            category_name = category.replace('_', ' ').title()
            
            # Adjust thresholds based on overall skill level
            if overall_score >= 84:  # Expert - very high standards
                if avg_percentage >= 90:
                    strengths.append(category_name)
                # Experts have no weaknesses shown unless catastrophically low
                elif avg_percentage < 60:
                    weaknesses.append(category_name)
            elif overall_score >= 75:  # Advanced
                if avg_percentage >= 80:
                    strengths.append(category_name)
                elif avg_percentage < 65:
                    weaknesses.append(category_name)
            elif overall_score >= 50:  # Intermediate
                if avg_percentage >= 70:
                    strengths.append(category_name)
                elif avg_percentage < 55:
                    weaknesses.append(category_name)
            else:  # Beginner
                if avg_percentage >= 60:
                    strengths.append(category_name)
                elif avg_percentage < 45:
                    weaknesses.append(category_name)
        
        return strengths, weaknesses
    
    def get_results_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive results summary.
        
        Returns:
            Dictionary with all assessment results
        """
        score = self.calculate_total_score()
        skill_level = self.determine_skill_level()
        strengths, weaknesses = self.analyze_strengths_weaknesses()
        
        duration = None
        if self.started_at and self.completed_at:
            duration = (self.completed_at - self.started_at).total_seconds()
        
        # Get readable responses
        responses = {}
        for question in self.questions:
            if question.id in self.answers:
                answer_idx = int(self.answers[question.id]) - 1
                if 0 <= answer_idx < len(question.options):
                    responses[question.text] = question.options[answer_idx]['text']
        
        return {
            'user_id': self.user_id,
            'cert': self.certification,
            'certification': self.certification,
            'score': round(score, 1),
            'score_percentage': round(score, 1),
            'skill_level': skill_level.value,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'category_scores': {
                cat: round(sum(scores) / len(scores), 1)
                for cat, scores in self.category_scores.items()
            },
            'total_questions': len(self.questions),
            'questions_answered': len(self.answers),
            'duration_seconds': duration,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'responses': responses
        }


class AssessmentManager:
    """Manages all assessment sessions across users."""
    
    def __init__(self, questions_data: Dict[str, List[Dict[str, Any]]], user_manager=None):
        """
        Initialize assessment manager.
        
        Args:
            questions_data: Questions loaded from YAML, keyed by certification
            user_manager: UserManager instance for saving results
        """
        self.questions_data = questions_data
        self.user_manager = user_manager
        self.active_sessions: Dict[str, AssessmentSession] = {}
        self.completed_sessions: List[AssessmentSession] = []
        logger.info("📊 Assessment Manager initialized")
    
    def _create_questions(self, certification: str) -> List[Question]:
        """
        Create Question objects for a certification.
        
        Args:
            certification: Certification code
            
        Returns:
            List of Question objects
        """
        questions = []
        cert_data = self.questions_data.get(certification, {})
        
        # Handle nested structure: certification -> difficulty_level -> questions
        if isinstance(cert_data, dict):
            # Iterate through difficulty levels (beginner, intermediate, advanced)
            for difficulty_level, questions_list in cert_data.items():
                if isinstance(questions_list, list):
                    for q_data in questions_list:
                        if isinstance(q_data, dict):
                            # Combine options and scoring into proper format
                            opts_dict = q_data.get('options', {})
                            score_dict = q_data.get('scoring', {})
                            opts_list = []
                            if isinstance(opts_dict, dict):
                                for key in sorted(opts_dict.keys()):
                                    opts_list.append({
                                        'text': opts_dict[key],
                                        'score': score_dict.get(key, 0) if isinstance(score_dict, dict) else 0
                                    })
                            
                            question = Question(
                                id=q_data.get('id', f"q_{len(questions) + 1}"),
                                text=q_data.get('question', q_data.get('text', '')),
                                category=q_data.get('topic', q_data.get('category', 'general')),
                                options=opts_list,
                                weight=q_data.get('weight', 1.0)
                            )
                            questions.append(question)
        
        logger.debug(f"Created {len(questions)} questions for {certification}")
        return questions
    
    def start_assessment(
        self,
        user_id: str,
        certification: str
    ) -> Optional[AssessmentSession]:
        """
        Start a new assessment for a user.
        
        Args:
            user_id: Discord user ID
            certification: Certification code
            
        Returns:
            AssessmentSession object or None if invalid cert
        """
        # Check if user has active session
        if user_id in self.active_sessions:
            logger.warning(f"⚠️ User {user_id} already has active assessment")
            return self.active_sessions[user_id]
        
        # Create questions
        questions = self._create_questions(certification)
        
        if not questions:
            logger.error(f"❌ No questions found for {certification}")
            return None
        
        # Create session
        session = AssessmentSession(user_id, certification, questions)
        session.start()
        
        self.active_sessions[user_id] = session
        
        logger.info(f"✅ Created assessment session for user {user_id} - {certification}")
        return session
    
    def get_session(self, user_id: str) -> Optional[AssessmentSession]:
        """
        Get active session for a user.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            AssessmentSession or None
        """
        return self.active_sessions.get(user_id)
    
    def submit_answer(self, user_id: str, answer: str) -> Tuple[bool, Optional[str]]:
        """
        Submit an answer for a user's current question.
        
        Args:
            user_id: Discord user ID
            answer: User's answer
            
        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        session = self.get_session(user_id)
        
        if not session:
            return False, "❌ No active assessment found. Use `/skillcheck` to start."
        
        if session.state != AssessmentState.IN_PROGRESS:
            return False, "⚠️ Assessment is not in progress."
        
        question = session.get_current_question()
        
        if not question:
            return False, "✅ No more questions available."
        
        if not question.validate_answer(answer):
            return False, f"❌ Invalid answer. Please enter a number between 1 and {len(question.options)}."
        
        success = session.submit_answer(answer)
        
        if not success:
            return False, "⚠️ Failed to record answer. Please try again."
        
        return True, None
    
    def complete_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Complete a user's assessment session.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            Results summary or None
        """
        session = self.active_sessions.get(user_id)
        
        if not session:
            return None
        
        if session.state != AssessmentState.COMPLETED:
            session.complete()
        
        # Get results summary
        results = session.get_results_summary()
        
        # CRITICAL: Save results to user_manager so /progress can retrieve them
        if self.user_manager and results:
            self.user_manager.save_assessment_results(user_id, results)
            logger.info(f"💾 Saved assessment results to user_manager for {user_id}")
        
        # Move to completed sessions
        self.completed_sessions.append(session)
        del self.active_sessions[user_id]
        
        logger.info(f"✅ Session completed for user {user_id}")
        return results
    
    def abandon_session(self, user_id: str):
        """
        Abandon a user's assessment session.
        
        Args:
            user_id: Discord user ID
        """
        session = self.active_sessions.get(user_id)
        
        if session:
            session.abandon()
            del self.active_sessions[user_id]
            logger.info(f"⚠️ Session abandoned for user {user_id}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get overall assessment statistics.
        
        Returns:
            Statistics dictionary
        """
        total_completed = len(self.completed_sessions)
        active_count = len(self.active_sessions)
        
        if total_completed == 0:
            avg_score = 0.0
            skill_distribution = {}
        else:
            avg_score = sum(
                s.calculate_total_score() for s in self.completed_sessions
            ) / total_completed
            
            skill_distribution = {}
            for session in self.completed_sessions:
                level = session.determine_skill_level().value
                skill_distribution[level] = skill_distribution.get(level, 0) + 1
        
        return {
            'total_completed': total_completed,
            'active_sessions': active_count,
            'average_score': round(avg_score, 1),
            'skill_distribution': skill_distribution
        }
    
    def has_active_session(self, user_id: str) -> bool:
        """
        Check if user has an active assessment session.
        
        Args:
            user_id: Discord user ID
            
        Returns:
            True if active session exists, False otherwise
        """
        return user_id in self.active_sessions
    
    def create_question_embed(
        self,
        question: Question,
        current: int,
        total: int,
        certification: str
    ) -> discord.Embed:
        """
        Create a Discord embed for a question.
        
        Args:
            question: Question object
            current: Current question number
            total: Total questions
            certification: Certification code
            
        Returns:
            Discord Embed
        """
        # Question text - medium size, balanced with buttons
        embed = discord.Embed(
            title=f"📝 {certification} Assessment - Question {current}/{total}",
            description=f"**{question.text}**",
            color=discord.Color.blue()
        )
        
        # Progress bar
        progress_filled = int((current / total) * 10)
        progress_empty = 10 - progress_filled
        progress_bar = "█" * progress_filled + "░" * progress_empty
        
        embed.set_footer(text=f"Progress: [{progress_bar}] {current}/{total} • Try Harder! 💪")
        
        return embed
    
    def create_results_embed(
        self,
        results: Dict[str, Any],
        username: str
    ) -> discord.Embed:
        """
        Create a Discord embed for assessment results.
        
        Args:
            results: Assessment results dictionary
            username: Discord username
            
        Returns:
            Discord Embed
        """
        skill_level = results['skill_level']
        score = results['score_percentage']
        
        # Color based on skill level
        color_map = {
            "Beginner": discord.Color.red(),
            "Intermediate": discord.Color.blue(),
            "Advanced": discord.Color.green(),
            "Expert": discord.Color.gold()
        }
        color = color_map.get(skill_level, discord.Color.greyple())
        
        # Emoji based on skill level
        emoji_map = {
            "Beginner": "🌱",
            "Intermediate": "⚡",
            "Advanced": "🔥",
            "Expert": "👑"
        }
        emoji = emoji_map.get(skill_level, "📊")
        
        embed = discord.Embed(
            title=f"{emoji} Assessment Complete - {results['cert']}",
            description=f"**{username}**, here are your results!",
            color=color,
            timestamp=datetime.utcnow()
        )
        
        # Score field
        embed.add_field(
            name="📊 Your Score",
            value=f"**{score}%**",
            inline=True
        )
        
        # Skill level field
        embed.add_field(
            name="🎯 Skill Level",
            value=f"**{skill_level}** {emoji}",
            inline=True
        )
        
        # Questions answered
        embed.add_field(
            name="✅ Completed",
            value=f"{results['questions_answered']}/{results['total_questions']} questions",
            inline=True
        )
        
        # Strengths
        if results.get('strengths'):
            strengths_text = "\n".join(f"✅ {s}" for s in results['strengths'][:5])
            embed.add_field(
                name="💪 Your Strengths",
                value=strengths_text,
                inline=True
            )
        
        # Weaknesses
        if results.get('weaknesses'):
            weaknesses_text = "\n".join(f"📚 {w}" for w in results['weaknesses'][:5])
            embed.add_field(
                name="📖 Areas to Improve",
                value=weaknesses_text,
                inline=True
            )
        
        # Next steps
        next_steps = (
            "🗺️ **Next Step:** Use `/roadmap` to generate your personalized study plan!\n"
            "💡 **Pro Tip:** Your roadmap will be customized based on these results."
        )
        embed.add_field(
            name="🚀 What's Next?",
            value=next_steps,
            inline=False
        )
        
        # Updated footer for Gemini AI
        embed.set_footer(text="Try Harder! • Powered by Google Gemini AI 🤖")
        
        return embed


# Default questions for when questions.yaml is not available
# Supports ALL 12 OffSec certifications
DEFAULT_QUESTIONS = {
    "OSCP": [
        {
            "id": "oscp_q1",
            "text": "How comfortable are you with Linux command line?",
            "category": "linux",
            "weight": 1.5,
            "options": [
                {"text": "Beginner - I know basic commands (ls, cd, cat)", "score": 30},
                {"text": "Intermediate - I can navigate, edit files, use pipes", "score": 60},
                {"text": "Advanced - I'm comfortable with scripting and system administration", "score": 90}
            ]
        },
        {
            "id": "oscp_q2",
            "text": "What is your experience with network enumeration?",
            "category": "networking",
            "weight": 2.0,
            "options": [
                {"text": "None - I don't know what enumeration means", "score": 20},
                {"text": "Basic - I've used nmap a few times", "score": 50},
                {"text": "Intermediate - I regularly use nmap, enum4linux, and other tools", "score": 80},
                {"text": "Advanced - I can write custom enumeration scripts", "score": 100}
            ]
        },
        {
            "id": "oscp_q3",
            "text": "How familiar are you with web application vulnerabilities?",
            "category": "web_exploitation",
            "weight": 1.8,
            "options": [
                {"text": "Not familiar - I don't know common web vulnerabilities", "score": 20},
                {"text": "Basic - I know about SQL injection and XSS", "score": 50},
                {"text": "Intermediate - I can identify and exploit OWASP Top 10", "score": 75},
                {"text": "Advanced - I've completed PortSwigger Academy or similar", "score": 95}
            ]
        },
        {
            "id": "oscp_q4",
            "text": "What is your experience with privilege escalation?",
            "category": "privilege_escalation",
            "weight": 2.0,
            "options": [
                {"text": "None - I don't know what privilege escalation is", "score": 20},
                {"text": "Basic - I understand the concept", "score": 45},
                {"text": "Intermediate - I've practiced on HTB/THM machines", "score": 70},
                {"text": "Advanced - I regularly find and exploit privesc vectors", "score": 95}
            ]
        },
        {
            "id": "oscp_q5",
            "text": "Have you completed any practice machines (HTB, THM, VulnHub)?",
            "category": "practice",
            "weight": 1.2,
            "options": [
                {"text": "None - I haven't tried any", "score": 10},
                {"text": "1-10 machines", "score": 40},
                {"text": "11-30 machines", "score": 65},
                {"text": "31-50 machines", "score": 85},
                {"text": "50+ machines", "score": 100}
            ]
        }
    ],
    "OSCC": [  # NEW - OffSec CyberCore Certified (Beginner)
        {
            "id": "oscc_q1",
            "text": "How comfortable are you with basic cybersecurity concepts?",
            "category": "fundamentals",
            "weight": 1.5,
            "options": [
                {"text": "Beginner - I'm new to cybersecurity", "score": 30},
                {"text": "Intermediate - I understand CIA Triad and basic threats", "score": 60},
                {"text": "Advanced - I'm familiar with security frameworks (NIST, ISO)", "score": 90}
            ]
        },
        {
            "id": "oscc_q2",
            "text": "What is your experience with Linux and Windows operating systems?",
            "category": "os_fundamentals",
            "weight": 2.0,
            "options": [
                {"text": "None - I'm not comfortable with either", "score": 20},
                {"text": "Basic - I can navigate file systems and run commands", "score": 50},
                {"text": "Intermediate - I understand permissions, processes, and services", "score": 80},
                {"text": "Advanced - I can script and perform system administration", "score": 100}
            ]
        },
        {
            "id": "oscc_q3",
            "text": "How familiar are you with networking basics (OSI model, TCP/IP)?",
            "category": "networking",
            "weight": 1.8,
            "options": [
                {"text": "Not familiar - I don't understand networking", "score": 20},
                {"text": "Basic - I know about IP addresses and ports", "score": 50},
                {"text": "Intermediate - I understand protocols and can use Wireshark", "score": 75},
                {"text": "Advanced - I've completed network analysis labs", "score": 95}
            ]
        },
        {
            "id": "oscc_q4",
            "text": "What is your scripting experience (Python, Bash, PowerShell)?",
            "category": "scripting",
            "weight": 2.0,
            "options": [
                {"text": "None - I can't write scripts", "score": 20},
                {"text": "Basic - I can modify existing scripts", "score": 45},
                {"text": "Intermediate - I can write basic automation scripts", "score": 70},
                {"text": "Advanced - I regularly write security automation tools", "score": 95}
            ]
        },
        {
            "id": "oscc_q5",
            "text": "Have you completed any cybersecurity training or labs?",
            "category": "practice",
            "weight": 1.2,
            "options": [
                {"text": "None - This is my first step", "score": 10},
                {"text": "Some online courses or videos", "score": 40},
                {"text": "TryHackMe Pre-Security or similar beginner paths", "score": 65},
                {"text": "Multiple SOC/pentesting beginner labs", "score": 85},
                {"text": "Extensive practice across multiple platforms", "score": 100}
            ]
        }
    ],
    "OSEE": [  # NEW - OffSec Exploitation Expert (Expert)
        {
            "id": "osee_q1",
            "text": "What is your experience with Windows internals and exploitation?",
            "category": "windows_internals",
            "weight": 2.5,
            "options": [
                {"text": "Beginner - Limited understanding of Windows internals", "score": 20},
                {"text": "Intermediate - Familiar with user-mode exploitation", "score": 50},
                {"text": "Advanced - Completed OSED, understand heap/kernel basics", "score": 80},
                {"text": "Expert - Deep knowledge of Windows mitigations and bypasses", "score": 100}
            ]
        },
        {
            "id": "osee_q2",
            "text": "How comfortable are you with x86_64 assembly and debugging?",
            "category": "assembly",
            "weight": 2.0,
            "options": [
                {"text": "Not comfortable - Limited assembly knowledge", "score": 15},
                {"text": "Basic - Can read simple assembly", "score": 45},
                {"text": "Intermediate - Can write shellcode and debug with WinDBG", "score": 75},
                {"text": "Advanced - Expert in assembly, ROP chains, and WinDBG", "score": 100}
            ]
        },
        {
            "id": "osee_q3",
            "text": "What is your experience with modern exploit mitigations (DEP, ASLR, CFG)?",
            "category": "mitigations",
            "weight": 2.2,
            "options": [
                {"text": "None - Don't understand mitigations", "score": 10},
                {"text": "Basic - Know what they are conceptually", "score": 40},
                {"text": "Intermediate - Have bypassed DEP/ASLR in practice", "score": 70},
                {"text": "Advanced - Successfully bypassed CFG, CET, and ACG", "score": 95}
            ]
        },
        {
            "id": "osee_q4",
            "text": "Have you worked with heap exploitation or Use-After-Free vulnerabilities?",
            "category": "heap_exploitation",
            "weight": 2.5,
            "options": [
                {"text": "No experience", "score": 10},
                {"text": "Basic understanding of concepts", "score": 35},
                {"text": "Intermediate - Completed basic heap challenges", "score": 65},
                {"text": "Advanced - Exploited UAF in real-world software", "score": 100}
            ]
        },
        {
            "id": "osee_q5",
            "text": "What is your experience with kernel-mode exploitation?",
            "category": "kernel_exploitation",
            "weight": 2.0,
            "options": [
                {"text": "None - Never touched kernel exploitation", "score": 10},
                {"text": "Basic - Understand kernel vs user mode", "score": 40},
                {"text": "Intermediate - Completed HEVD or similar challenges", "score": 70},
                {"text": "Advanced - Exploited Windows kernel vulnerabilities", "score": 100}
            ]
        }
    ],
    "OSIR": [  # NEW - OffSec Incident Responder (Foundational)
        {
            "id": "osir_q1",
            "text": "How familiar are you with the incident response lifecycle?",
            "category": "ir_fundamentals",
            "weight": 1.8,
            "options": [
                {"text": "Not familiar - Don't know IR process", "score": 20},
                {"text": "Basic - Know NIST IR phases conceptually", "score": 50},
                {"text": "Intermediate - Have performed IR activities in labs", "score": 75},
                {"text": "Advanced - Regular IR experience in SOC/DFIR role", "score": 95}
            ]
        },
        {
            "id": "osir_q2",
            "text": "What is your experience with SIEM platforms (Splunk, ELK)?",
            "category": "siem",
            "weight": 2.0,
            "options": [
                {"text": "None - Never used a SIEM", "score": 15},
                {"text": "Basic - Can run simple searches", "score": 45},
                {"text": "Intermediate - Proficient with SPL queries and dashboards", "score": 75},
                {"text": "Advanced - Expert in threat hunting with SIEM", "score": 100}
            ]
        },
        {
            "id": "osir_q3",
            "text": "How comfortable are you with digital forensics (Windows/Linux artifacts)?",
            "category": "forensics",
            "weight": 2.2,
            "options": [
                {"text": "Not comfortable - No forensics experience", "score": 20},
                {"text": "Basic - Know common artifacts (Event Logs, Registry)", "score": 50},
                {"text": "Intermediate - Can analyze disk images with Autopsy", "score": 80},
                {"text": "Advanced - Expert in memory/disk forensics", "score": 100}
            ]
        },
        {
            "id": "osir_q4",
            "text": "What is your experience with MITRE ATT&CK framework?",
            "category": "threat_intelligence",
            "weight": 1.5,
            "options": [
                {"text": "None - Haven't used it", "score": 20},
                {"text": "Basic - Familiar with tactics and techniques", "score": 50},
                {"text": "Intermediate - Regularly map incidents to ATT&CK", "score": 80},
                {"text": "Advanced - Expert in TTP analysis and threat hunting", "score": 100}
            ]
        },
        {
            "id": "osir_q5",
            "text": "Have you completed any IR/forensics practice labs or challenges?",
            "category": "practice",
            "weight": 1.3,
            "options": [
                {"text": "None - No hands-on practice", "score": 10},
                {"text": "Basic - Completed a few TryHackMe rooms", "score": 40},
                {"text": "Intermediate - Boss of the SOC or CyberDefenders challenges", "score": 70},
                {"text": "Advanced - Multiple DFIR competitions or CTFs", "score": 90},
                {"text": "Expert - Real-world SOC/IR experience", "score": 100}
            ]
        }
    ]
}


if __name__ == "__main__":
    # Test the assessment manager
    print("🧪 Testing Assessment Manager...")
    print(f"📋 Supported certifications: {len(DEFAULT_QUESTIONS)}")
    
    manager = AssessmentManager(DEFAULT_QUESTIONS)
    
    # Test with OSCP
    print("\n" + "="*60)
    print("Testing OSCP Assessment")
    print("="*60)
    session = manager.start_assessment("test_user_123", "OSCP")
    
    if session:
        print(f"✅ Session created: {session.certification}")
        print(f"📝 Total questions: {len(session.questions)}")
        
        # Simulate answers
        test_answers = ["2", "3", "2", "3", "4"]
        
        for answer in test_answers:
            question = session.get_current_question()
            if question:
                print(f"\nQ: {question.text}")
                print(f"A: Option {answer}")
                session.submit_answer(answer)
        
        # Get results
        results = session.get_results_summary()
        print(f"\n📊 Results:")
        print(f"Score: {results['score']}%")
        print(f"Level: {results['skill_level']}")
        print(f"Strengths: {', '.join(results['strengths']) if results['strengths'] else 'None identified'}")
        print(f"Weaknesses: {', '.join(results['weaknesses']) if results['weaknesses'] else 'None identified'}")
    
    # Test with new certifications
    print("\n" + "="*60)
    print("Testing NEW Certifications")
    print("="*60)
    
    for cert in ["OSCC", "OSEE", "OSIR"]:
        questions = manager._create_questions(cert)
        print(f"\n✅ {cert}: {len(questions)} questions loaded")
    
    print("\n✅ All tests completed!")
    print(f"📋 Total certifications supported: {len(DEFAULT_QUESTIONS)}")
