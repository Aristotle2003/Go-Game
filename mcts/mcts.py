import math
import random

from core.gotypes import Player, Point
from core.util import GameHelp, GameRule


class MctsAgent:

    def __init__(self, num_rounds, temperature):
        self.num_rounds = num_rounds  # 执行次数
        self.temperature = temperature  # 热度

    @staticmethod
    def random_go_mock(node):
        index = random.randint(0, len(node.unvisited_point) - 1)  # 随机获取有效落子下标
        r_point = node.unvisited_point.pop(index)
        r_point.player = node.game.current_player
        _game = GameHelp.virtual_new_game(node.game)
        GameHelp.update_go(_game, r_point)  # 随机落子
        new_game = GameHelp.quick_random_mock_game(_game, None, False)  # 基于当前点位快速模拟一盘
        winner = new_game.who_win()
        _array = GameRule.get_go_by_rules(_game)
        if len(_array) > 0:
            # 获取未更新棋盘状态前的旗手
            before_player = Player.black if _game.current_player == Player.white else Player.white
            new_node = Mcts(_game, Point(r_point.row, r_point.col, before_player), node, _array)
            node.children.append(new_node)
            while new_node is not None:
                new_node.record_win(winner)
                new_node = new_node.parent  # 反向传播，即回溯

    @staticmethod
    def next_go_mock(node):
        next_player = Player.next_player(node.game.current_player)
        _array = GameRule.get_go_by_rules(node.game)
        if len(_array) > 0:
            index = random.randint(0, len(_array) - 1)  # 随机获取有效落子下标
            r_point = _array.pop(index)
            r_point.player = next_player
            _game = GameHelp.virtual_new_game(node.game)
            GameHelp.update_go(_game, r_point)  # 随机落子
            new_game = GameHelp.quick_random_mock_game(_game, None, False)  # 基于当前点位快速模拟一盘
            winner = new_game.who_win()
            _array = GameRule.get_go_by_rules(_game)
            if len(_array) > 0:
                # 获取未更新棋盘状态前的旗手
                before_player = Player.black if _game.current_player == Player.white else Player.white
                new_node = Mcts(_game, Point(r_point.row, r_point.col, before_player), node, _array)
                node.children.append(new_node)
                while new_node is not None:
                    new_node.record_win(winner)
                    new_node = new_node.parent  # 反向传播，即回溯

    # 选择需要落子的点位
    def select_point(self, game, array):
        root = Mcts(GameHelp.virtual_new_game(game), None, None, array)  # 构造一个当前游戏状态的虚拟镜像并初始化根节点
        for i in range(0, self.num_rounds):  # 模拟次数
            node = root  # 每模拟一次后都要回到根节点重新选择
            if len(node.unvisited_point) > 0:  # 优先探索所有没有探索过的节点
                self.random_go_mock(node)
            else:
                while len(node.children) > 0:
                    node = self.select_child(node)  # 最佳选择
                if len(node.unvisited_point) > 0:  # 优先探索所有没有探索过的节点
                    self.random_go_mock(node)
                else:
                    self.next_go_mock(node)
        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.rate_of_winning(root.game.current_player)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.point
        print(
            '经反向传播，统计得出：一共模拟了{}次，其中黑旗总共获胜{}次，白旗总共获胜{}次'
            .format(
                root.num_rollouts,
                root.win_counts[Player.black],
                root.win_counts[Player.white]
            )
        )
        return best_move

    def select_child(self, node):
        # UCT公式（搜索树置信区间上界公式）
        total_rollouts = sum(child.num_rollouts for child in node.children)  # 当前节点下的所有子节点的模拟次数总和
        log_rollouts = (0 if total_rollouts <= 0 else math.log(total_rollouts))
        best_score = -1
        best_child = None
        for child in node.children:
            win_percentage = child.rate_of_winning(child.point.player)
            exploration_factor = math.sqrt(log_rollouts / child.num_rollouts)
            uct_score = win_percentage + self.temperature * exploration_factor
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child


# 主要定义的是一个数据结构
class Mcts:

    def __init__(self, game, point=None, parent=None, unvisited_point=None):
        self.game = game  # 当前游戏对象
        self.point = point  # 当前点位
        self.parent = parent  # 当前节点的父节点
        # 推演统计信息
        self.win_counts = {
            Player.black: 0,  # 黑旗赢的次数
            Player.white: 0,  # 白旗赢的次数
        }
        self.num_rollouts = 0  # 基于当前节点总共模拟的次数
        self.children = []  # 当前节点的所有子节点列表
        self.unvisited_point = unvisited_point  # 从当前棋局开始，所有可能的合法动作列表

    # 记录获胜次数
    def record_win(self, winner_player):
        self.win_counts[winner_player] += 1  # 赢者次数+1
        self.num_rollouts += 1  # 总模拟次数+1

    # 计算胜率
    def rate_of_winning(self, player):
        return float(self.win_counts[player]) / float(self.num_rollouts)
