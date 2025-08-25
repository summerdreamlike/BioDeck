"""
日期时间工具函数
"""
from datetime import datetime, timedelta

def now():
    """获取当前时间"""
    return datetime.now()

def format_datetime(dt, fmt="%Y-%m-%d %H:%M:%S"):
    """格式化日期时间"""
    return dt.strftime(fmt)

def parse_datetime(date_str, fmt="%Y-%m-%d %H:%M:%S"):
    """解析日期时间字符串"""
    return datetime.strptime(date_str, fmt)

def days_between(date1, date2):
    """计算两个日期之间的天数"""
    if isinstance(date1, str):
        date1 = parse_datetime(date1)
    if isinstance(date2, str):
        date2 = parse_datetime(date2)
    return abs((date2 - date1).days)

def format_date(dt):
    """格式化为日期字符串"""
    return dt.strftime("%Y-%m-%d")

def format_time(dt):
    """格式化为时间字符串"""
    return dt.strftime("%H:%M:%S")

def add_days(dt, days):
    """添加天数"""
    return dt + timedelta(days=days)

def add_hours(dt, hours):
    """添加小时数"""
    return dt + timedelta(hours=hours)

def is_same_day(dt1, dt2):
    """判断是否是同一天"""
    return format_date(dt1) == format_date(dt2)

def get_current_academic_year():
    """获取当前学年，格式为：2023-2024"""
    today = datetime.now()
    year = today.year
    month = today.month
    
    # 如果当前月份在9月或以后，学年开始年份为当前年份
    # 否则开始年份为前一年
    start_year = year if month >= 9 else year - 1
    end_year = start_year + 1
    
    return f"{start_year}-{end_year}"

def get_current_term():
    """获取当前学期，返回"第一学期"或"第二学期" """
    today = datetime.now()
    month = today.month
    
    # 9月到次年2月为第一学期，3月到8月为第二学期
    return "第一学期" if 9 <= month <= 12 or 1 <= month <= 2 else "第二学期" 