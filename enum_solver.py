"""
有界枚举判定器 (EnumSolver)

背景: 2026-07-27 验证。当契约涉及两个及以上自由变量相乘(非线性),
且每个变量都有明确的有限整数范围时, 直接暴力枚举比symbolic推理更可靠。
sp.simplify对这类式子常常化简失败(既不能证明恒成立也不能证明有反例),
枚举没有这个盲区: 只要范围有限, 穷尽验证永远给出确定答案。

限制: 只适用于每个变量都有显式上下界的情况。范围无界时返回UNKNOWN,
不能强行枚举(会退化成假装判定, 重蹈老方法的覆辙)。
"""
from itertools import product
from proof_result import ProofResult


def check_bounded_predicate(var_ranges, predicate_fn, max_combinations=1_000_000):
    """
    var_ranges: dict, 例如 {'dmin': (1,5), 'crit': (1,2)}
    predicate_fn: 函数, 接收 **kwargs (变量名=具体整数值), 返回 True/False
                  表示"这组取值是否满足契约"
    返回: (ProofResult, 反例列表或None)
    """
    names = list(var_ranges.keys())
    ranges = [range(lo, hi + 1) for lo, hi in var_ranges.values()]

    total = 1
    for r in ranges:
        total *= len(r)
    if total > max_combinations:
        return ProofResult.UNKNOWN, None  # 组合数太大, 不硬枚举, 老实报告未知

    violations = []
    for combo in product(*ranges):
        kwargs = dict(zip(names, combo))
        if not predicate_fn(**kwargs):
            violations.append(kwargs)
            if len(violations) >= 5:  # 反例够用就停, 不用穷尽收集
                break

    if violations:
        return ProofResult.VIOLATION, violations
    return ProofResult.PASS, None
