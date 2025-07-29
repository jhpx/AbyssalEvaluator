import unittest
from pathlib import Path

import json
from src.enka.model.artifact import Artifact
from src.enka.model.weapon import Weapon
from src.enka.stage.parser import EnkaParser
from src.enka.config.prop_id_map import ID_MAP, SUB_ID_MAP


class TestIDMap(unittest.TestCase):
    def test_artifact_main_stat_mapping(self):
        # 加载 player.json 文件
        json_path = Path("json/uid/player.json")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        avatar_info_list = data.get("avatarInfoList", [])
        if not avatar_info_list:
            print("未找到任何角色信息。")
            return

        for avatar_info in avatar_info_list:
            equip_list = avatar_info.get("equipList", [])

            for equip_item in equip_list:
                obj_item = EnkaParser.parse_equip_item(equip_item)
                if isinstance(obj_item, Weapon):
                    continue
                elif not isinstance(obj_item, Artifact):
                    raise Exception("未知的装备类型")

                expected_stat_type = obj_item.main_stat.stat_type
                expected_position = obj_item.position
                main_stat_id = obj_item.main_stat_id

                # 尝试从 id_map 中查找对应的位置和属性类型
                seek_pair = ID_MAP.get(main_stat_id)
                if not seek_pair:
                    print(f"[警告] 应新增 mainPropId: {main_stat_id}: expected_stat_type:{expected_stat_type}")
                    continue

                position, stat_type = seek_pair

                # 逐项验证
                with self.subTest(main_stat_id=main_stat_id):
                    self.assertEqual(position, expected_position,
                                     msg=f"main_stat_id={main_stat_id} 位置不匹配，应该是{expected_position}")
                    self.assertEqual(stat_type, expected_stat_type,
                                     msg=f"main_stat_id={main_stat_id} 属性类型不匹配，应该是{expected_stat_type}")

    def test_artifact_sub_stat_mapping(self):
        # 加载 player.json 文件
        json_path = Path("json/uid/player.json")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        avatar_info_list = data.get("avatarInfoList", [])
        if not avatar_info_list:
            print("未找到任何角色信息。")
            return

        for avatar_info in avatar_info_list:
            equip_list = avatar_info.get("equipList", [])

            for equip_item in equip_list:
                obj_item = EnkaParser.parse_equip_item(equip_item)
                if isinstance(obj_item, Weapon):
                    continue
                elif not isinstance(obj_item, Artifact):
                    raise Exception("未知的装备类型")


                sub_stats = obj_item.sub_stats
                sub_stat_ids = obj_item.sub_stat_ids

                for i in range(len(sub_stats)):
                    sub_stat_id = sub_stat_ids[i]
                    sub_stat_id_div10 = int(sub_stat_id / 10)
                    expected_stat_type = sub_stats[i].stat_type
                    if sub_stat_id_div10 not in SUB_ID_MAP:
                        print(f"[警告] 应新增 sub_stat_id: {sub_stat_id}: expected_stat_type:{expected_stat_type}")
                        continue
                    stat_type = SUB_ID_MAP.get(sub_stat_id_div10)

                    # 逐项验证
                    with self.subTest(sub_stat_id=sub_stat_id):
                        self.assertEqual(stat_type, expected_stat_type,
                                         msg=f"sub_stat_id={sub_stat_id} 属性类型不匹配，应该是{expected_stat_type}")


if __name__ == '__main__':
    unittest.main()
