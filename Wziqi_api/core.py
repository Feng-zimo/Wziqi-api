import copy
import time
import numpy as np
from collections import defaultdict
from functools import lru_cache

class WuziqiAPI:
    def __init__(self, rows=15, cols=15, search_depth=3):
        """
        初始化棋盘
        Args:
            rows: 行数
            cols: 列数
            search_depth: 搜索深度，默认为3
        """
        self.rows = rows
        self.cols = cols
        self.search_depth = search_depth
        self.directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 横、竖、斜、反斜
        
        # 创建方向向量的NumPy数组以提高性能
        self.direction_arrays = [np.array(d) for d in self.directions]
        
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
    
    def Runapi(self, QiPan, auto_add=True, search_depth=None):
        """
        AI计算下一步棋
        Args:
            QiPan: 当前棋盘状态
            auto_add: 是否自动将AI的落子添加到棋盘
            search_depth: 搜索深度，如果为None则使用默认值
        Returns:
            dict: AI的落子位置
        """
        start_time = time.time()
        
        # 使用指定的搜索深度或默认值
        depth = search_depth if search_depth is not None else self.search_depth
        
        # 解析棋盘
        board = self._parse_board(QiPan)
        
        # 寻找最佳移动
        best_move = self._find_best_move(board, depth)
        
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
        """将棋盘字典转换为NumPy数组"""
        # 使用NumPy数组提高性能
        board = np.zeros((self.rows, self.cols), dtype=np.int8)
        
        for pos, player in QiPan.items():
            row, col = map(int, pos.split(','))
            if player == "users":
                board[row-1, col-1] = 1  # 用户为1
            elif player == "api":
                board[row-1, col-1] = 2  # AI为2
            # 空位置保持为0
        
        return board
    
    def _find_best_move(self, board, depth):
        """寻找最佳移动"""
        # 如果是开局，选择中心附近
        if self._is_opening(board):
            return self._opening_move(board)
        
        # 检查是否有立即获胜的机会
        winning_move = self._find_winning_move_numpy(board, 2)  # 2代表AI
        if winning_move:
            return winning_move
        
        # 检查是否需要防守用户的获胜机会
        defensive_move = self._find_winning_move_numpy(board, 1)  # 1代表用户
        if defensive_move:
            return defensive_move
        
        # 使用Minimax算法搜索最佳移动
        best_score = float('-inf')
        best_move = None
        
        for move in self._get_possible_moves_numpy(board):
            row, col = move
            board[row-1, col-1] = 2  # AI落子
            score = self._minimax_numpy(board, depth - 1, False, float('-inf'), float('inf'))
            board[row-1, col-1] = 0  # 撤销落子
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def _is_opening(self, board):
        """判断是否是开局"""
        # 使用NumPy的sum提高性能
        move_count = np.sum(board != 0)
        return move_count <= 2
    
    def _opening_move(self, board):
        """开局策略"""
        center_row, center_col = self.rows // 2, self.cols // 2
        
        # 如果中心为空，选择中心
        if board[center_row, center_col] == 0:
            return (center_row + 1, center_col + 1)  # 转换为1索引
        
        # 否则选择中心周围的空位
        for dr, dc in [(0,1), (1,0), (0,-1), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]:
            r, c = center_row + dr, center_col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols and board[r, c] == 0:
                return (r + 1, c + 1)  # 转换为1索引
        
        return None
    
    def _find_winning_move_numpy(self, board, player):
        """寻找获胜移动或防守移动（NumPy优化版）"""
        for i in range(self.rows):
            for j in range(self.cols):
                if board[i, j] == 0:  # 空位置
                    # 检查如果在此落子是否能形成五连
                    board[i, j] = player
                    if self._check_win_numpy(board, i, j, player):
                        board[i, j] = 0
                        return (i + 1, j + 1)  # 转换为1索引
                    board[i, j] = 0
        return None
    
    def _minimax_numpy(self, board, depth, is_maximizing, alpha, beta):
        """Minimax算法与Alpha-Beta剪枝（NumPy优化版）"""
        if depth == 0 or self._is_game_over_numpy(board):
            return self._evaluate_board_numpy(board)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in self._get_possible_moves_numpy(board):
                row, col = move
                # 转换为0索引
                r, c = row - 1, col - 1
                board[r, c] = 2  # AI为2
                eval_score = self._minimax_numpy(board, depth - 1, False, alpha, beta)
                board[r, c] = 0  # 撤销
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self._get_possible_moves_numpy(board):
                row, col = move
                # 转换为0索引
                r, c = row - 1, col - 1
                board[r, c] = 1  # 用户为1
                eval_score = self._minimax_numpy(board, depth - 1, True, alpha, beta)
                board[r, c] = 0  # 撤销
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval
    
    def _get_possible_moves_numpy(self, board):
        """获取可能的移动位置（NumPy优化版）"""
        moves = set()
        
        # 找到所有非空位置
        non_empty = np.where(board != 0)
        non_empty_positions = list(zip(non_empty[0], non_empty[1]))
        
        # 在已有棋子周围2格范围内搜索空位
        for i, j in non_empty_positions:
            for di in range(-2, 3):
                for dj in range(-2, 3):
                    ni, nj = i + di, j + dj
                    if (0 <= ni < self.rows and 0 <= nj < self.cols and 
                        board[ni, nj] == 0):
                        moves.add((ni + 1, nj + 1))  # 转换为1索引
        
        # 如果没有找到可能的移动，返回中心位置
        if not moves:
            center = (self.rows // 2 + 1, self.cols // 2 + 1)
            # 检查中心是否为空
            center_r, center_c = center[0] - 1, center[1] - 1  # 转换为0索引检查
            if (0 <= center_r < self.rows and 0 <= center_c < self.cols and 
                board[center_r, center_c] == 0):
                moves.add(center)
            else:
                # 如果中心不为空，则找最近的空位
                empty_positions = np.where(board == 0)
                if len(empty_positions[0]) > 0:
                    moves.add((empty_positions[0][0] + 1, empty_positions[1][0] + 1))
        
        return list(moves)
    
    def _evaluate_board_numpy(self, board):
        """评估棋盘分数（NumPy优化版）"""
        score = 0
        
        # 评估AI的局势
        score += self._evaluate_player_numpy(board, 2) * 1.2  # AI稍微加强
        
        # 评估用户的局势
        score -= self._evaluate_player_numpy(board, 1)
        
        return score
    
    def _evaluate_player_numpy(self, board, player):
        """评估某个玩家的局势（NumPy优化版）"""
        score = 0
        
        # 检查所有方向
        for dr, dc in self.directions:
            # 向量化检查连续棋子
            for i in range(self.rows):
                for j in range(self.cols):
                    score += self._evaluate_position(board, i, j, dr, dc, player)
        
        return score
    
    def _evaluate_position(self, board, row, col, dr, dc, player):
        """评估特定位置和方向的得分"""
        score = 0
        count = 0
        blocks = 0
        empty_before = False
        empty_after = False
        
        # 向前检查5个位置
        for k in range(5):
            ni, nj = row + k * dr, col + k * dc
            if not (0 <= ni < self.rows and 0 <= nj < self.cols):
                blocks += 1
                break
            if board[ni, nj] == player:
                count += 1
            elif board[ni, nj] == 0:  # 空位置
                if k == 0:
                    empty_before = True
                else:
                    empty_after = True
                    break
            else:  # 对方棋子
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
        elif count == 1:
            if empty_before and empty_after:
                score += 1      # 单子价值
        
        # 检查更复杂的模式
        if count >= 3:
            # 检查跳棋模式
            pattern_score = self._check_patterns_numpy(board, row, col, dr, dc, player)
            score += pattern_score
            
        return score
    
    def _check_patterns_numpy(self, board, row, col, dr, dc, player):
        """检查特殊棋型模式（NumPy优化版）"""
        score = 0
        pattern = []
        
        # 获取5个位置的棋子状态
        for k in range(5):
            ni, nj = row + k * dr, col + k * dc
            if not (0 <= ni < self.rows and 0 <= nj < self.cols):
                pattern.append(None)
            else:
                pattern.append(board[ni, nj])
        
        # 检查跳四等模式
        player_count = pattern.count(player)
        empty_count = pattern.count(0)
        
        if player_count == 3 and empty_count == 2:
            score += 50  # 跳三
        elif player_count == 2 and empty_count == 3:
            score += 20  # 跳二
            
        return score
    
    def _check_win_numpy(self, board, row, col, player):
        """检查是否获胜（NumPy优化版）"""
        for dr, dc in self.directions:
            count = 1
            
            # 正向检查
            for k in range(1, 5):
                ni, nj = row + k * dr, col + k * dc
                if not (0 <= ni < self.rows and 0 <= nj < self.cols) or board[ni, nj] != player:
                    break
                count += 1
            
            # 反向检查
            for k in range(1, 5):
                ni, nj = row - k * dr, col - k * dc
                if not (0 <= ni < self.rows and 0 <= nj < self.cols) or board[ni, nj] != player:
                    break
                count += 1
            
            if count >= 5:
                return True
        
        return False
    
    def _is_game_over_numpy(self, board):
        """检查游戏是否结束（NumPy优化版）"""
        # 检查所有位置是否有五连
        for i in range(self.rows):
            for j in range(self.cols):
                if board[i, j] != 0:
                    if (self._check_win_numpy(board, i, j, 1) or 
                        self._check_win_numpy(board, i, j, 2)):
                        return True
        
        # 检查是否棋盘已满
        if np.sum(board == 0) == 0:
            return True
        
        return False

# 使用示例
def init(rows=15, cols=15, search_depth=3):
    """初始化函数"""
    return WuziqiAPI(rows, cols, search_depth)

def Runapi(QiPan, auto_add=True, search_depth=None):
    """运行API的便捷函数"""
    api = WuziqiAPI()
    return api.Runapi(QiPan, auto_add, search_depth)