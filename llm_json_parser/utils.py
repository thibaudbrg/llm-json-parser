import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""
    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: Fore.BLUE + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)
    return logger

def print_heading(heading):
    print(Fore.CYAN + Style.BRIGHT + f"\n{'=' * 10} {heading} {'=' * 10}" + Style.RESET_ALL)

def print_info(info):
    print(Fore.GREEN + Style.BRIGHT + info + Style.RESET_ALL)

def print_warning(warning):
    print(Fore.YELLOW + Style.BRIGHT + warning + Style.RESET_ALL)

def print_error(error):
    print(Fore.RED + Style.BRIGHT + error + Style.RESET_ALL)
