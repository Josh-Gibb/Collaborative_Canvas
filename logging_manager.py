import logging

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG) 
logger.propagate = False 

# Create handlers for each log level
debug_handler = logging.FileHandler('logs/debug.log')
debug_handler.setLevel(logging.DEBUG)

error_handler = logging.FileHandler('logs/error.log')
error_handler.setLevel(logging.ERROR)

info_handler = logging.FileHandler('logs/info.log')
info_handler.setLevel(logging.INFO)

warning_handler = logging.FileHandler('logs/warning.log')
warning_handler.setLevel(logging.WARNING)

# Format for my logging files
log_format = logging.Formatter('%(asctime)s - %(filename)s - %(message)s')

# Apply format to each handler
debug_handler.setFormatter(log_format)
error_handler.setFormatter(log_format)
info_handler.setFormatter(log_format)
warning_handler.setFormatter(log_format)

# Add handlers to the logger
if not logger.hasHandlers():
    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)
    logger.addHandler(info_handler)
    logger.addHandler(warning_handler)
