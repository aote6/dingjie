import sympy as sp
from invariants.value_predicates.range_consistency import value_range, pairwise_le

dmin, dmax = sp.symbols('dmin dmax', integer=True)
violation = sp.And(sp.Eq(dmin, 15), sp.Eq(dmax, 10))
invariant = pairwise_le(dmin, dmax)
is_violation = sp.simplify(sp.And(violation, sp.Not(invariant))) != False
print(f"场景1判定逻辑 非法赋值被检出: {is_violation}")
assert is_violation

px = sp.Symbol('px', integer=True)
violation2 = sp.Eq(px, 150)
invariant2 = value_range(px, 0, 100)
is_violation2 = sp.simplify(sp.And(violation2, sp.Not(invariant2))) != False
print(f"场景2判定逻辑 非法赋值被检出: {is_violation2}")
assert is_violation2
print("两个场景判定逻辑均确认正确")
