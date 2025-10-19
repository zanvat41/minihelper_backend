import logging


class TestFilter(logging.Filter):

    # record(log details)
    def filter(self, record):
        if '----' in record.msg:
            return False
        else:
            return True
