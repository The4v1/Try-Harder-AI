#!/usr/bin/env python3
"""
Validate that all questions have topic fields for Areas to Focus feature.
"""
import yaml
from pathlib import Path
from collections import defaultdict

def main():
    questions_file = Path(__file__).parent.parent / 'data' / 'questions.yaml'
    
    with open(questions_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Skip metadata
    certs = {k: v for k, v in data.items() if k != 'metadata'}
    
    print("=" * 60)
    print("  Topic Coverage Validation")
    print("=" * 60)
    
    missing_topics = {}
    topic_stats = defaultdict(lambda: defaultdict(int))
    
    for cert, levels in certs.items():
        if not isinstance(levels, dict):
            print(f"\n❌ {cert}: Invalid structure (not a dict)")
            continue
            
        print(f"\n📋 {cert}:")
        cert_missing = []
        
        for level in ['beginner', 'intermediate', 'advanced']:
            if level not in levels:
                continue
                
            questions = levels[level]
            for i, q in enumerate(questions, 1):
                question_id = q.get('id', f'{cert}_{level}_{i}')
                
                if 'topic' not in q or not q['topic']:
                    cert_missing.append(f"  {level}/{i}: {question_id}")
                else:
                    topic_stats[cert][q['topic']] += 1
        
        if cert_missing:
            missing_topics[cert] = cert_missing
            print(f"  ❌ Missing topics: {len(cert_missing)}")
        else:
            print(f"  ✅ All questions have topics")
            print(f"  Topics: {', '.join(sorted(topic_stats[cert].keys()))}")
    
    print("\n" + "=" * 60)
    
    if missing_topics:
        print("\n⚠️ Certifications with missing topics:\n")
        for cert, missing in missing_topics.items():
            print(f"{cert}:")
            for m in missing[:5]:  # Show first 5
                print(m)
            if len(missing) > 5:
                print(f"  ...and {len(missing) - 5} more")
            print()
        return 1
    else:
        print("\n🎉 All certifications have complete topic coverage!")
        
        print("\n📊 Topic Distribution:")
        for cert in sorted(topic_stats.keys()):
            topics = topic_stats[cert]
            print(f"\n{cert} ({sum(topics.values())} questions):")
            for topic, count in sorted(topics.items()):
                print(f"  • {topic}: {count} questions")
        
        return 0

if __name__ == "__main__":
    exit(main())
