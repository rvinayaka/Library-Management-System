import logging
import os

def logger(name):
    # social logger instance
    logger = logging.getLogger(name)
    # stop propagating to root logger
    logger.propagate = False
    # set level 1 i.e. DEBUG level
    logger.setLevel(logging.DEBUG)
    # Setting path for the log files
    log_direct = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'Logs')
    # Setting format for the log message
    log_file_name = os.path.join(log_direct, 'library.log')
    # creating format for the log message
    formatter = logging.Formatter('%(levelname)s :- %(asctime)s - %(name)s : %(message)s')
    # creating file handler for the log file
    file_handler = logging.FileHandler(log_file_name)
    # setting level for the handler
    file_handler.setLevel(logging.DEBUG)
    # setting format for the handler
    file_handler.setFormatter(formatter)
    # adding handler to the logger
    logger.addHandler(file_handler)
    # return the logger instance
    return logger
