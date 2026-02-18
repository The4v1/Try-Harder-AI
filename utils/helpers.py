"""
Helper Utilities
================

Common utility functions used throughout the Try-Harder-AI bot.

Features:
- File operations (YAML, JSON)
- Data validation and sanitization
- Time and date utilities
- String manipulation
- Configuration helpers
- Logging utilities
- Error handling helpers
- Data persistence
- Caching mechanisms

Author: Try-Harder-AI Team
"""

import os
import json
import yaml
import hashlib
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import logging


# =============================================================================
# LOGGING SETUP
# =============================================================================

logger = logging.getLogger(__name__)


# =============================================================================
# FILE OPERATIONS
# =============================================================================

def load_yaml(filepath: str) -> Dict:
    """
    Load YAML file and return as dictionary.
    
    Args:
        filepath: Path to YAML file
        
    Returns:
        Parsed YAML as dictionary
        
    Raises:
        FileNotFoundError: If file doesn't exist
        yaml.YAMLError: If YAML is invalid
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.error(f"YAML file not found: {filepath}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file {filepath}: {e}")
        raise


def save_yaml(data: Dict, filepath: str) -> bool:
    """
    Save dictionary to YAML file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            yaml.safe_dump(data, file, default_flow_style=False, allow_unicode=True)
        return True
    except Exception as e:
        logger.error(f"Error saving YAML file {filepath}: {e}")
        return False


def load_json(filepath: str) -> Dict:
    """
    Load JSON file and return as dictionary.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Parsed JSON as dictionary
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If JSON is invalid
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"JSON file not found: {filepath}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON file {filepath}: {e}")
        raise


def save_json(data: Dict, filepath: str, indent: int = 2) -> bool:
    """
    Save dictionary to JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save file
        indent: JSON indentation level
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=indent, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Error saving JSON file {filepath}: {e}")
        return False


def ensure_directory(directory: str) -> bool:
    """
    Ensure directory exists, create if not.
    
    Args:
        directory: Directory path
        
    Returns:
        True if directory exists or was created
    """
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {e}")
        return False


def file_exists(filepath: str) -> bool:
    """Check if file exists"""
    return os.path.isfile(filepath)


def get_file_size(filepath: str) -> int:
    """
    Get file size in bytes.
    
    Args:
        filepath: Path to file
        
    Returns:
        File size in bytes, -1 if file doesn't exist
    """
    try:
        return os.path.getsize(filepath)
    except OSError:
        return -1


# =============================================================================
# DATA VALIDATION
# =============================================================================

def validate_certification(certification: str) -> bool:
    """
    Validate certification code.
    
    Args:
        certification: Certification code to validate
        
    Returns:
        True if valid certification code
    """
    valid_certs = [
        'OSCP', 'OSEP', 'OSWE', 'OSED', 'OSWP',
        'OSWA', 'OSMR', 'OSDA', 'KLCP'
    ]
    return certification.upper() in valid_certs


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_user_id(user_id: Union[str, int]) -> bool:
    """
    Validate Discord user ID.
    
    Args:
        user_id: Discord user ID
        
    Returns:
        True if valid user ID format
    """
    try:
        uid = int(user_id)
        return uid > 0
    except (ValueError, TypeError):
        return False


def validate_skill_level(level: str) -> bool:
    """
    Validate skill level.
    
    Args:
        level: Skill level string
        
    Returns:
        True if valid skill level
    """
    valid_levels = ['beginner', 'intermediate', 'advanced', 'expert']
    return level.lower() in valid_levels


def validate_percentage(value: Union[int, float]) -> bool:
    """
    Validate percentage value (0-100).
    
    Args:
        value: Percentage value
        
    Returns:
        True if valid percentage
    """
    try:
        val = float(value)
        return 0 <= val <= 100
    except (ValueError, TypeError):
        return False


# =============================================================================
# STRING MANIPULATION
# =============================================================================

def sanitize_input(text: str, max_length: int = 2000) -> str:
    """
    Sanitize user input for safety.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove potential code injection
    text = text.strip()
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    return text


def clean_filename(filename: str) -> str:
    """
    Clean filename to be filesystem-safe.
    
    Args:
        filename: Original filename
        
    Returns:
        Cleaned filename
    """
    # Remove invalid characters
    cleaned = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Replace spaces with underscores
    cleaned = cleaned.replace(' ', '_')
    
    # Limit length
    if len(cleaned) > 255:
        name, ext = os.path.splitext(cleaned)
        cleaned = name[:255-len(ext)] + ext
    
    return cleaned


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate string with suffix.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text.
    
    Args:
        text: Input text
        
    Returns:
        Text with normalized whitespace
    """
    return ' '.join(text.split())


def extract_code_blocks(text: str) -> List[str]:
    """
    Extract code blocks from markdown text.
    
    Args:
        text: Markdown text
        
    Returns:
        List of code blocks
    """
    pattern = r'```[\w]*\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


def remove_markdown(text: str) -> str:
    """
    Remove markdown formatting from text.
    
    Args:
        text: Markdown text
        
    Returns:
        Plain text
    """
    # Remove code blocks
    text = re.sub(r'```[\w]*\n.*?```', '', text, flags=re.DOTALL)
    
    # Remove inline code
    text = re.sub(r'`[^`]+`', '', text)
    
    # Remove bold/italic
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    
    # Remove links
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    return text


# =============================================================================
# TIME AND DATE UTILITIES
# =============================================================================

def get_current_timestamp() -> str:
    """
    Get current timestamp in ISO format.
    
    Returns:
        ISO formatted timestamp
    """
    return datetime.utcnow().isoformat() + 'Z'


def parse_timestamp(timestamp: str) -> Optional[datetime]:
    """
    Parse ISO timestamp string to datetime.
    
    Args:
        timestamp: ISO formatted timestamp
        
    Returns:
        Datetime object or None if invalid
    """
    try:
        # Handle both with and without Z suffix
        if timestamp.endswith('Z'):
            timestamp = timestamp[:-1]
        return datetime.fromisoformat(timestamp)
    except (ValueError, AttributeError):
        return None


def format_relative_time(dt: datetime) -> str:
    """
    Format datetime as relative time (e.g., "2 hours ago").
    
    Args:
        dt: Datetime object
        
    Returns:
        Relative time string
    """
    now = datetime.utcnow()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 2592000:
        weeks = int(seconds / 604800)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    else:
        months = int(seconds / 2592000)
        return f"{months} month{'s' if months != 1 else ''} ago"


def days_between(start: datetime, end: datetime) -> int:
    """
    Calculate days between two dates.
    
    Args:
        start: Start datetime
        end: End datetime
        
    Returns:
        Number of days
    """
    return (end - start).days


def add_days(dt: datetime, days: int) -> datetime:
    """
    Add days to datetime.
    
    Args:
        dt: Base datetime
        days: Number of days to add
        
    Returns:
        New datetime
    """
    return dt + timedelta(days=days)


# =============================================================================
# HASHING AND ENCODING
# =============================================================================

def hash_string(text: str, algorithm: str = 'sha256') -> str:
    """
    Hash string using specified algorithm.
    
    Args:
        text: Text to hash
        algorithm: Hash algorithm (md5, sha1, sha256)
        
    Returns:
        Hex digest of hash
    """
    if algorithm == 'md5':
        return hashlib.md5(text.encode()).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(text.encode()).hexdigest()
    else:  # default sha256
        return hashlib.sha256(text.encode()).hexdigest()


def generate_id(prefix: str = "", length: int = 8) -> str:
    """
    Generate unique ID.
    
    Args:
        prefix: ID prefix
        length: Hash length
        
    Returns:
        Unique ID string
    """
    timestamp = datetime.utcnow().isoformat()
    hash_val = hash_string(timestamp)[:length]
    
    if prefix:
        return f"{prefix}_{hash_val}"
    return hash_val


# =============================================================================
# CONFIGURATION HELPERS
# =============================================================================

def get_env_var(key: str, default: Any = None) -> Any:
    """
    Get environment variable with default.
    
    Args:
        key: Environment variable name
        default: Default value if not found
        
    Returns:
        Environment variable value or default
    """
    return os.getenv(key, default)


def get_env_bool(key: str, default: bool = False) -> bool:
    """
    Get boolean environment variable.
    
    Args:
        key: Environment variable name
        default: Default value
        
    Returns:
        Boolean value
    """
    value = os.getenv(key, str(default)).lower()
    return value in ('true', '1', 'yes', 'on')


def get_config_path(filename: str) -> str:
    """
    Get full path to config file.
    
    Args:
        filename: Config filename
        
    Returns:
        Full path to config file
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'config', filename)


def get_data_path(filename: str) -> str:
    """
    Get full path to data file.
    
    Args:
        filename: Data filename
        
    Returns:
        Full path to data file
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'data', filename)


def get_prompt_path(filename: str) -> str:
    """
    Get full path to prompt file.
    
    Args:
        filename: Prompt filename
        
    Returns:
        Full path to prompt file
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'prompts', filename)


# =============================================================================
# DATA MANIPULATION
# =============================================================================

def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Deep merge two dictionaries.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary (takes precedence)
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


def get_nested_value(data: Dict, key_path: str, default: Any = None) -> Any:
    """
    Get nested dictionary value using dot notation.
    
    Args:
        data: Dictionary to search
        key_path: Dot-separated key path (e.g., 'user.profile.name')
        default: Default value if not found
        
    Returns:
        Value at key path or default
    """
    keys = key_path.split('.')
    value = data
    
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default


def set_nested_value(data: Dict, key_path: str, value: Any) -> Dict:
    """
    Set nested dictionary value using dot notation.
    
    Args:
        data: Dictionary to modify
        key_path: Dot-separated key path
        value: Value to set
        
    Returns:
        Modified dictionary
    """
    keys = key_path.split('.')
    current = data
    
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    current[keys[-1]] = value
    return data


def filter_dict(data: Dict, keys: List[str]) -> Dict:
    """
    Filter dictionary to only include specified keys.
    
    Args:
        data: Dictionary to filter
        keys: Keys to include
        
    Returns:
        Filtered dictionary
    """
    return {k: v for k, v in data.items() if k in keys}


def flatten_dict(data: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """
    Flatten nested dictionary.
    
    Args:
        data: Dictionary to flatten
        parent_key: Parent key prefix
        sep: Separator for keys
        
    Returns:
        Flattened dictionary
    """
    items = []
    
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    
    return dict(items)


# =============================================================================
# LIST UTILITIES
# =============================================================================

def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """
    Split list into chunks.
    
    Args:
        lst: List to split
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def remove_duplicates(lst: List) -> List:
    """
    Remove duplicates from list while preserving order.
    
    Args:
        lst: List with potential duplicates
        
    Returns:
        List without duplicates
    """
    seen = set()
    result = []
    
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    
    return result


def safe_get_index(lst: List, index: int, default: Any = None) -> Any:
    """
    Safely get list item by index.
    
    Args:
        lst: List
        index: Index to access
        default: Default value if index out of range
        
    Returns:
        List item or default
    """
    try:
        return lst[index]
    except IndexError:
        return default


# =============================================================================
# ERROR HANDLING HELPERS
# =============================================================================

def safe_execute(func, *args, default=None, **kwargs):
    """
    Safely execute function with exception handling.
    
    Args:
        func: Function to execute
        *args: Positional arguments
        default: Default value on error
        **kwargs: Keyword arguments
        
    Returns:
        Function result or default on error
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error executing {func.__name__}: {e}")
        return default


def retry_on_failure(func, max_retries: int = 3, delay: float = 1.0):
    """
    Retry function on failure.
    
    Args:
        func: Function to retry
        max_retries: Maximum retry attempts
        delay: Delay between retries in seconds
        
    Returns:
        Function result or None on failure
    """
    import time
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                logger.error(f"All {max_retries} attempts failed")
                return None


# =============================================================================
# CACHING
# =============================================================================

_cache = {}

def cache_set(key: str, value: Any, ttl: int = 300):
    """
    Set cache value with TTL.
    
    Args:
        key: Cache key
        value: Value to cache
        ttl: Time to live in seconds
    """
    expiry = datetime.utcnow() + timedelta(seconds=ttl)
    _cache[key] = {'value': value, 'expiry': expiry}


def cache_get(key: str, default: Any = None) -> Any:
    """
    Get cached value.
    
    Args:
        key: Cache key
        default: Default value if not found or expired
        
    Returns:
        Cached value or default
    """
    if key not in _cache:
        return default
    
    item = _cache[key]
    
    if datetime.utcnow() > item['expiry']:
        del _cache[key]
        return default
    
    return item['value']


def cache_clear():
    """Clear entire cache"""
    global _cache
    _cache = {}


def cache_delete(key: str):
    """Delete specific cache key"""
    if key in _cache:
        del _cache[key]


# =============================================================================
# NUMBER UTILITIES
# =============================================================================

def clamp(value: Union[int, float], min_val: Union[int, float], 
          max_val: Union[int, float]) -> Union[int, float]:
    """
    Clamp value between min and max.
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(max_val, value))


def percentage(value: Union[int, float], total: Union[int, float]) -> float:
    """
    Calculate percentage.
    
    Args:
        value: Current value
        total: Total value
        
    Returns:
        Percentage (0-100)
    """
    if total == 0:
        return 0.0
    return round((value / total) * 100, 2)


def safe_divide(numerator: Union[int, float], 
                denominator: Union[int, float], 
                default: float = 0.0) -> float:
    """
    Safely divide with zero-division handling.
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Default value if division by zero
        
    Returns:
        Division result or default
    """
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return default


# =============================================================================
# RANDOM UTILITIES
# =============================================================================

def random_choice(items: List) -> Any:
    """
    Safely get random choice from list.
    
    Args:
        items: List of items
        
    Returns:
        Random item or None if list empty
    """
    import random
    
    if not items:
        return None
    
    return random.choice(items)


def shuffle_list(lst: List) -> List:
    """
    Shuffle list (returns new list).
    
    Args:
        lst: List to shuffle
        
    Returns:
        Shuffled list
    """
    import random
    
    shuffled = lst.copy()
    random.shuffle(shuffled)
    return shuffled