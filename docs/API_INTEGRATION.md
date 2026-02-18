# 🤖 API Integration Guide - Try-Harder-AI Bot

## Overview

This document provides comprehensive documentation for the **Google Gemini AI** integration in the Try-Harder-AI Discord bot. The bot uses Google's Gemini API directly, providing access to Gemini 1.5 Flash and other Gemini model variants for powerful AI-driven features. All bot commands use Discord **slash commands** (`/`).

---

## Table of Contents

1. [Google Gemini API Overview](#google-gemini-api-overview)
2. [Supported AI Models](#supported-ai-models)
3. [API Configuration](#api-configuration)
4. [Authentication](#authentication)
5. [Core Features](#core-features)
6. [API Endpoints](#api-endpoints)
7. [Request/Response Format](#requestresponse-format)
8. [Error Handling](#error-handling)
9. [Rate Limiting](#rate-limiting)
10. [Cost Management](#cost-management)
11. [Best Practices](#best-practices)
12. [Code Examples](#code-examples)
13. [Troubleshooting](#troubleshooting)

---

## 🌐 Google Gemini API Overview

**What is the Gemini API?**
- Google's official API for Gemini family of AI models
- Access to Gemini 1.5 Flash, Gemini 1.5 Pro, Gemini 1.0 Pro, and more
- Generous free tier with pay-as-you-go pricing on paid tier
- Native multimodal support (text, images, video, audio, code)
- Available via Google AI Studio or Vertex AI

**Official Resources:**
- Website: https://ai.google.dev
- Documentation: https://ai.google.dev/docs
- API Keys (Google AI Studio): https://aistudio.google.com/apikey
- Pricing: https://ai.google.dev/pricing
- Model Overview: https://ai.google.dev/gemini-api/docs/models/gemini

**Why Gemini 1.5 Flash for Try-Harder-AI?**
- ✅ Extremely fast inference — ideal for Discord's real-time UX
- ✅ Generous free tier (15 RPM, 1M TPM, 1500 RPD at no cost)
- ✅ 1 million token context window
- ✅ Native multimodal support for future features
- ✅ Simple single API key setup via Google AI Studio

---

## 🤖 Supported AI Models

The bot supports multiple Gemini model variants. Each has different strengths and pricing tiers:

### Primary Models

#### 1. **Gemini 1.5 Flash** ⚡ (RECOMMENDED — DEFAULT)
```python
Model ID: "gemini-1.5-flash"
```
- **Best for:** Fast responses, general Q&A, step-by-step guidance, Discord interactions
- **Strengths:** Very fast, cost-effective, 1M token context, multimodal
- **Use case:** Default model for all `/ask`, `/roadmap`, `/assess` commands
- **Free tier:** 15 RPM / 1,000,000 TPM / 1,500 RPD
- **Paid pricing:** $0.075 per 1M input tokens (≤128K) / $0.30 per 1M output tokens
- **Context window:** 1,000,000 tokens

#### 2. **Gemini 1.5 Flash-8B** 🪶 (BUDGET OPTION)
```python
Model ID: "gemini-1.5-flash-8b"
```
- **Best for:** Simple queries, quick lookups, lightweight interactions
- **Strengths:** Fastest in Flash family, lowest cost, very low latency
- **Use case:** Simple one-liner questions, quick commands
- **Free tier:** 15 RPM / 1,000,000 TPM / 1,500 RPD
- **Paid pricing:** $0.0375 per 1M input tokens (≤128K) / $0.15 per 1M output tokens
- **Context window:** 1,000,000 tokens

#### 3. **Gemini 1.5 Pro** 🧠 (ADVANCED)
```python
Model ID: "gemini-1.5-pro"
```
- **Best for:** Complex reasoning, long-form roadmap generation, detailed code analysis
- **Strengths:** Highest intelligence, 2M token context, best for nuanced content
- **Use case:** `/roadmap` with complex requirements, deep technical explanations
- **Free tier:** 2 RPM / 32,000 TPM / 50 RPD
- **Paid pricing:** $1.25 per 1M input tokens (≤128K) / $5.00 per 1M output tokens
- **Context window:** 2,000,000 tokens

#### 4. **Gemini 2.0 Flash** 🚀 (NEXT-GEN)
```python
Model ID: "gemini-2.0-flash"
```
- **Best for:** Cutting-edge tasks requiring the latest capabilities
- **Strengths:** Latest model, improved reasoning over 1.5 Flash, fast
- **Use case:** Future-facing features, improved guidance quality
- **Free tier:** 15 RPM / 1,000,000 TPM / 1,500 RPD
- **Paid pricing:** $0.10 per 1M input tokens / $0.40 per 1M output tokens
- **Context window:** 1,000,000 tokens

#### 5. **Gemini 1.0 Pro** (LEGACY)
```python
Model ID: "gemini-1.0-pro"
```
- **Best for:** Stable, well-tested workflows
- **Strengths:** Reliable, widely tested, text-only
- **Use case:** Fallback model if newer versions are unavailable
- **Free tier:** 15 RPM / 32,000 TPM / 1,500 RPD
- **Context window:** 32,768 tokens

---

### Model Selection Strategy

```python
# Default model — best balance of speed, quality, and cost
DEFAULT_MODEL = "gemini-1.5-flash"

# Model selection based on use case
MODEL_FOR_ROADMAP    = "gemini-1.5-pro"       # Long-form planning (2M context)
MODEL_FOR_QUICK_ASK  = "gemini-1.5-flash"     # Fast Discord responses
MODEL_FOR_CODE       = "gemini-1.5-pro"       # Code analysis and review
MODEL_FOR_SIMPLE     = "gemini-1.5-flash-8b"  # Lightweight queries
MODEL_FOR_LATEST     = "gemini-2.0-flash"     # Cutting-edge tasks
MODEL_FALLBACK       = "gemini-1.0-pro"       # Stable fallback
```

---

## ⚙️ API Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Optional - Model Selection
DEFAULT_AI_MODEL=gemini-1.5-flash

# Optional - Generation Parameters
AI_MAX_TOKENS=4096
AI_TEMPERATURE=0.7
AI_TIMEOUT=60

# Optional - Application Info
APP_NAME=Try-Harder-AI
```

### Configuration in Code

```python
# config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API Configuration
GEMINI_CONFIG = {
    "api_key": os.getenv("GEMINI_API_KEY"),
    "default_model": os.getenv("DEFAULT_AI_MODEL", "gemini-1.5-flash"),
    "max_tokens": int(os.getenv("AI_MAX_TOKENS", 4096)),
    "temperature": float(os.getenv("AI_TEMPERATURE", 0.7)),
    "timeout": int(os.getenv("AI_TIMEOUT", 60)),
    "app_name": os.getenv("APP_NAME", "Try-Harder-AI"),
}

# Model aliases for easy switching
MODEL_ALIASES = {
    "flash":      "gemini-1.5-flash",
    "flash8b":    "gemini-1.5-flash-8b",
    "pro":        "gemini-1.5-pro",
    "flash2":     "gemini-2.0-flash",
    "legacy":     "gemini-1.0-pro",
}
```

---

## 🔐 Authentication

### Getting an API Key

1. **Go to Google AI Studio**
   - Visit: https://aistudio.google.com/apikey
   - Sign in with your Google account

2. **Create an API Key**
   - Click **"Create API key"**
   - Select or create a Google Cloud project
   - Copy the key (starts with `AIzaSy`)

3. **Enable Billing (Optional for Paid Tier)**
   - Free tier works without billing enabled
   - For higher rate limits, link a billing account in Google Cloud Console

### Security Best Practices

```python
# ✅ GOOD - Use environment variables
api_key = os.getenv("GEMINI_API_KEY")

# ❌ BAD - Never hardcode the API key
api_key = "AIzaSyXXXXXXXXXX"  # NEVER DO THIS!

# ✅ GOOD - Validate key exists on startup
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# ✅ GOOD - Never log the full key
logger.info(f"Using Gemini API key: {api_key[:10]}...")
```

### Configuring the Gemini Client

```python
import google.generativeai as genai

# Configure once at startup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create a model instance
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "max_output_tokens": 4096,
        "temperature": 0.7,
        "top_p": 1,
    }
)
```

---

## 🎯 Core Features

### 1. **Skill Assessment** (`/assess`)
- AI analyzes user responses to assessment questions
- Provides detailed feedback on weak/strong areas
- Recommends appropriate difficulty level

```python
async def analyze_assessment(user_responses, certification):
    prompt = f"""
    Analyze this skill assessment for {certification}:
    User responses: {user_responses}
    
    Provide:
    1. Overall skill level (beginner/intermediate/advanced)
    2. Weak areas that need focus
    3. Strong areas
    4. Specific study recommendations
    """
    return await ai_engine.generate(prompt)
```

### 2. **Personalized Roadmap Generation** (`/roadmap`)
- Creates customized study plans (6–24 weeks)
- Adapts to user's skill level and time availability
- Includes milestones, resources, and practice machines

```python
async def generate_roadmap(certification, skill_level, weeks, weak_areas):
    prompt = f"""
    Create a {weeks}-week study roadmap for {certification}.
    Skill level: {skill_level}
    Focus on: {weak_areas}
    
    Include:
    - Weekly topics and goals
    - Specific resources and practice machines
    - Time estimates
    - Milestones
    """
    return await ai_engine.generate(prompt)
```

### 3. **Contextual Q&A** (`/ask` command)
- Answer certification-specific questions
- Provide step-by-step guidance with emojis
- Format responses for easy reading in Discord

```python
async def answer_question(question, certification):
    system_prompt = load_certification_prompt(certification)
    
    prompt = f"""
    Question: {question}
    Certification context: {certification}
    
    Provide a concise, step-by-step answer with:
    - Emojis for visual structure (✅ 🎯 💡 ⚠️)
    - Clear numbered steps
    - Practical examples
    - Key commands/techniques
    - No lengthy theory - focus on actionable info
    """
    return await ai_engine.generate(prompt, system_prompt)
```

### 4. **Resource Recommendations** (`/resources`)
- Suggest practice machines based on topic
- Recommend courses and tools
- Provide learning paths

---

## 🔌 API Endpoints

### Main Endpoint: Generate Content

```
POST https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}
```

**Request Body:**
```json
{
  "contents": [
    {
      "role": "user",
      "parts": [{ "text": "How do I exploit a SUID binary?" }]
    }
  ],
  "systemInstruction": {
    "parts": [{ "text": "You are an OffSec certification mentor..." }]
  },
  "generationConfig": {
    "maxOutputTokens": 4096,
    "temperature": 0.7,
    "topP": 1
  }
}
```

### Using the Official Python SDK (Recommended)

```bash
pip install google-generativeai
```

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("How do I exploit a SUID binary?")
print(response.text)
```

---

## 📨 Request/Response Format

### Request Structure (Async with SDK)

```python
import google.generativeai as genai
import asyncio
from typing import Optional

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def make_request(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_name: str = "gemini-1.5-flash",
    **kwargs
) -> str:
    """
    Make an async request to the Gemini API

    Args:
        prompt: User message/prompt
        system_prompt: Optional system instruction
        model_name: Gemini model ID
        **kwargs: Additional generation config overrides

    Returns:
        AI-generated response text
    """
    generation_config = {
        "max_output_tokens": kwargs.get("max_tokens", 4096),
        "temperature": kwargs.get("temperature", 0.7),
        "top_p": kwargs.get("top_p", 1),
    }

    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
        system_instruction=system_prompt,
    )

    # Run synchronous SDK call in thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None, lambda: model.generate_content(prompt)
    )

    return response.text
```

### Response Structure (SDK)

**Success:**
```python
response = model.generate_content("...")
print(response.text)           # The generated text
print(response.candidates)     # All candidate completions
print(response.usage_metadata) # Token counts
```

**Token usage:**
```python
usage = response.usage_metadata
print(usage.prompt_token_count)     # Input tokens
print(usage.candidates_token_count) # Output tokens
print(usage.total_token_count)      # Total tokens
```

**REST API Success Response:**
```json
{
  "candidates": [
    {
      "content": {
        "parts": [{ "text": "To exploit a SUID binary:\n\n1. Find SUID binaries..." }],
        "role": "model"
      },
      "finishReason": "STOP",
      "index": 0
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 150,
    "candidatesTokenCount": 250,
    "totalTokenCount": 400
  }
}
```

**REST API Error Response:**
```json
{
  "error": {
    "code": 400,
    "message": "API key not valid.",
    "status": "INVALID_ARGUMENT"
  }
}
```

---

## ⚠️ Error Handling

### Common Errors

| Error Code | Meaning | Solution |
|------------|---------|----------|
| 400 | Invalid request / bad API key | Check your API key and request format |
| 403 | Permission denied | Verify API key has access to the model |
| 429 | Rate limit exceeded | Implement exponential backoff |
| 500 | Internal server error | Retry with exponential backoff |
| 503 | Service unavailable | Retry or switch to fallback model |

### Error Handling Implementation

```python
import asyncio
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class GeminiError(Exception):
    """Base exception for Gemini API errors"""
    pass


class RateLimitError(GeminiError):
    """Rate limit exceeded"""
    pass


class InvalidKeyError(GeminiError):
    """API key is invalid or missing permissions"""
    pass


async def generate_with_retry(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_name: str = "gemini-1.5-flash",
    max_retries: int = 3,
    backoff_factor: float = 2.0
) -> Optional[str]:
    """
    Generate Gemini response with automatic retry and exponential backoff
    """
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_prompt,
    )
    loop = asyncio.get_event_loop()

    for attempt in range(max_retries):
        try:
            response = await loop.run_in_executor(
                None, lambda: model.generate_content(prompt)
            )
            return response.text

        except google_exceptions.ResourceExhausted as e:
            # 429 Rate limit
            wait_time = backoff_factor ** attempt
            logger.warning(f"Rate limited. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}...")
            await asyncio.sleep(wait_time)
            continue

        except google_exceptions.InvalidArgument as e:
            # 400 Bad request / invalid API key
            raise InvalidKeyError(f"Invalid API key or request: {e}")

        except google_exceptions.PermissionDenied as e:
            # 403 Not authorized
            raise InvalidKeyError(f"Permission denied: {e}")

        except google_exceptions.ServiceUnavailable as e:
            # 503 Server error
            wait_time = backoff_factor ** attempt
            logger.warning(f"Service unavailable. Retrying in {wait_time}s...")
            await asyncio.sleep(wait_time)
            continue

        except asyncio.TimeoutError:
            if attempt < max_retries - 1:
                logger.warning(f"Timeout. Retry {attempt + 1}/{max_retries}")
                await asyncio.sleep(backoff_factor ** attempt)
                continue
            raise

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise GeminiError(f"Unexpected error: {e}")

    raise GeminiError("Max retries exceeded")
```

---

## 🚦 Rate Limiting

### Gemini Free Tier Rate Limits

| Model | RPM | TPM | RPD |
|-------|-----|-----|-----|
| Gemini 1.5 Flash | 15 | 1,000,000 | 1,500 |
| Gemini 1.5 Flash-8B | 15 | 1,000,000 | 1,500 |
| Gemini 1.5 Pro | 2 | 32,000 | 50 |
| Gemini 2.0 Flash | 15 | 1,000,000 | 1,500 |
| Gemini 1.0 Pro | 15 | 32,000 | 1,500 |

> **RPM** = Requests Per Minute · **TPM** = Tokens Per Minute · **RPD** = Requests Per Day

### Rate Limiter Implementation

```python
import asyncio
from collections import deque
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple token-bucket rate limiter for Gemini API requests"""

    def __init__(self, max_requests: int = 14, time_window: int = 60):
        """
        Args:
            max_requests: Max requests allowed in time window
                          (default 14 = just under Gemini Flash's 15 RPM limit)
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()

    async def acquire(self):
        """Wait if necessary to stay within rate limit"""
        now = datetime.now()

        # Remove requests outside the time window
        while self.requests and self.requests[0] < now - timedelta(seconds=self.time_window):
            self.requests.popleft()

        if len(self.requests) >= self.max_requests:
            oldest_request = self.requests[0]
            wait_until = oldest_request + timedelta(seconds=self.time_window)
            wait_seconds = (wait_until - now).total_seconds()

            if wait_seconds > 0:
                logger.info(f"Rate limit reached. Waiting {wait_seconds:.1f}s")
                await asyncio.sleep(wait_seconds)

        self.requests.append(datetime.now())


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=14, time_window=60)


async def rate_limited_generate(prompt: str, **kwargs) -> str:
    await rate_limiter.acquire()
    return await generate_with_retry(prompt, **kwargs)
```

---

## 💰 Cost Management

### Gemini Pricing Overview

All prices are per **1 million tokens**. Prompts **≤128K tokens** use the standard rate:

| Model | Input (≤128K) | Output (≤128K) | Input (>128K) | Output (>128K) |
|-------|--------------|----------------|--------------|----------------|
| Gemini 1.5 Flash | $0.075 | $0.30 | $0.15 | $0.60 |
| Gemini 1.5 Flash-8B | $0.0375 | $0.15 | $0.075 | $0.30 |
| Gemini 1.5 Pro | $1.25 | $5.00 | $2.50 | $10.00 |
| Gemini 2.0 Flash | $0.10 | $0.40 | $0.10 | $0.40 |

> **Free tier:** All models have a free tier — no billing needed for development/testing.

### Tracking Token Usage

```python
class UsageTracker:
    """Track Gemini API usage and estimated costs"""

    # Pricing per 1M tokens (standard, ≤128K context)
    PRICING = {
        "gemini-1.5-flash":    {"input": 0.075,  "output": 0.30},
        "gemini-1.5-flash-8b": {"input": 0.0375, "output": 0.15},
        "gemini-1.5-pro":      {"input": 1.25,   "output": 5.00},
        "gemini-2.0-flash":    {"input": 0.10,   "output": 0.40},
        "gemini-1.0-pro":      {"input": 0.50,   "output": 1.50},
    }

    def __init__(self):
        self.total_requests = 0
        self.total_tokens = 0
        self.total_cost = 0.0
        self.usage_by_model = {}

    def track(self, model: str, prompt_tokens: int, completion_tokens: int):
        """Record usage and estimate cost for a single request"""
        self.total_requests += 1
        total = prompt_tokens + completion_tokens
        self.total_tokens += total

        if model in self.PRICING:
            cost = (
                (prompt_tokens / 1_000_000) * self.PRICING[model]["input"] +
                (completion_tokens / 1_000_000) * self.PRICING[model]["output"]
            )
            self.total_cost += cost

            if model not in self.usage_by_model:
                self.usage_by_model[model] = {"requests": 0, "tokens": 0, "cost": 0.0}

            self.usage_by_model[model]["requests"] += 1
            self.usage_by_model[model]["tokens"] += total
            self.usage_by_model[model]["cost"] += cost

    def get_summary(self) -> dict:
        return {
            "total_requests": self.total_requests,
            "total_tokens": self.total_tokens,
            "estimated_cost_usd": round(self.total_cost, 6),
            "by_model": self.usage_by_model,
        }


# Global tracker
usage_tracker = UsageTracker()

# Track after each request
response = model.generate_content(prompt)
usage = response.usage_metadata
usage_tracker.track(
    model="gemini-1.5-flash",
    prompt_tokens=usage.prompt_token_count,
    completion_tokens=usage.candidates_token_count,
)
```

### Cost Optimization Tips

1. **Use the right model for the task**
   - Use `gemini-1.5-flash` for most Discord commands (cheapest + fastest)
   - Reserve `gemini-1.5-pro` only for complex `/roadmap` generation

2. **Optimize prompts**
   - Be concise — trim unnecessary context
   - Use system instructions efficiently
   - Avoid re-sending large conversation history unnecessarily

3. **Set appropriate token limits**
   ```python
   max_output_tokens=800   # For short /ask answers
   max_output_tokens=4096  # For detailed /roadmap output
   ```

4. **Leverage the free tier**
   - `gemini-1.5-flash` has 1,500 free requests/day — more than enough for dev/testing
   - Only enable billing when the bot is production-ready

5. **Monitor usage**
   ```python
   if usage.total_token_count > 10_000:
       logger.warning(f"High token usage detected: {usage.total_token_count} tokens")
   ```

---

## ✅ Best Practices

### 1. Prompt Engineering

**Good Prompt Structure:**
```python
system_instruction = """
You are an OffSec certification mentor specializing in {certification}.

Guidelines:
- Provide step-by-step instructions with emojis (🎯 ✅ 💡)
- Focus on practical, actionable advice
- Keep responses concise — avoid lengthy theory
- Include specific commands and examples
- Format for easy Discord reading
"""

user_prompt = """
Question: {question}

Provide a clear, structured answer focused on:
1. The core concept
2. Practical steps
3. Example commands
4. Common pitfalls to avoid
"""
```

**Bad Prompt:**
```python
# ❌ Too vague
prompt = "Help me with OSCP"

# ✅ Specific and structured
prompt = "Explain Linux SUID privilege escalation with example commands and GTFOBins references"
```

### 2. Conversation / Chat History Management

```python
import google.generativeai as genai

class ConversationManager:
    """Manage multi-turn conversation history with Gemini"""

    def __init__(self, model_name: str = "gemini-1.5-flash", max_turns: int = 10):
        self.model = genai.GenerativeModel(model_name)
        self.chat = self.model.start_chat(history=[])
        self.max_turns = max_turns

    async def send(self, message: str) -> str:
        """Send a message and get a response, maintaining chat history"""
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, lambda: self.chat.send_message(message)
        )

        # Trim history to stay within token budget
        if len(self.chat.history) > self.max_turns * 2:
            # Keep only the most recent turns
            self.chat.history = self.chat.history[-(self.max_turns * 2):]

        return response.text

    def clear(self):
        """Reset conversation history"""
        self.chat = self.model.start_chat(history=[])
```

### 3. Response Formatting for Discord

```python
def format_ai_response(response: str, max_length: int = 2000) -> list:
    """
    Format Gemini response for Discord (2000 char limit per message)

    Returns list of message chunks
    """
    if len(response) <= max_length:
        return [response]

    chunks = []
    current_chunk = ""

    for para in response.split("\n\n"):
        if len(current_chunk) + len(para) + 2 <= max_length:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
```

### 4. Async Best Practices with Discord.py

```python
import discord
from discord import app_commands

# ✅ GOOD - Slash command with typing indicator
@app_commands.command(name="ask", description="Ask an OffSec question")
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer()  # Show "Bot is thinking..." in Discord
    response = await ai_engine.generate(question)
    await interaction.followup.send(response)

# ❌ BAD - Old prefix command approach (don't use)
# @bot.command()
# async def ask(ctx, *, question):
#     async with ctx.typing():
#         response = ai_engine.generate_sync(question)  # Blocks event loop!
#         await ctx.send(response)
```

---

## 💻 Code Examples

### Complete AI Engine Implementation

```python
# bot/ai_engine.py

import asyncio
import logging
import os
from typing import Optional

import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

logger = logging.getLogger(__name__)

# Configure the SDK at import time
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class GeminiAI:
    """Google Gemini AI integration for Try-Harder-AI Discord bot"""

    DEFAULT_MODEL = "gemini-1.5-flash"

    def __init__(self):
        self._validate_key()

    def _validate_key(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        logger.info(f"Gemini AI engine initialized (key: {api_key[:10]}...)")

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model_name: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate a Gemini AI response

        Args:
            prompt: User prompt text
            system_prompt: Optional system instruction context
            model_name: Gemini model to use (defaults to gemini-1.5-flash)
            **kwargs: Overrides for generation config (max_tokens, temperature, etc.)

        Returns:
            AI-generated response as string
        """
        model = genai.GenerativeModel(
            model_name=model_name or self.DEFAULT_MODEL,
            generation_config={
                "max_output_tokens": kwargs.get("max_tokens", 4096),
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 1),
            },
            system_instruction=system_prompt,
        )

        return await self._make_request(model, prompt)

    async def _make_request(self, model, prompt: str, max_retries: int = 3) -> str:
        """Internal method with retry logic"""
        loop = asyncio.get_event_loop()

        for attempt in range(max_retries):
            try:
                response = await loop.run_in_executor(
                    None, lambda: model.generate_content(prompt)
                )
                return response.text

            except google_exceptions.ResourceExhausted:
                wait = 2 ** attempt
                logger.warning(f"Rate limited. Retrying in {wait}s...")
                await asyncio.sleep(wait)

            except google_exceptions.ServiceUnavailable:
                wait = 2 ** attempt
                logger.warning(f"Service unavailable. Retrying in {wait}s...")
                await asyncio.sleep(wait)

            except Exception as e:
                logger.error(f"Gemini API error: {e}")
                raise

        raise RuntimeError("Gemini API max retries exceeded")


# Singleton instance
ai_engine = GeminiAI()
```

---

## 🔧 Troubleshooting

### Common Issues

**1. "API key not valid" Error**
```bash
# Check your .env file
cat .env | grep GEMINI_API_KEY

# Verify the key format (should start with AIzaSy)
# Regenerate key at: https://aistudio.google.com/apikey
```

**2. Rate Limit (429) Errors**
```python
# Implement rate limiter (see Rate Limiting section above)
# Reduce request frequency for free-tier usage
# Consider upgrading to paid tier for higher limits
```

**3. Slow Response Times**
```python
# Use Flash instead of Pro for faster responses
model_name = "gemini-1.5-flash"   # Faster
model_name = "gemini-1.5-flash-8b" # Fastest

# Reduce output token limit
max_output_tokens = 800  # Instead of 4096
```

**4. Context Window Exceeded**
```python
# Trim conversation history
chat.history = chat.history[-10:]  # Keep only last 5 turns

# Switch to a model with larger context
model_name = "gemini-1.5-pro"    # 2M token context
model_name = "gemini-1.5-flash"  # 1M token context
```

**5. Slash Commands Not Appearing in Discord**
```python
# Sync slash commands after registering them
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
```

**6. "Module not found" for google-generativeai**
```bash
pip install google-generativeai
# Or with extras:
pip install "google-generativeai[all]"
```

### Debug Mode

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Log generation details
logger.debug(f"Prompt: {prompt[:100]}...")
logger.debug(f"Model: {model_name}")
logger.debug(f"Response tokens: {response.usage_metadata.total_token_count}")
```

---

## 📚 Additional Resources

- **Gemini API Docs:** https://ai.google.dev/gemini-api/docs
- **Google AI Studio:** https://aistudio.google.com
- **Model Pricing:** https://ai.google.dev/pricing
- **Gemini Cookbook (Examples):** https://github.com/google-gemini/cookbook
- **Python SDK Reference:** https://ai.google.dev/api/python/google/generativeai
- **Discord.py Slash Commands:** https://discordpy.readthedocs.io/en/stable/interactions/api.html
- **API Status:** https://status.cloud.google.com

---

## 🔄 Updates & Versioning

**Current Version:** 3.0.0

**Changelog:**
- **v3.0.0** — Migrated from OpenRouter to Google Gemini API; all commands converted to Discord slash commands (`/`)
- **v2.0.0** — OpenRouter integration with multi-model support
- **v1.0.0** — Initial release with single model support

**Upcoming Features:**
- Streaming responses for real-time output in Discord
- Vision support via Gemini multimodal (image analysis)
- Gemini 2.0 Flash as new default once stable
- Prompt caching for cost reduction on repeated queries

---

## 📞 Support

**Issues with API Integration?**

1. Check this documentation first
2. Review error logs in the `logs/` directory
3. Test with a minimal example using Google AI Studio: https://aistudio.google.com
4. Check Google's API status: https://status.cloud.google.com
5. Open a GitHub issue with your error details and relevant logs

---

*Last Updated: February 2026*
*Maintained by: Try-Harder-AI Team*