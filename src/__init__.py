import sys
import logging
from pathlib import Path

# Define log directory and file path
log_dir = Path("logs")
log_filepath = log_dir / "logging.log"

# Ensure the log directory exists
log_dir.mkdir(parents=True, exist_ok=True)

# Set up logging configuration
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

# Get logger instance
logger = logging.getLogger("Credit-Card-Behaviour-logger")
