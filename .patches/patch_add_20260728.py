# -*- coding: utf-8 -*-
import pathlib

STATUS = pathlib.Path.home() / "dingjie" / "STATUS.md"

ANCHOR = "这不是推翻定理——是证明了你的问题根本不需要走到定理管的那块地盘。"

ADDITION = """

## 2026-07-28 更新：真实契约扫描的范围修正与最终边界确认

### 发现的问题：此前"真实契约0.22% UNKNOWN"结论不成立

对整个 home 目录做 AST 扫描时，把 vendor 依赖（如 .cargo/registry
下的第三方脚本）也当作"真实契约"统计进去了，导致覆盖率数字虚高。

收窄扫描范围到 unbounded/lingti/lu/dingjie 四个真实项目后重新统计（共1104条）：

- linear_trivial（0-1变量）: 437条 (39.6%)
- low_dim（2变量）: 300条 (27.2%)
- high_dim（3变量以上）: 59条 (5.3%)
- opaque_call（含函数调用）: 308条 (27.9%)

进一步拆分 opaque_call 后确认：
- 20.4%（63条）是纯函数调用（len/abs/min/max等），可安全展开参与判定
- 79.6%（246条）依赖字典/对象方法（`.get()`）、运行时可变世界状态
  （`world.get_tile()`）、或随机采样（`random.random()`），
  这些根本不是数值安全契约，不属于 DPRM 讨论的问题域

### 核心结论修正

DPRM/希尔伯特第十问题讨论的是整数多项式约束的可判定性，但代码库里
大多数"含比较运算符的语句"根本不是这类契约——它们是枚举/字符串比较、
状态机分支、随机采样。"覆盖率百分比"不是本模块该追求的指标。

BoundedEnumSolver 的职责边界正式收窄为：只负责显式标注的数值安全
契约（如伤害上限、资源上限一类的乘法/线性约束）。

### 真实契约实测（真实边界范围）

- dmin*crit<=20（dmin,crit ∈ 0-50）：72次扫描，0.000523秒，PASS/VIOLATION确定
- d*m<=50000（d,m ∈ 0-500）：50,997次扫描，0.113071秒，PASS/VIOLATION确定

两条真实契约实测均在毫秒级完成，性能达标，正式合入。

### 结论：本方向实验到此为止

不再扩大扫描规模验证覆盖率（边际信息量趋近于零）。下一步转向
灵体(lingti)的拖拽缩放（drag-to-resize）与预设组件库。
"""

content = STATUS.read_text(encoding="utf-8")
assert content.count(ANCHOR) == 1, f"锚点出现次数异常: {content.count(ANCHOR)}"
new_content = content.replace(ANCHOR, ANCHOR + ADDITION, 1)
STATUS.write_text(new_content, encoding="utf-8")
print("补丁成功，已追加 2026-07-28 章节。")
