"""
Wuziqi-API 测试文件
测试AI响应时间和自我对抗表现
使用tkinter GUI显示结果
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import threading
from wuziqi_api import init, Runapi

class WuziqiTester:
    """五子棋AI测试器"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("五子棋AI测试工具")
        self.root.geometry("800x600")
        
        # 测试结果存储
        self.response_times = []
        self.self_play_results = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 响应时间测试区域
        ttk.Label(main_frame, text="响应时间测试", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        response_frame = ttk.LabelFrame(main_frame, text="单次响应测试", padding="10")
        response_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(response_frame, text="测试单次AI响应时间", 
                  command=self.test_single_response).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(response_frame, text="批量测试响应时间(10次)", 
                  command=lambda: self.test_batch_response(10)).grid(row=0, column=1)
        
        # 自我对抗测试区域
        ttk.Label(main_frame, text="AI自我对抗测试", font=('Arial', 12, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=(10, 10))
        
        self_play_frame = ttk.LabelFrame(main_frame, text="自我对抗设置", padding="10")
        self_play_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(self_play_frame, text="最大步数:").grid(row=0, column=0, padx=(0, 5))
        self.max_steps = tk.IntVar(value=50)
        ttk.Entry(self_play_frame, textvariable=self.max_steps, width=10).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(self_play_frame, text="开始自我对抗测试", 
                  command=self.start_self_play).grid(row=0, column=2)
        
        # 结果显示区域
        results_frame = ttk.LabelFrame(main_frame, text="测试结果", padding="10")
        results_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # 文本结果显示
        self.results_text = scrolledtext.ScrolledText(results_frame, width=80, height=20)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 配置网格权重
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
    
    def log_message(self, message):
        """在结果区域添加消息"""
        self.results_text.insert(tk.END, f"{message}\n")
        self.results_text.see(tk.END)
        self.root.update()
    
    def test_single_response(self):
        """测试单次AI响应时间"""
        def run_test():
            self.progress.start()
            self.log_message("开始单次响应时间测试...")
            
            try:
                # 初始化棋盘
                api = init(15, 15)
                board = api.init_board()
                
                # 添加一些初始棋子模拟真实对局
                board["8,8"] = "users"
                board["7,7"] = "users"
                board["9,9"] = "api"
                
                start_time = time.time()
                ai_move = Runapi(board, auto_add=False)
                end_time = time.time()
                
                response_time = end_time - start_time
                self.response_times.append(response_time)
                
                self.log_message(f"单次响应时间: {response_time:.3f} 秒")
                self.log_message(f"AI建议落子: {ai_move}")
                self.log_message("-" * 50)
                
            except Exception as e:
                self.log_message(f"测试出错: {e}")
            finally:
                self.progress.stop()
        
        threading.Thread(target=run_test).start()
    
    def test_batch_response(self, num_tests):
        """批量测试响应时间"""
        def run_test():
            self.progress.start()
            self.log_message(f"开始批量响应时间测试 ({num_tests} 次)...")
            
            try:
                times = []
                api = init(15, 15)
                
                for i in range(num_tests):
                    board = api.init_board()
                    
                    # 创建不同的初始局面
                    if i % 3 == 0:
                        board["8,8"] = "users"
                        board["7,7"] = "api"
                    elif i % 3 == 1:
                        board["7,7"] = "users"
                        board["6,6"] = "users"
                        board["8,8"] = "api"
                    else:
                        board["8,8"] = "users"
                        board["9,9"] = "users"
                        board["7,7"] = "api"
                        board["6,6"] = "api"
                    
                    start_time = time.time()
                    Runapi(board, auto_add=False)
                    end_time = time.time()
                    
                    response_time = end_time - start_time
                    times.append(response_time)
                    self.response_times.append(response_time)
                    
                    self.log_message(f"测试 {i+1}/{num_tests}: {response_time:.3f} 秒")
                
                # 统计结果
                avg_time = sum(times) / len(times)
                max_time = max(times)
                min_time = min(times)
                
                self.log_message("\n批量测试结果统计:")
                self.log_message(f"平均响应时间: {avg_time:.3f} 秒")
                self.log_message(f"最快响应时间: {min_time:.3f} 秒")
                self.log_message(f"最慢响应时间: {max_time:.3f} 秒")
                self.log_message("=" * 50)
                
            except Exception as e:
                self.log_message(f"批量测试出错: {e}")
            finally:
                self.progress.stop()
        
        threading.Thread(target=run_test).start()
    
    def start_self_play(self):
        """开始AI自我对抗测试"""
        def run_self_play():
            self.progress.start()
            max_steps = self.max_steps.get()
            
            self.log_message(f"开始AI自我对抗测试 (最大步数: {max_steps})...")
            self.log_message("○: AI1 (先手)  ×: AI2 (后手)")
            self.log_message("-" * 50)
            
            try:
                # 初始化棋盘
                api = init(15, 15)
                board = api.init_board()
                
                current_player = "AI1"  # AI1 先手
                steps = 0
                game_over = False
                
                start_time = time.time()
                
                while steps < max_steps and not game_over:
                    steps += 1
                    
                    # 记录当前棋盘状态
                    occupied_positions = {k: v for k, v in board.items() if v != "None"}
                    self.log_message(f"第 {steps} 步 - {current_player} 思考中...")
                    self.log_message(f"当前棋盘棋子数: {len(occupied_positions)}")
                    
                    # AI 落子
                    move_start = time.time()
                    ai_move = Runapi(board, auto_add=True)
                    move_time = time.time() - move_start
                    
                    if ai_move:
                        move_pos = list(ai_move.keys())[0]
                        self.log_message(f"{current_player} 落子: {move_pos} (思考: {move_time:.2f}s)")
                        
                        # 切换玩家
                        current_player = "AI2" if current_player == "AI1" else "AI1"
                        
                        # 简单检查游戏是否结束（这里可以扩展真正的获胜检查）
                        if steps >= 5 and self.check_simple_win_condition(board, move_pos):
                            game_over = True
                            winner = "AI2" if current_player == "AI1" else "AI1"
                            self.log_message(f"游戏结束! 获胜方: {winner}")
                    else:
                        self.log_message(f"{current_player} 无法落子，游戏结束")
                        game_over = True
                    
                    self.log_message("")  # 空行分隔
                
                total_time = time.time() - start_time
                
                # 记录结果
                result = {
                    "total_steps": steps,
                    "total_time": total_time,
                    "avg_time_per_move": total_time / steps if steps > 0 else 0,
                    "winner": "平局" if not game_over else winner,
                    "max_steps_reached": steps >= max_steps
                }
                
                self.self_play_results.append(result)
                
                self.log_message("\n自我对抗测试完成!")
                self.log_message(f"总步数: {steps}")
                self.log_message(f"总时间: {total_time:.2f} 秒")
                self.log_message(f"平均每步时间: {total_time/steps:.2f} 秒" if steps > 0 else "无步数")
                self.log_message(f"结果: {result['winner']}")
                self.log_message("=" * 50)
                
            except Exception as e:
                self.log_message(f"自我对抗测试出错: {e}")
            finally:
                self.progress.stop()
        
        threading.Thread(target=run_self_play).start()
    
    def check_simple_win_condition(self, board, last_move):
        """
        简单的获胜条件检查（示例用）
        在实际应用中，你应该使用core.py中的完整获胜检查
        """
        # 这里只是一个简单的示例
        # 在实际使用中，你应该调用core.py中的获胜检查函数
        try:
            # 模拟获胜检查 - 在实际中应该调用你的获胜检查逻辑
            occupied_count = sum(1 for v in board.values() if v != "None")
            return occupied_count >= 10  # 简单示例：当棋子达到一定数量时结束
        except:
            return False
    
    def show_statistics(self):
        """显示统计信息"""
        if not self.response_times and not self.self_play_results:
            messagebox.showinfo("统计信息", "暂无测试数据")
            return
        
        stats_window = tk.Toplevel(self.root)
        stats_window.title("测试统计信息")
        stats_window.geometry("400x300")
        
        stats_text = scrolledtext.ScrolledText(stats_window, width=50, height=15)
        stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 响应时间统计
        if self.response_times:
            stats_text.insert(tk.END, "响应时间统计:\n")
            stats_text.insert(tk.END, f"测试次数: {len(self.response_times)}\n")
            stats_text.insert(tk.END, f"平均时间: {sum(self.response_times)/len(self.response_times):.3f}秒\n")
            stats_text.insert(tk.END, f"最短时间: {min(self.response_times):.3f}秒\n")
            stats_text.insert(tk.END, f"最长时间: {max(self.response_times):.3f}秒\n\n")
        
        # 自我对抗统计
        if self.self_play_results:
            stats_text.insert(tk.END, "自我对抗统计:\n")
            for i, result in enumerate(self.self_play_results, 1):
                stats_text.insert(tk.END, f"对局 {i}:\n")
                stats_text.insert(tk.END, f"  步数: {result['total_steps']}\n")
                stats_text.insert(tk.END, f"  结果: {result['winner']}\n")
                stats_text.insert(tk.END, f"  平均步时: {result['avg_time_per_move']:.2f}秒\n\n")
    
    def run(self):
        """运行测试器"""
        # 添加统计按钮
        ttk.Button(self.root, text="查看统计", command=self.show_statistics).grid(row=1, column=0, pady=10)
        
        self.log_message("五子棋AI测试工具已启动")
        self.log_message("请选择要进行的测试类型")
        self.log_message("=" * 50)
        
        self.root.mainloop()

def main():
    """主函数"""
    tester = WuziqiTester()
    tester.run()

if __name__ == "__main__":
    main()