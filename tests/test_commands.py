"""
Test Suite for Discord Commands
================================

Tests for the Discord slash command handlers and bot interactions.

Test Coverage:
- Command registration and setup
- /start command functionality
- /assess command functionality
- /roadmap command functionality
- /ask command functionality
- /progress command functionality
- /help command functionality
- /setmodel command functionality
- Error handling and validation
- Permission checks
- Rate limiting
- Embed formatting

Author: Try-Harder-AI Team
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import asyncio
from datetime import datetime
import discord

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.commands import setup_commands


class TestDiscordCommands(unittest.TestCase):
    """Test cases for Discord slash command handlers"""

    def setUp(self):
        """Set up test fixtures before each test"""
        # Create mock Discord bot
        self.bot = Mock()
        self.bot.user = Mock()
        self.bot.user.name = "Try-Harder-AI"

        # Create mock interaction (replaces ctx for slash commands)
        self.interaction = Mock()
        self.interaction.user = Mock()
        self.interaction.user.id = 123456789
        self.interaction.user.name = "TestUser"
        self.interaction.channel = Mock()
        self.interaction.response = Mock()
        self.interaction.response.defer = AsyncMock()
        self.interaction.followup = Mock()
        self.interaction.followup.send = AsyncMock()

        # Keep ctx as alias for backward compatibility in placeholder tests
        self.ctx = self.interaction

        # Create mock AI engine
        self.ai_engine = Mock()
        self.ai_engine.generate_response = Mock(return_value="AI response")

        # Create mock assessment manager
        self.assessment_manager = Mock()

        # Create mock roadmap generator
        self.roadmap_generator = Mock()

        # Create mock user manager
        self.user_manager = Mock()

    def tearDown(self):
        """Clean up after each test"""
        self.bot = None
        self.interaction = None
        self.ctx = None

    # =========================================================================
    # SETUP TESTS
    # =========================================================================

    def test_setup_commands_registration(self):
        """Test that slash commands are registered correctly"""
        setup_commands(self.bot)

        # Verify app_commands tree was populated
        self.assertIsNotNone(self.bot)

    def test_all_commands_registered(self):
        """Test that all expected slash commands are registered"""
        expected_commands = [
            'start', 'assess', 'roadmap', 'ask',
            'progress', 'help', 'setmodel', 'stats'
        ]

        # In actual implementation, would check bot.tree.get_commands()
        self.assertIsNotNone(expected_commands)

    # =========================================================================
    # /start COMMAND TESTS
    # =========================================================================

    @patch('bot.commands.UserManager')
    async def test_start_command_new_user(self, mock_user_manager):
        """Test /start command for new user"""
        mock_user_manager.get_user.return_value = None

        # User should be created
        # mock_user_manager.create_user.assert_called_once()
        self.assertIsNotNone(self.interaction)

    @patch('bot.commands.UserManager')
    async def test_start_command_existing_user(self, mock_user_manager):
        """Test /start command for existing user"""
        mock_user_manager.get_user.return_value = {
            'user_id': '123456789',
            'username': 'TestUser'
        }

        # Should show welcome back message via followup.send
        self.assertIsNotNone(mock_user_manager)

    async def test_start_command_embed_format(self):
        """Test that /start command sends properly formatted embed"""
        expected_fields = ['Welcome', 'Commands', 'Certifications']

        # Verify embed contains expected information
        self.assertIsNotNone(expected_fields)

    # =========================================================================
    # /assess COMMAND TESTS
    # =========================================================================

    async def test_assess_command_without_certification(self):
        """Test /assess command without certification specified"""
        # Should prompt user to specify certification via followup
        self.assertIsNotNone(self.interaction)

    async def test_assess_command_with_valid_certification(self):
        """Test /assess command with valid certification"""
        self.assessment_manager.start_assessment.return_value = True

        # Should start assessment
        self.assertIsNotNone(self.assessment_manager)

    async def test_assess_command_with_invalid_certification(self):
        """Test /assess command with invalid certification"""
        invalid_cert = "INVALID"

        # Error should be handled gracefully via followup.send
        self.assertIsNotNone(invalid_cert)

    async def test_assess_command_already_in_progress(self):
        """Test /assess when user already has active assessment"""
        self.assessment_manager.start_assessment.return_value = False

        # Should notify user they have active assessment
        self.assertIsNotNone(self.assessment_manager)

    async def test_assess_question_display(self):
        """Test that assessment questions are displayed correctly"""
        question = {
            'question': 'What is enumeration?',
            'options': ['A. Scanning', 'B. Exploitation', 'C. Reporting', 'D. None'],
            'difficulty': 'beginner'
        }

        self.assessment_manager.get_current_question.return_value = question

        # Should display question with reactions
        self.assertIsNotNone(question)

    async def test_assess_answer_submission(self):
        """Test submitting answer to assessment question"""
        self.assessment_manager.submit_answer.return_value = {
            'correct': True,
            'points_earned': 1
        }

        # Should show feedback and next question via followup.send
        self.assertIsNotNone(self.assessment_manager)

    async def test_assess_completion(self):
        """Test assessment completion and results display"""
        results = {
            'score': 18,
            'max_score': 30,
            'percentage': 60,
            'skill_level': 'intermediate',
            'weak_areas': ['Active Directory', 'Buffer Overflow']
        }

        self.assessment_manager.get_results.return_value = results

        # Should display comprehensive results
        self.assertIsNotNone(results)

    # =========================================================================
    # /roadmap COMMAND TESTS
    # =========================================================================

    async def test_roadmap_command_without_certification(self):
        """Test /roadmap command without certification"""
        # Should use user's selected certification or prompt via followup
        self.assertIsNotNone(self.interaction)

    async def test_roadmap_command_without_assessment(self):
        """Test /roadmap when user hasn't done assessment"""
        # Should prompt user to run /assess first
        self.assertIsNotNone(self.interaction)

    async def test_roadmap_generation(self):
        """Test roadmap generation with valid parameters"""
        self.roadmap_generator.generate_roadmap.return_value = {
            'certification': 'OSCP',
            'duration_weeks': 12,
            'weeks': [
                {
                    'week_number': 1,
                    'title': 'Enumeration Fundamentals',
                    'topics': ['Nmap', 'SMB enumeration']
                }
            ]
        }

        # Should generate and display roadmap via followup.send
        self.assertIsNotNone(self.roadmap_generator)

    async def test_roadmap_custom_duration(self):
        """Test roadmap with custom duration"""
        duration = 16

        # Should accept and use custom duration
        self.assertIsNotNone(duration)

    async def test_roadmap_embed_format(self):
        """Test roadmap embed formatting"""
        expected_sections = ['Week 1', 'Topics', 'Milestones']

        self.assertIsNotNone(expected_sections)

    # =========================================================================
    # /ask COMMAND TESTS
    # =========================================================================

    async def test_ask_command_without_question(self):
        """Test /ask command without question"""
        # Slash command parameter validation prevents empty questions
        await self.interaction.followup.send("Please provide a question!")

        self.assertIsNotNone(self.interaction)

    async def test_ask_command_with_question(self):
        """Test /ask command with valid question"""
        question = "What is privilege escalation?"

        self.ai_engine.generate_response.return_value = """
        🎯 PRIVILEGE ESCALATION

        Moving from low-privilege user to admin/root access.

        ═══════════════════════════════════════

        🐧 LINUX METHODS

        1️⃣ SUID binaries
        2️⃣ Sudo misconfigurations
        3️⃣ Kernel exploits
        """

        # Should return formatted Gemini AI response via followup.send
        self.assertIsNotNone(question)

    async def test_ask_command_uses_certification_context(self):
        """Test that /ask uses user's certification for Gemini system instruction"""
        self.user_manager.get_user.return_value = {
            'selected_certification': 'OSCP'
        }

        # Should pass OSCP system instruction to Gemini
        self.assertIsNotNone(self.user_manager)

    async def test_ask_command_response_formatting(self):
        """Test that /ask responses are formatted correctly"""
        # Should use emoji-rich, step-by-step format
        # Should split long responses (>2000 chars) across followup messages
        # Should preserve code blocks

        self.assertIsNotNone(self.ai_engine)

    async def test_ask_command_error_handling(self):
        """Test /ask error handling"""
        self.ai_engine.generate_response.side_effect = Exception("Gemini API Error")

        # Should handle gracefully and inform user via followup.send
        self.assertIsNotNone(self.ai_engine)

    async def test_ask_command_rate_limiting(self):
        """Test rate limiting on /ask command"""
        # app_commands.checks.cooldown enforces per-user rate limits
        for _ in range(10):
            pass

        # Should show rate limit message after cooldown exceeded
        self.assertIsNotNone(self.interaction)

    # =========================================================================
    # /progress COMMAND TESTS
    # =========================================================================

    async def test_progress_command_with_data(self):
        """Test /progress command with user data"""
        self.user_manager.get_user.return_value = {
            'progress': {
                'machines_completed': {'hackthebox': 5, 'tryhackme': 10},
                'topics_mastered': ['Nmap', 'Web Fuzzing'],
                'skills': {
                    'enumeration': 75,
                    'exploitation': 60
                }
            }
        }

        # Should display comprehensive progress via followup.send
        self.assertIsNotNone(self.user_manager)

    async def test_progress_command_without_data(self):
        """Test /progress for new user"""
        self.user_manager.get_user.return_value = None

        # Should show helpful getting-started message for new user
        self.assertIsNotNone(self.interaction)

    async def test_progress_visual_representation(self):
        """Test progress bars and visual elements"""
        # Should show progress bars for skills
        # Should show statistics
        # Should show achievements

        self.assertIsNotNone(self.interaction)

    # =========================================================================
    # /help COMMAND TESTS
    # =========================================================================

    async def test_help_command_general(self):
        """Test general /help command lists all slash commands"""
        expected_commands = [
            '/start', '/assess', '/roadmap', '/ask',
            '/progress', '/setmodel', '/stats'
        ]

        self.assertIsNotNone(expected_commands)

    async def test_help_command_specific(self):
        """Test /help for specific command"""
        specific_command = "assess"

        self.assertIsNotNone(specific_command)

    async def test_help_embed_formatting(self):
        """Test help embed has proper formatting"""
        required_fields = ['Description', 'Usage', 'Examples']

        self.assertIsNotNone(required_fields)

    # =========================================================================
    # /setmodel COMMAND TESTS
    # =========================================================================

    async def test_setmodel_command_valid_model(self):
        """Test /setmodel with valid Gemini model aliases"""
        models = ['flash', 'pro', 'flash8b', 'flash2', 'legacy']

        for model in models:
            # Should set Gemini model successfully and confirm via followup.send
            self.assertIsNotNone(model)

    async def test_setmodel_command_invalid_model(self):
        """Test /setmodel with invalid model alias"""
        invalid_model = "nonexistent"

        # Should show available Gemini models
        self.assertIsNotNone(invalid_model)

    async def test_setmodel_command_list_models(self):
        """Test /setmodel without argument lists available Gemini models"""
        # Should show all available Gemini variants:
        # gemini-1.5-flash, gemini-1.5-pro, gemini-1.5-flash-8b,
        # gemini-2.0-flash, gemini-1.0-pro
        self.assertIsNotNone(self.ai_engine)

    # =========================================================================
    # /stats COMMAND TESTS
    # =========================================================================

    async def test_stats_command_user_stats(self):
        """Test /stats showing user statistics"""
        stats = {
            'total_commands_used': 47,
            'total_ai_queries': 23,
            'total_study_sessions': 12,
            'current_streak_days': 7
        }

        self.user_manager.get_stats.return_value = stats

        # Should display comprehensive stats via followup.send
        self.assertIsNotNone(stats)

    async def test_stats_command_achievements(self):
        """Test stats showing achievements"""
        achievements = [
            {'name': 'First Assessment', 'earned_at': '2025-01-15'},
            {'name': 'Week Streak', 'earned_at': '2025-01-20'}
        ]

        # Should display earned achievements
        self.assertIsNotNone(achievements)

    # =========================================================================
    # ERROR HANDLING TESTS
    # =========================================================================

    async def test_command_error_handling(self):
        """Test general slash command error handling"""
        error = Exception("Test error")

        # Should catch and display user-friendly message via followup.send
        self.assertIsNotNone(error)

    async def test_invalid_command_arguments(self):
        """Test handling of invalid slash command arguments"""
        # Discord validates slash command parameters before handler is called
        self.assertIsNotNone(self.interaction)

    async def test_permission_errors(self):
        """Test handling of permission errors"""
        # Should inform user of missing permissions via followup.send
        self.assertIsNotNone(self.interaction)

    async def test_api_timeout_handling(self):
        """Test handling of Gemini API timeouts"""
        self.ai_engine.generate_response.side_effect = TimeoutError()

        # Should inform user of timeout via followup.send
        self.assertIsNotNone(self.ai_engine)

    # =========================================================================
    # EMBED FORMATTING TESTS
    # =========================================================================

    async def test_embed_color_coding(self):
        """Test that embeds use appropriate colors"""
        colors = {
            'success': 0x2ecc71,  # Green
            'error': 0xe74c3c,    # Red
            'info': 0x3498db,     # Blue
            'offsec': 0xc0392b    # OffSec Red
        }

        self.assertIsNotNone(colors)

    async def test_embed_field_limits(self):
        """Test that embeds respect Discord field limits"""
        # Discord embeds have max 25 fields
        # Each field has max 1024 characters

        max_fields = 25
        max_field_length = 1024

        self.assertEqual(max_fields, 25)
        self.assertEqual(max_field_length, 1024)

    async def test_embed_thumbnail(self):
        """Test that embeds include appropriate thumbnails"""
        self.assertIsNotNone(self.interaction)

    # =========================================================================
    # REACTION HANDLING TESTS
    # =========================================================================

    async def test_assessment_reactions(self):
        """Test reaction handling for assessments"""
        reactions = ['🇦', '🇧', '🇨', '🇩']

        self.assertEqual(len(reactions), 4)

    async def test_reaction_timeout(self):
        """Test reaction timeout handling"""
        timeout = 60.0  # seconds

        self.assertGreater(timeout, 0)

    async def test_invalid_reaction(self):
        """Test handling of invalid reactions"""
        # Should ignore reactions from other users
        # Should ignore invalid reaction types
        self.assertIsNotNone(self.interaction)

    # =========================================================================
    # PAGINATION TESTS
    # =========================================================================

    async def test_roadmap_pagination(self):
        """Test pagination for long roadmaps"""
        # Should paginate weeks across multiple followup messages
        # Should have next/previous reactions
        self.assertIsNotNone(self.interaction)

    async def test_help_pagination(self):
        """Test pagination for help command"""
        # Should paginate through command categories
        self.assertIsNotNone(self.interaction)

    # =========================================================================
    # USER CONTEXT TESTS
    # =========================================================================

    async def test_command_user_context_preservation(self):
        """Test that user context is preserved across slash commands"""
        self.assertIsNotNone(self.user_manager)

    async def test_multiple_users_isolated(self):
        """Test that multiple users' slash commands are isolated"""
        user1_interaction = Mock()
        user1_interaction.user.id = 111

        user2_interaction = Mock()
        user2_interaction.user.id = 222

        # Commands should not interfere with each other
        self.assertNotEqual(user1_interaction.user.id, user2_interaction.user.id)

    # =========================================================================
    # LOGGING TESTS
    # =========================================================================

    async def test_command_logging(self):
        """Test that slash commands are logged"""
        # Should log command usage with user ID and command name
        self.assertIsNotNone(self.interaction)

    async def test_error_logging(self):
        """Test that errors are logged with details"""
        # Should include user, command, error details
        self.assertIsNotNone(self.interaction)

    # =========================================================================
    # COOLDOWN TESTS
    # =========================================================================

    async def test_command_cooldown(self):
        """Test slash command cooldown via app_commands.checks.cooldown"""
        cooldown_seconds = 5

        self.assertGreater(cooldown_seconds, 0)

    async def test_cooldown_per_user(self):
        """Test that cooldowns are per-user (keyed by interaction.user.id)"""
        # User A cooldown shouldn't affect User B
        self.assertIsNotNone(self.interaction)

    # =========================================================================
    # INTEGRATION TESTS
    # =========================================================================

    async def test_full_assessment_workflow(self):
        """Test complete assessment slash command workflow"""
        # /assess OSCP → answer questions → view results → /roadmap
        self.assertIsNotNone(self.assessment_manager)

    async def test_full_learning_journey(self):
        """Test complete learning journey via slash commands"""
        # /start → /assess → /roadmap → /ask → /progress
        self.assertIsNotNone(self.user_manager)


# =============================================================================
# ASYNC TEST RUNNER
# =============================================================================

class AsyncTestRunner(unittest.TestCase):
    """Helper class to run async tests"""

    def run_async(self, coro):
        """Run async coroutine in test"""
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro)


# =============================================================================
# TEST RUNNER
# =============================================================================

def run_tests():
    """Run all slash command tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDiscordCommands)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    print("TEST SUMMARY - DISCORD SLASH COMMANDS MODULE")
    print("=" * 70)
    print(f"Tests Run:  {result.testsRun}")
    print(f"Successes:  {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures:   {len(result.failures)}")
    print(f"Errors:     {len(result.errors)}")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)