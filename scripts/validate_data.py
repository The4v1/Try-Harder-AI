#!/usr/bin/env python3
"""
Data Validation Script for Try-Harder-AI
=========================================

Validates that all certifications have complete resource data.

Usage:
    python scripts/validate_data.py
"""

import yaml
from pathlib import Path
import sys

def validate_resources():
    """Validate resources.yaml completeness."""
    print("🔍 Validating resources.yaml...")
    
    resources_file = Path(__file__).parent.parent / 'data' / 'resources.yaml'
    
    if not resources_file.exists():
        print("❌ resources.yaml not found!")
        return False
    
    with open(resources_file, 'r', encoding='utf-8') as f:
        resources = yaml.safe_load(f)
    
    # Expected certifications
    expected_certs = [
        "OSCP", "OSEP", "OSWE", "OSED", "OSWP",
        "OSWA", "OSMR", "OSDA", "KLCP", "OSCC", "OSIR", "OSEE"
    ]
    
    # Recommended sections (not all certs need all sections)
    optional_sections = ['github_resources', 'free_platforms', 'practice_platforms', 'cheatsheets', 'tools']
    
    print(f"\n📋 Checking {len(expected_certs)} certifications...\n")
    
    issues = []
    complete = []
    
    for cert in expected_certs:
        if cert not in resources:
            issues.append(f"❌ {cert}: Missing entirely from resources.yaml")
            continue
        
        cert_data = resources[cert]
        sections_found = []
        
        for section in optional_sections:
            if section in cert_data and cert_data[section]:
                sections_found.append(section)
        
        if len(sections_found) >= 2:  # At least 2 sections = good
            complete.append(f"✅ {cert}: {len(sections_found)} sections - {', '.join(sections_found)}")
        else:
            issues.append(f"⚠️  {cert}: Only {len(sections_found)} sections - needs more resources")
    
    # Print results
    if complete:
        print("✅ Complete Certifications:")
        for item in complete:
            print(f"  {item}")
    
    if issues:
        print("\n⚠️  Issues Found:")
        for item in issues:
            print(f"  {item}")
    
    print(f"\n📊 Summary:")
    print(f"  Complete: {len(complete)}/{len(expected_certs)}")
    print(f"  Issues: {len(issues)}/{len(expected_certs)}")
    
    return len(issues) == 0

def validate_certifications():
    """Validate certifications.yaml structure."""
    print("\n🔍 Validating certifications.yaml...")
    
    cert_file = Path(__file__).parent.parent / 'data' / 'certifications.yaml'
    
    if not cert_file.exists():
        print("❌ certifications.yaml not found!")
        return False
    
    with open(cert_file, 'r', encoding='utf-8') as f:
        certs = yaml.safe_load(f)
    
    certifications = certs.get('certifications', {})
    
    issues = []
    
    for cert_code, cert_data in certifications.items():
        if not isinstance(cert_data, dict):
            issues.append(f"❌ {cert_code}: Invalid structure")
            continue
        
        # Check required fields
        if 'name' not in cert_data:
            issues.append(f"⚠️  {cert_code}: Missing 'name' field")
        if 'description' not in cert_data:
            issues.append(f"⚠️  {cert_code}: Missing 'description' field")
        if 'difficulty' not in cert_data:
            issues.append(f"⚠️  {cert_code}: Missing 'difficulty' field")
    
    if issues:
        print("\n⚠️  Issues Found:")
        for item in issues:
            print(f"  {item}")
    else:
        print(f"✅ All {len(certifications)} certifications valid!")
    
    return len(issues) == 0

def validate_questions():
    """Validate questions.yaml structure."""
    print("\n🔍 Validating questions.yaml...")
    
    questions_file = Path(__file__).parent.parent / 'data' / 'questions.yaml'
    
    if not questions_file.exists():
        print("❌ questions.yaml not found!")
        return False
    
    with open(questions_file, 'r', encoding='utf-8') as f:
        questions_data = yaml.safe_load(f)
    
    issues = []
    total_questions = 0
    
    for cert_code, questions in questions_data.items():
        if not isinstance(questions, list):
            issues.append(f"❌ {cert_code}: Questions not a list")
            continue
        
        total_questions += len(questions)
        
        for i, question in enumerate(questions, 1):
            if 'question' not in question:
                issues.append(f"⚠️  {cert_code} Q{i}: Missing 'question' field")
            if 'options' not in question:
                issues.append(f"⚠️  {cert_code} Q{i}: Missing 'options' field")
            if 'correct_answer' not in question:
                issues.append(f"⚠️  {cert_code} Q{i}: Missing 'correct_answer' field")
    
    if issues:
        print("\n⚠️  Issues Found:")
        for item in issues[:10]:  # Show first 10 issues
            print(f"  {item}")
        if len(issues) > 10:
            print(f"  ...and {len(issues) - 10} more issues")
    else:
        print(f"✅ All {total_questions} questions across {len(questions_data)} certs valid!")
    
    return len(issues) == 0

def main():
    """Run all validation checks."""
    print("="*60)
    print("  Try-Harder-AI Data Validation Script")
    print("="*60)
    
    results = []
    
    results.append(("Resources", validate_resources()))
    results.append(("Certifications", validate_certifications()))
    results.append(("Questions", validate_questions()))
    
    print("\n" + "="*60)
    print("📊 Final Results:")
    print("="*60)
    
    all_pass = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_pass = False
    
    print("="*60)
    
    if all_pass:
        print("🎉 All validation checks passed!")
        return 0
    else:
        print("⚠️  Some validation checks failed. Fix issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
