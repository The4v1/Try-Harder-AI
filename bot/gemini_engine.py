"""
Google Gemini AI Engine
========================

Handles all interactions with the Google Gemini API for personalized
study plan generation, resource recommendations, and conversational guidance.

Features:
- Gemini 1.5 Flash/Pro support (FREE tier available!)
- 2M token context window (Pro) / 1M tokens (Flash)
- Async execution for high performance
- Rate limiting and error handling
- Emoji-rich response formatting
- Step-by-step answer generation
- Certification-specific guidance
- Cybersecurity-optimized safety settings
"""

import os
import logging
import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path
import aiohttp
import json

# Setup logging
logger = logging.getLogger(__name__)


class GeminiAI:
    """
    Google Gemini AI integration for personalized OffSec certification guidance.
    Supports Gemini 1.5 Flash (fast, free) and Gemini 1.5 Pro (best quality, free).
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize Gemini AI client.
        
        Args:
            api_key: Google Gemini API key (defaults to env variable)
            model: Model to use (defaults to gemini-3-flash-preview)
        """
        # Load primary key
        primary_key = api_key or os.getenv("GEMINI_API_KEY")
        
        # Initialize key list
        self.api_keys = []
        if primary_key:
            self.api_keys.append(primary_key)
            
        # Load additional keys (GEMINI_API_KEY_2, _3, etc.)
        for i in range(2, 6): # Support up to 5 api keys
            extra_key = os.getenv(f"GEMINI_API_KEY_{i}")
            if extra_key and extra_key not in self.api_keys:
                self.api_keys.append(extra_key)
        
        if not self.api_keys:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        self.current_key_index = 0
        self.api_key = self.api_keys[0] # Current active key
        
        logger.info(f"🔑 Loaded {len(self.api_keys)} API keys for rotation")
        
        # API Configuration
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = model or os.getenv("AI_MODEL", "gemini-3-flash-preview")
        self.fallback_model = os.getenv("AI_FALLBACK_MODEL", os.getenv("FALLBACK_AI_MODEL", "gemini-2.5-flash-lite-preview-09-2025"))

        # Clean model name - remove any 'models/' prefix if present
        self.model = self.model.replace('models/', '')
        self.max_tokens = int(os.getenv("AI_MAX_TOKENS", "8192"))
        self.temperature = float(os.getenv("AI_TEMPERATURE", "0.7"))
        
        # Rate limiting - 2 concurrent requests for free tier
        self.semaphore = asyncio.Semaphore(2)
        
        # Session management
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Load prompts
        self.prompts_dir = Path(__file__).parent.parent / "prompts"
        self.system_prompt = self._load_prompt("system_prompt.txt")
        self.cert_prompts = self._load_cert_prompts()
        
        logger.info(f"✅ Gemini AI engine initialized with model: {self.model}")
    
    def _load_prompt(self, filename: str) -> str:
        """
        Load a prompt template from file.
        
        Args:
            filename: Name of the prompt file
            
        Returns:
            Prompt content as string
        """
        try:
            prompt_path = self.prompts_dir / filename
            if prompt_path.exists():
                with open(prompt_path, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            else:
                logger.warning(f"⚠️ Prompt file not found: {filename}")
                return self._get_default_system_prompt()
        except Exception as e:
            logger.error(f"❌ Error loading prompt {filename}: {e}")
            return self._get_default_system_prompt()
    
    def _get_default_system_prompt(self) -> str:
        """
        Get default system prompt if file loading fails.
        
        Returns:
            Default system prompt
        """
        return """You are an elite OffSec certification mentor and penetration testing expert.

Your communication style:
- Use emojis liberally for visual appeal (🎯 💡 ✅ 🔥 ⚡ 📚 etc.)
- Format answers in clear steps with symbols (→ • ✓ ➜)
- Be concise and actionable, not lengthy or theoretical
- Use headers with ** ** for emphasis
- Number steps when providing instructions (1️⃣ 2️⃣ 3️⃣)
- Highlight key points with ✅ and warnings with ⚠️

Your expertise:
- All OffSec certifications (OSCP, OSEP, OSWE, OSED, OSWP, OSWA, OSMR, OSDA, KLCP)
- Penetration testing methodologies
- Cybersecurity tools and techniques
- Study strategies and exam preparation
- Career guidance in offensive security

Always provide practical, hands-on advice with specific examples and resources."""
    
    def _load_cert_prompts(self) -> Dict[str, str]:
        """
        Load all certification-specific prompts.
        
        Returns:
            Dictionary mapping cert codes to their prompts
        """
        cert_prompts = {}
        cert_codes = ["oscp", "osep", "oswe", "osed", "oswp", "oswa", "osmr", "osda", "klcp", "oscc", "osee", "osir"]
        
        for cert in cert_codes:
            prompt = self._load_prompt(f"{cert}_prompt.txt")
            if prompt and prompt != self._get_default_system_prompt():
                cert_prompts[cert.upper()] = prompt
        
        logger.info(f"📝 Loaded {len(cert_prompts)} certification prompts")
        return cert_prompts

    def _rotate_api_key(self):
        """Switch to next available API key."""
        if len(self.api_keys) > 1:
            self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
            self.api_key = self.api_keys[self.current_key_index]
            logger.warning(f"🔄 Switching to API Key #{self.current_key_index + 1} due to rate limit")
            return True
        return False
    
    async def _ensure_session(self):
        """Ensure aiohttp session is created."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
    
    async def _call_api(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        max_retries: int = 3,
        model_override: Optional[str] = None
    ) -> str:
        """
        Call Gemini API with retry logic.
        
        Args:
            prompt: User prompt/question
            system_instruction: System instruction (optional)
            max_retries: Maximum retry attempts
            model_override: Override default model (e.g., use 'gemini-3-flash-preview' for speed)
            
        Returns:
            AI response text
        """
        await self._ensure_session()
        
        # Build Gemini API request
        # Use override if provided, otherwise default self.model
        current_model = model_override or self.model
        
        # Adjust max_retries to ensure we try all keys if needed
        # If we have 3 keys, we want at least 3 attempts to try them all
        effective_retries = max(max_retries, len(self.api_keys) + 1)
        
        # Add extra retries if we have a fallback model to ensure we try it
        if self.fallback_model and current_model != self.fallback_model:
            effective_retries += 1
        
        for attempt in range(effective_retries):
            # Construct URL for current model
            model_name = current_model.replace('models/', '')
            url = f"{self.base_url}/models/{model_name}:generateContent"
            
            # ADD THIS DEBUG LINE:
            logger.info(f"🔍 DEBUG - Constructed URL: {url}")
            logger.info(f"🔍 DEBUG - Base URL: {self.base_url}")
            logger.info(f"🔍 DEBUG - Model name: {model_name}")

            # Prepend system instruction to prompt if provided (v1 API doesn't support systemInstruction field)
            full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt

            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": full_prompt}
                    ]
                }
            ],
                "generationConfig": {
                    "temperature": self.temperature,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": self.max_tokens,
                },
                "safetySettings": [
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_NONE"  # Allow cybersecurity content
                    },
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    }
                ]
            }
            
            # Update key param for current rotation
            params = {"key": self.api_key}
            
            try:
                async with self.session.post(
                    url,
                    params=params,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=90)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Extract text from Gemini response
                        try:
                            result = data['candidates'][0]['content']['parts'][0]['text']
                            
                            if result:
                                logger.info(f"✅ Gemini API response received (Attempt {attempt + 1})")
                                return result
                        except (KeyError, IndexError) as e:
                            logger.error(f"❌ Failed to parse Gemini response: {e}")
                            logger.debug(f"Response data: {data}")
                    
                    elif response.status in [404, 503]:
                        logger.warning(f"❌ Model Error {response.status}: {current_model}")
                        
                        # Switch to fallback if available and not already using it
                        if self.fallback_model and current_model != self.fallback_model:
                            logger.warning(f"🔄 Switching to fallback model: {self.fallback_model}")
                            current_model = self.fallback_model
                            continue
                            
                        error_text = await response.text()
                        logger.error(f"❌ API Error {response.status}: {error_text}")

                    elif response.status == 429:
                        logger.warning(f"⚠️ Rate limit hit (Attempt {attempt + 1})")
                        
                        # Try to rotate key!
                        rotated = self._rotate_api_key()
                        
                        if rotated:
                            logger.info("🔄 Retrying immediately with new key...")
                            # Don't wait, just continue next loop with new key
                            continue
                        else:
                             # No extra keys, use standard backoff
                            wait_time = 2 ** (attempt + 1)
                            await asyncio.sleep(wait_time)
                            continue
                    
                    elif response.status in [401, 403]:
                        error_text = await response.text()
                        logger.error(f"❌ API Authentication Error: {error_text}")
                        # Could try rotating here too if key is invalid
                        if self._rotate_api_key():
                             continue
                        return "⚠️ API key invalid. Please check your GEMINI_API_KEY! 🔑"
                    
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ API Error {response.status}: {error_text}")
                        
            except asyncio.TimeoutError:
                logger.error(f"⏰ Request timeout (Attempt {attempt + 1})")
                
            except Exception as e:
                logger.error(f"❌ API Error (Attempt {attempt + 1}): {e}")
            
            # Exponential backoff
            if attempt < max_retries - 1:
                wait_time = 2 ** (attempt + 1)
                logger.info(f"⏳ Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
        
        return "⚠️ AI Service is currently busy. Please 'Try Harder' in a few minutes! 💪"
    
    async def ask(
        self,
        question: str,
        use_emoji_format: bool = True
    ) -> str:
        """
        Ask a question and get an emoji-rich, step-by-step answer.
        
        Args:
            question: User's question
            use_emoji_format: Whether to use emoji-rich formatting
            
        Returns:
            Formatted answer
        """
        try:
            # Special system instruction for /ask command
            ask_system_instruction = """You are an elite cybersecurity mentor. 

CRITICAL FORMATTING RULES:
- ALWAYS use emojis heavily (🎯 💡 ✅ 🔥 ⚡ 📚 💪 🛡️ ⚔️ 🎓)
- Format in clear steps with symbols (→ • ✓ ➜ ▸)
- Use numbered steps with emoji numbers (1️⃣ 2️⃣ 3️⃣ 4️⃣)
- Keep answers CONCISE and ACTIONABLE
- NO lengthy paragraphs - use bullet points
- Highlight key points with ✅ or 🔥
- Show warnings with ⚠️
- Use ** ** for emphasis
- Add separators like ━━━━━ between sections

Example format:
🎯 **[Main Topic]**

📌 **Quick Overview:**
→ Point 1
→ Point 2

💡 **Key Points:**
✅ Important fact 1
✅ Important fact 2

⚡ **Quick Steps:**
1️⃣ First step
2️⃣ Second step
3️⃣ Third step

🔥 **Pro Tip:** [Insider advice]

Be direct, visual, and helpful!"""
            
            # Force using Flash model for speed (5-8s target)
            response = await self._call_api(
                prompt=ask_system_instruction + "\n\nQuestion: " + question,
                model_override="gemini-3-flash-preview"
            )
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Error in ask: {e}")
            return "⚠️ I encountered an error. Please try rephrasing your question! 🤔"
    
    async def generate_roadmap(
        self,
        certification: str,
        skill_level: str,
        assessment_data: Dict[str, Any],
        cert_data: Dict[str, Any],
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a personalized study roadmap.
        
        Args:
            certification: Certification code (e.g., "OSCP")
            skill_level: User's skill level (Beginner/Intermediate/Advanced)
            assessment_data: User's assessment responses and scores
            cert_data: Certification data from YAML database
            user_context: Additional user context (optional)
            
        Returns:
            Personalized study roadmap as formatted text
        """
        try:
            # Build the prompt
            prompt = self._build_roadmap_prompt(
                certification, skill_level, assessment_data, cert_data, user_context
            )
            
            # Get certification-specific system instruction
            cert_prompt = self.cert_prompts.get(certification, "")
            full_system_instruction = f"{self.system_prompt}\n\n{cert_prompt}" if cert_prompt else self.system_prompt
            
            logger.info(f"🗺️ Generating roadmap for {certification} ({skill_level})")
            
            async with self.semaphore:
                response = await self._call_api(prompt, full_system_instruction)
            
            logger.info(f"✅ Successfully generated roadmap ({len(response)} chars)")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error generating roadmap: {e}")
            return "⚠️ An error occurred while generating your roadmap. Please try again! 🔄"
    
    def _build_roadmap_prompt(
        self,
        certification: str,
        skill_level: str,
        assessment_data: Dict[str, Any],
        cert_data: Dict[str, Any],
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Build a comprehensive prompt for roadmap generation.
        
        Args:
            certification: Certification code
            skill_level: User's skill level
            assessment_data: Assessment responses
            cert_data: Certification data
            user_context: Additional context
            
        Returns:
            Complete prompt
        """
        # Define comprehensive fallback defaults for incomplete cert data
        DEFAULT_EXAM = {
            'duration': '24 hours practical exam + 24 hours for report',
            'passing_score': '70 points',
            'format': 'Hands-on practical exam with professional report'
        }
        
        DEFAULT_TOPICS = [
            {'name': 'Core concepts and fundamentals', 'weight': 30},
            {'name': 'Practical techniques and methodologies', 'weight': 40},
            {'name': 'Advanced exploitation and tools', 'weight': 20},
            {'name': 'Documentation and reporting', 'weight': 10}
        ]
        
        DEFAULT_RESOURCES = {
            'essential': [
                {'name': 'Official course material', 'cost': 'Included', 'priority': 'High'},
                {'name': 'Practice labs', 'cost': 'Included', 'priority': 'High'}
            ],
            'practice_platforms': [
                {'name': 'HackTheBox', 'cost': 'Free/VIP $14/month'},
                {'name': 'TryHackMe', 'cost': 'Free/Premium $10.99/month'},
                {'name': 'Proving Grounds', 'cost': '$19/month'}
            ]
        }
        
        # Use cert data with intelligent fallbacks
        exam_info = cert_data.get('exam') or DEFAULT_EXAM
        if not exam_info or (isinstance(exam_info, dict) and not exam_info):
            exam_info = DEFAULT_EXAM
        
        topics = cert_data.get('topics') or DEFAULT_TOPICS
        if not topics or (isinstance(topics, list) and not topics):
            topics = DEFAULT_TOPICS
        
        resources = cert_data.get('resources') or DEFAULT_RESOURCES
        if not resources or (isinstance(resources, dict) and not resources):
            resources = DEFAULT_RESOURCES
        
        study_plan = cert_data.get('study_plan', {})
        
        prompt = f"""Generate a personalized study roadmap for {certification} certification.

**User Profile:**
- Skill Level: {skill_level}
- Assessment Score: {assessment_data.get('score_percentage', 'N/A')}%
- Strengths: {', '.join(assessment_data.get('strengths', ['General knowledge']))}
- Areas to Improve: {', '.join(assessment_data.get('weaknesses', ['Various areas']))}

**Assessment Responses:**
"""
        
        for question, answer in list(assessment_data.get('responses', {}).items())[:5]:
            prompt += f"- {question}: {answer}\n"
        
        duration_weeks = user_context.get('duration_weeks', 12) if user_context else 12
        
        prompt += f"""

**Certification Details:**
- Exam Duration: {exam_info.get('duration', 'N/A')}
- Passing Score: {exam_info.get('passing_score', 'N/A')}
- Target Study Duration: {duration_weeks} weeks

**Key Topics ({len(topics)} total):**
"""
        
        for topic in topics[:8]:
            topic_name = topic.get('name', 'Unknown')
            weight = topic.get('weight', 0)
            prompt += f"- {topic_name} ({weight}% weight)\n"
        
        prompt += f"""

**Available Resources:**
- Essential:
"""
        for item in resources.get('essential', [])[:5]:
            prompt += f"  - {item.get('name')} ({item.get('url', 'N/A')})\n"

        # Add other resource categories
        for category in ['tools', 'cheatsheets', 'videos', 'books', 'communities']:
            if category in resources and resources[category]:
                prompt += f"\n- {category.replace('_', ' ').title()}:\n"
                for item in resources[category][:5]:
                     prompt += f"  - {item.get('name')} ({item.get('url', 'N/A')})\n"
        
        prompt += """

**GENERATE A ROADMAP WITH:**

1️⃣ **Week-by-Week Timeline** ({duration_weeks} weeks total)
   - Specific weekly goals
   - Adjusted for {skill_level} level
   - Realistic time estimates

2️⃣ **Prioritized Learning Path**
   - Focus on weaknesses: {', '.join(assessment_data.get('weaknesses', [])[:3])}
   - Build on strengths: {', '.join(assessment_data.get('strengths', [])[:3])}
   - Progressive difficulty

3️⃣ **Resource Recommendations**
   - Top 5 essential resources (MUST use `[Name](URL)` markdown format)
   - ⚠️ **CRITICAL:** Use ONLY the URLs provided in 'Available Resources' above. Do NOT use your own links.
   - Specific practice machines/challenges
   - Free vs paid options
   - Time investment estimate

4️⃣ **Weekly Milestones**
   - Clear completion criteria
   - Skills to master each week
   - Progress checkpoints

5️⃣ **Exam Preparation** (Final 2 weeks)
   - Mock exam schedule
   - Report writing practice
   - Last-minute review

6️⃣ **Success Tips**
   - Common pitfalls to avoid
   - Time management strategies
   - Motivation boosters

**FORMATTING REQUIREMENTS (CRITICAL):**
✅ Use `##` or `###` for main headers (Make them BIG)
✅ **Add empty lines** between every list item and section for readability
✅ Use blockquotes (`>`) for key goals or milestones
✅ Use widely spaced bullet points
✅ Example format:

### 📅 PHASE 1: [Title]

> *Focus: [Key Goal]*

**Week 1: [Topic]**
• Task A
• Task B

**Week 2: [Topic]**
• Task C
• Task D
...

✅ Use emojis for visual appeal (📚 🎯 💪 ⚡ ✅ 🔥)
✅ Keep sections concise and actionable
✅ Add encouraging tone throughout
✅ Include specific machine names or challenges where applicable

Make it motivating, spacious, and beautiful! 🚀"""
        
        return prompt
    
    async def get_resource_recommendations(
        self,
        certification: str,
        skill_level: str,
        focus_areas: List[str],
        cert_data: Dict[str, Any]
    ) -> str:
        """
        Get AI-powered resource recommendations.
        
        Args:
            certification: Certification code
            skill_level: User's skill level
            focus_areas: Specific areas user wants to focus on
            cert_data: Certification data
            
        Returns:
            Formatted resource recommendations
        """
        try:
            resources = cert_data.get('resources', {})
            
            prompt = f"""Recommend the best resources for {certification} preparation.

**User Context:**
- Skill Level: {skill_level}
- Focus Areas: {', '.join(focus_areas)}

**Available Resources:**
"""
            
            for category, items in list(resources.items())[:5]:
                if isinstance(items, list) and items:
                    prompt += f"\n**{category.replace('_', ' ').title()}:**\n"
                    for item in items[:5]:
                        name = item.get('name', 'Unknown')
                        cost = item.get('cost', 'Unknown')
                        priority = item.get('priority', 'N/A')
                        prompt += f"- {name} (Cost: {cost}, Priority: {priority})\n"
            
            prompt += """

**Provide:**
1. Top 5 resources prioritized for this user
2. Why each is recommended
3. Suggested order
4. Free alternatives
5. Time investment estimate

Use emojis (📚 💰 ⚡ ✅) and clear formatting!"""
            
            async with self.semaphore:
                response = await self._call_api(prompt, self.system_prompt)
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Error getting recommendations: {e}")
            return "⚠️ Error generating recommendations. Please try again! 🔄"
    
    async def get_exam_tips(
        self,
        certification: str,
        cert_data: Dict[str, Any]
    ) -> str:
        """
        Get AI-powered exam tips and strategies.
        
        Args:
            certification: Certification code
            cert_data: Certification data
            
        Returns:
            Formatted exam tips
        """
        try:
            exam_info = cert_data.get('exam', {})
            
            # FIX: Handle tips structure properly - can be dict or list
            tips_data = cert_data.get('tips', {})
            success_tips = []
            
            # Tips can be a dict with categories or a list
            if isinstance(tips_data, dict):
                # Extract tips from all categories (general, study_tips, exam_day, etc.)
                for category, tips_list in tips_data.items():
                    if isinstance(tips_list, list):
                        success_tips.extend(tips_list)
            elif isinstance(tips_data, list):
                success_tips = tips_data
            
            logger.debug(f"📝 Found {len(success_tips)} tips for {certification}")
            
            prompt = f"""Provide comprehensive exam tips for {certification}.

**Exam Format:**
- Duration: {exam_info.get('duration', 'N/A')}
- Format: {exam_info.get('format', 'N/A')}
- Passing Score: {exam_info.get('passing_score', 'N/A')}

**Known Success Tips:**
"""
            
            # Add tips if available (limit to first 10)
            if success_tips:
                for tip in success_tips[:10]:
                    prompt += f"- {tip}\n"
            else:
                prompt += "(No predefined tips available - AI will generate fresh tips)\n"
            
            prompt += """

**Provide:**
1️⃣ **Day Before Exam**: Preparation checklist
2️⃣ **Exam Day**: Hour-by-hour strategy
3️⃣ **Time Management**: How to allocate time
4️⃣ **Common Mistakes**: What to avoid
5️⃣ **Report Writing**: Documentation tips
6️⃣ **Mental Game**: Staying focused
7️⃣ **Post-Exam**: Next steps

Use emojis (🎯 ⚠️ ✅ 💡) and be specific and encouraging!"""
            
            async with self.semaphore:
                response = await self._call_api(prompt, self.system_prompt)
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Error getting exam tips: {e}", exc_info=True)
            return "⚠️ Error generating exam tips. Please try again! 🔄"
    
    async def chat_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        user_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a conversational response.
        
        Args:
            user_message: User's message
            conversation_history: Previous messages (optional)
            user_data: User context (optional)
            
        Returns:
            AI response
        """
        try:
            # Build system instruction with user context
            system = self.system_prompt
            if user_data:
                cert = user_data.get('current_cert', '')
                level = user_data.get('skill_level', '')
                if cert and level:
                    system += f"\n\nUser is preparing for {cert} at {level} level."
            
            # For Gemini, we'll include conversation history in the prompt
            full_prompt = user_message
            if conversation_history:
                history_text = "\n\n**Previous conversation:**\n"
                for msg in conversation_history[-5:]:  # Last 5 messages
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    history_text += f"{role}: {content}\n"
                full_prompt = history_text + "\n\n**Current question:**\n" + user_message
            
            async with self.semaphore:
                response = await self._call_api(full_prompt, system)
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Error in chat response: {e}")
            return "⚠️ I encountered an error. Please try rephrasing! 🤔"
    
    def get_model_info(self) -> Dict[str, str]:
        """
        Get information about the current AI model.
        
        Returns:
            Dictionary with model information
        """
        return {
            "provider": "Google Gemini",
            "model": self.model,
            "max_tokens": str(self.max_tokens),
            "temperature": str(self.temperature),
            "context_window": "1M tokens (Flash) / 2M tokens (Pro)",
            "capabilities": "Cybersecurity expertise, roadmap generation, resource recommendations, conversational guidance"
        }
    
    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()
            logger.info("🔒 Gemini AI session closed")


# Utility functions for testing
async def test_connection(api_key: Optional[str] = None) -> bool:
    """
    Test the connection to Gemini API.
    
    Args:
        api_key: API key to test (optional)
        
    Returns:
        True if connection successful, False otherwise
    """
    try:
        ai = GeminiAI(api_key)
        response = await ai.ask("Test: What is OSCP?")
        await ai.close()
        return bool(response and "⚠️" not in response)
    except Exception as e:
        logger.error(f"❌ Connection test failed: {e}")
        return False


if __name__ == "__main__":
    # Test the AI engine
    import asyncio
    
    async def main():
        print("🧪 Testing Gemini AI Engine...")
        ai = GeminiAI()
        print(f"✅ Initialized: {ai.get_model_info()}")
        
        # Test ask command with emoji formatting
        print("\n💬 Testing /ask command format:")
        response = await ai.ask("What is OSCP?")
        print(response)
        
        await ai.close()
        print("\n✅ Test completed!")
    
    asyncio.run(main())