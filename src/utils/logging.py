import logging, sys
def get_logger(name: str = "chatbot") -> logging.Logger:
    log = logging.getLogger(name)
    if not log.handlers:
        log.addHandler(logging.StreamHandler(sys.stdout))
        log.setLevel(logging.INFO)
    return log
