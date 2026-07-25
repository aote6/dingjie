import os
content = """# 定界 (dingjie)

在代码真正执行之前，用数学方法证明它不会违反约定的前提条件。

## 是什么

一个精化类型(refinement types) + 效应系统(effect system)结合的最小原型。
不是一门编程语言，是一层可以嵌进现有Python项目、在关键函数执行前做契约检查的工具。

## 为什么

大部分Bug不是"某个值错了"，是"操作前后的关系被破坏了"——
背包超容量、余额算错、坐标越界，这类问题靠单元测试只能事后发现，
定界尝试在执行前用形式化的方式直接拦住。

## 能力边界（明确写出来，不含糊）

- 契约谓词限制在线性整数算术（加减、比较），这个范围内的检查是可靠的、
  有数学证明支撑的（Presburger算术，可判定）
- 一旦涉及变量相乘，不再保证可判定（希尔伯特第十问题），本项目现阶段不碰这块

## 快速示例

```python
from inventory import Inventory, ContractViolation

inv = Inventory()
inv.add("wood", 10)

try:
    inv.remove("wood", -5)  # 契约违反：count必须>0
except ContractViolation as e:
    print(e)
```

## 运行测试

```bash
python3 core.py           # 单变量契约+效应
python3 core2.py          # 多变量关系契约
python3 check_inventory.py  # 无界项目背包契约验证
```

## 许可证

AGPL-3.0，详见 LICENSE
"""
with open(os.path.expanduser("~/dingjie/README.md"), "w") as f:
    f.write(content)
print("done")
