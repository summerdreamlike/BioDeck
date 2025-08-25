# 从各个模块导入模型类

# 用户模型
from .user import User

# 学生相关模型
from .student import Student
from .study import StudyData

# 题目与考试相关
from .question import Question
from .paper import Paper

# 课程相关
from .course import Course, CourseMessage

# 教学资源相关
from .material import Material
from .category import Category, Tag

# 任务相关
from .task import Task

# 反馈相关
from .feedback import Feedback

# 考勤相关
from .attendance import Attendance

# 练习和错题本
from .practice import Practice, WrongBook

# 消息相关
from .message import Message 