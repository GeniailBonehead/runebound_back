import random


# Рандомизатор фиксируется в items.py, вверху
# TODO: Настроить pytest и зафиксировать рандомизатор внутри test-case


def test_battle_example():
    # В items фиксируется random.seed(3)
    random.seed(3)
    from battle_basic import Battle, GenerateCreature
    from items import heroesItems, SkillBlock, HotornNative, KorbinNative

    cards = SkillBlock()

    Korbin = GenerateCreature(10, heroesItems["Korbin"], [KorbinNative()], first_move=True, card_block=cards, id=123)
    Hotorn = GenerateCreature(10, heroesItems["Hotorn"], [HotornNative(min_points=0)], first_move=False, card_block=cards,
                              id=333)
    assert Korbin.ini == 0
    assert Hotorn.ini == 1
    fight = Battle(Korbin, Hotorn)

    def info(fight):
        ID = fight.get_active_hero_id()
        if Korbin.id == ID:
            print("Ходит Корбин")
        elif Hotorn.id == ID:
            print("Ходит Хоторн")
        print(Korbin.get_active_items(), Korbin.get_active_actions())
        print(Hotorn.get_active_items(), Hotorn.get_active_actions())
        return ID

    block = SkillBlock()

    assert info(fight) == Korbin.id
    res = fight.move([0, 1, 2], )
    result_hit = fight.extra_move([0])
    assert result_hit == 3
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    print("По итогу прилетело {}".format(result_hit))
    assert info(fight) == Hotorn.id
    # Хотторн способностью перебросил жетон
    res = fight.move([2], action=0)
    assert info(fight) == Korbin.id
    result_hit = fight.extra_move()
    assert result_hit == 0
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    print("По итогу прилетело {}".format(result_hit))
    assert info(fight) == Korbin.id
    print("_______________________-")
    # Корбин пытается использовать способность, но количество молний недостаточно
    res = fight.move([], action=0)
    result_hit = fight.extra_move()
    assert result_hit == 0
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    print("По итогу прилетело {}".format(result_hit))
    res = fight.move([1])
    result_hit = fight.extra_move()
    assert result_hit == 1
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    print("По итогу прилетело {}".format(result_hit))
    assert info(fight) == Hotorn.id
    print("_______________________-")
    res = fight.move([2])
    result_hit = fight.extra_move()
    assert result_hit == 1
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    print("По итогу прилетело {}".format(result_hit))
    assert info(fight) == Hotorn.id
    res = fight.move([0, 1, 2])
    result_hit = fight.extra_move([1])
    assert result_hit == 3
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    print("По итогу прилетело {}".format(result_hit))
    assert info(fight) == Korbin.id
    #
    res = fight.move([0], action=0)
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    print("По итогу прилетело {}".format(result_hit))
    assert info(fight) == Hotorn.id
    res = fight.move([], action=0)
    assert info(fight) == Korbin.id
    res = fight.move([2])
    assert info(fight) == Korbin.id

# battle_example()


def test_battle_example2():
    random.seed(3)
    from battle_basic import Battle, GenerateCreature
    from items import heroesItems, SkillBlock, LaurelNative, \
        MokNative

    cards = SkillBlock()

    Mok = GenerateCreature(10, heroesItems["Mok"], [MokNative()], first_move=True, card_block=cards, id=123)
    Laurel = GenerateCreature(10, heroesItems["Laurel"], [LaurelNative(min_points=0)], first_move=False, card_block=cards,
                              id=333)
    Mok.wisdom = 5  #Допустим, что он умный
    assert Mok.ini == 1
    assert Laurel.ini == 1
    fight = Battle(Mok, Laurel)

    def info(fight):
        ID = fight.get_active_hero_id()
        if Mok.id == ID:
            print("Ходит Мок")
        elif Laurel.id == ID:
            print("Ходит Лаурель")
        print("Мок: ", Mok.get_active_items(), Mok.get_active_actions())
        print("Лаурель, ", Laurel.get_active_items(), Laurel.get_active_actions())
        return ID

    assert info(fight) == Mok.id
    res = fight.move([0], action=0)
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    result_hit = fight.extra_move([1])
    print("По итогу прилетело {}".format(result_hit))
    assert info(fight) == Laurel.id
    fight.move([1], action=0)
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    result_hit = fight.extra_move([0])
    print("По итогу прилетело {}".format(result_hit))
    assert info(fight) == Mok.id


test_battle_example()
