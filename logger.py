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

def useAdapter():
    print("adapter")

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


if __name__ == "__main__":
    useFactory()
    # useAdapter()
    # useFilter()