from os import stat
import platform
import logging
import os

class LoggingHandler:

    def __init__(self, logger_name:str="My_login"):
        """
        Manages the loggin sessions
        PARAMETERS:
        ----------
        logger_name: String if the instance of logger will  habe a name in the logg register.
        """

        # instance loggin
        logging.basicConfig(filename = "scraper_scraper_logger",
                                    filemode='a',
                                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S',
                                    level=logging.INFO)
        pc_name = platform.node()

        logging.info(f"STARTING LOGGING at Machine: {pc_name}")

        self.logger = logging.getLogger(logger_name)