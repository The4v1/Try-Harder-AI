"""
YAML Questions Validator
========================
Validates questions.yaml for all 12 certifications.

Checks:
- All questions have 4 options (A, B, C, D)
- All questions have scoring (A=0, B=1, C=2, D=3)
- Question IDs are unique
- No invalid range formats (e.g., "30+" should be specific ranges)
- All difficulty levels present
"""

import yaml
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

class QuestionValidator:
    def __init__(self, yaml_path: str):
        self.yaml_path = yaml_path
        self.errors = []
        self.warnings = []
        self.stats = {}
        
    def load_yaml(self) -> Dict:
        """Load and parse questions YAML."""
        try:
            with open(self.yaml_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.errors.append(f"Failed to load YAML: {e}")
            return {}
    
    def validate_options(self, question: Dict, q_id: str, cert: str) -> bool:
        """Validate question has 4 options (A, B, C, D)."""
        if 'options' not in question:
            self.errors.append(f"{cert} - {q_id}: Missing 'options' field")
            return False
        
        options = question['options']
        expected_keys = {'A', 'B', 'C', 'D'}
        actual_keys = set(options.keys())
        
        if actual_keys != expected_keys:
            missing = expected_keys - actual_keys
            extra = actual_keys - expected_keys
            msg = f"{cert} - {q_id}: "
            if missing:
                msg += f"Missing options: {missing}. "
            if extra:
                msg += f"Extra options: {extra}."
            self.errors.append(msg)
            return False
        
        return True
    
    def validate_scoring(self, question: Dict, q_id: str, cert: str) -> bool:
        """Validate question has scoring (A=0, B=1, C=2, D=3)."""
        if 'scoring' not in question:
            self.errors.append(f"{cert} - {q_id}: Missing 'scoring' field")
            return False
        
        scoring = question['scoring']
        expected_scoring = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
        
        if scoring != expected_scoring:
            self.errors.append(
                f"{cert} - {q_id}: Invalid scoring. Expected {expected_scoring}, got {scoring}"
            )
            return False
        
        return True
    
    def check_range_format(self, text: str, q_id: str, cert: str):
        """Check for invalid range formats like '30+'."""
        # Common patterns to flag
        invalid_patterns = [
            ('30+', '30-50+ or 50-100+'),
            ('20+', '20-50+ or 50+'),
            ('10+', '10-20+ or 20+'),
            ('5+', '5-10+ or 10+'),
        ]
        
        for pattern, suggestion in invalid_patterns:
            if pattern in text and not any(x in text for x in ['20-50+', '30-50+', '10-20+']):
                self.warnings.append(
                    f"{cert} - {q_id}: Found '{pattern}' in option text. "
                    f"Consider using specific range like '{suggestion}'"
                )
    
    def validate_certification(self, cert_name: str, cert_data: Dict) -> Dict:
        """Validate all questions for a certification."""
        stats = {
            'total_questions': 0,
            'beginner': 0,
            'intermediate': 0,
            'advanced': 0,
            'errors': 0,
            'warnings': 0
        }
        
        question_ids: Set[str] = set()
        
        for difficulty in ['beginner', 'intermediate', 'advanced']:
            if difficulty not in cert_data:
                self.warnings.append(f"{cert_name}: Missing '{difficulty}' difficulty level")
                continue
            
            questions = cert_data[difficulty]
            if not questions:
                self.warnings.append(f"{cert_name}: No questions in '{difficulty}' level")
                continue
            
            stats[difficulty] = len(questions)
            
            for q in questions:
                stats['total_questions'] += 1
                q_id = q.get('id', 'UNKNOWN')
                
                # Check unique ID
                if q_id in question_ids:
                    self.errors.append(f"{cert_name} - {q_id}: Duplicate question ID")
                    stats['errors'] += 1
                else:
                    question_ids.add(q_id)
                
                # Validate options
                if not self.validate_options(q, q_id, cert_name):
                    stats['errors'] += 1
                
                # Validate scoring
                if not self.validate_scoring(q, q_id, cert_name):
                    stats['errors'] += 1
                
                # Check range formats in all options
                if 'options' in q:
                    for opt_key, opt_text in q['options'].items():
                        self.check_range_format(str(opt_text), q_id, cert_name)
        
        return stats
    
    def run_validation(self) -> bool:
        """Run full validation on all certifications."""
        print("=" * 70)
        print("YAML Questions Validator - Try-Harder-AI")
        print("=" * 70)
        print()
        
        data = self.load_yaml()
        if not data or self.errors:
            return False
        
        # Expected certifications
        expected_certs = [
            'OSCP', 'OSEP', 'OSWE', 'OSED', 'OSWP', 'OSWA', 
            'OSMR', 'OSDA', 'KLCP', 'OSCC', 'OSIR', 'OSEE'
        ]
        
        # Validate each certification
        for cert in expected_certs:
            if cert not in data:
                self.errors.append(f"Missing certification: {cert}")
                continue
            
            print(f"Validating {cert}...")
            self.stats[cert] = self.validate_certification(cert, data[cert])
        
        # Print results
        print()
        print("=" * 70)
        print("VALIDATION RESULTS")
        print("=" * 70)
        print()
        
        # Summary table
        print(f"{'Certification':<15} {'Total':<8} {'Beginner':<12} {'Intermediate':<15} {'Advanced':<10}")
        print("-" * 70)
        for cert in expected_certs:
            if cert in self.stats:
                s = self.stats[cert]
                print(f"{cert:<15} {s['total_questions']:<8} {s['beginner']:<12} {s['intermediate']:<15} {s['advanced']:<10}")
        
        print()
        
        # Errors
        if self.errors:
            print(f"❌ ERRORS FOUND: {len(self.errors)}")
            print("-" * 70)
            for err in self.errors:
                print(f"  • {err}")
            print()
        else:
            print("✅ No errors found!")
            print()
        
        # Warnings
        if self.warnings:
            print(f"⚠️  WARNINGS: {len(self.warnings)}")
            print("-" * 70)
            for warn in self.warnings:
                print(f"  • {warn}")
            print()
        else:
            print("✅ No warnings!")
            print()
        
        # Overall summary
        total_questions = sum(s['total_questions'] for s in self.stats.values())
        print("=" * 70)
        print(f"SUMMARY: {len(expected_certs)} certifications, {total_questions} total questions")
        print(f"Status: {'❌ FAILED' if self.errors else '✅ PASSED'}")
        print("=" * 70)
        
        return len(self.errors) == 0


if __name__ == "__main__":
    validator = QuestionValidator("data/questions.yaml")
    success = validator.run_validation()
    sys.exit(0 if success else 1)
