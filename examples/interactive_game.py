"""
交互式游戏示例
提供一个简单的命令行界面与AI对弈
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import sys
from Wziqi_api import init, Runapi

class WuziqiGame:
    """五子棋交互式游戏"""
    
    def __init__(self, board_size=15, ai_depth=3):
        self.board_size = board_size
        self.ai_depth = ai_depth
        self.api = init(board_size, board_size, ai_depth)
        self.QiPan = self.api.init_board()
        self.game_over = False
        self.winner = None
    
    def play(self):
        """开始游戏"""
        print("=== 五子棋人机对弈 ===")
        print("您执白子(○)，AI执黑子(●)")
        print("输入坐标格式: 行,列 (例如: 8,8)")
        print("输入 'quit' 退出游戏")
        print("输入 'help' 显示帮助")
        
        # 用户先手
        user_turn = True
        
        while not self.game_over:
            self.display_board()
            
            if user_turn:
                self.user_move()
            else:
                self.ai_move()
            
            user_turn = not user_turn
        
        self.display_board()
        if self.winner:
            print(f"\n游戏结束! {self.winner} 获胜!")
        else:
            print("\n游戏结束! 平局!")
    
    def display_board(self):
        """显示棋盘"""
        print("\n  ", end="")
        for j in range(1, self.board_size + 1):
            print(f"{j:2d}", end=" ")
        print()
        
        for i in range(1, self.board_size + 1):
            print(f"{i:2d}", end=" ")
            for j in range(1, self.board_size + 1):
                if self.QiPan[f"{i},{j}"] == "users":
                    print("○", end="  ")
                elif self.QiPan[f"{i},{j}"] == "api":
                    print("●", end="  ")
                else:
                    print("﹢", end="  ")
            print()
    
    def user_move(self):
        """用户移动"""
        while True:
            try:
                user_input = input("\n请输入您的落子位置 (行,列): ").strip()
                
                if user_input.lower() == 'quit':
                    print("感谢游戏!")
                    sys.exit(0)
                
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                # 解析输入
                row, col = map(int, user_input.split(','))
                
                # 检查坐标有效性
                if not (1 <= row <= self.board_size and 1 <= col <= self.board_size):
                    print(f"坐标必须在 1-{self.board_size} 范围内!")
                    continue
                
                # 检查位置是否为空
                if self.QiPan[f"{row},{col}"] != "None":
                    print("该位置已有棋子，请选择其他位置!")
                    continue
                
                # 落子
                self.QiPan[f"{row},{col}"] = "users"
                
                # 检查是否获胜
                if self.check_win(row, col, "users"):
                    self.game_over = True
                    self.winner = "您"
                
                # 检查是否平局
                if self.is_board_full():
                    self.game_over = True
                
                break
                
            except ValueError:
                print("输入格式错误，请输入: 行,列 (例如: 8,8)")
            except KeyboardInterrupt:
                print("\n\n游戏退出!")
                sys.exit(0)
    
    def ai_move(self):
        """AI移动"""
        print("\nAI思考中...")
        ai_move = self.api.Runapi(self.QiPan, auto_add=False, search_depth=self.ai_depth)
        
        if ai_move:
            pos = list(ai_move.keys())[0]
            row, col = map(int, pos.split(','))
            self.QiPan[pos] = "api"
            print(f"AI在({row},{col})落子")
            
            # 检查是否获胜
            if self.check_win(row, col, "api"):
                self.game_over = True
                self.winner = "AI"
            
            # 检查是否平局
            if self.is_board_full():
                self.game_over = True
        else:
            print("AI无法落子，游戏结束!")
            self.game_over = True
    
    def check_win(self, row, col, player):
        """检查是否获胜"""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 横、竖、斜、反斜
        
        for dr, dc in directions:
            count = 1
            
            # 正向检查
            for k in range(1, 5):
                ni, nj = row + k * dr, col + k * dc
                if not (1 <= ni <= self.board_size and 1 <= nj <= self.board_size) or \
                   self.QiPan[f"{ni},{nj}"] != player:
                    break
                count += 1
            
            # 反向检查
            for k in range(1, 5):
                ni, nj = row - k * dr, col - k * dc
                if not (1 <= ni <= self.board_size and 1 <= nj <= self.board_size) or \
                   self.QiPan[f"{ni},{nj}"] != player:
                    break
                count += 1
            
            if count >= 5:
                return True
        
        return False
    
    def is_board_full(self):
        """检查棋盘是否已满"""
        for i in range(1, self.board_size + 1):
            for j in range(1, self.board_size + 1):
                if self.QiPan[f"{i},{j}"] == "None":
                    return False
        return True
    
    def show_help(self):
        """显示帮助信息"""
        print("\n=== 帮助信息 ===")
        print("1. 游戏目标: 在15×15的棋盘上率先形成五子连线(横、竖、斜均可)")
        print("2. 输入格式: 行号,列号 (例如: 8,8 表示第8行第8列)")
        print("3. 您执白子(○)，AI执黑子(●)")
        print("4. 命令:")
        print("   - quit: 退出游戏")
        print("   - help: 显示此帮助信息")

def main():
    """主函数"""
    print("选择游戏难度:")
    print("1. 简单 (搜索深度2)")
    print("2. 中等 (搜索深度3)")
    print("3. 困难 (搜索深度4)")
    
    while True:
        try:
            choice = int(input("请选择难度 (1-3): "))
            if choice == 1:
                depth = 2
                break
            elif choice == 2:
                depth = 3
                break
            elif choice == 3:
                depth = 4
                break
            else:
                print("请输入1-3之间的数字!")
        except ValueError:
            print("请输入有效的数字!")
    
    game = WuziqiGame(board_size=15, ai_depth=depth)
    game.play()

if __name__ == "__main__":
    main()