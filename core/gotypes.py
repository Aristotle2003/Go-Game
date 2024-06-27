from enum import Enum, unique

"""
围棋基本类型文件，主要提供4个类
1、棋手类（黑旗和白旗）
2、点位类（横坐标和纵坐标）
3、对战类（约定VS的左右两侧为：左执黑子右执白子）
"""


# 棋手类（黑旗和白旗）
@unique  # 强制限定枚举的所有值（value）都不能相同
class Player(Enum):  # 枚举类，继承自Enum

    black = 1  # 黑子
    white = -1  # 白子

    # 获取交替选手
    def next_player(self):
        # 三目运算符：如果是white则返回black，如果是black则返回white
        return Player.black if self == Player.white else Player.white


# 点位类（横坐标和纵坐标）
class Point:
    """
    具名元祖：
    class Point(namedtuple('Point', ['row', 'col'])):
    也可以写成：
    class Point(namedtuple('Point', 'row col')):
    """

    def __init__(self, row, col, player):
        self.row = row
        self.col = col
        self.player = player

    # 获取当前点位的四个邻居（左右下上）
    def neighbors(self):
        # 中心点的左（←）右（→）下（↓）上（↑）4个点
        return [(self.row - 1, self.col), (self.row + 1, self.col), (self.row, self.col - 1), (self.row, self.col + 1)]

    # 获取唯一key值
    def get_unique_key(self):
        return str(self.row) + ',' + str(self.col) + ',' + ('None' if self.player is None else self.player.name)

    def __hash__(self):
        return hash(str(self.row) + ',' + str(self.col))


# 对战类（约定VS的左右两侧为：左执黑子右执白子）
@unique
class Battle(Enum):
    # 机器人VS机器人
    BOT_VS_BOT = 1
    # 机器人VS人类
    BOT_VS_HUMAN = 2
    # 人类VS机器人
    HUMAN_VS_BOT = 3
    # 人类VS人类
    HUMAN_VS_HUMAN = 4

# 棋盘尺寸类
@unique
class BoardSize(Enum):
    # 小：9*9
    SMALL = 9
    # 中：13*13
    MEDIUM = 13
    # 大：19*19
    LARGE = 19
