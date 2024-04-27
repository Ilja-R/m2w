import logging

from common.configuration import Configuration


class Logger:

    def __init__(self, name):
        self.logger_config = Configuration().get_config('logger')
        self.name = name
        self.logger_format = self.logger_config['format']
        self.log_level = self.logger_config['level']

        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.log_level)
        formatter = logging.Formatter(self.logger_format)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(self.log_level)
        self.logger.addHandler(console_handler)

    # green
    def info(self, message):
        self.logger.info('\033[0;32m%s\033[0m' % message)

    # yellow
    def warning(self, message):
        self.logger.warning('\033[0;33m%s\033[0m' % message)

    # red
    def error(self, message):
        self.logger.error('\033[0;31m%s\033[0m' % message)