from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    # 基本信息
    name="wuziqi-api",
    version="1.0.0",
    author="Feng-zimo",
    author_email="feng_to_zhang@163.com",  # 请替换为你的邮箱
    description="一个高性能的五子棋AI API库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # 项目URL
    url="https://github.com/Feng-zimo/Wziqi-api",
    
    # 包发现
    packages=find_packages(),
    
    # 分类信息
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    
    # Python版本要求
    python_requires=">=3.6",
    
    # 依赖包
    install_requires=[
        "numpy>=1.21.0",      # 数值计算，用于优化算法性能
        "colorama>=0.4.4",    # 终端颜色输出，用于美化界面
        "click>=8.0.0",       # 命令行界面工具
    ],
    
    # 项目关键词
    keywords="wuziqi, gomoku, ai, game, python",
    
    # 许可证
    license="MIT",
    
    # 入口点（如果需要命令行工具）
    # entry_points={
    #     'console_scripts': [
    #         'wuziqi=wuziqi_api.cli:main',
    #     ],
    # },
)