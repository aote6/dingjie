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
- 状态: 已验证两个独立场景，已入库 invariants/value_predicates/range_consistency.py
  - 真实测试：range_consistency作为kuai的block可运行（合法/非法值均正确判定），但两项目模块均命名为core，同时在sys.path会互相遮蔽，若未来合并需先解决命名空间冲突，成本不可忽略
  - 场景1: EquipmentInstance.__post_init__ 拦截 damage_min=10 > damage_max=5（from_dict路径，真实抛异常）
  - 场景2: 灵体 KeyModel 百分比坐标 0-100（判定逻辑已验证）
