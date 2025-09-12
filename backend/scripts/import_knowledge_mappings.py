import os
import sys
# 确保可从任意目录运行：将 backend 目录加入 sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import json
from typing import Dict, List
from models.card_system import CardSystem
from services.knowledge_mapping_service import KnowledgeMappingService

"""
使用方法：
  方式A（推荐）：在 backend 目录下以模块方式运行
    python -m scripts.import_knowledge_mappings scripts/knowledge_mappings.sample.json

  方式B：直接运行脚本（任意目录均可，已自动修正导入路径）
    python backend/scripts/import_knowledge_mappings.py backend/scripts/knowledge_mappings.sample.json

JSON 格式示例：
{
  "level_to_knowledge": [
    { "level_name": "有丝分裂", "knowledge_point": "细胞分裂基础" },
    { "level_name": "减数分裂", "knowledge_point": "染色体行为" }
  ],
  "knowledge_to_cards": [
    { "knowledge_point": "细胞分裂基础", "card_id": "SR001", "relevance": 1.2 },
    { "knowledge_point": "染色体行为", "card_id": "UR003", "relevance": 2.0 }
  ]
}
"""


def main(json_path: str):
    KnowledgeMappingService.ensure_tables()
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 导入 level -> knowledge
    for item in data.get('level_to_knowledge', []) or []:
        level = item.get('level_name')
        kp = item.get('knowledge_point')
        if not level or not kp:
            print(f"跳过无效 level_to_knowledge 记录: {item}")
            continue
        res = KnowledgeMappingService.upsert_level_mapping(level, kp)
        print(f"保存关卡映射: {res}")

    # 导入 knowledge -> cards
    for item in data.get('knowledge_to_cards', []) or []:
        kp = item.get('knowledge_point')
        cid = item.get('card_id')
        rel = item.get('relevance', 1.0)
        if not kp or not cid:
            print(f"跳过无效 knowledge_to_cards 记录: {item}")
            continue
        res = KnowledgeMappingService.upsert_card_mapping(kp, cid, rel)
        print(f"保存卡牌映射: {res}")

    print("导入完成")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python backend/scripts/import_knowledge_mappings.py <json路径>")
        print("或:   python -m scripts.import_knowledge_mappings scripts/knowledge_mappings.sample.json  (在 backend 目录下)")
        sys.exit(1)
    main(sys.argv[1]) 