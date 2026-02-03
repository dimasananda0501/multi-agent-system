"""
Structured Logging Utility
Menggunakan structlog untuk logging yang lebih informatif dan mudah di-parse
"""
import structlog
import logging
import sys
from src.utils.config import settings


def setup_logging():
    """
    Setup structured logging dengan format yang sesuai untuk production
    """
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper())
    )
    
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer() if settings.app_env == "production" 
            else structlog.dev.ConsoleRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str):
    """
    Get a structured logger instance
    
    Args:
        name: Logger name (biasanya __name__ dari module)
    
    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)
