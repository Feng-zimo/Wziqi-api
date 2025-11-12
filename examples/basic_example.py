"""
基础使用示例
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Wziqi_api import init, Runapi

def basic_example():
    """基础使用示例"""
    print("=== 五子棋AI基础使用示例 ===")
    
    # 初始化15×15棋盘
    QiPan = init(15, 15).init_board()
    
    # 显示初始棋盘状态
    print("初始棋盘:")
    print_board(QiPan)
    
    # 用户先行，放在中心位置
    QiPan["8,8"] = "users"
    print("\n用户在(8,8)落子后:")
    print_board(QiPan)
    
    # AI响应（自动更新棋盘）
    print("\nAI思考中...")
    ai_move = Runapi(QiPan, auto_add=True)
    print(f"AI落子: {ai_move}")
    print_board(QiPan)
    
    # 继续对弈
    QiPan["7,7"] = "users"
    print("\n用户在(7,7)落子后:")
    print_board(QiPan)
    
    print("\nAI再次思考中...")
    next_ai_move = Runapi(QiPan, auto_add=True)
    print(f"AI落子: {next_ai_move}")
    print_board(QiPan)

def print_board(QiPan):
    """打印棋盘状态"""
    print("  ", end="")
    for j in range(1, 16):
        print(f"{j:2d}", end=" ")
    print()
    
    for i in range(1, 16):
        print(f"{i:2d}", end=" ")
        for j in range(1, 16):
            if QiPan[f"{i},{j}"] == "users":
                print("○", end="  ")
            elif QiPan[f"{i},{j}"] == "api":
                print("●", end="  ")
            else:
                print("﹢", end="  ")
        print()

if __name__ == "__main__":
    basic_example()