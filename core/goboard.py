import turtle

from core.gotypes import Point


class Draw:
    """
    画图类
    纯粹的画图类（包括绘制棋盘、落子、提子和绘制结束），不与围棋的逻辑有任何关联
    """

    # 初始化画板
    def __init__(self, board_size):
        if board_size not in (9, 13, 19):
            raise Exception("目前只支持9*9、13*13和19*19这三种类型的棋盘")
        # 棋盘尺寸
        self.board_size = board_size
        # 棋盘背景颜色（黄褐色）
        self.board_background_color = '#C28642'
        # 平行线间的距离
        self.step = 40
        # 序号距离
        self.index_no = 30
        # 起始点位（这个值其实是不可变的！！！其它逻辑都是基于(0,0)来处理的）
        self.start_point = 0
        # board_size的半值（在四个象限下，比如横坐标范围-100到100，其实只要确定半值0-100就可以了，因为负的坐标可以通过绝对值获取）
        self.half_value = (board_size - 1) / 2
        # 最小点位值
        self.min_point = self.start_point - self.half_value * self.step
        # 最大点位值
        self.max_point = self.start_point + self.half_value * self.step

    # 画棋盘
    def draw_board(self, finish=False):
        if finish:
            turtle.done()  # 绘制结束
        else:
            turtle.title('围棋')
            # 窗体
            turtle.setup(910, 910)
            # 画布
            turtle.screensize(900, 900, self.board_background_color)
            # 加速绘制
            turtle.speed(0)
            for sx in range(self.board_size):
                # 绘制竖线
                turtle.penup()
                turtle.goto(self.start_point - self.half_value * self.step + sx * self.step,
                            self.start_point + self.half_value * self.step)
                turtle.pendown()
                turtle.goto(self.start_point - self.half_value * self.step + sx * self.step,
                            self.start_point - self.half_value * self.step)
                # 绘制序号
                turtle.penup()
                turtle.goto(self.start_point - self.half_value * self.step + sx * self.step,
                            self.start_point + self.half_value * self.step + self.index_no)
                turtle.pendown()
                turtle.write(sx + 1)
            for hx in range(self.board_size):
                # 绘制横线
                turtle.penup()
                turtle.goto(self.start_point - self.half_value * self.step,
                            self.start_point + self.half_value * self.step - hx * self.step)
                turtle.pendown()
                turtle.goto(self.start_point + self.half_value * self.step,
                            self.start_point + self.half_value * self.step - hx * self.step)
                # 绘制序号
                turtle.penup()
                turtle.goto(self.start_point - self.half_value * self.step - self.index_no,
                            self.start_point + self.half_value * self.step - hx * self.step - self.step / 5)
                turtle.pendown()
                turtle.write(hx + 1)
            # 绘制星位
            r = ()
            if self.board_size == 9:
                r = (3, 7)
                turtle.penup()
                turtle.goto(self.start_point - self.half_value * self.step + (5 - 1) * self.step,
                            self.start_point + self.half_value * self.step - (5 - 1) * self.step)
                turtle.pendown()
                turtle.dot(5)
            if self.board_size == 13:
                r = (4, 10)
                turtle.penup()
                turtle.goto(self.start_point - self.half_value * self.step + (7 - 1) * self.step,
                            self.start_point + self.half_value * self.step - (7 - 1) * self.step)
                turtle.pendown()
                turtle.dot(5)
            if self.board_size == 19:
                r = (4, 10, 16)
            for m in r:
                for n in r:
                    turtle.penup()
                    turtle.goto(self.start_point - self.half_value * self.step + (m - 1) * self.step,
                                self.start_point + self.half_value * self.step - (n - 1) * self.step)
                    turtle.pendown()
                    turtle.dot(5)
            turtle.hideturtle()  # 隐藏笔的形状
            # turtle.done()  # 绘制结束

    # 画落子（为了方便，左上角的位置不再记为(0,0)，而是记为(1,1)，其它以此类推）
    def draw_point(self, point):
        if not isinstance(point, Point):
            raise Exception("坐标位置错误")
        if point.row < 1 or point.row > self.board_size:
            raise Exception("横坐标范围为：1-" + str(self.board_size))
        if point.col < 1 or point.col > self.board_size:
            raise Exception("纵坐标范围为：1-" + str(self.board_size))
        turtle.penup()
        turtle.goto(self.start_point - self.half_value * self.step + (point.col - 1) * self.step,
                    self.start_point + self.half_value * self.step - (point.row - 1) * self.step)
        turtle.pendown()
        turtle.pencolor(point.player.name)
        turtle.dot(25)

    # 画提子（为了方便，左上角的位置不再记为(0,0)，而是记为(1,1)，其它以此类推）
    def drop_draw_point(self, point):
        if not isinstance(point, Point):
            raise Exception("坐标位置错误")
        if point.row < 1 or point.row > self.board_size:
            raise Exception("横坐标范围为：1-" + str(self.board_size))
        if point.col < 1 or point.col > self.board_size:
            raise Exception("纵坐标范围为：1-" + str(self.board_size))
        # 这是笨办法。。。
        turtle.penup()
        turtle.goto(self.start_point - self.half_value * self.step + (point.col - 1) * self.step,
                    self.start_point + self.half_value * self.step - (point.row - 1) * self.step)
        turtle.pendown()
        turtle.color(self.board_background_color)
        turtle.dot(25)
        turtle.color('black')
        current_position = (turtle.pos()[0], turtle.pos()[1])
        # 获取当前点位的上下左右四个点
        current_position_shang = (current_position[0], current_position[1] + self.step)
        current_position_xia = (current_position[0], current_position[1] - self.step)
        current_position_zuo = (current_position[0] - self.step, current_position[1])
        current_position_you = (current_position[0] + self.step, current_position[1])
        if current_position_shang[1] <= self.max_point:
            turtle.penup()
            turtle.goto(current_position)
            turtle.pendown()
            turtle.goto(current_position[0], current_position[1] + self.step / 2)
        if current_position_xia[1] >= self.min_point:
            turtle.penup()
            turtle.goto(current_position)
            turtle.pendown()
            turtle.goto(current_position[0], current_position[1] - self.step / 2)
        if current_position_zuo[0] >= self.min_point:
            turtle.penup()
            turtle.goto(current_position)
            turtle.pendown()
            turtle.goto(current_position[0] - self.step / 2, current_position[1])
        if current_position_you[0] <= self.max_point:
            turtle.penup()
            turtle.goto(current_position)
            turtle.pendown()
            turtle.goto(current_position[0] + self.step / 2, current_position[1])
        if self.board_size == 9:
            if (((point.row == 3 or point.row == 7) and (point.col == 3 or point.col == 7)) or (
                    point.row == 5 and point.col == 5)) and point.player is None:
                turtle.penup()
                turtle.goto(self.start_point - self.half_value * self.step + (point.row - 1) * self.step,
                            self.start_point + self.half_value * self.step - (point.col - 1) * self.step)
                turtle.pendown()
                turtle.dot(5)
        if self.board_size == 13:
            if (((point.row == 4 or point.row == 10) and (point.col == 4 or point.col == 10)) or (
                    point.row == 7 and point.col == 7)) and point.player is None:
                turtle.penup()
                turtle.goto(self.start_point - self.half_value * self.step + (point.row - 1) * self.step,
                            self.start_point + self.half_value * self.step - (point.col - 1) * self.step)
                turtle.pendown()
                turtle.dot(5)
        if self.board_size == 19:
            if ((point.row == 4 or point.row == 10 or point.row == 16) and (
                    point.col == 4 or point.col == 10 or point.col == 16)) and point.player is None:
                turtle.penup()
                turtle.goto(self.start_point - self.half_value * self.step + (point.row - 1) * self.step,
                            self.start_point + self.half_value * self.step - (point.col - 1) * self.step)
                turtle.pendown()
                turtle.dot(5)
