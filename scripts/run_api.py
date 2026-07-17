#!/usr/bin/env python3
"""
便捷脚本：启动 API 服务
用法: python scripts/run_api.py
"""

import subprocess
import sys


def main():
    cmd = [
        "uvicorn",
        "src.api:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload",
    ]
    subprocess.run(cmd)


if __name__ == "__main__":
    main()
