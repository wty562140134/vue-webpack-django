import time
from datetime import datetime


def datetime_to_string(date, time_format='%Y-%m-%d %H:%M:%S'):
    """
    把datetime转成字符串
    :param date: datetime类型 如datetime.now() 或datetime.utcnow()
    :type datetime
    :param time_format: 需要转换成的时间字符串格式,默认为%Y-%m-%d %H:%M:%S
    :type str
    :return: 转换成指定字格式的字符串时间
    :type str
    """
    return date.strftime(time_format)


def string_to_datetime(date_str, time_format='%Y-%m-%d %H:%M:%S'):
    """
    把字符串转成datetime
    :param date_str:时间字符串
    :type str
    :param time_format: 时间字符串的格式,默认为%Y-%m-%d %H:%M:%S
    :type str
    :return:转换为datetime类型的时间
    :type datetime
    """
    return datetime.strptime(date_str, time_format)


def string_to_timestamp(date_str):
    """
    把字符串转成时间戳形式
    :param date_str: 时间字符串
    :type str
    :return: 时间戳(秒)
    :type float
    """
    return time.mktime(string_to_datetime(date_str).timetuple())


def timestamp_to_string(stamp, time_format='%Y-%m-%d %H:%M:%S'):
    """
    把时间戳转成字符串形式
    :param stamp: 时间戳(秒)
    :type float
    :param time_format: 需要将时间戳格式化为的字符串时间格式,默认为%Y-%m-%d %H:%M:%S
    :type str
    :return: 格式化为指定格式的时间字符串
    :type str
    """
    return time.strftime(time_format, time.localtime(stamp))


def datetime_to_timestamp(date_time):
    """
    把datetime类型转外时间戳形式
    :param date_time: datetime类型 如datetime.now() 或datetime.utcnow()
    :type datetime
    :return: 时间戳(秒)
    :type float
    """
    return time.mktime(date_time.timetuple())

# Wed May 01 2019 00:00:00 GMT+0800 (中国标准时间)
# GMT_FORMAT = '%a %b %d %Y %H:%M:%S GMT+0800 (CST)'
# GMT_data = datetime_to_string(datetime.now(), GMT_FORMAT)
# print(GMT_data)
# str_da = string_to_datetime(GMT_data, GMT_FORMAT)
# print(str_da)
# print(datetime_to_string(str_da))
# timestamp = datetime_to_timestamp(str_da)
# subtract = 5 * 24 * 60 * 60
# s = timestamp - subtract
# print(timestamp_to_string(s, GMT_FORMAT))
