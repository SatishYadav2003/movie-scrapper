import logging

logging.basicConfig(filename="eye_watcher.txt",level=logging.INFO)


def log_message(message):
    logging.info(message)