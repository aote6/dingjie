"""
三值判定结果 (ProofResult)

背景: 2026-07-27 发现 core2.py 的 check_transfer_symbolic 用
"sp.simplify化简失败" 冒充 "存在反例", 导致真实存在的 False Negative:
契约恒成立(枚举穷尽验证过)却被判定为拒绝。

根源: 布尔值(True/False)无法表达"证明器能力不足, 无法判定"这第三种情况。
SMT/定理证明器的行业标准做法是三值: PASS / VIOLATION / UNKNOWN。
"""
from enum import Enum


class ProofResult(Enum):
    PASS = "pass"           # 已证明契约恒成立
    VIOLATION = "violation" # 已找到具体反例
    UNKNOWN = "unknown"     # 判定器能力不足或超出可判定片段, 无法给出结论

    def __bool__(self):
        # 故意不支持 if result: 这种写法, 逼迫调用方显式处理三种情况
        raise TypeError(
            "ProofResult不支持bool()转换, 必须显式判断 "
            "result == ProofResult.PASS / VIOLATION / UNKNOWN, "
            "防止UNKNOWN被静默当成False处理"
        )
