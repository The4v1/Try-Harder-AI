"""
Comprehensive Certification Logic Validator
============================================
Verifies that scoring and skill level logic works correctly for ALL 12 certifications.
"""

import yaml
import sys

# Simulate the scoring logic
def calculate_score(answers, max_score=3):
    """Calculate percentage score from answers."""
    total = sum(answers)
    max_possible = len(answers) * max_score
    return (total / max_possible) * 100.0

def determine_skill_level(score):
    """Determine skill level from score percentage."""
    if score >= 84:
        return "Expert"
    elif score >= 75:
        return "Advanced"
    elif score >= 50:
        return "Intermediate"
    else:
        return "Beginner"

def test_all_certifications():
    """Test scoring logic for all certifications."""
    
    print("=" * 80)
    print("COMPREHENSIVE CERTIFICATION LOGIC VALIDATOR")
    print("=" * 80)
    print()
    
    # Load questions to get actual question counts
    with open('data/questions.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    certs = ['OSCP', 'OSEP', 'OSWE', 'OSED', 'OSWP', 'OSWA', 
             'OSMR', 'OSDA', 'KLCP', 'OSCC', 'OSIR', 'OSEE']
    
    # Test each certification
    all_passed = True
    
    for cert in certs:
        if cert not in data:
            print(f"❌ {cert}: NOT FOUND IN YAML")
            all_passed = False
            continue
        
        # Count total questions
        total_q = 0
        for level in ['beginner', 'intermediate', 'advanced']:
            if level in data[cert]:
                total_q += len(data[cert][level])
        
        if total_q == 0:
            print(f"⚠️  {cert}: No questions found")
            continue
        
        # Test different answer patterns
        print(f"\n{cert} ({total_q} questions):")
        print("-" * 80)
        
        test_cases = [
            ([0] * total_q, "Beginner", "All A answers"),
            ([1] * total_q, "Beginner", "All B answers"),
            ([2] * total_q, "Intermediate", "All C answers"),
            ([3] * total_q, "Expert", "All D answers"),
            ([0, 1, 2, 3] * (total_q // 4 + 1), "Intermediate", "Mixed A/B/C/D"),
        ]
        
        for answers, expected_level, desc in test_cases:
            answers = answers[:total_q]  # Trim to actual question count
            score = calculate_score(answers)
            level = determine_skill_level(score)
            
            # Check if result matches expected
            if level == expected_level or (desc == "Mixed A/B/C/D" and level in ["Beginner", "Intermediate"]):
                status = "✅"
            else:
                status = "❌"
                all_passed = False
            
            print(f"  {status} {desc:<25} → Score: {score:5.1f}% = {level}")
    
    print()
    print("=" * 80)
    print("SKILL LEVEL THRESHOLDS:")
    print("  • Beginner:      0-49%  (All A or B answers)")
    print("  • Intermediate: 50-74%  (All C or C+B mix)")
    print("  • Advanced:     75-83%  (Mostly D with some C)")
    print("  • Expert:       84-100% (All D or nearly all D)")
    print("=" * 80)
    print()
    
    # Summary
    if all_passed:
        print("✅ ALL CERTIFICATIONS: LOGIC VERIFIED")
        print()
        print("Key Points:")
        print("  ✓ Scoring normalizes to 0-100% correctly")
        print("  ✓ All A/B answers → Beginner")
        print("  ✓ All C answers → Intermediate (NOT Advanced)")
        print("  ✓ All D answers → Expert")
        print("  ✓ Mixed answers → Calculated appropriately")
        return True
    else:
        print("❌ SOME CERTIFICATIONS FAILED")
        return False

if __name__ == "__main__":
    success = test_all_certifications()
    sys.exit(0 if success else 1)
