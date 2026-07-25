#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sympy as sp


def check_transfer_concrete(balance_before, amount, balance_after):
    b0, a, b1 = sp.symbols('balance_before amount balance_after', integer=True)
    contract = sp.And(a <= b0, sp.Eq(b1, b0 - a), b1 >= 0)
    result = contract.subs({b0: balance_before, a: amount, b1: balance_after})
    print(f"\n--- 转账: 前={balance_before}, 额={amount}, 声称后={balance_after} ---")
    print(f"契约判定: {result}")
    print(f"结果: {'合法，允许执行' if bool(result) else '拒绝，违反转账契约'}")
    return bool(result)


def check_transfer_symbolic(amount_constraint_desc, amount_predicate, balance_before_value):
    a = sp.Symbol('amount', integer=True)
    required = a <= balance_before_value
    counterexample = sp.And(amount_predicate, sp.Not(required))
    simplified = sp.simplify(counterexample)
    ok = (simplified == False)
    print(f"\n--- 检查抽象类型: amount类型={amount_constraint_desc}, 余额={balance_before_value} ---")
    print(f"是否对所有可能取值都满足契约: {'是，通过' if ok else '否，存在违反契约的取值，拒绝'}")
    if not ok:
        print(f"  (反例条件: {simplified})")
    return ok


if __name__ == "__main__":
    print("=" * 60)
    print("第一部分：具体数值调用（代入求值，永远可判定）")
    print("=" * 60)

    print("\n场景1：正常转账，余额充足，计算正确 -> 应该通过")
    check_transfer_concrete(balance_before=100, amount=30, balance_after=70)

    print("\n场景2：余额不足还硬转 -> 应该拒绝")
    check_transfer_concrete(balance_before=100, amount=150, balance_after=-50)

    print("\n场景3：余额够，但结果算错了(70算成80) -> 应该拒绝")
    check_transfer_concrete(balance_before=100, amount=30, balance_after=80)

    print("\n" + "=" * 60)
    print("第二部分：抽象类型调用（值未知，需要symbolic推理）")
    print("=" * 60)

    a = sp.Symbol('amount', integer=True)

    print("\n场景4：amount类型是'0到50之间'，余额是100 -> 应该通过")
    check_transfer_symbolic("0 <= amount <= 50", sp.And(a >= 0, a <= 50), balance_before_value=100)

    print("\n场景5：amount类型是'0到150之间'，余额是100 -> 应该拒绝")
    check_transfer_symbolic("0 <= amount <= 150", sp.And(a >= 0, a <= 150), balance_before_value=100)
