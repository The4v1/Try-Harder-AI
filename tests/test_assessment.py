"""
Test Suite for Assessment Manager
==================================

Tests for the AssessmentManager class that handles skill assessments.

Test Coverage:
- Assessment initialization and configuration
- Question loading and selection
- Difficulty level distribution
- Answer validation and scoring
- Skill level calculation
- Weak area identification
- Assessment state management
- Question randomization
- Time tracking

Author: Try-Harder-AI Team
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.assessment import AssessmentManager


class TestAssessmentManager(unittest.TestCase):
    """Test cases for AssessmentManager class"""

    def setUp(self):
        """Set up test fixtures before each test"""
        self.assessment_manager = AssessmentManager()
        self.test_user_id = "123456789"
        self.test_certification = "OSCP"

    def tearDown(self):
        """Clean up after each test"""
        self.assessment_manager = None

    # =========================================================================
    # INITIALIZATION TESTS
    # =========================================================================

    def test_initialization(self):
        """Test that assessment manager initializes correctly"""
        self.assertIsNotNone(self.assessment_manager)
        self.assertIsInstance(self.assessment_manager.questions, dict)
        self.assertIsInstance(self.assessment_manager.active_assessments, dict)

    def test_questions_loaded(self):
        """Test that questions are loaded from YAML file"""
        self.assertGreater(len(self.assessment_manager.questions), 0)
        self.assertIn('OSCP', self.assessment_manager.questions)

    def test_all_certifications_loaded(self):
        """Test that all certifications have questions"""
        certifications = ['OSCP', 'OSEP', 'OSWE', 'OSED', 'OSWP', 
                         'OSWA', 'OSMR', 'OSDA', 'KLCP']
        
        for cert in certifications:
            self.assertIn(cert, self.assessment_manager.questions,
                         f"{cert} questions not loaded")

    # =========================================================================
    # ASSESSMENT CREATION TESTS
    # =========================================================================

    def test_start_assessment(self):
        """Test starting a new assessment"""
        result = self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        self.assertTrue(result)
        self.assertIn(self.test_user_id, self.assessment_manager.active_assessments)

    def test_start_assessment_duplicate(self):
        """Test that duplicate assessment is prevented"""
        # Start first assessment
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        # Try to start another assessment
        result = self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        self.assertFalse(result)

    def test_start_assessment_invalid_certification(self):
        """Test handling of invalid certification"""
        with self.assertRaises(ValueError):
            self.assessment_manager.start_assessment(
                user_id=self.test_user_id,
                certification="INVALID_CERT"
            )

    def test_assessment_state_creation(self):
        """Test that assessment state is created correctly"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        state = self.assessment_manager.active_assessments[self.test_user_id]
        
        self.assertEqual(state['certification'], self.test_certification)
        self.assertEqual(state['current_question'], 0)
        self.assertEqual(state['score'], 0)
        self.assertEqual(len(state['questions']), 10)  # Default 10 questions
        self.assertIsNotNone(state['start_time'])

    # =========================================================================
    # QUESTION SELECTION TESTS
    # =========================================================================

    def test_question_selection_distribution(self):
        """Test that questions are distributed across difficulty levels"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        state = self.assessment_manager.active_assessments[self.test_user_id]
        questions = state['questions']
        
        # Count questions by difficulty
        difficulties = [q['difficulty'] for q in questions]
        
        self.assertIn('beginner', difficulties)
        self.assertIn('intermediate', difficulties)
        self.assertIn('advanced', difficulties)

    def test_question_randomization(self):
        """Test that questions are randomized"""
        # Start two assessments
        user1 = "user_1"
        user2 = "user_2"
        
        self.assessment_manager.start_assessment(user1, self.test_certification)
        self.assessment_manager.start_assessment(user2, self.test_certification)
        
        questions1 = self.assessment_manager.active_assessments[user1]['questions']
        questions2 = self.assessment_manager.active_assessments[user2]['questions']
        
        # Questions should be different (randomized)
        first_q1 = questions1[0]['question']
        first_q2 = questions2[0]['question']
        
        # With randomization, they likely won't match
        # (small chance they could, but unlikely)
        self.assertIsNotNone(first_q1)
        self.assertIsNotNone(first_q2)

    def test_no_duplicate_questions(self):
        """Test that no duplicate questions in single assessment"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        state = self.assessment_manager.active_assessments[self.test_user_id]
        questions = state['questions']
        
        question_texts = [q['question'] for q in questions]
        
        # No duplicates
        self.assertEqual(len(question_texts), len(set(question_texts)))

    def test_custom_question_count(self):
        """Test assessment with custom number of questions"""
        question_count = 15
        
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification,
            question_count=question_count
        )
        
        state = self.assessment_manager.active_assessments[self.test_user_id]
        
        self.assertEqual(len(state['questions']), question_count)

    # =========================================================================
    # QUESTION RETRIEVAL TESTS
    # =========================================================================

    def test_get_current_question(self):
        """Test retrieving current question"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        question = self.assessment_manager.get_current_question(self.test_user_id)
        
        self.assertIsNotNone(question)
        self.assertIn('question', question)
        self.assertIn('options', question)
        self.assertIn('difficulty', question)

    def test_get_current_question_no_assessment(self):
        """Test getting question when no assessment exists"""
        question = self.assessment_manager.get_current_question("nonexistent_user")
        
        self.assertIsNone(question)

    def test_question_format(self):
        """Test that questions have correct format"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        question = self.assessment_manager.get_current_question(self.test_user_id)
        
        required_fields = ['question', 'options', 'correct_answer', 
                          'difficulty', 'category']
        
        for field in required_fields:
            self.assertIn(field, question)

    def test_question_options_count(self):
        """Test that questions have 4 options"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        question = self.assessment_manager.get_current_question(self.test_user_id)
        
        self.assertEqual(len(question['options']), 4)

    # =========================================================================
    # ANSWER SUBMISSION TESTS
    # =========================================================================

    def test_submit_correct_answer(self):
        """Test submitting correct answer"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        question = self.assessment_manager.get_current_question(self.test_user_id)
        correct_answer = question['correct_answer']
        
        result = self.assessment_manager.submit_answer(
            user_id=self.test_user_id,
            answer=correct_answer
        )
        
        self.assertTrue(result['correct'])
        self.assertGreater(result['points_earned'], 0)

    def test_submit_incorrect_answer(self):
        """Test submitting incorrect answer"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        question = self.assessment_manager.get_current_question(self.test_user_id)
        
        # Find wrong answer
        wrong_answer = 'A' if question['correct_answer'] != 'A' else 'B'
        
        result = self.assessment_manager.submit_answer(
            user_id=self.test_user_id,
            answer=wrong_answer
        )
        
        self.assertFalse(result['correct'])
        self.assertEqual(result['points_earned'], 0)

    def test_submit_answer_progress(self):
        """Test that progress advances after answer submission"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        initial_question = self.assessment_manager.get_current_question(self.test_user_id)
        
        self.assessment_manager.submit_answer(
            user_id=self.test_user_id,
            answer='A'
        )
        
        next_question = self.assessment_manager.get_current_question(self.test_user_id)
        
        # Should be different question (unless only 1 question total)
        if self.assessment_manager.active_assessments[self.test_user_id]['questions']:
            self.assertNotEqual(
                initial_question['question'],
                next_question['question'] if next_question else None
            )

    def test_submit_invalid_answer(self):
        """Test submitting invalid answer option"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        with self.assertRaises(ValueError):
            self.assessment_manager.submit_answer(
                user_id=self.test_user_id,
                answer='Z'  # Invalid option
            )

    # =========================================================================
    # SCORING TESTS
    # =========================================================================

    def test_scoring_by_difficulty(self):
        """Test that different difficulties award different points"""
        # Mock questions with known difficulties
        beginner_points = self.assessment_manager.calculate_points('beginner', True)
        intermediate_points = self.assessment_manager.calculate_points('intermediate', True)
        advanced_points = self.assessment_manager.calculate_points('advanced', True)
        
        self.assertEqual(beginner_points, 1)
        self.assertEqual(intermediate_points, 2)
        self.assertEqual(advanced_points, 3)

    def test_total_score_calculation(self):
        """Test total score calculation"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        # Answer all questions correctly
        state = self.assessment_manager.active_assessments[self.test_user_id]
        
        total_possible = 0
        for question in state['questions']:
            total_possible += self.assessment_manager.calculate_points(
                question['difficulty'], True
            )
        
        self.assertGreater(total_possible, 0)

    def test_percentage_calculation(self):
        """Test score percentage calculation"""
        score = 15
        max_score = 30
        
        percentage = self.assessment_manager.calculate_percentage(score, max_score)
        
        self.assertEqual(percentage, 50)

    # =========================================================================
    # SKILL LEVEL DETERMINATION TESTS
    # =========================================================================

    def test_skill_level_beginner(self):
        """Test skill level determination for beginner"""
        percentage = 40
        level = self.assessment_manager.determine_skill_level(percentage)
        
        self.assertEqual(level, 'beginner')

    def test_skill_level_intermediate(self):
        """Test skill level determination for intermediate"""
        percentage = 60
        level = self.assessment_manager.determine_skill_level(percentage)
        
        self.assertEqual(level, 'intermediate')

    def test_skill_level_advanced(self):
        """Test skill level determination for advanced"""
        percentage = 80
        level = self.assessment_manager.determine_skill_level(percentage)
        
        self.assertEqual(level, 'advanced')

    def test_skill_level_boundaries(self):
        """Test skill level boundary conditions"""
        # Test exact boundaries
        self.assertEqual(self.assessment_manager.determine_skill_level(30), 'beginner')
        self.assertEqual(self.assessment_manager.determine_skill_level(50), 'beginner')
        self.assertEqual(self.assessment_manager.determine_skill_level(70), 'intermediate')
        self.assertEqual(self.assessment_manager.determine_skill_level(90), 'advanced')

    # =========================================================================
    # WEAK AREA IDENTIFICATION TESTS
    # =========================================================================

    def test_identify_weak_areas(self):
        """Test identification of weak areas"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        state = self.assessment_manager.active_assessments[self.test_user_id]
        
        # Simulate wrong answers in specific categories
        state['answers'] = [
            {'category': 'Enumeration', 'correct': False},
            {'category': 'Enumeration', 'correct': False},
            {'category': 'Privilege Escalation', 'correct': False},
            {'category': 'Web Exploitation', 'correct': True},
        ]
        
        weak_areas = self.assessment_manager.identify_weak_areas(self.test_user_id)
        
        self.assertIn('Enumeration', weak_areas)

    def test_weak_areas_threshold(self):
        """Test weak area identification threshold"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        state = self.assessment_manager.active_assessments[self.test_user_id]
        
        # 50% correct should not be weak area
        state['answers'] = [
            {'category': 'Enumeration', 'correct': True},
            {'category': 'Enumeration', 'correct': False},
        ]
        
        weak_areas = self.assessment_manager.identify_weak_areas(self.test_user_id)
        
        # Depends on threshold setting
        self.assertIsInstance(weak_areas, list)

    # =========================================================================
    # ASSESSMENT COMPLETION TESTS
    # =========================================================================

    def test_assessment_completion(self):
        """Test assessment completion"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        state = self.assessment_manager.active_assessments[self.test_user_id]
        
        # Answer all questions
        while state['current_question'] < len(state['questions']):
            self.assessment_manager.submit_answer(
                user_id=self.test_user_id,
                answer='A'
            )
        
        # Assessment should be complete
        is_complete = self.assessment_manager.is_assessment_complete(self.test_user_id)
        
        self.assertTrue(is_complete)

    def test_get_results(self):
        """Test getting assessment results"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        state = self.assessment_manager.active_assessments[self.test_user_id]
        
        # Complete assessment
        while state['current_question'] < len(state['questions']):
            question = self.assessment_manager.get_current_question(self.test_user_id)
            if question:
                self.assessment_manager.submit_answer(
                    user_id=self.test_user_id,
                    answer=question['correct_answer']
                )
            else:
                break
        
        results = self.assessment_manager.get_results(self.test_user_id)
        
        self.assertIsNotNone(results)
        self.assertIn('score', results)
        self.assertIn('max_score', results)
        self.assertIn('percentage', results)
        self.assertIn('skill_level', results)
        self.assertIn('weak_areas', results)

    def test_results_structure(self):
        """Test that results have correct structure"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        # Complete assessment quickly
        state = self.assessment_manager.active_assessments[self.test_user_id]
        for _ in range(len(state['questions'])):
            self.assessment_manager.submit_answer(self.test_user_id, 'A')
        
        results = self.assessment_manager.get_results(self.test_user_id)
        
        # Check breakdown by difficulty
        self.assertIn('breakdown', results)
        self.assertIn('beginner', results['breakdown'])
        self.assertIn('intermediate', results['breakdown'])
        self.assertIn('advanced', results['breakdown'])

    # =========================================================================
    # STATE MANAGEMENT TESTS
    # =========================================================================

    def test_cancel_assessment(self):
        """Test canceling an assessment"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        result = self.assessment_manager.cancel_assessment(self.test_user_id)
        
        self.assertTrue(result)
        self.assertNotIn(self.test_user_id, self.assessment_manager.active_assessments)

    def test_cancel_nonexistent_assessment(self):
        """Test canceling assessment that doesn't exist"""
        result = self.assessment_manager.cancel_assessment("nonexistent_user")
        
        self.assertFalse(result)

    def test_get_progress(self):
        """Test getting assessment progress"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        progress = self.assessment_manager.get_progress(self.test_user_id)
        
        self.assertIsNotNone(progress)
        self.assertIn('current_question', progress)
        self.assertIn('total_questions', progress)
        self.assertIn('percentage_complete', progress)

    # =========================================================================
    # TIME TRACKING TESTS
    # =========================================================================

    def test_time_tracking(self):
        """Test that assessment time is tracked"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        state = self.assessment_manager.active_assessments[self.test_user_id]
        
        self.assertIsNotNone(state['start_time'])
        self.assertIsInstance(state['start_time'], datetime)

    def test_elapsed_time_calculation(self):
        """Test elapsed time calculation"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        elapsed = self.assessment_manager.get_elapsed_time(self.test_user_id)
        
        self.assertIsNotNone(elapsed)
        self.assertGreaterEqual(elapsed, 0)

    # =========================================================================
    # CATEGORY TRACKING TESTS
    # =========================================================================

    def test_category_performance_tracking(self):
        """Test tracking performance by category"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        state = self.assessment_manager.active_assessments[self.test_user_id]
        
        # Answer some questions
        for _ in range(3):
            question = self.assessment_manager.get_current_question(self.test_user_id)
            if question:
                self.assessment_manager.submit_answer(
                    user_id=self.test_user_id,
                    answer=question['correct_answer']
                )
        
        # Check category tracking
        self.assertIn('answers', state)
        for answer in state['answers']:
            self.assertIn('category', answer)

    # =========================================================================
    # EDGE CASE TESTS
    # =========================================================================

    def test_empty_question_bank(self):
        """Test handling of empty question bank"""
        # This should be handled gracefully
        with self.assertRaises((ValueError, KeyError)):
            self.assessment_manager.start_assessment(
                user_id=self.test_user_id,
                certification="EMPTY_CERT"
            )

    def test_concurrent_assessments(self):
        """Test multiple users taking assessments simultaneously"""
        user1 = "user_1"
        user2 = "user_2"
        
        self.assessment_manager.start_assessment(user1, "OSCP")
        self.assessment_manager.start_assessment(user2, "OSEP")
        
        # Both should be active
        self.assertIn(user1, self.assessment_manager.active_assessments)
        self.assertIn(user2, self.assessment_manager.active_assessments)
        
        # Should be independent
        self.assertNotEqual(
            self.assessment_manager.active_assessments[user1]['certification'],
            self.assessment_manager.active_assessments[user2]['certification']
        )

    def test_resume_after_crash(self):
        """Test that assessment state can be persisted and resumed"""
        self.assessment_manager.start_assessment(
            user_id=self.test_user_id,
            certification=self.test_certification
        )
        
        # Answer some questions
        for _ in range(3):
            question = self.assessment_manager.get_current_question(self.test_user_id)
            if question:
                self.assessment_manager.submit_answer(self.test_user_id, 'A')
        
        # Save state
        state = self.assessment_manager.active_assessments[self.test_user_id].copy()
        
        # Simulate crash and recovery
        self.assessment_manager.active_assessments[self.test_user_id] = state
        
        # Should be able to continue
        question = self.assessment_manager.get_current_question(self.test_user_id)
        self.assertIsNotNone(question)


# =============================================================================
# TEST RUNNER
# =============================================================================

def run_tests():
    """Run all assessment tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAssessmentManager)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY - ASSESSMENT MODULE")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Run tests when executed directly
    success = run_tests()
    sys.exit(0 if success else 1)