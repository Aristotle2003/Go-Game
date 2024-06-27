from core.gotypes import Player, Point
from core.util import GameHelp, GameRule
from mcts.mcts import MctsAgent
from Interface import *
import random
import time
import numpy as np

class Game:
    """
    游戏类
    """

    # 初始化游戏
    def __init__(self, main):
        self.main = main
        self.board_size = main.board_size  # 棋盘规格
        self.grid = GameHelp.init_board_grid_points(main.board_size)  # 棋盘点位
        self.black_go_strings_stones = []  # 黑旗棋链
        self.white_go_strings_stones = []  # 白旗棋链
        self.grid_history = []  # 每一步形成的整个棋盘列表
        self.point_history = []  # 每一步形成的点位列表
        self.current_player = Player.black  # 先手旗手（默认永远是黑旗）
        self.is_game_over = False  # 游戏是否结束

        self.last_grid = []
        self.AIType = 0

    # 落子后的最终棋盘结果
    def place_go_result(self, point):
        """
        落子后的最终棋盘结果
        本方法不关心当前是黑子还是白子，只要有Point的三个值（row、col、player）即可
        """
        # -------------------------------------------------- 落子 --------------------------------------------------
        cpi = GameHelp.cal_point_index(point.row, point.col, self.board_size)
        self.grid[cpi] = point  # 更新棋盘点位（先把子落下去）
        # -------------------------------------------------- 对手 --------------------------------------------------
        """
        先处理对手的棋链和气
        对手的棋链逻辑：已经存在的棋链不会改变，只会整个棋链被提掉
        """
        # 获取当前对手的棋链
        stones = self.white_go_strings_stones if point.player == Player.black else self.black_go_strings_stones
        result = GameHelp.remove_stones(self.board_size, self.grid, stones)  # 移除没气的棋链（如果有），返回新的棋链
        if point.player == Player.black:
            self.white_go_strings_stones = result
        else:
            self.black_go_strings_stones = result
        # -------------------------------------------------- 自己 --------------------------------------------------
        """
        处理自己的棋链和气
        自己的棋链逻辑：新增独立棋链或合并棋链
        """
        stones2 = self.black_go_strings_stones if point.player == Player.black else self.white_go_strings_stones
        stones3 = GameHelp.get_combine_and_un_combine_stones(stones2, point)  # 获取需要合并的棋链和不需要合并的棋链
        result2 = GameHelp.remove_stones(self.board_size, self.grid, stones3)  # 移除没气的棋链（如果有），返回新的棋链
        if point.player == Player.black:
            self.black_go_strings_stones = result2
        else:
            self.white_go_strings_stones = result2

    # 计算胜负
    def who_win(self):
        black_count = 0
        while_count = 0
        # 同色棋子数统计
        for e in self.grid:
            _p = e.player
            if _p is not None:
                if _p == Player.black:
                    black_count += 1
                else:
                    while_count += 1
        """
        # 同色棋链拥有的气统计
        black_array = []
        white_array = []
        black_stones = self.black_go_strings_stones
        white_stones = self.white_go_strings_stones
        for stone in black_stones:
            for each_point in stone:
                four_neighbors = each_point.neighbors()
                for i in range(0, len(four_neighbors)):
                    x_point = four_neighbors[i][0]
                    y_point = four_neighbors[i][1]
                    if (1 <= x_point <= self.board_size) and (1 <= y_point <= self.board_size):  # 防止越界
                        cpi = GameHelp.cal_point_index(x_point, y_point, self.board_size)
                        black_array.append(cpi)
        for stone in white_stones:
            for each_point in stone:
                four_neighbors = each_point.neighbors()
                for i in range(0, len(four_neighbors)):
                    x_point = four_neighbors[i][0]
                    y_point = four_neighbors[i][1]
                    if (1 <= x_point <= self.board_size) and (1 <= y_point <= self.board_size):  # 防止越界
                        cpi = GameHelp.cal_point_index(x_point, y_point, self.board_size)
                        white_array.append(cpi)
        black_count += len(set(black_array))
        while_count += len(set(white_array))
        """
        if self.board_size == 9:
            while_count += 3.5
        elif self.board_size == 13:
            while_count += 5.5
        elif self.board_size == 19:
            while_count += 7.5
        # print(black_count, while_count)
        return Player.black if black_count > while_count else Player.white

    # 落子和提子的画图逻辑方法
    def draw_and_drop_point(self):        
        step = self.main.lens / (self.main.board_size - 1)
        w = step * 0.9
        for i in range(0, len(self.grid)):
            if self.grid[i].player is not None:
                surf = pygame.Surface((w,w))  
                surf.fill(self.main.colours["GAME BACKGROUND"]) 
                x = self.main.sx + (self.grid[i].col-1) * step - w/2
                y = self.main.sy + (self.grid[i].row-1) * step - w/2                           
                if self.grid[i].player.name == "black":             
                    pygame.draw.circle(surf,self.main.colours["BLACK"],(w/2,w/2),w/2)
                    self.main.window.screen.blit(surf,pygame.Rect(x,y,w,w))
                elif self.grid[i].player.name == "white":   
                    pygame.draw.circle(surf,self.main.colours["WHITE"],(w/2,w/2),w/2)
                    self.main.window.screen.blit(surf,pygame.Rect(x,y,w,w))
                else:
                    pass

    def start_game(self,ai):
    
        self.main.window.set_attribute("background",self.main.colours["GAME BACKGROUND"])
        self.main.set_attribute("in game",True)
            
        new_interface = GameElements(self.main)

        last_grid = GameHelp.init_board_grid_points(self.main.board_size)
        cost_time = time.perf_counter()
        self.AIType = ai

    def humanGo(self):        
        if self.main.get_attribute("left mouse up"):
            mouse_pos = self.main.get_attribute("mouse pos")    
            step = self.main.lens / (self.main.board_size - 1)     
            for row in range(1,self.main.board_size+1):
                for col in range(1,self.main.board_size+1):
                    tx1 = mouse_pos[0]
                    ty1 = mouse_pos[1]
                    tx2 = self.main.sx + (col-1) * step
                    ty2 = self.main.sy + (row-1) * step                              
                    if ((pow(tx1 - tx2,2) + pow(ty1 - ty2,2)) < pow(step*0.33,2)):   
                        point = Point(row, col, self.current_player)
                        GameHelp.update_go(self, point)
                        self.main.unclick()
                        self.main.window.update_info_box(0,"Current Player : " + self.current_player.name)
                        self.draw_and_drop_point()
                        return

    #随机bot
    def botRandomGo(self):
        _array = GameRule.get_empty_zone_array(self)
        self.is_game_over = True
        for i in _array[::-1]:
            r = random.choice(_array)  # 随机选择一个点
            point = Point(r.row, r.col, self.current_player)
            if GameRule.base_rule_check(self, point):
                GameHelp.update_go(self, point)
                self.main.window.update_info_box(0,"Current Player : " + self.current_player.name)
                self.is_game_over = False
                break
            else:
                _array.remove(i)

    #启发bot
    def botHeuristicGo(self):
        
        _array = GameRule.get_empty_zone_array(self)
        self.is_game_over = True
        maxOne = None
        maxValue = -99999999
        for r in _array:
            point = Point(r.row, r.col, self.current_player) 
            if GameRule.base_rule_check(self, point):

                _game = GameHelp.virtual_new_game(self)
                GameHelp.update_go(_game, point) 

                board_array=self.evaluation(_game)
                count_b=np.sum(board_array[board_array[:]>=1])
                count_w=abs(np.sum(board_array[board_array[:]<=-1]))

                one = {'p':point,'score':count_w-count_b}
                if one['score'] > maxValue:
                    maxValue = one['score']
                    maxOne = one

        if maxOne is not None:
            GameHelp.update_go(self, maxOne['p'])
            self.main.window.update_info_box(0,"Current Player : " + self.current_player.name)
            self.is_game_over = False
                

    #蒙特卡洛bot
    def botMonteCarloGo(self):
        _array = GameRule.get_go_by_rules(self)
        if len(_array) == 0:
            self.is_game_over = True
        else:
            #num_rounds = self.board_size ** 2 * 1 #这个参数标志随机的次数，越多越智能，速度越慢
            num_rounds = self.board_size
            temperature = 1.4 #深度广度的平衡参数
            better_point = MctsAgent(num_rounds, temperature).select_point(self, _array)  # 蒙特卡洛树搜素获取胜率最高的点
            point = Point(better_point.row, better_point.col, self.current_player)  # 落子
            GameHelp.update_go(self, point)
            self.main.window.update_info_box(0,"Current Player : " + self.current_player.name)

    def update(self):
        
        self.draw_and_drop_point()

        if self.is_game_over:
            return
        if len(GameRule.get_empty_zone_array(self)) == 0:
            self.is_game_over = True
            return

        mouse_pos = self.main.get_attribute("mouse pos")    
        step = self.main.lens / (self.main.board_size - 1)     

        if self.AIType == 0: #human vs human  
            self.humanGo()            

        elif self.AIType == 1: #random bot  
            if self.current_player.name == "black":#human is black
                self.humanGo()
            else: #bot
                self.botRandomGo()

        elif self.AIType == 2:
            if self.current_player.name == "black":#human is black
                self.humanGo()
            else: #bot
                self.botHeuristicGo()

        elif self.AIType == 3:
            if self.current_player.name == "black":#human is black
                self.humanGo()
                self.draw_and_drop_point()
            else: #bot            
                self.botMonteCarloGo()

        if self.is_game_over:
            board_array=self.evaluation(self)
            count_b=np.sum(board_array[board_array[:]>=1])
            count_w=abs(np.sum(board_array[board_array[:]<=-1]))
            if count_b > count_w:
                self.main.window.update_info_box(0,"Black Win!!!")
            else:
                self.main.window.update_info_box(0,"White Win!!!")

    #评估当前棋盘的局势
    def evaluation(self,game): 
        '''
        综合考虑子的数量，气的数量，以及在棋盘的位置与距离
        max_influence和basis都是超参
        '''

        si = self.main.board_size

        board_array=np.zeros((si,si),dtype='int') #空位是0
        for one in game.grid:
            if one.player is not None:
                if one.player.name == 'black':
                    board_array[one.row-1,one.col-1] = 1
                elif one.player.name == 'white':
                    board_array[one.row-1,one.col-1] = -1

        si = si - 1

        eval_array=np.zeros(board_array.shape)
        #max_influence=int(min(board.width-1,board.height-1)/3.5) #相隔n子外的棋子影响力<1
        max_influence=2
        #stones_count=board_array.size-board_array[board_array[:]==0].size #计算落子总数
        #max_influence-=int(stones_count/40) #动态调整落子的势力影响范围
        #max_influence=max(max_influence,1)
        basis=2.5 #2.5个子就可以压迫一个对方子
        #黑子用正值势力表示，白子用负值势力表示
        for i in range(eval_array.shape[0]):
            for j in range(eval_array.shape[1]):
                for x in range(board_array.shape[0]):
                    for y in range(board_array.shape[1]):
                        if board_array[x,y]==0:
                            continue
                        #liberties=len(board.stones.get((x,y)).liberties) #考虑子的气的数量                        
                        L=abs(i-x)+abs(j-y)
                        #开始对棋盘分块
                        if (x<=3 or x>=si-3) and (y<=3 or y>=si-3): #4个角
                            if x<=3 and y<=3: # 左下角
                                if i<=x and j<=y: #在子的左下角
                                    max_influence=(x+y)/2+1
                                    basis=3.5
                            elif x<=3 and y>=si-3: # 右下角
                                if i<=x and j>=y: #在子的右下角
                                    max_influence=(x+si-y)/2+1
                                    basis=3.5
                            elif x>=si-3 and y>=si-3: # 右上角
                                if i>=x and j>=y: #在子的右上角
                                    max_influence=(si-x+si-y)/2+1
                                    basis=3.5
                            elif x>=si-3 and y<=3: # 左上角
                                if i>=x and j>=y: #在子的左上角
                                    max_influence=(si-x+y)/2+1
                                    basis=3.5
                            else:
                                pass

                        elif (x<=3 or x>=si-3) or (y<=3 or y>=si-3): #4个边
                            if x<=3: #down
                                if i<=x:
                                    max_influence=x
                                    basis=3
                            elif y>=si-3: #right
                                if j>=y:
                                    max_influence=si-y
                                    basis=3
                            elif x>=si-3: #up
                                if i>=x:
                                    max_influence=si-x
                                    basis=3
                            elif y<=3: #left
                                if j<=y:
                                    max_influence=y
                                    basis=3
                            else:
                                pass
                        else: #中心位置
                            pass #使用默认值
                        #influence=liberties*basis**(max_influence-L)*board_array[x,y]
                        influence=basis**(max_influence-L)*board_array[x,y]
                        eval_array[i,j]+=influence

        return eval_array

    def end_game(self,*args):     
        self.main.set_attribute("in game",False)
        self.main.window.find_interface("game elements").delete_self()
        self.main.window.set_attribute("background",self.main.colours["SECONDARY BLUE"])
        new_interface = MainMenu(self.main)
        self.__init__(self.main)