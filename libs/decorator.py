import logging


def withlog(func):
    logger: logging.Logger = logging.getLogger(func.__name__)

    def inner(*args, **kwargs):
        logger.debug(rf"Start running under args: {args}, kwargs: {kwargs}")
        return_val = func(*args, **kwargs, logger=logger)
        logger.debug(rf"Running finished under args: {args}, kwargs: {kwargs}")
        if return_val is not None:
            logger.debug(f"Returned: '{return_val}'")
        return return_val

    return inner
