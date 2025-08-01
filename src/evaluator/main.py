from src.enka.model import player
from src.enka.model.character import Character
from src.enka.model.player import Player
from src.enka.model.stat import StatType


def print_player(player: Player):
    print(f"\n[UID={player.uid}]{player.nickname} 的角色信息如下：")
    print(f"等级: {player.level}")
    print(f"世界等级: {player.world_level}")
    print(f"成就数量: {player.finish_achievement_num}")
    print(f"深境螺旋: 第{player.tower_floor_index}层 第{player.tower_level_index}间")
    print(f"满好感角色数量: {player.full_friendship_num}")
    for idx, character in enumerate(player.characters, 1):
        print(f"\n{idx}. ", end="")
        print_character(character)


def print_character(character):
    print(f"{character.name}(ID: {character.id}|{character.icon})")
    print(f"   等级: {character.level}")
    print(f"   好感度: {character.friendship}")
    wp = character.weapon
    print(
        f"   武器: {wp.name}(ID: {wp.id}|{wp.icon}) (类型: {wp.type}) (等级: {wp.level}) (精炼: {wp.refine}) (效果: {wp.weapon_stats})")
    print_artifacts(character)


def print_artifacts(character):
    for aft in [character.artifact_flower, character.artifact_plume, character.artifact_sands,
                character.artifact_goblet, character.artifact_circlet]:
        if aft:
            print(
                f"   圣遗物{aft.position}(套装:{aft.set_name}): {aft.name}({aft.id}|{aft.icon}) (等级: {aft.level}) (效果: {aft.main_stat},{aft.sub_stats}) (评分: {aft.score})")


# 定义每个圣遗物词条的系数（小助手公式）
XZS_ARTIFACT_STAT_FACTORS = {
    StatType.CRIT_RATE: 2.0,  # 暴击率
    StatType.CRIT_DMG: 1.0,  # 暴击伤害
    StatType.ATK_PERCENT: 1.33,  # 攻击百分比
    StatType.HP_PERCENT: 1.33,  # 生命百分比
    StatType.DEF_PERCENT: 1.06,  # 防御百分比
    StatType.ATK: 0.398 * 0.5,  # 攻击力 0.199
    StatType.HP: 0.026 * 0.66,  # 生命值 0.01716
    StatType.DEF: 0.335 * 0.66,  # 防御力 0.2211
    StatType.ELEMENTAL_MASTERY: 0.33,  # 元素精通
    StatType.ELEMENTAL_CHARGE: 1.1979,  # 充能效率
}

# 定义每个圣遗物词条的系数（刻晴办公桌公式）
YUANMO_ARTIFACT_STAT_FACTORS = {
    StatType.CRIT_RATE: 1.6,  # 暴击率
    StatType.CRIT_DMG: 1.0,  # 暴击伤害
    StatType.ATK_PERCENT: 1.33,  # 攻击百分比
    StatType.HP_PERCENT: 1.33,  # 生命百分比
    StatType.DEF_PERCENT: 1.06,  # 防御百分比
    StatType.ATK: 0.266,  # 攻击力 0.199
    StatType.HP: 0.026 * 0.66,  # 生命值 0.01716
    StatType.DEF: 0.162676,  # 防御力
    StatType.ELEMENTAL_MASTERY: 0.33,  # 元素精通
    StatType.ELEMENTAL_CHARGE: 1.2,  # 充能效率
}

CHARACTER_STAT_WEIGHTS_YELAN = {
    StatType.CRIT_RATE: 1,  # 暴击率
    StatType.CRIT_DMG: 1,  # 暴击伤害
    StatType.HP_PERCENT: 0.8,  # 攻击百分比
    StatType.HP: 0.8,  # 防御力
    StatType.ELEMENTAL_CHARGE: 0.55,  # 充能效率
}
CHARACTER_STAT_WEIGHTS_LEIDIAN = {
    StatType.CRIT_RATE: 1,  # 暴击率
    StatType.CRIT_DMG: 1,  # 暴击伤害
    StatType.ATK_PERCENT: 1,  # 攻击百分比
    StatType.ATK: 1,  # 攻击力
    StatType.ELEMENTAL_CHARGE: 1,  # 充能效率
}

CHARACTER_STAT_WEIGHTS_NUOAIE = {
    StatType.CRIT_RATE: 1,  # 暴击率
    StatType.CRIT_DMG: 1,  # 暴击伤害
    StatType.ATK_PERCENT: 0.5,  # 攻击百分比
    StatType.DEF_PERCENT: 1,  # 防御百分比
    StatType.ATK: 0.5,  # 攻击力
    StatType.DEF: 1,  # 防御力
    StatType.ELEMENTAL_CHARGE: 1,  # 充能效率
}


CHARACTER_STAT_WEIGHTS_XINGQIU = {
    StatType.CRIT_RATE: 1,  # 暴击率
    StatType.CRIT_DMG: 1,  # 暴击伤害
    StatType.ATK_PERCENT: 1,  # 攻击百分比
    StatType.ATK: 1,  # 攻击力
    StatType.ELEMENTAL_CHARGE: 1,  # 充能效率
}
def evaluate_character(c: Character, factor_dict: dict, character_weight: dict):
    for aft in [c.artifact_flower, c.artifact_plume, c.artifact_sands,
                c.artifact_goblet, c.artifact_circlet]:
        aft.score = WAE.evaluate(aft, factor_dict, character_weight, "ym")
    print(c.name)
    print_artifacts(c)


headers = ['HP', 'HP_PERCENT', 'ATK_BASE', 'ATK', 'ATK_PERCENT', 'DEF', 'DEF_PERCENT', 'CRIT_RATE', 'CRIT_DMG',
           'PYRO_DMG_BONUS', 'ELECTRO_DMG_BONUS', 'CRYO_DMG_BONUS', 'HYDRO_DMG_BONUS', 'GEO_DMG_BONUS',
           'ANEMO_DMG_BONUS',
           'DENDRO_DMG_BONUS', 'PHYSICAL_DMG_BONUS', 'ENERGY_RECHARGE', 'ELEMENTAL_MASTERY', 'HEALING_BONUS']


def print_matrix():
    print("Character\t" + "\t".join(headers))
    for c in player.characters:
        for aft in [c.artifact_flower, c.artifact_plume, c.artifact_sands,
                    c.artifact_goblet, c.artifact_circlet]:
            print(c.name, end="\t")
            for k in headers:
                print(aft.matrix()[k], end="\t")
            print("")


    # with open("data\\player\\101242308.pkl", "rb") as f:
    #     player = pickle.load(f)
    #     # print_matrix()
    #     yelan = player.characters[7]
    #     leidian = player.characters[6]
    #     nuoaie = player.characters[3]
    #     xingqiu = player.characters[10]
    #
    #     evaluate_character(yelan, YUANMO_ARTIFACT_STAT_FACTORS, CHARACTER_STAT_WEIGHTS_YELAN)
    #     evaluate_character(leidian, YUANMO_ARTIFACT_STAT_FACTORS, CHARACTER_STAT_WEIGHTS_LEIDIAN)
    #     evaluate_character(nuoaie, YUANMO_ARTIFACT_STAT_FACTORS, CHARACTER_STAT_WEIGHTS_NUOAIE)
    #     evaluate_character(xingqiu, YUANMO_ARTIFACT_STAT_FACTORS, CHARACTER_STAT_WEIGHTS_XINGQIU)