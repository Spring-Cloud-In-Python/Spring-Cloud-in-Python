# standard library
import os

__author__ = "benbenbang (bn@benbenbang.io)"
__license__ = "Apache 2.0"


# standard library
import sys

# pypi/conda library
from loguru import logger as __logger


class Formatter:
    def __init__(self, fmt):
        self.padding = 0
        self.fmt = fmt

    def format(self, record):
        length = len("{name}:{function}:{line}" % {**record})
        self.padding = max(self.padding, length)
        record["extra"]["padding"] = " " * (self.padding - length)
        return self.fmt


def getLogger(name=None, debug=False, diagnose=False, fmt=None, *, logger_=__logger, formatter_=Formatter):
    """ logger = getLogger() -> Production ready
    Logger stream to std our / err, can be easily parsed by K8s, Kibana...etc

    Level name  Severity value  Logger method
    TRACE       5               logger.trace()
    DEBUG       10              logger.debug()
    INFO        20              logger.info()
    SUCCESS     25              logger.success()
    WARNING     30              logger.warning()
    ERROR       40              logger.error()
    CRITICAL    50              logger.critical()

    Examples:

        Plug and play:
            logger = getLogger()

        For debugging:
            logger = getLogger(debug=True)

            You can also enable the diagnose to see what was wrong:
            logger = getLogger(debug=True, diagnose=True)

        To collect all the same module together, you can put, for example, the module name:
            # In spring_cloud.gatway
            logger = getLogger("spring_cloud")
            logger.info("hi 123")

            # In spring_cloud.context
            logger = getLogger("spring_cloud")
            logger.info("hi 456")
            ----
            └ This will render the output to be:
                2020-11-28 at 00:00:00 | INFO     | spring_cloud:<module>:7 - hi 123
                2020-11-28 at 00:00:00 | INFO     | spring_cloud:<module>:7 - hi 456

            # In ribbon.loadbalancer
            logger = getLogger("ribbon.loadbalancer")
            logger.info("hi 789")
            ----
            └ This will render the output to be:
                2020-11-28 at 00:00:00 | INFO     | ribbon.loadbalancer:<module>:7 - hi 789
    """

    name = name or "{name}"
    fmt = (
        fmt
        or "<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>%(name)s</cyan>:<cyan>{function}</cyan>:<cyan>{line}{extra[padding]}</cyan> - <level>{message}</level>\n{exception}"
        % {"name": name}
    )

    # Remove default settings
    logger_.remove()

    # Debug level settings
    if bool(os.environ.get("logging.debug")):
        debug = True
    DEBUG_LEVEL = "DEBUG" if debug else "INFO"
    DEBUG_FILTER = None if debug else lambda record: record["level"].no <= 30

    # Patch name if provided
    logger_ = logger_.patch(lambda record: record["extra"].update(name=name))

    # Init Formatter
    Formatter = formatter_(fmt=fmt)

    # Add handlers for stdout / stderr
    logger_.add(sys.stdout, level=DEBUG_LEVEL, filter=DEBUG_FILTER, diagnose=diagnose, format=Formatter.format)
    logger_.add(
        sys.stderr,
        level="ERROR",
        filter=lambda record: record["level"].no >= 40,
        diagnose=diagnose,
        format=Formatter.format,
    )

    return logger_
