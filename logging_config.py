import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    handler = RotatingFileHandler(
        os.path.join(log_dir, "app.log"),
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3
    )

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.logger.info("Logging is configured")
