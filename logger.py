#!/usr/bin/env python3

import sys
import uuid
import logging

def testFunction():
    logging.debug("debug message")
    logging.info("info message")
    logging.warning("warning message")
    logging.error("error message")
    logging.critical("critical message")


def useFactory():
    print("factory")

    logging.basicConfig(format="%(trace_id)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.CRITICAL, stream=sys.stdout)

    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.trace_id = "22"
        return record
  
    logging.setLogRecordFactory(record_factory)

    testFunction()


def useFormatter():
    print("formatter")

    logger = logging.getLogger()

    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(trace_id)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s")
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    logger.setLevel(logging.CRITICAL)

    extra = {"trace_id": "32"}
    logger = logging.LoggerAdapter(logger, extra)

    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")


def useAdapter():
    print("adapter")

    class LoggerAdapter(logging.LoggerAdapter):
        def __init__(self, logger, prefix):
            super(LoggerAdapter, self).__init__(logger, {})
            self.prefix = prefix

        def process(self, msg, kwargs):
            return '[%s] %s' % (self.prefix, msg), kwargs

    logger = logging.getLogger(__name__)
    myHandler = logging.StreamHandler()
    myFormatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    myHandler.setFormatter(myFormatter)
    logger.addHandler(myHandler)
    logger.setLevel(logging.CRITICAL)

    logger = LoggerAdapter(logger, 'custom prefix')

    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")


def useFilter():
    print("filter")

    class AppFilter(logging.Filter):
        def filter(self, record):
            record.trace_id = "42"
            return True

    logger = logging.getLogger()

    logger.addFilter(AppFilter())
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(trace_id)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s")
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    logger.setLevel(logging.CRITICAL)

    testFunction()


def useFormat():
    logging.basicConfig(format="%(trace_id)s - %(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.CRITICAL)
    
    values={"trace_id": "52"}
    logging.debug("debug message", extra=values)
    logging.info("info message", extra=values)
    logging.warning("warning message", extra=values)
    logging.error("error message", extra=values)
    logging.critical("critical message", extra=values)


if __name__ == "__main__":
    useFactory()
    # useFormatter
    # useAdapter()
    # useFilter()
    # useFormat()