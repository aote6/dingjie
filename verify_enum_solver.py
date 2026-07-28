from proof_result import ProofResult
from enum_solver import check_bounded_predicate

print("场景1: dmin[1,5] crit[1,2] cap=20 (最大乘积10<=20, 应恒成立PASS)")
result1, _ = check_bounded_predicate(
    {'dmin': (1, 5), 'crit': (1, 2)},
    lambda dmin, crit: dmin * crit <= 20
)
print(f"  判定: {result1}")
assert result1 == ProofResult.PASS
print("  -> 通过 (老方法在此场景误判为拒绝, 枚举法判对了)")

print()
print("场景2: dmin[8,12] crit[1,5] cap=50 (存在dmin=11,crit=5=55>50, 应VIOLATION)")
result2, counterex = check_bounded_predicate(
    {'dmin': (8, 12), 'crit': (1, 5)},
    lambda dmin, crit: dmin * crit <= 50
)
print(f"  判定: {result2}, 反例: {counterex}")
assert result2 == ProofResult.VIOLATION
print("  -> 通过")

print()
print("场景3: 范围过大(模拟未来真实无界情况), 应返回UNKNOWN而不是硬扛")
result3, _ = check_bounded_predicate(
    {'a': (1, 2000), 'b': (1, 2000)},
    lambda a, b: a * b <= 10**10,
    max_combinations=100_000
)
print(f"  判定: {result3}")
assert result3 == ProofResult.UNKNOWN
print("  -> 通过 (没有硬枚举400万组合, 老实报告未知)")

print()
print("场景4: ProofResult禁止bool()转换, 逼迫显式判断")
try:
    if result3:
        pass
    print("  !! 不该走到这里, __bool__应该报错")
except TypeError as e:
    print(f"  -> 通过, 正确抛出: {e}")

print()
print("四个场景全部通过")
