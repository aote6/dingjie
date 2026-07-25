#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sympy as sp

x = sp.Symbol('x', integer=True)


class RefinementType:
    def __init__(self, predicate, name="x"):
        self.predicate = predicate
        self.name = name

    def __repr__(self):
        return f"{{{self.name}: Int | {self.predicate}}}"

    def implies(self, other):
        c = sp.And(self.predicate, sp.Not(other.predicate))
        return sp.simplify(c) == False


class EffectSet:
    ALLOWED = {"Read", "Write", "Throw"}

    def __init__(self, effects):
        effects = set(effects)
        illegal = effects - self.ALLOWED
        if illegal:
            raise ValueError(f"未知效应：{illegal}")
        self.effects = effects

    def __repr__(self):
        return "{" + ",".join(sorted(self.effects)) + "}"

    def is_subset_of(self, other):
        return self.effects.issubset(other.effects)


class FuncType:
    def __init__(self, param_type, return_type, effects):
        self.param_type = param_type
        self.return_type = return_type
        self.effects = effects

    def __repr__(self):
        return f"{self.param_type} -> {self.return_type} ! {self.effects}"

    def accepts_argument(self, arg):
        return arg.implies(self.param_type)

    def calling_declares_enough_effects(self, caller):
        return self.effects.is_subset_of(caller)


def typecheck_call(func, arg_type, caller_effects, label=""):
    print(f"\n--- {label} ---")
    print(f"函数类型: {func}")
    print(f"实参类型: {arg_type}")
    print(f"调用者效应: {caller_effects}")
    ck = func.accepts_argument(arg_type)
    ek = func.calling_declares_enough_effects(caller_effects)
    print(f"[契约] {'通过' if ck else '拒绝'}")
    print(f"[效应] {'通过' if ek else '拒绝'}")
    ok = ck and ek
    print(f"=> {'通过' if ok else '编译期拒绝'}")
    return ok


if __name__ == "__main__":
    print("=" * 50)
    print("测试1：正常调用")
    print("=" * 50)
    nonzero = RefinementType(sp.Ne(x, 0), "y")
    any_int = RefinementType(sp.true, "r")
    safe_div = FuncType(nonzero, any_int, EffectSet(["Throw"]))
    five = RefinementType(sp.Eq(x, 5), "y")
    typecheck_call(safe_div, five, EffectSet(["Throw","Read"]), "safe_div(5)")

    print("\n" + "=" * 50)
    print("测试2：违反契约")
    print("=" * 50)
    maybe_zero = RefinementType(sp.true, "y")
    typecheck_call(safe_div, maybe_zero, EffectSet(["Throw"]), "safe_div(未校验)")

    print("\n" + "=" * 50)
    print("测试3：效应泄漏")
    print("=" * 50)
    writer = FuncType(any_int, any_int, EffectSet(["Write"]))
    typecheck_call(writer, five, EffectSet(["Read"]), "write(5) 缺Write")
