# 候选不变量记录

## count非负
- 场景1: Inventory.add/remove, 2026-07-25
- 场景2: (待发现)

## min <= max (范围一致性)
- 场景1: EquipmentInstance.damage_min <= damage_max, 2026-07-25
- 场景2: (待发现)

## min <= max (范围一致性) — 已入库 invariants/value_predicates/range_consistency.py
- 场景1: EquipmentInstance.damage_min <= damage_max, 2026-07-25
- 场景2: 灵体 KeyModel 百分比坐标 0-100 且 W>0 H>0, 2026-07-25
- 状态: 谓词逻辑自测通过，尚未接入真实代码调用点，不算已验证（本条记录本身此前绕过了lu_patch直接写入，已作为炉的一次真实漏洞记录）
