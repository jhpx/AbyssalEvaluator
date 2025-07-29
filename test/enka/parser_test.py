# parser_test.py

import unittest

import json
from src.enka.model.artifact import Artifact
from src.enka.model.character import Character
from src.enka.model.player import Player
from src.models.enum.position import Position
from src.enka.model.stat import Stat, StatType
from src.enka.model.weapon import Weapon
from src.enka.stage.parser import EnkaParser


class TestEnkaParser(unittest.TestCase):

    def test_parse_weapon(self, weapon_json='json/item_weapon.json'):
        # 读取 item_weapon.json 文件作为样本数据
        with open(weapon_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        weapon = EnkaParser.parse_weapon(data)

        # 预期结果
        expected_weapon = Weapon(
            id=11302,
            name="TEXT_MAP_1608953539",
            description="",
            level=1,
            promote_level=0,
            refine=5,  # affixMap["111302"] = 4 → refine = 4 + 1 = 5
            rank=3,
            icon="UI_EquipIcon_Sword_Dawn",
            weapon_stats=[
                Stat(StatType("FIGHT_PROP_BASE_ATTACK"), stat_value=39),
                Stat(StatType("FIGHT_PROP_CRITICAL_HURT"), stat_value=10.2)
            ]
        )

        # 逐项验证
        self.assertEqual(weapon.id, expected_weapon.id)
        self.assertEqual(weapon.name, expected_weapon.name)
        self.assertEqual(weapon.description, expected_weapon.description)
        self.assertEqual(weapon.level, expected_weapon.level)
        self.assertEqual(weapon.promote_level, expected_weapon.promote_level)
        self.assertEqual(weapon.refine, expected_weapon.refine)
        self.assertEqual(weapon.rank, expected_weapon.rank)
        self.assertEqual(weapon.icon, expected_weapon.icon)

        # 主词条验证
        self.assertEqual(len(weapon.weapon_stats), len(expected_weapon.weapon_stats))
        for i in range(len(weapon.weapon_stats)):
            self.assertEqual(weapon.weapon_stats[i].stat_type, expected_weapon.weapon_stats[i].stat_type)
            self.assertAlmostEqual(weapon.weapon_stats[i].stat_value, expected_weapon.weapon_stats[i].stat_value,
                                   delta=0.01)

    def test_parse_artifact(self, reliquary_json='json/item_reliquary.json'):
        # 读取测试 JSON 文件
        with open(reliquary_json, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 调用解析方法
        artifact = EnkaParser.parse_artifact(data)

        # 验证解析结果
        expected_artifact = Artifact(
            id=77534,
            name="TEXT_MAP_3931114612",
            level=21,
            position=Position("EQUIP_DRESS"),
            rank=5,
            set_id=15003,
            set_name="TEXT_MAP_147298547",
            icon="UI_RelicIcon_15003_3",
            main_stat_id=13007,
            sub_stat_ids=[
                501234,
                501062,
                501222,
                501242,
                501221,
                501241,
                501222,
                501242,
                501234
            ],
            main_stat=Stat(StatType("FIGHT_PROP_CRITICAL"), stat_value=31.1),
            sub_stats=[
                Stat(StatType("FIGHT_PROP_CHARGE_EFFICIENCY"), stat_value=13),
                Stat(StatType("FIGHT_PROP_ATTACK_PERCENT"), stat_value=4.7),
                Stat(StatType("FIGHT_PROP_CRITICAL_HURT"), stat_value=17.9),
                Stat(StatType("FIGHT_PROP_ELEMENT_MASTERY"), stat_value=54)
            ]
        )

        # 逐字段比较
        self.assertEqual(artifact.id, expected_artifact.id)
        self.assertEqual(artifact.name, expected_artifact.name)
        self.assertEqual(artifact.level, expected_artifact.level)
        self.assertEqual(artifact.position, expected_artifact.position)
        self.assertEqual(artifact.rank, expected_artifact.rank)
        self.assertEqual(artifact.set_id, expected_artifact.set_id)
        self.assertEqual(artifact.set_name, expected_artifact.set_name)
        self.assertEqual(artifact.icon, expected_artifact.icon)

        # 主属性比较
        self.assertEqual(artifact.main_stat.stat_type, expected_artifact.main_stat.stat_type)
        self.assertAlmostEqual(artifact.main_stat.stat_value, expected_artifact.main_stat.stat_value, delta=0.01)
        self.assertEqual(artifact.main_stat_id, expected_artifact.main_stat_id)

        # 副属性比较
        self.assertEqual(len(artifact.sub_stats), len(expected_artifact.sub_stats))
        for i in range(len(artifact.sub_stats)):
            self.assertEqual(artifact.sub_stats[i].stat_type, expected_artifact.sub_stats[i].stat_type)
            self.assertAlmostEqual(artifact.sub_stats[i].stat_value, expected_artifact.sub_stats[i].stat_value,
                                   delta=0.01)
        self.assertSetEqual(set(artifact.sub_stat_ids), set(expected_artifact.sub_stat_ids))

    def test_parse_item(self):
        with open('json/item_weapon.json', 'r', encoding='utf-8') as f:
            data1 = json.load(f)
        weapon = EnkaParser.parse_equip_item(data1)
        self.assertIsInstance(weapon, Weapon)

        with open('json/item_reliquary.json', 'r', encoding='utf-8') as f:
            data2 = json.load(f)
        artifact = EnkaParser.parse_equip_item(data2)
        self.assertIsInstance(artifact, Artifact)

    def test_parse_character(self):
        with open('json/character.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        character = EnkaParser.parse_character(data)
        self.assertIsInstance(character, Character)

    def test_parse_player(self):
        with open('json/uid/player.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        player = EnkaParser.parse_player(data)
        self.assertIsInstance(player, Player)


if __name__ == '__main__':
    unittest.main()
