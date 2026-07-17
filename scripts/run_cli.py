#!/usr/bin/env python3
"""
便捷脚本：快速运行 CLI 工作流
用法: python scripts/run_cli.py "你的问题"
"""

import subprocess
import sys


def main():
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "什么是LangGraph？"
    cmd = ["python", "-m", "src.main", query]
    subprocess.run(cmd, cwd="..")


if __name__ == "__main__":
    main()
