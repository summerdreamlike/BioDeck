# 从各个模块导入模型类

# 用户模型
from .user import User

# 学生相关模型
from .student import Student
from .study import StudyData

# 题目与考试相关
# 已删除试卷和题目管理模块

# 教学资源相关
from .material import Material
from .category import Category, Tag

# 反馈相关


# 考勤相关
from .daily_checkin import DailyCheckin

# 练习和错题本
from .practice import Practice, WrongBook

# 消息相关
from .message import Message 