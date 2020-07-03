#!/usr/bin/env python3
"""
__author__ = "Qihang_Guan"
__studentID__ = "320180939761"
__email__ = "guanqh8@lzu.edu.cn"
__version__ = "v1.0"
"""

from subprocess import Popen, check_output

def gitFileDynamics(filename, range, repo):
    cmd = ["git", "-stat", "--oneline", "--follow", range, filename]
    result = check_output(cmd, cwd=repo).decode("utf-8")
    print(result)

