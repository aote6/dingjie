import sympy as sp
from invariants.value_predicates.range_consistency import value_range, pairwise_le

damage_min, damage_max = sp.symbols('damage_min damage_max', integer=True)

violation = sp.And(damage_min == 15, damage_max == 10)
invariant = pairwise_le(damage_min, damage_max)
is_violation = sp.simplify(sp.And(violation, sp.Not(invariant))) != False
print(f"场景1(装备min/max) 非法赋值被检出: {is_violation}")
assert is_violation, "错误：应该检出违反，但没检出"

px = sp.Symbol('px', integer=True)
violation2 = sp.Eq(px, 150)
invariant2 = value_range(px, 0, 100)
is_violation2 = sp.simplify(sp.And(violation2, sp.Not(invariant2))) != False
print(f"场景2(灵体坐标) 非法赋值被检出: {is_violation2}")
assert is_violation2, "错误：应该检出违反，但没检出"

print("两个场景的判定逻辑本身正确 —— 但这只证明了谓词对，没有证明已接入真实代码")
