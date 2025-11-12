"""
高级使用示例
展示如何自定义AI难度和其他高级功能
"""

import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Wziqi_api import init, Runapi

def advanced_example():
    """高级使用示例"""
    print("=== 五子棋AI高级使用示例 ===")
    
    # 1. 不同难度级别的AI
    print("\n1. 不同难度级别的AI:")
    QiPan = init(15, 15).init_board()
    
    # 用户先手
    QiPan["8,8"] = "users"
    print("用户在(8,8)落子")
    
    # 初级AI (搜索深度2)
    print("\n初级AI (搜索深度2) 思考中...")
    start = time.time()
    move1 = Runapi(QiPan, auto_add=False, search_depth=2)
    time1 = time.time() - start
    print(f"初级AI建议落子: {move1}, 用时: {time1:.2f}秒")
    
    # 中级AI (搜索深度3，也是默认值)
    print("\n中级AI (搜索深度3) 思考中...")
    start = time.time()
    move2 = Runapi(QiPan, auto_add=False, search_depth=3)
    time2 = time.time() - start
    print(f"中级AI建议落子: {move2}, 用时: {time2:.2f}秒")
    
    # 高级AI (搜索深度4)
    print("\n高级AI (搜索深度4) 思考中...")
    start = time.time()
    move3 = Runapi(QiPan, auto_add=False, search_depth=4)
    time3 = time.time() - start
    print(f"高级AI建议落子: {move3}, 用时: {time3:.2f}秒")
    
    # 2. 自定义AI实例
    print("\n\n2. 自定义AI实例:")
    # 创建一个搜索深度为5的强力AI
    strong_ai = init(15, 15, search_depth=5)
    QiPan2 = strong_ai.init_board()
    
    # 设置一个复杂的局面
    QiPan2["8,8"] = "users"
    QiPan2["8,9"] = "api"
    QiPan2["9,8"] = "users"
    QiPan2["9,9"] = "api"
    QiPan2["10,8"] = "users"
    
    print("复杂局面:")
    print_compact_board(QiPan2)
    
    print("\n强力AI思考中...")
    start = time.time()
    strong_move = strong_ai.Runapi(QiPan2, auto_add=True, search_depth=5)
    strong_time = time.time() - start
    print(f"强力AI落子: {strong_move}, 用时: {strong_time:.2f}秒")
    print("落子后局面:")
    print_compact_board(QiPan2)

def print_compact_board(QiPan):
    """紧凑打印棋盘状态"""
    print("   ", end="")
    for j in range(1, 16):
        print(f"{j:2d}", end=" ")
    print()
    
    for i in range(1, 16):
        print(f"{i:2d} ", end="")
        for j in range(1, 16):
            if QiPan[f"{i},{j}"] == "users":
                print("○", end=" ")
            elif QiPan[f"{i},{j}"] == "api":
                print("●", end=" ")
            else:
                print("﹢", end=" ")
        print()

if __name__ == "__main__":
    advanced_example()