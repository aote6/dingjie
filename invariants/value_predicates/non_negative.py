"""
不变量：非负 (value >= 0)

已验证场景：
1. Inventory.add/remove 的 count 参数 (2026-07-25)
2. [待补充]

状态：候选中，还差一个独立场景
"""
import sympy as sp

def non_negative(value_symbol):
    return value_symbol >= 0
