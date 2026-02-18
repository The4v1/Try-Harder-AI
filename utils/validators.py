"""
Input Validators
================

Comprehensive validation functions for user inputs, commands, and data.

Features:
- Command argument validation
- User input sanitization
- Certification validation
- Model selection validation
- Question/answer validation
- Roadmap parameter validation
- File input validation
- Rate limiting validation
- Permission validation

Author: Try-Harder-AI Team
"""

import re
from typing import Optional, List, Dict, Union, Tuple
from datetime import datetime, timedelta
import logging


# =============================================================================
# LOGGING SETUP
# =============================================================================

logger = logging.getLogger(__name__)


# =============================================================================
# CONSTANTS
# =============================================================================

VALID_CERTIFICATIONS = [
    'OSCP', 'OSEP', 'OSWE', 'OSED', 'OSWP',
    'OSWA', 'OSMR', 'OSDA', 'KLCP'
]

VALID_SKILL_LEVELS = ['beginner', 'intermediate', 'advanced', 'expert']

VALID_AI_MODELS = [
    # Shortcut aliases
    'flash', 'pro', 'flash8b', 'flash2', 'legacy',
    # Full Gemini model IDs
    'gemini-1.5-flash',
    'gemini-1.5-pro',
    'gemini-1.5-flash-8b',
    'gemini-2.0-flash',
    'gemini-1.0-pro',
]

VALID_ANSWER_OPTIONS = ['A', 'B', 'C', 'D']

MIN_ROADMAP_WEEKS = 6
MAX_ROADMAP_WEEKS = 24
DEFAULT_ROADMAP_WEEKS = 12

MIN_ASSESSMENT_QUESTIONS = 5
MAX_ASSESSMENT_QUESTIONS = 20
DEFAULT_ASSESSMENT_QUESTIONS = 10


# =============================================================================
# CERTIFICATION VALIDATION
# =============================================================================

def validate_certification(certification: str) -> Tuple[bool, Optional[str]]:
    """
    Validate certification code.
    
    Args:
        certification: Certification code to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not certification:
        return False, "Certification cannot be empty"
    
    cert_upper = certification.upper().strip()
    
    if cert_upper not in VALID_CERTIFICATIONS:
        valid_certs = ", ".join(VALID_CERTIFICATIONS)
        return False, f"Invalid certification. Valid options: {valid_certs}"
    
    return True, None


def get_certification_name(certification: str) -> Optional[str]:
    """
    Get full certification name from code.
    
    Args:
        certification: Certification code
        
    Returns:
        Full certification name or None if invalid
    """
    cert_names = {
        'OSCP': 'Offensive Security Certified Professional',
        'OSEP': 'Offensive Security Experienced Penetration Tester',
        'OSWE': 'Offensive Security Web Expert',
        'OSED': 'Offensive Security Exploit Developer',
        'OSWP': 'Offensive Security Wireless Professional',
        'OSWA': 'OffSec Web Assessor',
        'OSMR': 'OffSec macOS Researcher',
        'OSDA': 'OffSec Defense Analyst',
        'KLCP': 'Kali Linux Certified Professional'
    }
    
    return cert_names.get(certification.upper())


def suggest_certification(partial: str) -> List[str]:
    """
    Suggest certifications based on partial input.
    
    Args:
        partial: Partial certification code
        
    Returns:
        List of matching certifications
    """
    if not partial:
        return VALID_CERTIFICATIONS
    
    partial_upper = partial.upper()
    matches = [cert for cert in VALID_CERTIFICATIONS if cert.startswith(partial_upper)]
    
    return matches if matches else VALID_CERTIFICATIONS


# =============================================================================
# AI MODEL VALIDATION
# =============================================================================

def validate_ai_model(model: str) -> Tuple[bool, Optional[str]]:
    """
    Validate Gemini AI model selection.
    
    Args:
        model: Model name or shortcut alias
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not model:
        return False, "Model cannot be empty"
    
    model_lower = model.lower().strip()
    
    if model_lower not in VALID_AI_MODELS:
        available = ", ".join(['flash', 'pro', 'flash8b', 'flash2', 'legacy'])
        return False, f"Invalid model. Available Gemini models: {available}"
    
    return True, None


def get_model_full_name(model_shortcut: str) -> str:
    """
    Get full Gemini model ID from shortcut alias.
    
    Args:
        model_shortcut: Model shortcut (flash, pro, flash8b, flash2, legacy)
        
    Returns:
        Full Gemini model identifier
    """
    model_map = {
        'flash':   'gemini-1.5-flash',
        'pro':     'gemini-1.5-pro',
        'flash8b': 'gemini-1.5-flash-8b',
        'flash2':  'gemini-2.0-flash',
        'legacy':  'gemini-1.0-pro',
    }
    
    return model_map.get(model_shortcut.lower(), model_shortcut)


# =============================================================================
# USER INPUT VALIDATION
# =============================================================================

def validate_user_id(user_id: Union[str, int]) -> Tuple[bool, Optional[str]]:
    """
    Validate Discord user ID.
    
    Args:
        user_id: Discord user ID
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        uid = int(user_id)
        if uid <= 0:
            return False, "User ID must be positive"
        if uid > 9999999999999999999:  # Discord's max snowflake ID
            return False, "User ID too large"
        return True, None
    except (ValueError, TypeError):
        return False, "User ID must be a valid number"


def validate_username(username: str) -> Tuple[bool, Optional[str]]:
    """
    Validate Discord username.
    
    Args:
        username: Discord username
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not username:
        return False, "Username cannot be empty"
    
    if len(username) < 2:
        return False, "Username must be at least 2 characters"
    
    if len(username) > 32:
        return False, "Username must be 32 characters or less"
    
    # Check for valid Discord username characters
    if not re.match(r'^[a-zA-Z0-9_\.]+$', username.split('#')[0]):
        return False, "Username contains invalid characters"
    
    return True, None


def sanitize_user_input(text: str, max_length: int = 2000) -> str:
    """
    Sanitize user input for safe processing.
    
    Args:
        text: User input text
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Strip whitespace
    text = text.strip()
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Remove other control characters except newlines and tabs
    text = re.sub(r'[\x01-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text


def validate_question_text(question: str) -> Tuple[bool, Optional[str]]:
    """
    Validate question text for /ask command.
    
    Args:
        question: Question text
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not question:
        return False, "Question cannot be empty"
    
    sanitized = sanitize_user_input(question)
    
    if len(sanitized) < 5:
        return False, "Question is too short (minimum 5 characters)"
    
    if len(sanitized) > 500:
        return False, "Question is too long (maximum 500 characters)"
    
    # Check if it's just whitespace or special characters
    if not re.search(r'[a-zA-Z0-9]', sanitized):
        return False, "Question must contain alphanumeric characters"
    
    return True, None


# =============================================================================
# ASSESSMENT VALIDATION
# =============================================================================

def validate_answer_option(answer: str) -> Tuple[bool, Optional[str]]:
    """
    Validate assessment answer option.
    
    Args:
        answer: Answer option (A, B, C, D)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not answer:
        return False, "Answer cannot be empty"
    
    answer_upper = answer.upper().strip()
    
    if answer_upper not in VALID_ANSWER_OPTIONS:
        valid_options = ", ".join(VALID_ANSWER_OPTIONS)
        return False, f"Invalid answer option. Valid options: {valid_options}"
    
    return True, None


def validate_assessment_questions_count(count: Union[str, int]) -> Tuple[bool, Optional[str], int]:
    """
    Validate number of assessment questions.
    
    Args:
        count: Number of questions
        
    Returns:
        Tuple of (is_valid, error_message, validated_count)
    """
    try:
        num_questions = int(count)
    except (ValueError, TypeError):
        return False, "Question count must be a number", DEFAULT_ASSESSMENT_QUESTIONS
    
    if num_questions < MIN_ASSESSMENT_QUESTIONS:
        return False, f"Minimum {MIN_ASSESSMENT_QUESTIONS} questions required", MIN_ASSESSMENT_QUESTIONS
    
    if num_questions > MAX_ASSESSMENT_QUESTIONS:
        return False, f"Maximum {MAX_ASSESSMENT_QUESTIONS} questions allowed", MAX_ASSESSMENT_QUESTIONS
    
    return True, None, num_questions


def validate_skill_level(level: str) -> Tuple[bool, Optional[str]]:
    """
    Validate skill level.
    
    Args:
        level: Skill level string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not level:
        return False, "Skill level cannot be empty"
    
    level_lower = level.lower().strip()
    
    if level_lower not in VALID_SKILL_LEVELS:
        valid_levels = ", ".join(VALID_SKILL_LEVELS)
        return False, f"Invalid skill level. Valid options: {valid_levels}"
    
    return True, None


# =============================================================================
# ROADMAP VALIDATION
# =============================================================================

def validate_roadmap_weeks(weeks: Union[str, int]) -> Tuple[bool, Optional[str], int]:
    """
    Validate roadmap duration in weeks.
    
    Args:
        weeks: Number of weeks
        
    Returns:
        Tuple of (is_valid, error_message, validated_weeks)
    """
    try:
        num_weeks = int(weeks)
    except (ValueError, TypeError):
        return False, "Week count must be a number", DEFAULT_ROADMAP_WEEKS
    
    if num_weeks < MIN_ROADMAP_WEEKS:
        return False, f"Minimum {MIN_ROADMAP_WEEKS} weeks required", MIN_ROADMAP_WEEKS
    
    if num_weeks > MAX_ROADMAP_WEEKS:
        return False, f"Maximum {MAX_ROADMAP_WEEKS} weeks allowed", MAX_ROADMAP_WEEKS
    
    return True, None, num_weeks


def validate_study_hours_per_week(hours: Union[str, int, float]) -> Tuple[bool, Optional[str], float]:
    """
    Validate study hours per week.
    
    Args:
        hours: Study hours per week
        
    Returns:
        Tuple of (is_valid, error_message, validated_hours)
    """
    try:
        study_hours = float(hours)
    except (ValueError, TypeError):
        return False, "Study hours must be a number", 10.0
    
    if study_hours <= 0:
        return False, "Study hours must be positive", 10.0
    
    if study_hours > 168:  # Hours in a week
        return False, "Study hours cannot exceed 168 hours per week", 40.0
    
    if study_hours > 80:
        logger.warning(f"Very high study hours specified: {study_hours}")
        return True, "⚠️ Warning: This is a lot of study time per week!", study_hours
    
    return True, None, study_hours


# =============================================================================
# NUMERIC VALIDATION
# =============================================================================

def validate_percentage(value: Union[str, int, float]) -> Tuple[bool, Optional[str], float]:
    """
    Validate percentage value (0-100).
    
    Args:
        value: Percentage value
        
    Returns:
        Tuple of (is_valid, error_message, validated_value)
    """
    try:
        percentage = float(value)
    except (ValueError, TypeError):
        return False, "Percentage must be a number", 0.0
    
    if percentage < 0:
        return False, "Percentage cannot be negative", 0.0
    
    if percentage > 100:
        return False, "Percentage cannot exceed 100", 100.0
    
    return True, None, percentage


def validate_positive_integer(value: Union[str, int], min_value: int = 1, 
                              max_value: int = None) -> Tuple[bool, Optional[str], int]:
    """
    Validate positive integer with optional range.
    
    Args:
        value: Integer value
        min_value: Minimum allowed value
        max_value: Maximum allowed value (None for no limit)
        
    Returns:
        Tuple of (is_valid, error_message, validated_value)
    """
    try:
        num = int(value)
    except (ValueError, TypeError):
        return False, "Value must be an integer", min_value
    
    if num < min_value:
        return False, f"Value must be at least {min_value}", min_value
    
    if max_value is not None and num > max_value:
        return False, f"Value cannot exceed {max_value}", max_value
    
    return True, None, num


# =============================================================================
# DATE/TIME VALIDATION
# =============================================================================

def validate_date_string(date_str: str, format: str = "%Y-%m-%d") -> Tuple[bool, Optional[str], Optional[datetime]]:
    """
    Validate date string format.
    
    Args:
        date_str: Date string
        format: Expected date format
        
    Returns:
        Tuple of (is_valid, error_message, parsed_datetime)
    """
    try:
        parsed_date = datetime.strptime(date_str, format)
        return True, None, parsed_date
    except ValueError as e:
        return False, f"Invalid date format. Expected: {format}", None


def validate_future_date(date: datetime) -> Tuple[bool, Optional[str]]:
    """
    Validate that date is in the future.
    
    Args:
        date: Datetime to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if date <= datetime.utcnow():
        return False, "Date must be in the future"
    
    return True, None


def validate_date_range(start_date: datetime, end_date: datetime) -> Tuple[bool, Optional[str]]:
    """
    Validate date range.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if start_date >= end_date:
        return False, "Start date must be before end date"
    
    # Check if range is reasonable (not too long)
    max_days = 365 * 2  # 2 years
    if (end_date - start_date).days > max_days:
        return False, f"Date range cannot exceed {max_days} days"
    
    return True, None


# =============================================================================
# COMMAND ARGUMENT VALIDATION
# =============================================================================

def validate_command_args(args: List[str], min_args: int = 0, 
                         max_args: int = None) -> Tuple[bool, Optional[str]]:
    """
    Validate command argument count.
    
    Args:
        args: Command arguments
        min_args: Minimum required arguments
        max_args: Maximum allowed arguments (None for unlimited)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    arg_count = len(args)
    
    if arg_count < min_args:
        return False, f"Minimum {min_args} argument(s) required, got {arg_count}"
    
    if max_args is not None and arg_count > max_args:
        return False, f"Maximum {max_args} argument(s) allowed, got {arg_count}"
    
    return True, None


def parse_command_args(args_str: str, expected_args: List[str]) -> Tuple[bool, Optional[str], Dict]:
    """
    Parse and validate named command arguments.
    
    Args:
        args_str: Arguments string
        expected_args: List of expected argument names
        
    Returns:
        Tuple of (is_valid, error_message, parsed_args_dict)
    """
    parsed = {}
    
    # Simple key=value parsing
    pairs = args_str.split()
    
    for pair in pairs:
        if '=' not in pair:
            return False, f"Invalid argument format: {pair}. Use key=value", {}
        
        key, value = pair.split('=', 1)
        
        if key not in expected_args:
            valid = ", ".join(expected_args)
            return False, f"Unknown argument: {key}. Valid: {valid}", {}
        
        parsed[key] = value
    
    return True, None, parsed


# =============================================================================
# RATE LIMITING VALIDATION
# =============================================================================

_rate_limits: Dict[str, List[datetime]] = {}

def check_rate_limit(user_id: str, command: str, max_calls: int = 5, 
                     window_seconds: int = 60) -> Tuple[bool, Optional[str], int]:
    """
    Check if user has exceeded rate limit for command.
    
    Args:
        user_id: User identifier
        command: Command name
        max_calls: Maximum calls allowed in window
        window_seconds: Time window in seconds
        
    Returns:
        Tuple of (is_allowed, error_message, calls_remaining)
    """
    key = f"{user_id}:{command}"
    now = datetime.utcnow()
    cutoff = now - timedelta(seconds=window_seconds)
    
    # Initialize or get existing timestamps
    if key not in _rate_limits:
        _rate_limits[key] = []
    
    # Remove old timestamps
    _rate_limits[key] = [ts for ts in _rate_limits[key] if ts > cutoff]
    
    # Check limit
    current_calls = len(_rate_limits[key])
    
    if current_calls >= max_calls:
        remaining_time = int((min(_rate_limits[key]) + timedelta(seconds=window_seconds) - now).total_seconds())
        return False, f"Rate limit exceeded. Try again in {remaining_time} seconds", 0
    
    # Add current call
    _rate_limits[key].append(now)
    
    remaining = max_calls - current_calls - 1
    return True, None, remaining


def reset_rate_limit(user_id: str, command: str = None):
    """
    Reset rate limit for user.
    
    Args:
        user_id: User identifier
        command: Specific command (None to reset all)
    """
    if command:
        key = f"{user_id}:{command}"
        if key in _rate_limits:
            del _rate_limits[key]
    else:
        # Reset all commands for user
        keys_to_delete = [k for k in _rate_limits.keys() if k.startswith(f"{user_id}:")]
        for key in keys_to_delete:
            del _rate_limits[key]


# =============================================================================
# FILE VALIDATION
# =============================================================================

def validate_file_extension(filename: str, allowed_extensions: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate file extension.
    
    Args:
        filename: Filename to validate
        allowed_extensions: List of allowed extensions (e.g., ['.txt', '.json'])
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not filename:
        return False, "Filename cannot be empty"
    
    # Get extension
    ext = None
    if '.' in filename:
        ext = '.' + filename.rsplit('.', 1)[1].lower()
    
    if ext not in [e.lower() for e in allowed_extensions]:
        valid = ", ".join(allowed_extensions)
        return False, f"Invalid file extension. Allowed: {valid}"
    
    return True, None


def validate_filename(filename: str) -> Tuple[bool, Optional[str]]:
    """
    Validate filename for unsafe characters.
    
    Args:
        filename: Filename to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not filename:
        return False, "Filename cannot be empty"
    
    # Check for path traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        return False, "Filename contains invalid path characters"
    
    # Check for invalid characters
    invalid_chars = '<>:"|?*\x00'
    if any(char in filename for char in invalid_chars):
        return False, "Filename contains invalid characters"
    
    # Check length
    if len(filename) > 255:
        return False, "Filename too long (max 255 characters)"
    
    return True, None


# =============================================================================
# BATCH VALIDATION
# =============================================================================

class ValidationResult:
    """Container for validation results"""
    
    def __init__(self):
        self.is_valid = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.validated_data: Dict = {}
    
    def add_error(self, error: str):
        """Add an error"""
        self.is_valid = False
        self.errors.append(error)
    
    def add_warning(self, warning: str):
        """Add a warning"""
        self.warnings.append(warning)
    
    def set_data(self, key: str, value):
        """Set validated data"""
        self.validated_data[key] = value
    
    def get_error_message(self) -> str:
        """Get formatted error message"""
        if not self.errors:
            return ""
        return "\n".join([f"❌ {error}" for error in self.errors])
    
    def get_warning_message(self) -> str:
        """Get formatted warning message"""
        if not self.warnings:
            return ""
        return "\n".join([f"⚠️ {warning}" for warning in self.warnings])


def validate_assessment_start(certification: str, question_count: Union[str, int] = None) -> ValidationResult:
    """
    Validate parameters for starting an assessment.
    
    Args:
        certification: Certification code
        question_count: Number of questions (optional)
        
    Returns:
        ValidationResult object
    """
    result = ValidationResult()
    
    # Validate certification
    valid, error = validate_certification(certification)
    if not valid:
        result.add_error(error)
    else:
        result.set_data('certification', certification.upper())
    
    # Validate question count if provided
    if question_count is not None:
        valid, error, count = validate_assessment_questions_count(question_count)
        if not valid:
            result.add_error(error)
        result.set_data('question_count', count)
    else:
        result.set_data('question_count', DEFAULT_ASSESSMENT_QUESTIONS)
    
    return result


def validate_roadmap_generation(certification: str, weeks: Union[str, int] = None,
                                study_hours: Union[str, int, float] = None) -> ValidationResult:
    """
    Validate parameters for roadmap generation.
    
    Args:
        certification: Certification code
        weeks: Roadmap duration in weeks (optional)
        study_hours: Study hours per week (optional)
        
    Returns:
        ValidationResult object
    """
    result = ValidationResult()
    
    # Validate certification
    valid, error = validate_certification(certification)
    if not valid:
        result.add_error(error)
    else:
        result.set_data('certification', certification.upper())
    
    # Validate weeks
    if weeks is not None:
        valid, error, validated_weeks = validate_roadmap_weeks(weeks)
        if not valid:
            result.add_error(error)
        result.set_data('weeks', validated_weeks)
    else:
        result.set_data('weeks', DEFAULT_ROADMAP_WEEKS)
    
    # Validate study hours
    if study_hours is not None:
        valid, warning, validated_hours = validate_study_hours_per_week(study_hours)
        if not valid:
            result.add_error(warning)
        elif warning:
            result.add_warning(warning)
        result.set_data('study_hours', validated_hours)
    else:
        result.set_data('study_hours', 10.0)
    
    return result


# =============================================================================
# TYPE CHECKING
# =============================================================================

from typing import Any

def is_string(value: Any) -> bool:
    """Check if value is a string"""
    return isinstance(value, str)


def is_integer(value: Any) -> bool:
    """Check if value is an integer"""
    return isinstance(value, int) and not isinstance(value, bool)


def is_float(value: Any) -> bool:
    """Check if value is a float"""
    return isinstance(value, float)


def is_boolean(value: Any) -> bool:
    """Check if value is a boolean"""
    return isinstance(value, bool)


def is_list(value: Any) -> bool:
    """Check if value is a list"""
    return isinstance(value, list)


def is_dict(value: Any) -> bool:
    """Check if value is a dictionary"""
    return isinstance(value, dict)