#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定界 × 无界：背包操作契约检查
对 inventory.py 的 add / remove 做编译期契约验证
"""
import sympy as sp


def check_add(capacity, current_total, add_count):
    """
    背包添加物品契约：
    - add_count > 0（不能加0个或负数）
    - current_total + add_count <= capacity（不能超容量）
    """
    c, cur, a = sp.symbols('capacity current add', integer=True)
    contract = sp.And(a > 0, cur + a <= c)

    result = contract.subs({c: capacity, cur: current_total, a: add_count})
    print(f"\n--- add: 容量={capacity}, 当前={current_total}, 添加={add_count} ---")
    print(f"契约判定: {result}")
    print(f"=> {'合法' if bool(result) else '拒绝，违反契约'}")
    return bool(result)


def check_remove(current_count, remove_count):
    """
    背包移除物品契约：
    - remove_count > 0（不能移除0个或负数）
    - remove_count <= current_count（不能移除超过持有的数量）
    """
    cur, r = sp.symbols('current remove', integer=True)
    contract = sp.And(r > 0, r <= cur)

    result = contract.subs({cur: current_count, r: remove_count})
    print(f"\n--- remove: 持有={current_count}, 移除={remove_count} ---")
    print(f"契约判定: {result}")
    print(f"=> {'合法' if bool(result) else '拒绝，违反契约'}")
    return bool(result)


if __name__ == "__main__":
    print("=" * 55)
    print("无界背包契约检查")
    print("=" * 55)

    # ── add 测试 ──
    print("\n【add 契约：a > 0 ∧ cur + a ≤ cap】")

    print("\n场景A1：容量20，当前5，加3个 -> 应通过")
    check_add(capacity=20, current_total=5, add_count=3)

    print("\n场景A2：容量20，当前18，加5个 -> 应拒绝（超容量）")
    check_add(capacity=20, current_total=18, add_count=5)

    print("\n场景A3：容量20，当前5，加0个 -> 应拒绝（无效操作）")
    check_add(capacity=20, current_total=5, add_count=0)

    print("\n场景A4：容量20，当前5，加-3个 -> 应拒绝（负数）")
    check_add(capacity=20, current_total=5, add_count=-3)

    # ── remove 测试 ──
    print("\n" + "=" * 55)
    print("\n【remove 契约：r > 0 ∧ r ≤ cur】")

    print("\n场景R1：持有10，移除3个 -> 应通过")
    check_remove(current_count=10, remove_count=3)

    print("\n场景R2：持有10，移除15个 -> 应拒绝（不够）")
    check_remove(current_count=10, remove_count=15)

    print("\n场景R3：持有10，移除0个 -> 应拒绝（无效）")
    check_remove(current_count=10, remove_count=0)

    print("\n场景R4：持有10，移除-5个 -> 应拒绝（负数，会变相加）")
    check_remove(current_count=10, remove_count=-5)
