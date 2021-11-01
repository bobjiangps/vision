import logging


class Logger:
    @classmethod
    def get_logger(cls, name):
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")
        return logging.getLogger(name)
