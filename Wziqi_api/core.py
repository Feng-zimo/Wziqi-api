import copy
import time
from collections import defaultdict

class WuziqiAPI:
    def __init__(self, rows=15, cols=15):
        """
        初始化棋盘
        Args:
            rows: 行数
            cols: 列数
        """
        self.rows = rows
        self.cols = cols
        self.directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 横、竖、斜、反斜
        
    def init_board(self):
        """
        创建初始棋盘字典
        Returns:
            QiPan: 初始化后的棋盘字典
        """
        QiPan = {}
        for i in range(1, self.rows + 1):
            for j in range(1, self.cols + 1):
                QiPan[f"{i},{j}"] = "None"
        return QiPan
    
    def Runapi(self, QiPan, auto_add=True):
        """
        AI计算下一步棋
        Args:
            QiPan: 当前棋盘状态
            auto_add: 是否自动将AI的落子添加到棋盘
        Returns:
            dict: AI的落子位置
        """
        start_time = time.time()
        
        # 解析棋盘
        board = self._parse_board(QiPan)
        
        # 寻找最佳移动
        best_move = self._find_best_move(board)
        
        if best_move:
            row, col = best_move
            result = {f"{row},{col}": "api"}
            
            # 如果auto_add为True，自动更新棋盘
            if auto_add:
                QiPan[f"{row},{col}"] = "api"
            
            print(f"AI思考时间: {time.time() - start_time:.2f}秒")
            return result
        else:
            return {}
    
    def _parse_board(self, QiPan):
        """将棋盘字典转换为二维数组"""
        board = [['' for _ in range(self.cols)] for _ in range(self.rows)]
        
        for pos, player in QiPan.items():
            row, col = map(int, pos.split(','))
            if player == "users":
                board[row-1][col-1] = 'O'  # 用户为O
            elif player == "api":
                board[row-1][col-1] = 'X'  # AI为X
            else:
                board[row-1][col-1] = ''   # 空位置
        
        return board
    
    def _find_best_move(self, board):
        """寻找最佳移动"""
        # 如果是开局，选择中心附近
        if self._is_opening(board):
            return self._opening_move(board)
        
        # 检查是否有立即获胜的机会
        winning_move = self._find_winning_move(board, 'X')
        if winning_move:
            return winning_move
        
        # 检查是否需要防守用户的获胜机会
        defensive_move = self._find_winning_move(board, 'O')
        if defensive_move:
            return defensive_move
        
        # 使用Minimax算法搜索最佳移动
        best_score = float('-inf')
        best_move = None
        depth = 3  # 搜索深度，可根据需要调整
        
        for move in self._get_possible_moves(board):
            row, col = move
            board[row][col] = 'X'
            score = self._minimax(board, depth - 1, False, float('-inf'), float('inf'))
            board[row][col] = ''
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def _is_opening(self, board):
        """判断是否是开局"""
        move_count = sum(1 for i in range(self.rows) for j in range(self.cols) if board[i][j])
        return move_count <= 2
    
    def _opening_move(self, board):
        """开局策略"""
        center_row, center_col = self.rows // 2, self.cols // 2
        
        # 如果中心为空，选择中心
        if not board[center_row][center_col]:
            return (center_row, center_col)
        
        # 否则选择中心周围的空位
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]:
            r, c = center_row + dr, center_col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols and not board[r][c]:
                return (r, c)
        
        return None
    
    def _find_winning_move(self, board, player):
        """寻找获胜移动或防守移动"""
        for i in range(self.rows):
            for j in range(self.cols):
                if not board[i][j]:
                    # 检查如果在此落子是否能形成五连
                    board[i][j] = player
                    if self._check_win(board, i, j, player):
                        board[i][j] = ''
                        return (i, j)
                    board[i][j] = ''
        return None
    
    def _minimax(self, board, depth, is_maximizing, alpha, beta):
        """Minimax算法与Alpha-Beta剪枝"""
        if depth == 0 or self._is_game_over(board):
            return self._evaluate_board(board)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in self._get_possible_moves(board):
                row, col = move
                board[row][col] = 'X'
                eval_score = self._minimax(board, depth - 1, False, alpha, beta)
                board[row][col] = ''
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self._get_possible_moves(board):
                row, col = move
                board[row][col] = 'O'
                eval_score = self._minimax(board, depth - 1, True, alpha, beta)
                board[row][col] = ''
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    
    def _get_possible_moves(self, board):
        """获取可能的移动位置（只在已有棋子的周围搜索）"""
        moves = set()
        
        for i in range(self.rows):
            for j in range(self.cols):
                if board[i][j]:
                    # 在已有棋子周围2格范围内搜索空位
                    for di in range(-2, 3):
                        for dj in range(-2, 3):
                            ni, nj = i + di, j + dj
                            if (0 <= ni < self.rows and 0 <= nj < self.cols and 
                                not board[ni][nj] and (ni, nj) not in moves):
                                moves.add((ni, nj))
        
        # 如果没有找到可能的移动，返回中心位置
        if not moves:
            center = (self.rows // 2, self.cols // 2)
            if not board[center[0]][center[1]]:
                moves.add(center)
        
        return list(moves)
    
    def _evaluate_board(self, board):
        """评估棋盘分数"""
        score = 0
        
        # 评估AI的局势
        score += self._evaluate_player(board, 'X') * 10
        
        # 评估用户的局势
        score -= self._evaluate_player(board, 'O') * 10
        
        return score
    
    def _evaluate_player(self, board, player):
        """评估某个玩家的局势"""
        score = 0
        
        # 检查所有方向
        for dr, dc in self.directions:
            for i in range(self.rows):
                for j in range(self.cols):
                    # 检查连续棋子
                    count = 0
                    blocks = 0
                    
                    # 向前检查
                    for k in range(5):
                        ni, nj = i + k * dr, j + k * dc
                        if not (0 <= ni < self.rows and 0 <= nj < self.cols):
                            blocks += 1
                            break
                        if board[ni][nj] == player:
                            count += 1
                        elif board[ni][nj]:
                            blocks += 1
                            break
                    
                    # 根据连续棋子和阻挡情况评分
                    if count == 5:
                        score += 100000  # 五连
                    elif count == 4:
                        if blocks == 0:
                            score += 10000  # 活四
                        elif blocks == 1:
                            score += 1000   # 冲四
                    elif count == 3:
                        if blocks == 0:
                            score += 100    # 活三
                        elif blocks == 1:
                            score += 10     # 冲三
                    elif count == 2:
                        if blocks == 0:
                            score += 5      # 活二
        
        return score
    
    def _check_win(self, board, row, col, player):
        """检查是否获胜"""
        for dr, dc in self.directions:
            count = 1
            
            # 正向检查
            for k in range(1, 5):
                ni, nj = row + k * dr, col + k * dc
                if not (0 <= ni < self.rows and 0 <= nj < self.cols) or board[ni][nj] != player:
                    break
                count += 1
            
            # 反向检查
            for k in range(1, 5):
                ni, nj = row - k * dr, col - k * dc
                if not (0 <= ni < self.rows and 0 <= nj < self.cols) or board[ni][nj] != player:
                    break
                count += 1
            
            if count >= 5:
                return True
        
        return False
    
    def _is_game_over(self, board):
        """检查游戏是否结束"""
        # 检查所有位置是否有五连
        for i in range(self.rows):
            for j in range(self.cols):
                if board[i][j]:
                    if (self._check_win(board, i, j, 'X') or 
                        self._check_win(board, i, j, 'O')):
                        return True
        
        # 检查是否棋盘已满
        for i in range(self.rows):
            for j in range(self.cols):
                if not board[i][j]:
                    return False
        
        return True

# 使用示例
def init(rows=15, cols=15):
    """初始化函数"""
    return WuziqiAPI(rows, cols)

def Runapi(QiPan, auto_add=True):
    """运行API的便捷函数"""
    api = WuziqiAPI()
    return api.Runapi(QiPan, auto_add)