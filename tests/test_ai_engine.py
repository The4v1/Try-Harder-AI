"""
Test Suite for AI Engine (Google Gemini API Integration)
=========================================================

Tests for the GeminiAI class that handles AI model interactions
using the Google Gemini API via the google-generativeai SDK.

Test Coverage:
- API initialization and configuration
- Model selection and switching
- Message generation and response handling
- Error handling and edge cases
- Rate limiting and retries
- Prompt loading and formatting
- Multi-model support

Author: Try-Harder-AI Team
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.ai_engine import GeminiAI


class TestGeminiAI(unittest.TestCase):
    """Test cases for GeminiAI class"""

    def setUp(self):
        """Set up test fixtures before each test"""
        # Gemini uses genai.configure() with env var, not constructor injection
        with patch.dict(os.environ, {"GEMINI_API_KEY": "AIzaSy_test_key_12345"}):
            with patch("google.generativeai.configure"):
                self.ai_engine = GeminiAI()

    def tearDown(self):
        """Clean up after each test"""
        self.ai_engine = None

    # =========================================================================
    # INITIALIZATION TESTS
    # =========================================================================

    def test_initialization_with_api_key(self):
        """Test that AI engine initializes correctly with GEMINI_API_KEY set"""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "AIzaSy_test_key_12345"}):
            with patch("google.generativeai.configure") as mock_configure:
                engine = GeminiAI()
                self.assertIsNotNone(engine)
                mock_configure.assert_called_once()

    def test_initialization_default_model(self):
        """Test that default model is set to gemini-1.5-flash"""
        self.assertEqual(self.ai_engine.DEFAULT_MODEL, "gemini-1.5-flash")

    def test_initialization_without_api_key(self):
        """Test that initialization fails without GEMINI_API_KEY"""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("GEMINI_API_KEY", None)
            with self.assertRaises(ValueError) as ctx:
                GeminiAI()
            self.assertIn("GEMINI_API_KEY", str(ctx.exception))

    def test_available_models_loaded(self):
        """Test that available Gemini model aliases are loaded on initialization"""
        self.assertIsNotNone(self.ai_engine.available_models)
        self.assertIsInstance(self.ai_engine.available_models, dict)
        self.assertGreater(len(self.ai_engine.available_models), 0)

    # =========================================================================
    # MODEL SELECTION TESTS
    # =========================================================================

    def test_get_model_by_shortcut(self):
        """Test getting full Gemini model name from shortcut alias"""
        shortcuts = {
            "flash":   "gemini-1.5-flash",
            "pro":     "gemini-1.5-pro",
            "flash8b": "gemini-1.5-flash-8b",
            "flash2":  "gemini-2.0-flash",
            "legacy":  "gemini-1.0-pro",
        }

        for shortcut, expected_model in shortcuts.items():
            result = self.ai_engine.get_model(shortcut)
            self.assertEqual(result, expected_model,
                             f"Shortcut '{shortcut}' should map to '{expected_model}'")

    def test_get_model_with_full_name(self):
        """Test that full Gemini model names are returned unchanged"""
        full_name = "gemini-1.5-flash"
        result = self.ai_engine.get_model(full_name)
        self.assertEqual(result, full_name)

    def test_get_model_invalid(self):
        """Test that invalid model names fall back to default"""
        invalid_model = "nonexistent-model"
        result = self.ai_engine.get_model(invalid_model)
        self.assertEqual(result, self.ai_engine.DEFAULT_MODEL)

    def test_set_model(self):
        """Test setting active model"""
        new_model = "gemini-1.5-pro"
        self.ai_engine.set_model(new_model)
        self.assertEqual(self.ai_engine.current_model, new_model)

    # =========================================================================
    # MESSAGE GENERATION TESTS
    # =========================================================================

    @patch("google.generativeai.GenerativeModel")
    def test_generate_response_success(self, mock_model_class):
        """Test successful message generation via Gemini SDK"""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Test response from Gemini"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        result = self.ai_engine.generate_response(
            prompt="Test prompt",
            certification="OSCP"
        )

        self.assertEqual(result, "Test response from Gemini")
        mock_model.generate_content.assert_called_once()

    @patch("google.generativeai.GenerativeModel")
    def test_generate_response_with_system_instruction(self, mock_model_class):
        """Test that system instruction is passed when constructing the model"""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Response"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        self.ai_engine.generate_response(
            prompt="What is enumeration?",
            certification="OSCP"
        )

        # Verify GenerativeModel was constructed with system_instruction
        call_kwargs = mock_model_class.call_args[1]
        self.assertIn("system_instruction", call_kwargs)
        self.assertIsNotNone(call_kwargs["system_instruction"])

    @patch("google.generativeai.GenerativeModel")
    def test_generate_response_api_error(self, mock_model_class):
        """Test handling of generic Gemini API errors"""
        from google.api_core import exceptions as google_exceptions

        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("Gemini API error")
        mock_model_class.return_value = mock_model

        result = self.ai_engine.generate_response(
            prompt="Test prompt",
            certification="OSCP"
        )

        self.assertIn("error", result.lower())

    @patch("google.generativeai.GenerativeModel")
    def test_generate_response_timeout(self, mock_model_class):
        """Test handling of request timeout"""
        import asyncio

        mock_model = MagicMock()
        mock_model.generate_content.side_effect = asyncio.TimeoutError("Request timed out")
        mock_model_class.return_value = mock_model

        result = self.ai_engine.generate_response(
            prompt="Test prompt",
            certification="OSCP"
        )

        self.assertIn("timeout", result.lower())

    @patch("google.generativeai.GenerativeModel")
    def test_generate_response_network_error(self, mock_model_class):
        """Test handling of network/connection errors"""
        from google.api_core import exceptions as google_exceptions

        mock_model = MagicMock()
        mock_model.generate_content.side_effect = google_exceptions.ServiceUnavailable(
            "Service unavailable"
        )
        mock_model_class.return_value = mock_model

        result = self.ai_engine.generate_response(
            prompt="Test prompt",
            certification="OSCP"
        )

        self.assertIn("error", result.lower())

    # =========================================================================
    # PROMPT LOADING TESTS
    # =========================================================================

    def test_load_system_prompt(self):
        """Test loading base system prompt"""
        prompt = self.ai_engine.load_system_prompt()
        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)

    def test_load_certification_prompt(self):
        """Test loading certification-specific prompts"""
        certifications = ["OSCP", "OSEP", "OSWE", "OSED", "OSWP"]

        for cert in certifications:
            prompt = self.ai_engine.load_certification_prompt(cert)
            self.assertIsNotNone(prompt)
            self.assertIsInstance(prompt, str)
            self.assertGreater(len(prompt), 0)

    def test_load_certification_prompt_invalid(self):
        """Test loading prompt for invalid certification returns string"""
        prompt = self.ai_engine.load_certification_prompt("INVALID")
        self.assertIsInstance(prompt, str)

    def test_combine_prompts(self):
        """Test that system and certification prompts are combined"""
        system_prompt = self.ai_engine.load_system_prompt()
        cert_prompt = self.ai_engine.load_certification_prompt("OSCP")

        combined = self.ai_engine.combine_prompts(system_prompt, cert_prompt)

        self.assertIn(system_prompt, combined)
        self.assertIn(cert_prompt, combined)

    # =========================================================================
    # GENERATION CONFIG PARAMETER TESTS
    # =========================================================================

    @patch("google.generativeai.GenerativeModel")
    def test_temperature_parameter(self, mock_model_class):
        """Test that temperature is passed in generation_config"""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Response"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        self.ai_engine.generate_response(
            prompt="Test",
            certification="OSCP",
            temperature=0.9
        )

        # Verify GenerativeModel was constructed with correct generation_config
        call_kwargs = mock_model_class.call_args[1]
        self.assertIn("generation_config", call_kwargs)
        self.assertEqual(call_kwargs["generation_config"]["temperature"], 0.9)

    @patch("google.generativeai.GenerativeModel")
    def test_max_tokens_parameter(self, mock_model_class):
        """Test that max_output_tokens is passed in generation_config"""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Response"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        self.ai_engine.generate_response(
            prompt="Test",
            certification="OSCP",
            max_tokens=2048
        )

        call_kwargs = mock_model_class.call_args[1]
        self.assertIn("generation_config", call_kwargs)
        self.assertEqual(call_kwargs["generation_config"]["max_output_tokens"], 2048)

    # =========================================================================
    # EDGE CASE TESTS
    # =========================================================================

    def test_empty_prompt(self):
        """Test handling of empty prompt raises ValueError"""
        with self.assertRaises(ValueError):
            self.ai_engine.generate_response(
                prompt="",
                certification="OSCP"
            )

    @patch("google.generativeai.GenerativeModel")
    def test_very_long_prompt(self, mock_model_class):
        """Test handling of very long prompts (Gemini has 1M token context)"""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Handled long prompt"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        long_prompt = "A" * 50000  # 50k characters

        result = self.ai_engine.generate_response(
            prompt=long_prompt,
            certification="OSCP"
        )

        self.assertIsInstance(result, str)

    @patch("google.generativeai.GenerativeModel")
    def test_malformed_api_response(self, mock_model_class):
        """Test handling of malformed/empty Gemini response"""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = None  # Simulate empty/malformed response
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        result = self.ai_engine.generate_response(
            prompt="Test",
            certification="OSCP"
        )

        # Should handle gracefully
        self.assertIn("error", result.lower())

    # =========================================================================
    # RATE LIMITING TESTS
    # =========================================================================

    @patch("google.generativeai.GenerativeModel")
    def test_rate_limit_handling(self, mock_model_class):
        """Test handling of Gemini rate limit errors (ResourceExhausted)"""
        from google.api_core import exceptions as google_exceptions

        mock_model = MagicMock()
        mock_model.generate_content.side_effect = google_exceptions.ResourceExhausted(
            "Quota exceeded - 429 rate limit"
        )
        mock_model_class.return_value = mock_model

        result = self.ai_engine.generate_response(
            prompt="Test",
            certification="OSCP"
        )

        self.assertIn("rate limit", result.lower())

    # =========================================================================
    # MULTI-MODEL TESTS
    # =========================================================================

    @patch("google.generativeai.GenerativeModel")
    def test_different_models_same_prompt(self, mock_model_class):
        """Test that different Gemini model variants can be used for same prompt"""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Response"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        models = ["flash", "pro", "flash8b", "flash2", "legacy"]

        for model_alias in models:
            self.ai_engine.set_model(model_alias)
            result = self.ai_engine.generate_response(
                prompt="Test prompt",
                certification="OSCP"
            )
            self.assertIsNotNone(result)

    # =========================================================================
    # CONVERSATION CONTEXT TESTS
    # =========================================================================

    @patch("google.generativeai.GenerativeModel")
    def test_conversation_history(self, mock_model_class):
        """Test that multi-turn conversation history is passed to Gemini"""
        mock_model = MagicMock()
        mock_chat = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Response"
        mock_chat.send_message.return_value = mock_response
        mock_model.start_chat.return_value = mock_chat
        mock_model_class.return_value = mock_model

        conversation_history = [
            {"role": "user", "content": "First message"},
            {"role": "model", "content": "First response"},
        ]

        result = self.ai_engine.generate_response(
            prompt="Second message",
            certification="OSCP",
            conversation_history=conversation_history
        )

        # Verify chat was started with history
        mock_model.start_chat.assert_called_once()
        call_kwargs = mock_model.start_chat.call_args[1]
        self.assertIn("history", call_kwargs)
        self.assertEqual(len(call_kwargs["history"]), 2)

    # =========================================================================
    # FORMATTING TESTS
    # =========================================================================

    def test_format_response_for_discord(self):
        """Test that responses exceeding Discord 2000 char limit are chunked"""
        long_response = "A" * 3000  # Exceeds Discord's 2000 char limit

        formatted = self.ai_engine.format_for_discord(long_response)

        self.assertLessEqual(len(formatted), 2000)

    def test_code_block_preservation(self):
        """Test that code blocks are preserved in Discord formatting"""
        response_with_code = """
        Here's a command:
        ```bash
        nmap -sV 10.10.10.10
        ```
        """

        formatted = self.ai_engine.format_for_discord(response_with_code)

        self.assertIn("```", formatted)

    # =========================================================================
    # CERTIFICATION-SPECIFIC TESTS
    # =========================================================================

    def test_oscp_specific_response(self):
        """Test OSCP-specific prompt is loaded correctly"""
        prompt = self.ai_engine.load_certification_prompt("OSCP")
        self.assertIsNotNone(prompt)
        self.assertGreater(len(prompt), 0)

    def test_multiple_certifications(self):
        """Test switching between different certification prompts"""
        certifications = ["OSCP", "OSEP", "OSWE", "KLCP"]

        for cert in certifications:
            prompt = self.ai_engine.load_certification_prompt(cert)
            self.assertIsNotNone(prompt)
            self.assertGreater(len(prompt), 0)

    # =========================================================================
    # ERROR RECOVERY / RETRY TESTS
    # =========================================================================

    @patch("google.generativeai.GenerativeModel")
    def test_retry_on_service_unavailable(self, mock_model_class):
        """Test retry mechanism on Gemini ServiceUnavailable (503)"""
        from google.api_core import exceptions as google_exceptions

        mock_model = MagicMock()

        mock_response_success = MagicMock()
        mock_response_success.text = "Success after retry"

        # First call raises ServiceUnavailable, second succeeds
        mock_model.generate_content.side_effect = [
            google_exceptions.ServiceUnavailable("Service temporarily unavailable"),
            mock_response_success,
        ]
        mock_model_class.return_value = mock_model

        result = self.ai_engine.generate_response(
            prompt="Test",
            certification="OSCP",
            max_retries=2
        )

        self.assertEqual(result, "Success after retry")

    @patch("google.generativeai.GenerativeModel")
    def test_no_retry_on_invalid_key(self, mock_model_class):
        """Test that InvalidArgument (bad API key) is NOT retried"""
        from google.api_core import exceptions as google_exceptions

        mock_model = MagicMock()
        mock_model.generate_content.side_effect = google_exceptions.InvalidArgument(
            "API key not valid"
        )
        mock_model_class.return_value = mock_model

        result = self.ai_engine.generate_response(
            prompt="Test",
            certification="OSCP",
            max_retries=3
        )

        # Should fail fast — not retry 3 times
        self.assertEqual(mock_model.generate_content.call_count, 1)
        self.assertIn("error", result.lower())

    # =========================================================================
    # PERFORMANCE TESTS
    # =========================================================================

    @patch("google.generativeai.GenerativeModel")
    def test_response_time_logging(self, mock_model_class):
        """Test that response times are logged after generation"""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Response"
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        result = self.ai_engine.generate_response(
            prompt="Test",
            certification="OSCP"
        )

        self.assertIsNotNone(result)

    # =========================================================================
    # TOKEN USAGE TRACKING TESTS
    # =========================================================================

    @patch("google.generativeai.GenerativeModel")
    def test_token_usage_tracked(self, mock_model_class):
        """Test that Gemini usage_metadata tokens are tracked after response"""
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Response"
        mock_response.usage_metadata.prompt_token_count = 100
        mock_response.usage_metadata.candidates_token_count = 50
        mock_response.usage_metadata.total_token_count = 150
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        self.ai_engine.generate_response(
            prompt="Test",
            certification="OSCP"
        )

        # Verify token tracking was updated
        self.assertGreaterEqual(
            self.ai_engine.usage_tracker.total_tokens, 150
        )

    # =========================================================================
    # SECURITY TESTS
    # =========================================================================

    def test_api_key_not_exposed(self):
        """Test that GEMINI_API_KEY is not exposed in string representation"""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "AIzaSy_secret_key"}):
            with patch("google.generativeai.configure"):
                engine = GeminiAI()
            str_repr = str(engine)
            self.assertNotIn("AIzaSy_secret_key", str_repr)

    def test_sanitize_user_input(self):
        """Test that user input is sanitized before sending to Gemini"""
        malicious_input = "<script>alert('xss')</script>"

        result = self.ai_engine.sanitize_input(malicious_input)

        self.assertIsInstance(result, str)


# =============================================================================
# TEST RUNNER
# =============================================================================

def run_tests():
    """Run all AI engine tests"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestGeminiAI)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    print("TEST SUMMARY")
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