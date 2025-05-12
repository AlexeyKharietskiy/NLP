from datetime import timedelta


class DateParser:
    @staticmethod
    def parse(unit, value):
        if unit == 'hour':
            return timedelta(hours=value)
        elif unit == 'minute':
            return timedelta(minutes=value)
        elif unit == 'second':
            return timedelta(seconds=value)