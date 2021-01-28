

class DataPointMissingError(Exception):

    def __init__(self, datetime_stamp):
        self.datetime_stamp = datetime_stamp
        msg = (f"Data point for {datetime_stamp} missing")
        super().__init__(msg)
