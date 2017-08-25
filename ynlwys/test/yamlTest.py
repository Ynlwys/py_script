# -*- coding: utf-8 -*

"""
    author: Ynlwys

    目的:
        用于测试ymal 文件
"""

import yaml

obj = yaml.load("""
    - Hesperiidae:
        - s:0
    - Papilionidae:
        - s:1
    - Apatelodidae:
        - s:2
    - Epiplemidae:
        - s:3
""")

print obj
