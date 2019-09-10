#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Eric Winn
# @Email          : eng.eric.winn@gmail.com
# @Time           : 19-9-3 下午9:18
# @Version        : 1.0
# @File           : run_server
# @Software       : PyCharm

import sys
import subprocess

if __name__ == '__main__':
    subprocess.call('python3 cms start all', shell=True,
                    stdin=sys.stdin, stdout=sys.stdout)
