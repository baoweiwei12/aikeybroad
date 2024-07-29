import logging
import colorlog


color_formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s%(reset)s:     %(asctime)s     %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
    secondary_log_colors={},
    style="%",
)


file_formatter = logging.Formatter("%(levelname)s:     %(asctime)s     %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(color_formatter)

file_handler = logging.FileHandler("log.txt", encoding="utf-8")
file_handler.setFormatter(file_formatter)

logging.basicConfig(level=logging.INFO, handlers=[stream_handler, file_handler])
