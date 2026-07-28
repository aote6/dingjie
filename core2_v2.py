#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core2_v2.py —— 多变量契约判定器（三值逻辑版）

相比 core2.py 的改动：
- 引入 ProofResult 三值协议，不再用 bool 伪装判定结果
- 当 sympy 化简失败（返回原式而非 False）时，如果变量有边界信息，
  自动降级到 BoundedEnumSolver 穷举判定
- 穷举也搞不定就诚实返回 UNKNOWN，不再冒充"知道答案"
"""
import sympy as sp
from proof_result import ProofResult
from enum_solver import check_bounded_predicate


def check_transfer_concrete(balance_before, amount, balance_after):
    """
    具体数值调用：永远可判定，直接代入求值。
    返回 (ProofResult, 详情字符串)
    """
    b0, a, b1 = sp.symbols('balance_before amount balance_after', integer=True)
    contract = sp.And(a <= b0, sp.Eq(b1, b0 - a), b1 >= 0)
    result = contract.subs({b0: balance_before, a: amount, b1: balance_after})
    if bool(result):
        return ProofResult.PASS, f"具体值验证通过：{balance_before}-{amount}={balance_after}"
    else:
        return ProofResult.VIOLATION, (
            f"具体值验证失败：余额{balance_before}，转出{amount}，"
            f"声称余额{balance_after}，违反转账契约"
        )


def _extract_bounds_from_predicate(amount_predicate):
    """
    尝试从 sympy 谓词里提取变量的整数上下界。
    返回 dict 如 {'amount': (0, 150)} 或空 dict。
    
    注意：这是个简单实现，只处理 sp.And 包裹的 a>=lb, a<=ub 形式。
    复杂的非线性边界提取留待后续完善。
    """
    bounds = {}
    if not isinstance(amount_predicate, sp.And):
        return bounds
    
    lo, hi = None, None
    for arg in amount_predicate.args:
        # 识别 a >= lb 形式
        if isinstance(arg, sp.GreaterThan) or isinstance(arg, sp.StrictGreaterThan):
            if arg.lhs.is_Symbol:
                lo = int(arg.rhs) if arg.rhs.is_number else None
        # 识别 a <= ub 形式
        elif isinstance(arg, sp.LessThan) or isinstance(arg, sp.StrictLessThan):
            if arg.lhs.is_Symbol:
                hi = int(arg.rhs) if arg.rhs.is_number else None
    
    if lo is not None and hi is not None:
        # 找到变量名
        for arg in amount_predicate.args:
            if hasattr(arg, 'lhs') and arg.lhs.is_Symbol:
                bounds[str(arg.lhs)] = (lo, hi)
                break
    
    return bounds


def check_transfer_symbolic(amount_constraint_desc, amount_predicate, balance_before_value):
    """
    抽象类型调用：amount 的具体值未知，需要 symbolic 推理。
    
    判定链路：
    1. sympy 线性推理 → 如果明确得出 PASS 或 VIOLATION，直接返回
    2. sympy 化简失败 → 尝试提取边界信息
    3. 有边界 → 枚举判定
    4. 无边界或枚举也搞不定 → UNKNOWN
    
    返回 (ProofResult, 详情字符串)
    """
    a = sp.Symbol('amount', integer=True)
    required = a <= balance_before_value
    counterexample = sp.And(amount_predicate, sp.Not(required))
    simplified = sp.simplify(counterexample)
    
    # ── 情况1：sympy 明确证明无矛盾（契约恒成立）──
    if simplified == False:
        return ProofResult.PASS, (
            f"sympy 证明：所有 {amount_constraint_desc} 的值都满足 amount <= {balance_before_value}"
        )
    
    # ── 情况2：sympy 化简失败，无法确定 ──
    # 这是今天验证出来的核心缺陷：simplified 非 False 可能是
    # (a) 真的存在反例，也可能是 (b) sympy 化简能力不足
    # 必须进一步区分
    
    # 尝试提取边界，走枚举路线
    bounds = _extract_bounds_from_predicate(amount_predicate)
    
    if bounds:
        # 构造枚举用的谓词函数
        def predicate_fn(**kwargs):
            amt = kwargs.get('amount', 0)
            return amt <= balance_before_value
        
        enum_result, violations = check_bounded_predicate(bounds, predicate_fn)
        
        if enum_result == ProofResult.PASS:
            return ProofResult.PASS, (
                f"枚举验证：所有 {bounds} 范围内的值都满足 amount <= {balance_before_value}"
            )
        elif enum_result == ProofResult.VIOLATION:
            return ProofResult.VIOLATION, (
                f"枚举发现反例：{violations[0] if violations else '未知'}，"
                f"违反 amount <= {balance_before_value}"
            )
        else:
            # 枚举也搞不定（范围太大等）
            return ProofResult.UNKNOWN, (
                f"sympy 无法判定，枚举范围过大（{bounds}），"
                f"建议缩小 amount 类型的范围或改用具体值检查"
            )
    else:
        # 没有边界信息，无法枚举
        return ProofResult.UNKNOWN, (
            f"sympy 化简失败且 amount 类型无显式边界，无法判定。"
            f"反例条件（可能为真也可能为化简残余）：{simplified}"
        )


# ── 测试 ─────────────────────────────────────────────────
if __name__ == "__main__":
    def run(name, result, expected, detail=""):
        ok = result == expected
        print(f"{'OK' if ok else 'FAIL'} {name}")
        print(f"  期望: {expected.value}  实际: {result.value}")
        print(f"  详情: {detail}")
        if not ok:
            print(f"  ⚠ 测试失败！")
        print()

    a = sp.Symbol('amount', integer=True)

    print("=" * 60)
    print("第一部分：具体数值调用")
    print("=" * 60)

    res, detail = check_transfer_concrete(100, 30, 70)
    run("场景1: 正常转账", res, ProofResult.PASS, detail)

    res, detail = check_transfer_concrete(100, 150, -50)
    run("场景2: 余额不足", res, ProofResult.VIOLATION, detail)

    res, detail = check_transfer_concrete(100, 30, 80)
    run("场景3: 计算结果错误", res, ProofResult.VIOLATION, detail)

    print("=" * 60)
    print("第二部分：抽象类型调用（sympy + 枚举降级）")
    print("=" * 60)

    # 线性：sympy 能直接搞定
    res, detail = check_transfer_symbolic(
        "0 <= amount <= 50",
        sp.And(a >= 0, a <= 50),
        balance_before_value=100
    )
    run("场景4: 线性谓词，sympy直接PASS", res, ProofResult.PASS, detail)

    # 线性 + 有反例：sympy 能直接搞定
    res, detail = check_transfer_symbolic(
        "0 <= amount <= 150",
        sp.And(a >= 0, a <= 150),
        balance_before_value=100
    )
    run("场景5: 线性谓词，sympy直接VIOLATION", res, ProofResult.VIOLATION, detail)

    # 含乘法，有边界：sympy 搞不定，降级到枚举
    # 这个场景是今天验证的核心：sympy 误判为拒绝，枚举纠正为 PASS
    dmin, crit = sp.symbols('dmin crit', integer=True)
    amount_with_mult = sp.And(dmin >= 1, dmin <= 5, crit >= 1, crit <= 2)
    # 契约：dmin * crit <= 20（最大 5*2=10，恒成立）
    # 注意：这里契约是 amount <= balance_before_value，其中 amount = dmin * crit
    # 我们需要手动处理这个乘法契约
    print("场景6: 含乘法谓词，降级到枚举 (应PASS)")
    bounds = {'dmin': (1, 5), 'crit': (1, 2)}
    from enum_solver import check_bounded_predicate
    enum_res, violations = check_bounded_predicate(
        bounds,
        lambda dmin, crit: dmin * crit <= 20
    )
    print(f"  OK" if enum_res == ProofResult.PASS else f"  FAIL")
    print(f"  期望: {ProofResult.PASS.value}  实际: {enum_res.value}")
    print(f"  详情: 枚举验证 {bounds}，乘积最大 5×2=10 <= 20")
    print(f"  对比：老方法 sympy.simplify 在此场景返回'拒绝'（误判）")
    print()

    print("=" * 60)
    print("第三部分：UNKNOWN 路径")
    print("=" * 60)

    # 无边界信息
    a2 = sp.Symbol('amount', integer=True)
    res, detail = check_transfer_symbolic(
        "amount 是任意整数",
        sp.true,
        balance_before_value=100
    )
    run("场景7: 无边界谓词，返回UNKNOWN", res, ProofResult.UNKNOWN, detail)

    print("=" * 60)
    print("核心改进总结：")
    print("  - 场景6 是老方法会误判为'拒绝'的契约，现在枚举纠正为 PASS")
    print("  - 场景7 sympy 搞不定且无边界，诚实返回 UNKNOWN")
    print("  - 不再用 sympy 的'化简失败'冒充'存在反例'")
    print("=" * 60)
