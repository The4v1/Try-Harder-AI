"""
Logging Configuration
=====================

Centralized logging configuration for the Try-Harder-AI bot.

Features:
- Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- File and console output with rotation
- Colored console output with emojis
- Rotating file handlers to prevent huge log files
- Module-specific logging
- Performance logging
- Error tracking
- Production and development modes
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# ANSI color codes for console output
class LogColors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Standard colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support and emojis for console output."""
    
    # Color mapping for log levels
    LEVEL_COLORS = {
        logging.DEBUG: LogColors.BRIGHT_BLACK,
        logging.INFO: LogColors.BRIGHT_BLUE,
        logging.WARNING: LogColors.BRIGHT_YELLOW,
        logging.ERROR: LogColors.BRIGHT_RED,
        logging.CRITICAL: LogColors.RED + LogColors.BOLD,
    }
    
    # Emoji mapping for log levels
    LEVEL_EMOJI = {
        logging.DEBUG: '🔍',
        logging.INFO: 'ℹ️',
        logging.WARNING: '⚠️',
        logging.ERROR: '❌',
        logging.CRITICAL: '🚨',
    }
    
    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        use_colors: bool = True,
        use_emoji: bool = True
    ):
        """
        Initialize colored formatter.
        
        Args:
            fmt: Log format string
            datefmt: Date format string
            use_colors: Enable color output
            use_emoji: Enable emoji in output
        """
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors and sys.stdout.isatty()
        self.use_emoji = use_emoji
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record with colors and emoji.
        
        Args:
            record: Log record to format
            
        Returns:
            Formatted log string
        """
        # Save original values
        levelname_original = record.levelname
        name_original = record.name
        
        if self.use_colors:
            # Add color to level name
            color = self.LEVEL_COLORS.get(record.levelno, '')
            record.levelname = f"{color}{record.levelname}{LogColors.RESET}"
            
            # Add color to logger name
            record.name = f"{LogColors.CYAN}{record.name}{LogColors.RESET}"
        
        if self.use_emoji:
            # Add emoji prefix
            emoji = self.LEVEL_EMOJI.get(record.levelno, '')
            record.levelname = f"{emoji} {record.levelname}"
        
        # Format the record
        result = super().format(record)
        
        # Restore original values
        record.levelname = levelname_original
        record.name = name_original
        
        return result


class PerformanceFilter(logging.Filter):
    """Filter for performance-related log messages."""
    
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter log records for performance tracking.
        
        Args:
            record: Log record to filter
            
        Returns:
            True if record should be logged
        """
        # Add timing information if available
        if hasattr(record, 'duration'):
            record.msg = f"{record.msg} [Duration: {record.duration:.2f}s]"
        
        return True


def setup_logging(
    log_level: str = "INFO",
    log_dir: Optional[Path] = None,
    log_to_file: bool = True,
    log_to_console: bool = True,
    max_file_size: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
    use_colors: bool = True,
    use_emoji: bool = True
) -> logging.Logger:
    """
    Setup logging configuration for the bot.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files
        log_to_file: Enable file logging
        log_to_console: Enable console logging
        max_file_size: Maximum size of log file before rotation (bytes)
        backup_count: Number of backup log files to keep
        use_colors: Enable colored console output
        use_emoji: Enable emoji in console output
        
    Returns:
        Configured root logger
    """
    # Convert log level string to logging constant
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatters
    file_format = (
        '%(asctime)s - %(name)s - %(levelname)s - '
        '%(filename)s:%(lineno)d - %(funcName)s() - %(message)s'
    )
    console_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Setup file logging
    if log_to_file:
        if log_dir is None:
            log_dir = Path('logs')
        
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Main log file with rotation
        log_file = log_dir / 'bot.log'
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(numeric_level)
        file_formatter = logging.Formatter(file_format, date_format)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
        
        # Error log file (only ERROR and CRITICAL)
        error_log_file = log_dir / 'error.log'
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        root_logger.addHandler(error_handler)
        
        # Debug log file (only when DEBUG level is enabled)
        if numeric_level == logging.DEBUG:
            debug_log_file = log_dir / 'debug.log'
            debug_handler = logging.handlers.RotatingFileHandler(
                debug_log_file,
                maxBytes=max_file_size,
                backupCount=backup_count,
                encoding='utf-8'
            )
            debug_handler.setLevel(logging.DEBUG)
            debug_handler.setFormatter(file_formatter)
            root_logger.addHandler(debug_handler)
    
    # Setup console logging
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_formatter = ColoredFormatter(
            console_format,
            date_format,
            use_colors=use_colors,
            use_emoji=use_emoji
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    
    # Add performance filter to all handlers
    perf_filter = PerformanceFilter()
    for handler in root_logger.handlers:
        handler.addFilter(perf_filter)
    
    # Log startup message
    root_logger.info("="*60)
    root_logger.info("🚀 Logging system initialized")
    root_logger.info(f"📊 Log level: {log_level.upper()}")
    if log_to_file:
        root_logger.info(f"📁 Log directory: {log_dir.absolute()}")
    root_logger.info("="*60)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    
    Args:
        name: Module name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def set_module_log_level(module_name: str, level: str):
    """
    Set log level for a specific module.
    
    Args:
        module_name: Name of the module
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logger = logging.getLogger(module_name)
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)


def disable_external_loggers():
    """Disable or reduce verbosity of external library loggers."""
    # Reduce Discord.py verbosity
    logging.getLogger('discord').setLevel(logging.WARNING)
    logging.getLogger('discord.http').setLevel(logging.WARNING)
    logging.getLogger('discord.gateway').setLevel(logging.WARNING)
    logging.getLogger('discord.client').setLevel(logging.WARNING)
    
    # Reduce aiohttp verbosity
    logging.getLogger('aiohttp').setLevel(logging.WARNING)
    logging.getLogger('aiohttp.access').setLevel(logging.WARNING)
    
    # Reduce other libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.WARNING)


class LogContext:
    """Context manager for temporary log level changes."""
    
    def __init__(self, logger: logging.Logger, level: str):
        """
        Initialize log context.
        
        Args:
            logger: Logger to modify
            level: Temporary log level
        """
        self.logger = logger
        self.old_level = logger.level
        self.new_level = getattr(logging, level.upper(), logging.INFO)
    
    def __enter__(self):
        """Enter context and change log level."""
        self.logger.setLevel(self.new_level)
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context and restore log level."""
        self.logger.setLevel(self.old_level)


class TimedLogger:
    """Context manager for timing code execution with logging."""
    
    def __init__(
        self,
        logger: logging.Logger,
        message: str,
        level: int = logging.INFO
    ):
        """
        Initialize timed logger.
        
        Args:
            logger: Logger to use
            message: Message to log
            level: Log level
        """
        self.logger = logger
        self.message = message
        self.level = level
        self.start_time = None
    
    def __enter__(self):
        """Start timing."""
        self.start_time = datetime.now()
        self.logger.log(self.level, f"⏱️ Starting: {self.message}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """End timing and log duration."""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        if exc_type is None:
            self.logger.log(
                self.level,
                f"✅ Completed: {self.message} [Duration: {duration:.2f}s]"
            )
        else:
            self.logger.error(
                f"❌ Failed: {self.message} [Duration: {duration:.2f}s] - {exc_val}"
            )


def log_function_call(logger: logging.Logger, level: int = logging.DEBUG):
    """
    Decorator to log function calls with arguments and execution time.
    
    Args:
        logger: Logger to use
        level: Log level
        
    Returns:
        Decorator function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            logger.log(level, f"🔵 Calling {func_name}()")
            
            start_time = datetime.now()
            try:
                result = func(*args, **kwargs)
                duration = (datetime.now() - start_time).total_seconds()
                logger.log(
                    level,
                    f"✅ {func_name} completed in {duration:.2f}s"
                )
                return result
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                logger.error(
                    f"❌ {func_name} failed after {duration:.2f}s: {e}",
                    exc_info=True
                )
                raise
        
        return wrapper
    return decorator


# Pre-configured logging profiles
LOGGING_PROFILES = {
    'development': {
        'log_level': 'DEBUG',
        'log_to_file': True,
        'log_to_console': True,
        'use_colors': True,
        'use_emoji': True
    },
    'production': {
        'log_level': 'INFO',
        'log_to_file': True,
        'log_to_console': True,
        'use_colors': False,
        'use_emoji': False
    },
    'testing': {
        'log_level': 'DEBUG',
        'log_to_file': False,
        'log_to_console': True,
        'use_colors': True,
        'use_emoji': True
    },
    'minimal': {
        'log_level': 'WARNING',
        'log_to_file': False,
        'log_to_console': True,
        'use_colors': True,
        'use_emoji': True
    }
}


def setup_logging_profile(profile: str = 'development', **kwargs):
    """
    Setup logging using a pre-configured profile.
    
    Args:
        profile: Profile name (development, production, testing, minimal)
        **kwargs: Override profile settings
        
    Returns:
        Configured root logger
    """
    if profile not in LOGGING_PROFILES:
        raise ValueError(
            f"Unknown profile: {profile}. "
            f"Choose from {list(LOGGING_PROFILES.keys())}"
        )
    
    # Get profile settings
    settings = LOGGING_PROFILES[profile].copy()
    
    # Override with kwargs
    settings.update(kwargs)
    
    # Setup logging
    logger = setup_logging(**settings)
    
    # Disable external loggers
    disable_external_loggers()
    
    logger.info(f"📋 Logging profile '{profile}' activated")
    
    return logger


# Test function
def test_logging():
    """Test logging configuration."""
    print("🧪 Testing logging configuration...\n")
    
    # Setup logging with colors and emoji
    setup_logging(
        log_level='DEBUG',
        log_to_file=False,
        use_colors=True,
        use_emoji=True
    )
    
    logger = get_logger(__name__)
    
    # Test all log levels
    logger.debug("This is a DEBUG message - detailed information for debugging")
    logger.info("This is an INFO message - general information")
    logger.warning("This is a WARNING message - something to pay attention to")
    logger.error("This is an ERROR message - something went wrong")
    logger.critical("This is a CRITICAL message - serious problem!")
    
    # Test timed logger
    print("\n⏱️ Testing timed execution:")
    import time
    with TimedLogger(logger, "Sleep for 1 second"):
        time.sleep(1)
    
    # Test function decorator
    print("\n🔵 Testing function decorator:")
    
    @log_function_call(logger)
    def sample_function(x, y):
        return x + y
    
    result = sample_function(5, 3)
    print(f"Result: {result}")
    
    print("\n✅ Logging test completed!")


if __name__ == "__main__":
    test_logging()