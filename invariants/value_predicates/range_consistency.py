"""
不变量：范围一致性 (a <= b)

已验证场景：
1. EquipmentInstance.damage_min <= damage_max (unbounded/equipment.py, 2026-07-25)
2. 灵体 KeyModel 百分比坐标：0 <= percentX/Y/W/H <= 100 且 W > 0, H > 0 (lingti, 2026-07-25)

机制：线性算术谓词，直接复用 core.py/core2.py 现有判定
"""
import sympy as sp


def lower_bound(value_symbol, bound):
    """value >= bound"""
    return value_symbol >= bound


def upper_bound(value_symbol, bound):
    """value <= bound"""
    return value_symbol <= bound


def value_range(value_symbol, low, high):
    """low <= value <= high"""
    return sp.And(value_symbol >= low, value_symbol <= high)


def pairwise_le(a_symbol, b_symbol):
    """a <= b（两个不同变量之间的顺序约束）"""
    return a_symbol <= b_symbol
