import random


# Рандомизатор фиксируется в items.py, вверху


def test_battle_example():
    # В items фиксируется random.seed(3)
    random.seed(3)
    from battle_basic import Battle, generateCreature
    from items import heroesItems, skill_block, HotornNative, KorbinNative

    cards = skill_block()

    Korbin = generateCreature(10, heroesItems["Korbin"], [KorbinNative()], firstMove=True, card_block=cards, ID=123)
    Hotorn = generateCreature(10, heroesItems["Hotorn"], [HotornNative(minPoints=0)], firstMove=False, card_block=cards,
                              ID=333)
    assert Korbin.getIni() == 0
    assert Hotorn.getIni() == 1
    fight = Battle(Korbin, Hotorn)

    def info(fight):
        ID = fight.getActiveHeroID()
        if Korbin.ID == ID:
            print("Ходит Корбин")
        elif Hotorn.ID == ID:
            print("Ходит Хоторн")
        print(Korbin.getActiveItems(), Korbin.getActiveActions())
        print(Hotorn.getActiveItems(), Hotorn.getActiveActions())
        return ID

    block = skill_block()

    assert info(fight) == Korbin.ID
    res = fight.move([0, 1, 2], )
    result_hit = fight.extraMove([0])
    assert result_hit == 3
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    print("По итогу прилетело {}".format(result_hit))
    assert info(fight) == Hotorn.ID
    # Хотторн способностью перебросил жетон
    res = fight.move([2], action=0)
    assert info(fight) == Korbin.ID
    result_hit = fight.extraMove()
    assert result_hit == 0
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    print("По итогу прилетело {}".format(result_hit))
    assert info(fight) == Korbin.ID
    print("_______________________-")
    # Корбин пытается использовать способность, но количество молний недостаточно
    res = fight.move([], action=0)
    result_hit = fight.extraMove()
    assert result_hit == 0
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    print("По итогу прилетело {}".format(result_hit))
    res = fight.move([1])
    result_hit = fight.extraMove()
    assert result_hit == 1
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    print("По итогу прилетело {}".format(result_hit))
    assert info(fight) == Hotorn.ID
    print("_______________________-")
    res = fight.move([2])
    result_hit = fight.extraMove()
    assert result_hit == 1
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    print("По итогу прилетело {}".format(result_hit))
    assert info(fight) == Hotorn.ID
    res = fight.move([0, 1, 2])
    result_hit = fight.extraMove([1])
    assert result_hit == 3
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    print("По итогу прилетело {}".format(result_hit))
    assert info(fight) == Korbin.ID
    #
    res = fight.move([0], action=0)
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    print("По итогу прилетело {}".format(result_hit))
    assert info(fight) == Hotorn.ID
    res = fight.move([], action=0)
    assert info(fight) == Korbin.ID
    res = fight.move([2])
    assert info(fight) == Korbin.ID

# battle_example()

def test_battle_example2():
    random.seed(3)
    from battle_basic import Battle, generateCreature
    from items import heroesItems, skill_block, LaurelNative, \
        MokNative

    cards = skill_block()

    Mok = generateCreature(10, heroesItems["Mok"], [MokNative()], firstMove=True, card_block=cards, ID=123)
    Laurel = generateCreature(10, heroesItems["Laurel"], [LaurelNative(minPoints=0)], firstMove=False, card_block=cards,
                              ID=333)
    Mok.wisdom = 5  #Допустим, что он умный
    assert Mok.getIni() == 1
    assert Laurel.getIni() == 1
    fight = Battle(Mok, Laurel)

    def info(fight):
        ID = fight.getActiveHeroID()
        if Mok.ID == ID:
            print("Ходит Мок")
        elif Laurel.ID == ID:
            print("Ходит Лаурель")
        print("Мок: ", Mok.getActiveItems(), Mok.getActiveActions())
        print("Лаурель, ", Laurel.getActiveItems(), Laurel.getActiveActions())
        return ID

    assert info(fight) == Mok.ID
    res = fight.move([0], action=0)
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    result_hit = fight.extraMove([1])
    print("По итогу прилетело {}".format(result_hit))
    assert info(fight) == Laurel.ID
    fight.move([1], action=0)
    print("Прилетает урон на {}, можно защититься жетоном {}".format(res["value"], res["type"]))
    result_hit = fight.extraMove([0])
    print("По итогу прилетело {}".format(result_hit))
    assert info(fight) == Mok.ID


