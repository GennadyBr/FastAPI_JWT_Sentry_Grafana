import logging.handlers


class LoggerSetup:
    def __init__(self) -> None:
        self.logger = logging.getLogger("")
        self.setup_logging()

    def setup_logging(self) -> None:
        """Logging setup console and file handlers log/fastapi_elk.log"""
        # define log format
        LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - ELK - %(message)s"
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

        # make formatter for logging
        formatter = logging.Formatter(LOG_FORMAT)

        # make console handler
        console = logging.StreamHandler()
        console.setFormatter(formatter)

        # make TimeRotatingFileHandler
        log_file = "logs/fastapi_elk.log"
        # log_file = "src/logs/fastapi_elk.log"
        file = logging.handlers.TimedRotatingFileHandler(
            filename=log_file, when="midnight", interval=1, backupCount=5
        )
        file.setFormatter(formatter)

        # add handlers
        self.logger.addHandler(console)
        self.logger.addHandler(file)
