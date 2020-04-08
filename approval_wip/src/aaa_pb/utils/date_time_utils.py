class DateTimeUtils:

    @classmethod
    def getDateTimeFileName(cls) -> str:
        """
        :return: a datetime string, e.g. '20180716-175916'
        """
        import time
        timestr = time.strftime("%Y%m%d-%H%M%S")
        return timestr
