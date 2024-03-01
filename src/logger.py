import logging

DEFAULT_LOGGING_FILE = "editor.log"


class FileLogger:
    __logger: logging.Logger

    def __init__(self) -> None:
        self.__logger = logging.getLogger("file_logger")
        logging.basicConfig(filename=DEFAULT_LOGGING_FILE, level=logging.DEBUG)

    def log_debug(self, message: str):
        self.__logger.debug(message)
