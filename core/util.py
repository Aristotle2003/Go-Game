import math

import numpy as np

from core.gotypes import Point, Player
from core.zobrist import HASH_CODE


#  游戏帮助类
class GameHelp:

    # 获取一条棋链的所有气
    @classmethod
    def get_go_string_liberties(cls, board_size, grid, stone):
        count = 0
        for each_point in stone:  # 遍历棋链的每个点
            if count > 0:
                break
            four_neighbors = each_point.neighbors()
            for i in range(0, len(four_neighbors)):
                x_point = four_neighbors[i][0]
                y_point = four_neighbors[i][1]
                if (1 <= x_point <= board_size) and (1 <= y_point <= board_size):  # 防止越界
                    cpi = GameHelp.cal_point_index(x_point, y_point, board_size)
                    if grid[cpi].player is None:
                        count = 1
                        break
        return count  # 只要不是0即可

    # 移除没气的棋链（如果有），返回新的棋链
    @classmethod
    def remove_stones(cls, board_size, grid, stones):
        for stone in stones[::-1]:  # 遍历每条棋链
            liberties = GameHelp.get_go_string_liberties(board_size, grid, stone)  # 获取每条棋链现有的气
            if liberties == 0:  # 表示棋链没有气，则需要提子
                for each_point in stone:
                    cpi = GameHelp.cal_point_index(each_point.row, each_point.col, board_size)
                    grid[cpi].player = None
                stones.remove(stone)
        return stones

    # 获取需要合并的棋链和不需要合并的棋链
    @classmethod
    def get_combine_and_un_combine_stones(cls, stones, point):
        combine_stones = []  # 需要合并的棋链
        un_combine_stones = []  # 不需要合并的棋链
        for stone in stones:  # 遍历每条棋链
            four_neighbors = point.neighbors()  # 当前点的四个邻居点
            combine = False
            for each_point in stone:  # 遍历棋链的每个点
                if (each_point.row == four_neighbors[0][0] and each_point.col == four_neighbors[0][1]) or \
                   (each_point.row == four_neighbors[1][0] and each_point.col == four_neighbors[1][1]) or \
                   (each_point.row == four_neighbors[2][0] and each_point.col == four_neighbors[2][1]) or \
                   (each_point.row == four_neighbors[3][0] and each_point.col == four_neighbors[3][1]):
                    combine = True
                    break
            if combine:
                combine_stones.append(stone)
            else:
                un_combine_stones.append(stone)
        combine_out = []  # 最终合并后的新的棋链
        if len(combine_stones) > 0:
            for combine_stone in combine_stones:
                for each_point in combine_stone:
                    combine_out.append(each_point)
        combine_out.append(point)
        un_combine_stones.append(combine_out)  # 将最终合并后的新的棋链加入不需要合并的棋链列表中去
        return un_combine_stones

    # 点位下标计算（棋盘的横纵坐标转换为数组的下标）
    @classmethod
    def cal_point_index(cls, row, col, board_size):
        """
        点位下标计算
                              0     1     2     3     4     5     6     7     8
        以3*3为例，初始化后就是：[None, None, None, None, None, None, None, None, None]
           1 2 3
        1 |0|1|2|
        2 |3|4|5|
        3 |6|7|8|
        算法就是：(x-1)*board_size+(y-1)
        比如坐标(1,3)，对应数组的下标就是：(1-1)*3+(3-1)=2
        比如坐标(3,2)，对应数组的下标就是：(3-1)*3+(2-1)=7
        比如坐标(3,3)，对应数组的下标就是：(3-1)*3+(3-1)=8
        """
        return (row - 1) * board_size + (col - 1)

    # 棋盘点位计算（数组的下标转换为棋盘的横纵坐标）
    @classmethod
    def cal_board_point(cls, point_index, board_size):
        return (1 + int(point_index / board_size)), (1 + point_index % board_size)

    # 初始化棋盘点位对象
    @classmethod
    def init_board_grid_points(cls, board_size):
        _grid = []
        _border = board_size + 1
        for i in range(1, _border):
            for j in range(1, _border):
                _grid.append(Point(i, j, None))
        return _grid

    # 计算当前棋局的HASH值
    @classmethod
    def cal_current_grid_hash(cls, grid):
        _v = 0
        for i in grid:
            _row = i.row
            _col = i.col
            _player = i.player
            _key = str(_row) + ',' + str(_col) + ',' + ('None' if _player is None else _player.name)
            _v = _v ^ HASH_CODE[_key]
        return _v

    # 更新棋局
    @classmethod
    def update_go(cls, game, point):
        game.place_go_result(point)  # 落子
        game.grid_history.append(GameHelp.cal_current_grid_hash(game.grid))  # 记录每一局整个棋盘历史
        game.point_history.append(point.get_unique_key())  # 记录每一落子历史
        game.current_player = Player.next_player(game.current_player)  # 切换棋手

    # 虚拟一个新游戏
    @classmethod
    def virtual_new_game(cls, current_game, current_player=None):
        from core.gogame import Game
        _game = Game(current_game.main)
        _game.grid = []
        for i in current_game.grid:
            _game.grid.append(Point(i.row, i.col, i.player))
        _game.black_go_strings_stones = []
        for each_stone in current_game.black_go_strings_stones:
            temp = []
            for each_point in each_stone:
                temp.append(Point(each_point.row, each_point.col, each_point.player))
            _game.black_go_strings_stones.append(temp)
        _game.white_go_strings_stones = []
        for each_stone in current_game.white_go_strings_stones:
            temp = []
            for each_point in each_stone:
                temp.append(Point(each_point.row, each_point.col, each_point.player))
            _game.white_go_strings_stones.append(temp)
        _game.grid_history = []
        for i in current_game.grid_history:
            _game.grid_history.append(i)
        _game.current_player = (current_game.current_player if current_player is None else current_player)
        _game.is_game_over = current_game.is_game_over
        return _game

    @classmethod
    def quick_random_mock_game(cls, current_game, current_player=None, change_origin_game_state=False):
        from core.strategy import bot_move_random
        if change_origin_game_state:
            while not current_game.is_game_over:
                bot_move_random(current_game)
            return current_game
        else:
            _game = cls.virtual_new_game(current_game, current_player)
            while not _game.is_game_over:
                bot_move_random(_game)
            return _game

    @classmethod
    def encode_grid(cls, board_size, grid):
        # board_size = int(math.sqrt(len(grid)))
        board_matrix = np.zeros((board_size, board_size))  # 棋盘矩阵
        for point in grid:
            if point.player is not None:
                board_matrix[point.row-1][point.col-1] = (1 if point.player == Player.black else -1)
        return board_matrix

    @classmethod
    def decode_grid(cls, board_matrix, row, col):
        point_val = board_matrix[row-1][col-1]
        if point_val == 0:
            player = None
        else:
            player = (Player.black if point_val == 1 else Player.white)
        return Point(row, col, player)


# 游戏规则类
class GameRule:

    # 围棋最基础的规则1：只有空区域（即没有任何黑旗子或白棋子的区域）才能落子
    @classmethod
    def get_empty_zone_array(cls, game):
        _array = []
        for i in game.grid:
            # 围棋最基础的规则1：只有空区域（即没有任何黑旗子或白棋子的区域）才能落子
            if i.player is None:
                _array.append(i)
        return _array

    # 基础规则校验（这些是经验下的基本规则，但是对围棋规则来说，并不是必须的，只是大家基本都会遵循这个规则）
    @classmethod
    def base_rule_check(cls, game, point):
        # 机器人基础规则2：自己不要填自己的眼
        _point_neighbors = point.neighbors()
        _board_size = game.board_size
        _grid = game.grid
        count = 0
        for i in range(0, len(_point_neighbors)):
            x_point = _point_neighbors[i][0]
            y_point = _point_neighbors[i][1]
            if (1 <= x_point <= _board_size) and (1 <= y_point <= _board_size):  # 防止越界
                cpi = GameHelp.cal_point_index(x_point, y_point, _board_size)
                if _grid[cpi].player == point.player:
                    count += 1
            else:
                count += 1
        if count == 4:
            return False
        # 机器人基础规则3：落子后不能导致自己气尽
        go_on_flag = False
        _point = Point(point.row, point.col, point.player)
        _game = GameHelp.virtual_new_game(game, _point.player)
        _game.place_go_result(_point)
        now_point = _game.grid[GameHelp.cal_point_index(_point.row, _point.col, _board_size)]
        if now_point.player is not None:
            point_neighbors = now_point.neighbors()
            for i in range(0, len(point_neighbors)):
                x_point = point_neighbors[i][0]
                y_point = point_neighbors[i][1]
                if (1 <= x_point <= _board_size) and (1 <= y_point <= _board_size):
                    cpi = GameHelp.cal_point_index(x_point, y_point, _board_size)
                    if _game.grid[cpi].player is None or _game.grid[cpi].player == now_point.player:
                        go_on_flag = True
                        break
        if not go_on_flag:
            return False
        # 机器人基础规则4：不要出现劫争
        ko_result = True
        # 真实每一步形成的整个棋盘列表的HASH值
        real_grid_list = game.grid_history
        if len(real_grid_list) > 1:
            # 真实的上上步的棋盘状态HASH值
            two_step_real_grid_hash = real_grid_list[len(real_grid_list)-2]
            # 计算虚拟结果的棋盘状态HASH值
            current_virtual_grid_hash = GameHelp.cal_current_grid_hash(_game.grid)
            if two_step_real_grid_hash == current_virtual_grid_hash:
                ko_result = False
        return ko_result

    # 获得遵循一定基础规则的可落子点位（为get_empty_zone_array和base_rule_check的整合版）
    @classmethod
    def get_go_by_rules(cls, game):
        array = cls.get_empty_zone_array(game)
        for i in array[::-1]:
            _point = Point(i.row, i.col, game.current_player)
            if not GameRule.base_rule_check(game, _point):
                array.remove(i)
        _new_array = []
        for i in array:
            _new_array.append(Point(i.row, i.col, i.player))
        return _new_array
