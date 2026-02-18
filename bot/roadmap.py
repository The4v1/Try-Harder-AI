"""
Roadmap Generator
=================

AI-powered study plan generation for OffSec certifications.

Features:
- Personalized roadmap generation using Google Gemini AI
- Skill-level adaptive planning
- Resource integration from database
- Timeline customization
- Progress tracking integration
- Multiple certification support
- Professional formatting with emojis
"""

import logging
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path

# Setup logging
logger = logging.getLogger(__name__)


class RoadmapGenerator:
    """Generates personalized study roadmaps based on user assessments."""
    
    def __init__(self, cert_data: Optional[Dict[str, Any]] = None, ai_engine = None):
        """
        Initialize roadmap generator.
        
        Args:
            cert_data: Certification data from YAML
            ai_engine: Google Gemini AI engine instance
        """
        self.ai_engine = ai_engine
        self.cert_data = cert_data if cert_data is not None else {}
        
        logger.info("🗺️ Roadmap Generator initialized")
    
    async def generate_roadmap(
        self,
        user_id: str,
        certification: str,
        assessment_results: Dict[str, Any],
        custom_duration: Optional[int] = None,
        focus_areas: Optional[List[str]] = None
    ) -> str:
        """
        Generate a complete personalized study roadmap.
        
        Args:
            user_id: User's Discord ID
            certification: Certification code (e.g., "OSCP")
            assessment_results: User's assessment results
            custom_duration: Custom duration in weeks (optional)
            focus_areas: Specific areas to focus on (optional)
            
        Returns:
            Formatted roadmap as markdown text
        """
        try:
            logger.info(f"🗺️ Generating roadmap for user {user_id} - {certification}")
            
            # Get certification data
            certs = self.cert_data.get('certifications', self.cert_data)
            cert_info = certs.get(certification)
            
            
            if not cert_info:
                logger.warning(f"⚠️ Certification {certification} has incomplete data - using defaults")
                cert_info = {
                    'name': certification,
                    'description': f'{certification} certification preparation'
                }
            
            # Extract assessment data
            skill_level = assessment_results.get('skill_level', 'Intermediate')
            score = assessment_results.get('score_percentage', 50)
            strengths = assessment_results.get('strengths', [])
            weaknesses = assessment_results.get('weaknesses', [])
            
            # Determine study duration based on skill level
            duration_weeks = custom_duration or self._calculate_duration(skill_level, score)
            
            # Prepare user context
            user_context = {
                'duration_weeks': duration_weeks,
                'focus_areas': focus_areas or weaknesses,
                'user_id': user_id
            }
            
            # Generate roadmap using AI
            if self.ai_engine:
                roadmap = await self.ai_engine.generate_roadmap(
                    certification=certification,
                    skill_level=skill_level,
                    assessment_data=assessment_results,
                    cert_data=cert_info,
                    user_context=user_context
                )
            else:
                logger.warning("⚠️ AI engine not available, using fallback")
                roadmap = self._generate_fallback_roadmap(certification, assessment_results)
            
            # Add metadata and formatting
            formatted_roadmap = self._format_roadmap(
                roadmap=roadmap,
                certification=certification,
                skill_level=skill_level,
                duration_weeks=duration_weeks,
                cert_info=cert_info,
                assessment_results=assessment_results
            )
            
            logger.info(f"✅ Successfully generated roadmap for {certification}")
            return formatted_roadmap
            
        except Exception as e:
            logger.error(f"❌ Error generating roadmap: {e}")
            return self._generate_fallback_roadmap(certification, assessment_results)
    
    def _calculate_duration(self, skill_level: str, score: float) -> int:
        """
        Calculate recommended study duration based on skill level.
        
        Args:
            skill_level: User's skill level
            score: Assessment score
            
        Returns:
            Recommended duration in weeks
        """
        # Base durations by skill level
        base_durations = {
            'Beginner': 16,
            'Intermediate': 12,
            'Advanced': 8,
            'Expert': 6
        }
        
        duration = base_durations.get(skill_level, 12)
        
        # Adjust based on score
        if score < 30:
            duration += 4
        elif score < 50:
            duration += 2
        elif score > 85:
            duration -= 2
        
        # Ensure minimum and maximum bounds
        return max(6, min(24, duration))
    
    def _format_roadmap(
        self,
        roadmap: str,
        certification: str,
        skill_level: str,
        duration_weeks: int,
        cert_info: Dict[str, Any],
        assessment_results: Dict[str, Any]
    ) -> str:
        """
        Format the roadmap with additional information and structure.
        
        Args:
            roadmap: AI-generated roadmap
            certification: Certification code
            skill_level: User's skill level
            duration_weeks: Study duration
            cert_info: Certification information
            assessment_results: Assessment results
            
        Returns:
            Formatted roadmap
        """
        # Calculate timeline
        start_date = datetime.now()
        end_date = start_date + timedelta(weeks=duration_weeks)
        
        # Build header with emojis
        header = f"""# 🗺️ Your Personalized {certification} Study Roadmap

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**📋 Certification:** {cert_info.get('name', certification)}
**🎯 Your Skill Level:** {skill_level}
**📈 Assessment Score:** {assessment_results.get('score_percentage', 0)}%
**⏱️ Study Duration:** {duration_weeks} weeks
**📅 Start Date:** {start_date.strftime('%B %d, %Y')}
**🎓 Target Exam Date:** {end_date.strftime('%B %d, %Y')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        
        # Add strengths and weaknesses
        strengths = assessment_results.get('strengths', [])
        weaknesses = assessment_results.get('weaknesses', [])
        
        if strengths or weaknesses:
            header += "## 📊 Your Profile\n\n"
            
            if strengths:
                header += "**💪 Your Strengths:**\n"
                for strength in strengths:
                    header += f"✅ {strength}\n"
                header += "\n"
            
            if weaknesses:
                header += "**📚 Areas to Focus On:**\n"
                for weakness in weaknesses:
                    header += f"🎯 {weakness}\n"
                header += "\n"
            
            header += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Add AI-generated content
        formatted = header + roadmap
        
        # Add footer with additional resources
        footer = self._create_footer(cert_info, certification)
        
        formatted += "\n\n" + footer
        
        return formatted
    
    def _create_footer(self, cert_info: Dict[str, Any], certification: str) -> str:
        """
        Create footer with additional resources and tips.
        
        Args:
            cert_info: Certification information
            certification: Certification code
            
        Returns:
            Formatted footer
        """
        footer = """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📚 Quick Reference Resources

"""
        
        # Add practice platforms
        resources = cert_info.get('resources', {})
        platforms = resources.get('practice_platforms', [])
        
        if platforms:
            footer += "**🎮 Practice Platforms:**\n"
            for platform in platforms[:5]:
                name = platform.get('name', 'Unknown')
                cost = platform.get('cost', 'Unknown')
                footer += f"• **{name}** - {cost}\n"
            footer += "\n"
        
        # Add essential tools
        tools = resources.get('tools', {})
        if tools:
            footer += "**🛠️ Essential Tools:**\n"
            for category, tool_list in list(tools.items())[:3]:
                if isinstance(tool_list, list):
                    category_name = category.replace('_', ' ').title()
                    footer += f"• **{category_name}:** {', '.join(tool_list[:5])}\n"
            footer += "\n"
        
        # Add success tips
        tips = cert_info.get('tips', [])
        if tips:
            footer += "**💡 Success Tips:**\n"
            for tip in tips[:5]:
                footer += f"✅ {tip}\n"
            footer += "\n"
        
        # Add community resources
        footer += """**🤝 Community Resources:**
- OffSec Discord Server
- r/oscp on Reddit
- InfoSec Prep Discord
- NetSecFocus Discord (Trophy Bot)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎯 Remember

✨ **Consistency** is more important than intensity
💪 **Try Harder** - but also take breaks when stuck
📝 **Document everything** - your notes will save you during the exam
🔄 **Review regularly** - revisit topics you've learned
❤️ **Join the community** - learn from others on the same journey

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

*🚀 Use `/progress` to track your journey*
*💬 Use `/ask` for any questions*
*📖 Use `/resources` for more materials*

**Good luck, and Try Harder! 💪**
"""
        
        return footer
    
    def _generate_fallback_roadmap(
        self,
        certification: str,
        assessment_results: Dict[str, Any]
    ) -> str:
        """
        Generate a basic fallback roadmap if AI generation fails.
        
        Args:
            certification: Certification code
            assessment_results: Assessment results
            
        Returns:
            Basic roadmap
        """
        skill_level = assessment_results.get('skill_level', 'Intermediate')
        score = assessment_results.get('score_percentage', 50)
        
        roadmap = f"""
## 🎯 {certification} Study Roadmap

**Your Level:** {skill_level} ({score}%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📖 Phase 1: Foundation Building (Weeks 1-4)

**🎯 Goals:**
→ Establish strong fundamentals
→ Set up your lab environment  
→ Learn essential tools
→ Complete basic practice machines

**📚 What to Study:**
✅ Linux command line mastery
✅ Windows fundamentals
✅ Networking basics (TCP/IP, ports, protocols)
✅ Basic enumeration techniques

**🛠️ Essential Tools to Install:**
→ [AutoRecon](https://github.com/Tib3rius/AutoRecon) - Automated enumeration
→ [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) - Payload reference
→ [SecLists](https://github.com/danielmiessler/SecLists) - Essential wordlists
→ [PEASS-ng](https://github.com/carlospolop/PEASS-ng) - LinPEAS/WinPEAS privesc scripts

**🎮 Practice Machines (Easy - Week 1-2):**
**Linux:**
→ HTB: Lame, Legacy, Shocker, Nibbles
→ THM: Linux PrivEsc Room, Basic Pentesting
→ VulnHub: Kioptrix 1-2

**Windows:**
→ HTB: Devel, Blue, Jerry, Optimum  
→ THM: Windows PrivEsc Room
→ VulnHub: FristiLeaks

**🎮 Practice Machines (Easy - Week 3-4):**
→ HTB: Beep, Sense, Bashed, Networked
→ THM: OSCP Buffer Overflow Prep
→ Root-Me: Start with Realistic challenges

**📝 Week-by-Week Breakdown:**
**Week 1:** Setup Kali + VMs, complete 2-3 easy Linux boxes
**Week 2:** Complete 2-3 easy Windows boxes, practice enumeration
**Week 3:** Focus on web vulnerabilities, 3-4 more boxes
**Week 4:** Review + practice report writing for all boxes

**⏱️ Time Commitment:** 15-20 hours/week (2-3 hours/day)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ⚡ Phase 2: Skill Development (Weeks 5-9)

**🎯 Goals:**
→ Master exploitation techniques
→ Learn privilege escalation
→ Understand Active Directory basics
→ Develop your methodology

**📚 What to Study:**
✅ Web application vulnerabilities (OWASP Top 10)
✅ Linux privilege escalation
✅ Windows privilege escalation
✅ Buffer overflows (if applicable)
✅ Active Directory enumeration and attacks

**🛠️ GitHub Tools to Master:**
→ [Impacket](https://github.com/fortra/impacket) - AD attack tools
→ [BloodHound](https://github.com/BloodHoundAD/BloodHound) - AD visualization
→ [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec) - AD swiss army knife
→ [Evil-WinRM](https://github.com/Hackplayers/evil-winrm) - Windows shell
→ [pwncat](https://github.com/calebstewart/pwncat) - Better reverse shells

**🎮 Practice Machines (Medium - Weeks 5-6):**
**Linux:**
→ HTB: Cronos, Node, Solidstate, Poison
→ PG Practice: Hetemit, Lampião, DC-9
→ Follow [TJNull's OSCP List](https://docs.google.com/spreadsheets/u/1/d/1dwSMIAPIam0PuRBkCiDI88pU3yzrqqHkDtBngUHNCw8/htmlview)

**Windows:**
→ HTB: Bastard, Chatterbox, Querier, Heist
→ PG Practice: Vault, Helpdesk, Shenzi

**🎮 Active Directory Practice (Weeks 7-9):**
**AD Machines:**
→ HTB: Forest, Sauna, Cascade (Medium AD)
→ HTB: Blackfield (Hard AD)
→ PG Practice: Hutch, Vault, Heist

**Free AD Labs:**
→ Deploy [GOAD](https://github.com/Orange-Cyberdefense/GOAD) (Game of Active Directory)
→ THM: Attacktive Directory, AD Certificate Templates
→ HTB Academy: Free AD modules

**📝 Week-by-Week Breakdown:**
**Week 5-6:** Complete 6-8 medium machines, focus on web + privesc
**Week 7-8:** AD fundamentals - complete 3-4 AD boxes, deploy GOAD
**Week 9:** Advanced AD attacks, kerberoasting, delegation attacks

**⏱️ Time Commitment:** 20-25 hours/week (3-4 hours/day)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🔥 Phase 3: Advanced Topics (Weeks 10-11)

**🎯 Goals:**
→ Master advanced attack techniques
→ Practice in realistic environments
→ Develop speed and efficiency
→ Perfect your methodology

**📚 What to Study:**
✅ Advanced Active Directory attacks
✅ Lateral movement techniques
✅ Post-exploitation strategies
✅ Evasion techniques (if applicable)

**🎮 Practice:**
→ Complete challenge labs
→ Practice full network penetrations
→ Work on speed - aim to complete machines in 2-4 hours
→ Review and consolidate knowledge

**⏱️ Time Commitment:** 25-30 hours per week

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎓 Phase 4: Exam Preparation (Weeks 12+)

**🎯 Goals:**
→ Simulate exam conditions
→ Perfect report writing
→ Build confidence
→ Final review

**📚 What to Study:**
✅ Review all weak areas
✅ Practice report writing
✅ Time management strategies
✅ Exam day preparation

**🎮 Practice:**
→ Complete mock exams (24-hour sessions)
→ Proving Grounds Practice machines
→ Official {certification} Challenge Labs
→ Practice writing professional reports

**📝 Report Writing Practice:**
- Use official OffSec templates
- Practice documenting as you go
- Time yourself - aim for 2-3 hours for a full report
- Get feedback on your reports

**⏱️ Time Commitment:** 30+ hours per week

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ✅ Weekly Milestones

**Week 4:** ✓ 15 machines completed, lab environment ready
**Week 8:** ✓ 40 machines completed, comfortable with methodology
**Week 10:** ✓ Advanced topics mastered, AD proficiency
**Week 12:** ✓ Exam ready, confident in abilities

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🆓 Free Resources & GitHub Tools

**📚 Essential GitHub Repos:**
→ [HackTricks](https://book.hacktricks.xyz) - Pentesting methodology bible
→ [GTFOBins](https://gtfobins.github.io) - Linux privilege escalation binaries
→ [LOLBAS](https://lolbas-project.github.io) - Windows living-off-the-land
→ [WADComs](https://wadcoms.github.io) - Active Directory attack cheatsheet
→ [Chisel](https://github.com/jpillora/chisel) - Fast tunneling for pivoting

**🎮 Free Practice Platforms:**
→ [TryHackMe](https://tryhackme.com) - 350+ free rooms
→ [Root-Me](https://www.root-me.org) - 500+ challenges
→ [OverTheWire](https://overthewire.org) - Linux fundamentals
→ [PicoCTF](https://picoctf.org) - Beginner-friendly CTF

**🎓 Study Techniques:**
→ **Pomodoro (25 min focus / 5 min break)** - Prevents burnout
→ **Spaced Repetition** - Review old boxes weekly
→ **Active Recall** - Try boxes without walkthroughs first
→ **Feynman Technique** - Explain concepts in simple terms
→ **Document Everything** - Your notes = your cheat sheet

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎯 Exam Day Strategy

**Before the Exam:**
✅ Get a good night's sleep (seriously!)
✅ Prepare snacks and meals
✅ Test your VPN connection
✅ Have backup internet ready
✅ Organize your notes and cheat sheets

**During the Exam:**
1️⃣ Start with full enumeration of all targets
2️⃣ Pick the easiest-looking target first
3️⃣ Document EVERYTHING as you go
4️⃣ Take breaks every 2 hours (Pomodoro technique)
5️⃣ If stuck for >2 hours, switch targets
6️⃣ Leave time for report writing (3-4 hours)

**Common Pitfalls to Avoid:**
⚠️ Rabbit holes - don't overcomplicate
⚠️ Not taking breaks - leads to burnout
⚠️ Poor documentation - screenshot everything
⚠️ Time mismanagement - pace yourself
⚠️ Giving up too early - persistence pays off

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 💪 Motivation & Mindset

Remember:
🔥 **"Try Harder"** doesn't mean bang your head against the wall
💡 It means **enumerate more**, **think differently**, **take breaks**
📚 Every failed attempt is a **learning opportunity**
🎯 Focus on **progress**, not perfection
❤️ The community is here to support you

**You've got this!** 🚀
"""
        
        return roadmap
    
    def get_phase_details(
        self,
        certification: str,
        phase_number: int
    ) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific study phase.
        
        Args:
            certification: Certification code
            phase_number: Phase number (1, 2, 3, etc.)
            
        Returns:
            Phase details dictionary or None
        """
        try:
            certs = self.cert_data.get('certifications', self.cert_data)
            cert_info = certs.get(certification)
            
            if not cert_info:
                return None
            
            study_plan = cert_info.get('study_plan', {})
            phases = study_plan.get('phases', [])
            
            if 0 <= phase_number - 1 < len(phases):
                return phases[phase_number - 1]
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error getting phase details: {e}")
            return None
    
    def get_milestone_checklist(
        self,
        certification: str,
        skill_level: str
    ) -> List[Dict[str, Any]]:
        """
        Generate a milestone checklist for the certification.
        
        Args:
            certification: Certification code
            skill_level: User's skill level
            
        Returns:
            List of milestone dictionaries
        """
        try:
            certs = self.cert_data.get('certifications', self.cert_data)
            cert_info = certs.get(certification)
            
            if not cert_info:
                return []
            
            # Base milestones
            milestones = [
                {
                    'week': 2,
                    'title': '🔧 Environment Setup',
                    'description': 'Lab environment configured and tested',
                    'tasks': [
                        'Install required tools',
                        'Setup VM/lab environment',
                        'Complete first practice machine',
                        'Setup note-taking system'
                    ]
                },
                {
                    'week': 4,
                    'title': '📚 Foundation Complete',
                    'description': 'Basic concepts mastered',
                    'tasks': [
                        'Complete 10-15 easy machines',
                        'Master enumeration techniques',
                        'Understand basic exploitation',
                        'Document methodology'
                    ]
                },
                {
                    'week': 8,
                    'title': '⚡ Skill Development',
                    'description': 'Core skills developed',
                    'tasks': [
                        'Complete 30-40 machines total',
                        'Master privilege escalation',
                        'Complete course material',
                        'Comfortable with methodology'
                    ]
                },
                {
                    'week': 10,
                    'title': '🔥 Advanced Topics',
                    'description': 'Advanced techniques learned',
                    'tasks': [
                        'Complete advanced modules',
                        'Practice complex scenarios',
                        'Master Active Directory (if applicable)',
                        'Start exam preparation'
                    ]
                },
                {
                    'week': 12,
                    'title': '🎓 Exam Ready',
                    'description': 'Ready to take the exam',
                    'tasks': [
                        'Complete mock exams',
                        'Perfect report writing',
                        'Review all weak areas',
                        'Schedule exam date'
                    ]
                }
            ]
            
            # Adjust based on skill level
            if skill_level == 'Beginner':
                # Add more granular milestones for beginners
                milestones.insert(1, {
                    'week': 1,
                    'title': '🌱 Getting Started',
                    'description': 'Initial orientation',
                    'tasks': [
                        'Complete course introduction',
                        'Join community forums',
                        'Setup study schedule',
                        'Learn basic Linux commands'
                    ]
                })
            elif skill_level == 'Advanced' or skill_level == 'Expert':
                # Accelerate timeline for advanced users
                for milestone in milestones:
                    milestone['week'] = max(1, milestone['week'] - 3)
            
            return milestones
            
        except Exception as e:
            logger.error(f"❌ Error generating milestone checklist: {e}")
            return []
    
    def estimate_study_hours(
        self,
        certification: str,
        skill_level: str,
        weeks: int
    ) -> Dict[str, Any]:
        """
        Estimate total study hours needed.
        
        Args:
            certification: Certification code
            skill_level: User's skill level
            weeks: Study duration in weeks
            
        Returns:
            Dictionary with hour estimates
        """
        # Base hours per week by skill level
        hours_per_week = {
            'Beginner': 20,
            'Intermediate': 15,
            'Advanced': 10,
            'Expert': 8
        }
        
        weekly_hours = hours_per_week.get(skill_level, 15)
        total_hours = weekly_hours * weeks
        
        # Break down by activity
        breakdown = {
            'total_hours': total_hours,
            'weekly_hours': weekly_hours,
            'breakdown': {
                'Course Material': int(total_hours * 0.25),
                'Hands-on Practice': int(total_hours * 0.50),
                'Note-taking & Documentation': int(total_hours * 0.10),
                'Review & Research': int(total_hours * 0.10),
                'Mock Exams': int(total_hours * 0.05)
            },
            'daily_recommendation': {
                'weekday': round(weekly_hours / 7 * 5 / 5, 1),  # 5 weekdays
                'weekend': round(weekly_hours / 7 * 2 / 2, 1)   # 2 weekend days
            }
        }
        
        return breakdown


# Utility function for testing
if __name__ == "__main__":
    print("🧪 Testing Roadmap Generator...")
    
    # Create mock data
    mock_cert_data = {
        'certifications': {
            'OSCP': {
                'name': 'Offensive Security Certified Professional',
                'level': 'Intermediate',
                'exam': {'duration': '23 hours 45 minutes'},
                'resources': {
                    'practice_platforms': [
                        {'name': 'HackTheBox', 'url': 'https://hackthebox.com', 'cost': 'Free/Premium'}
                    ]
                },
                'tips': ['Enumerate thoroughly', 'Try Harder!'],
                'study_plan': {
                    'phases': [
                        {'name': 'Foundation', 'duration': '3 weeks'},
                        {'name': 'Skill Development', 'duration': '5 weeks'}
                    ]
                }
            }
        }
    }
    
    mock_assessment = {
        'certification': 'OSCP',
        'skill_level': 'Intermediate',
        'score_percentage': 65,
        'strengths': ['Networking', 'Linux'],
        'weaknesses': ['Web Exploitation'],
        'responses': {}
    }
    
    # Initialize
    generator = RoadmapGenerator(mock_cert_data, None)
    
    # Test milestone generation
    milestones = generator.get_milestone_checklist('OSCP', 'Intermediate')
    print(f"\n✅ Generated {len(milestones)} milestones")
    
    for milestone in milestones:
        print(f"Week {milestone['week']}: {milestone['title']}")
    
    # Test hour estimates
    hours = generator.estimate_study_hours('OSCP', 'Intermediate', 12)
    print(f"\n📊 Hour Estimates:")
    print(f"Total Hours: {hours['total_hours']}")
    print(f"Weekly Hours: {hours['weekly_hours']}")
    print(f"Daily (Weekday): {hours['daily_recommendation']['weekday']} hours")
    print(f"Daily (Weekend): {hours['daily_recommendation']['weekend']} hours")
    
    print("\n✅ Test completed!")