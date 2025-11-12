"""
性能测试示例
测试不同搜索深度下的AI性能表现
"""

import sys
import os
import time
import statistics

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from Wziqi_api import init, Runapi

def performance_test():
    """性能测试"""
    print("=== 五子棋AI性能测试 ===")
    
    # 测试不同搜索深度的性能
    depths = [2, 3, 4, 5]
    test_cases = generate_test_cases()
    
    print(f"{'深度':<6} {'平均时间(秒)':<12} {'最小时间(秒)':<12} {'最大时间(秒)':<12} {'测试次数':<8}")
    print("-" * 60)
    
    for depth in depths:
        times = []
        
        for case in test_cases:
            # 初始化棋盘并设置测试局面
            QiPan = init(15, 15).init_board()
            for pos, player in case.items():
                QiPan[pos] = player
            
            # 测试AI响应时间
            start_time = time.time()
            Runapi(QiPan, auto_add=False, search_depth=depth)
            end_time = time.time()
            
            times.append(end_time - start_time)
        
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"{depth:<6} {avg_time:<12.3f} {min_time:<12.3f} {max_time:<12.3f} {len(times):<8}")
    
    print("\n测试完成!")

def generate_test_cases():
    """生成测试用例"""
    test_cases = []
    
    # 测试用例1: 开局
    case1 = {"8,8": "users"}
    test_cases.append(case1)
    
    # 测试用例2: 中期局面
    case2 = {
        "8,8": "users",
        "8,9": "api",
        "9,8": "users",
        "9,9": "api",
        "10,8": "users"
    }
    test_cases.append(case2)
    
    # 测试用例3: 复杂局面
    case3 = {
        "8,8": "users",
        "8,9": "api",
        "9,8": "users",
        "9,9": "api",
        "10,8": "users",
        "10,9": "api",
        "7,8": "users",
        "7,9": "api",
        "8,7": "users"
    }
    test_cases.append(case3)
    
    # 测试用例4: 残局
    case4 = {
        "1,1": "users",
        "1,2": "api",
        "2,1": "users",
        "2,2": "api",
        "3,1": "users",
        "3,2": "api",
        "4,1": "users"
    }
    test_cases.append(case4)
    
    return test_cases

def speed_vs_quality():
    """速度与质量权衡测试"""
    print("\n=== 速度与质量权衡测试 ===")
    
    # 创建一个相对复杂的局面
    QiPan = init(15, 15).init_board()
    positions = [
        ("8,8", "users"),
        ("8,9", "api"),
        ("9,8", "users"),
        ("9,9", "api"),
        ("10,8", "users"),
        ("10,9", "api"),
        ("7,8", "users"),
        ("7,9", "api")
    ]
    
    for pos, player in positions:
        QiPan[pos] = player
    
    print("测试局面:")
    print_mini_board(QiPan)
    
    print(f"\n{'深度':<6} {'响应时间(秒)':<12} {'推荐着法':<15}")
    print("-" * 35)
    
    for depth in range(2, 6):
        start_time = time.time()
        move = Runapi(QiPan, auto_add=False, search_depth=depth)
        response_time = time.time() - start_time
        
        move_str = list(move.keys())[0] if move else "无"
        print(f"{depth:<6} {response_time:<12.3f} {move_str:<15}")

def print_mini_board(QiPan):
    """迷你打印棋盘状态"""
    print("    ", end="")
    for j in range(6, 12):
        print(f"{j:2d}", end=" ")
    print()
    
    for i in range(6, 12):
        print(f"{i:2d}  ", end="")
        for j in range(6, 12):
            if QiPan[f"{i},{j}"] == "users":
                print("○", end=" ")
            elif QiPan[f"{i},{j}"] == "api":
                print("●", end=" ")
            else:
                print("﹢", end=" ")
        print()

if __name__ == "__main__":
    performance_test()
    speed_vs_quality()