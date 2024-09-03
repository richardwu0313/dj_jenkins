import time
from datetime import datetime

from typing import List

from loguru import logger


class TimeUtil:

    @staticmethod
    def get_time() -> int:
        """
        get int of current time
        :return:
        """
        return int(time.time())

    @staticmethod
    def get_local_time(fmt="%H:%M:%S") -> time:
        """
        return current time
        :param fmt:
        :return:
        """
        time_str = TimeUtil.get_local_time_str(fmt=fmt)
        return datetime.strptime(time_str, fmt).time()

    @staticmethod
    def get_local_time_str(fmt="%H:%M:%S") -> str:
        """
        return string of local time
        :param fmt:
        :return: string
        """
        return time.strftime(fmt, time.localtime())

    @staticmethod
    def get_local_date(fmt="%Y-%m-%d") -> datetime.date:
        """
        return current date
        :param fmt:
        :return:
        """
        date_str = TimeUtil.get_local_date_str(fmt=fmt)
        return datetime.strptime(date_str, fmt).date()

    @staticmethod
    def get_local_date_str(fmt="%Y-%m-%d") -> str:
        """
        return string of local date
        :param fmt:
        :return: string
        """
        return time.strftime(fmt, time.localtime())

    @staticmethod
    def get_local_datetime(fmt="%Y-%m-%d %H:%M:%S") -> datetime:
        """
        return current datetime
        :param fmt:
        :return:
        """
        datetime_str = TimeUtil.get_local_datetime_str(fmt=fmt)
        return datetime.strptime(datetime_str, fmt)

    @staticmethod
    def get_local_datetime_str(fmt="%Y-%m-%d %H:%M:%S") -> str:
        """
        return string of local datetime
        :param fmt:
        :return: string
        """
        return time.strftime(fmt, time.localtime())

    @staticmethod
    def get_log_timestamp(fmt="%Y-%m-%d %H:%M:%S.%f"):
        return datetime.now().strftime(f"[{fmt}]")

    @staticmethod
    def get_time_deta(start_at, end_at):
        if not isinstance(start_at, datetime) or not isinstance(end_at, datetime):
            return None
        return end_at - start_at

    @staticmethod
    def get_time_deta_str(start_at, end_at) -> str:
        time_diff = TimeUtil.get_time_deta(start_at, end_at)
        hours = time_diff.seconds // 3600
        minutes = time_diff.seconds % 3600 // 60
        seconds = time_diff.seconds % 60
        return "{}h:{}m:{}s".format(hours, minutes, seconds)

    @staticmethod
    def str2date(str_date, fmt="%Y-%m-%d") -> datetime.date:
        dt = datetime.strptime(str_date, fmt)
        return dt.date()

    @staticmethod
    def date2str(date, fmt="%Y-%m-%d") -> str:
        str = date.strftime(fmt)
        return str

    @staticmethod
    def kd_str2date(str_kd_date, fmt="%Y-%m-%d") -> datetime.date:
        dt = datetime.strptime(str_kd_date.split("T")[0], fmt)
        return dt.date()

    @staticmethod
    def str2datetime(str_datetime, fmt="%Y-%m-%dT%H:%M:%S") -> datetime:
        dt = datetime.strptime(str_datetime, fmt)
        return dt

    @staticmethod
    def timestamp2datetime(timestamp) -> datetime:
        try:
            dt = datetime.fromtimestamp(timestamp)
            return dt
        except Exception as ex:
            logger.error(str(ex))
        return None

    @staticmethod
    def jenkins_timestamp2datetime(timestamp) -> datetime or None:
        try:
            dt = datetime.fromtimestamp(timestamp/1000)
            return dt
        except Exception as ex:
            logger.error(str(ex))
        return None

    @staticmethod
    def timestamp2datetime_str(timestamp, fmt="%Y-%m-%dT%H:%M:%S") -> str:
        dt = TimeUtil.timestamp2datetime(timestamp)
        if dt:
            dt_str = dt.strftime(fmt=fmt)
            return dt_str
        return ""

    @staticmethod
    def get_year_dates(year: int) -> List[str]:
        from calendar import monthrange
        dates = []
        for month in range(1, 13):
            _, last_day = monthrange(year, month)
            for day in range(1, last_day + 1):
                date_str = "{}-{:02d}-{:02d}".format(year, month, day)
                dates.append(date_str)
        return dates

    @staticmethod
    def get_year_month_dates(year: int, month: int) -> List[str]:
        dates = []
        from calendar import monthrange
        _, last_day = monthrange(year, month)
        for day in range(1, last_day + 1):
            date_str = "{}-{:02d}-{:02d}".format(year, month, day)
            dates.append(date_str)
        return dates
