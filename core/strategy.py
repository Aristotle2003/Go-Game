import random
import time

from core.gotypes import Player, Point
from core.util import GameHelp, GameRule
from mcts.mcts import MctsAgent


# -------------------------------------------------- 华丽的分割线 --------------------------------------------------
# 机器人落子（随机）
def bot_move_random(game):
    _array = GameRule.get_empty_zone_array(game)
    game.is_game_over = True
    for i in _array[::-1]:
        r = random.choice(_array)  # 随机选择一个点
        point = Point(r.row, r.col, game.current_player)  # 模拟落子
        if GameRule.base_rule_check(game, point):
            GameHelp.update_go(game, point)
            """
            print(
                "当前旗手为：{}，落子点位为：({},{})，黑旗棋链为：{}条，白旗棋链为：{}条"
                .format(
                    ('black' if game.current_player.name == 'white' else 'white'),
                    point.row,
                    point.col,
                    len(game.black_go_strings_stones),
                    len(game.white_go_strings_stones)
                )
            )
            """
            game.is_game_over = False
            break
        else:
            _array.remove(i)


# 机器人落子（蒙特卡洛树搜索）
def bot_move_mcts(game):
    cost_time = time.perf_counter()
    # 这里做了筛选，只有有价值的点位（至少得符合围棋的一些基本规则）才会去进行蒙特卡洛树搜索
    _array = GameRule.get_go_by_rules(game)
    if len(_array) == 0:
        game.is_game_over = True
    else:
        print("可供蒙特卡洛搜索树搜索的有效点位一共有：" + str(len(_array)) + "个")
        """
        执行次数：默认为棋盘规格的平方*10（如规格为19的棋盘就模拟19*19*10=3610），当然模拟次数越多结果相对就越理想
        热度：可以简单理解为起到平衡搜索深度和广度的作用
        """
        num_rounds = game.board_size ** 2 * 1
        temperature = 1.4
        better_point = MctsAgent(num_rounds, temperature).select_point(game, _array)  # 蒙特卡洛树搜素获取胜率最高的点
        point = Point(better_point.row, better_point.col, game.current_player)  # 落子
        GameHelp.update_go(game, point)
        print(
            "当前旗手为：{}，落子点位为：({},{})，总模拟次数为：{}次，一共耗时{}，平衡搜索深度和广度的系数为：{}，黑旗棋链为：{}条，白旗棋链为：{}条"
            .format(
                ('black' if game.current_player.name == 'white' else 'white'),
                point.row,
                point.col,
                num_rounds,
                time.perf_counter() - cost_time,
                temperature,
                len(game.black_go_strings_stones),
                len(game.white_go_strings_stones)
            )
        )
        print('----------------------------------------------------------------------------------------------------')
