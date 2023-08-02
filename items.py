import random
# random.seed(3)


class WarMoving:
    """ Действие, написанное на жетоне или сгенерированное иным способом """
    typ = "-"
    value = 1
    first_move = False

    def __init__(self, typ="-", value=1, first_move=False):
        self.typ = typ
        self.value = value
        self.first_move = first_move

    def tell_typ(self):
        return self.typ

    def do(self, player, target_item_id, koef, to_enemy=True):
        pass

    def extra_move(self, koef):
        return {"value": self.value * koef, "type": type(self)}


class DefenseMoving(WarMoving):
    """ Защита от удара """

    def __init__(self, value=1, first_move=False):
        super().__init__(typ="defense", value=value, first_move=first_move)


class MagicDamageMoving(WarMoving):
    """ Нанесение урона """
    block = DefenseMoving

    def __init__(self, value=1, block=DefenseMoving, first_move=False):
        super().__init__(typ="magic_damage", value=value, first_move=first_move)
        self.block = block

    def do(self, player, target_item_id, koef, to_enemy=True):
        # player.getHit(self.value * koef)
        return {"value": self.value * koef, "type": self.block}


class DamageMoving(WarMoving):
    """ Нанесение урона """
    block = DefenseMoving

    def __init__(self, value=1, block=DefenseMoving, first_move=False):
        super().__init__(typ="damage", value=value, first_move=first_move)
        self.block = block

    def do(self, player, target_item_id, koef, to_enemy=True):
        # player.getHit(self.value * koef)
        return {"value": self.value * koef, "type": self.block}


class ReverseMoving(WarMoving):
    """Переворот жетона"""

    def __init__(self, first_move=False):
        super().__init__(typ="reverse", first_move=first_move)

    def do(self, player, target_item_id, koef, to_enemy=True):
        if to_enemy:
            player.get_item_by_id(target_item_id).random_state()
        else:
            player.get_item_by_id(target_item_id).reverse()


class DoubleMoving(WarMoving):
    """ Удвоение жетона """

    def __init__(self, first_move=False):
        super().__init__(typ="double", first_move=first_move)

    def do(self, player, target_item_id, koef, to_enemy=False):
        player.get_item_by_id(target_item_id).koef *= 2


class DeleteMoving(WarMoving):
    """ Убрать жетон """

    def __init__(self, first_move=False):
        super().__init__(typ="delete", first_move=first_move)

    def do(self, player, target_item_id, koef, to_enemy=True):
        player.get_item_by_id(target_item_id).active = False


class ActionMoving(WarMoving):
    """Особое действие"""

    def __init__(self, value=1, first_move=False):
        super().__init__(typ="action", value=value, first_move=first_move)

    def do(self, player, target_item_id, koef, to_enemy=False):
        return self.value * koef


class ActivateMoving(WarMoving):
    """Особое действие"""

    def __init__(self, first_move=False):
        super().__init__(typ="activate", first_move=first_move)

    def do(self, player, target_item_id, koef, to_enemy=True):
        player.get_item_by_id(target_item_id).active = True


class WarItem:
    """Игровой жетон"""
    item = [None, None]
    state = 0
    active = True
    koef = 1        # коеффициент усиления

    def __init__(self, side1, side2):
        self.item = [side1, side2]
        self.random_state()

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

    def set_state(self, state):
        """ Установить сторону жетона """
        self.state = bool(state)

    def random_state(self):
        """ Переброс/бросок жетона """
        self.state = random.randint(0, 1)

    def get_item_state(self):
        return self.item[self.state]

    def reverse(self):
        """ Перевернуть жетон """
        self.state = not self.state

    def do(self, player, targetItemID, to_enemy=True):
        if not self.active:
            return None
        else:
            return self.item[self.state].do(player, targetItemID, self.koef, to_enemy=to_enemy)

    def extra_move(self):
        """ Действие в ответ (защита от удара) """
        self.active = False
        return self.item[self.state].extra_move(self.koef)


armourItems = {
    'a8': WarItem(DefenseMoving(), WarMoving(first_move=True)),
    'a9': WarItem(WarMoving(), ReverseMoving()),
    'a10': WarItem(DefenseMoving(), WarMoving()),
    'a11': WarItem(MagicDamageMoving(first_move=True), ActionMoving(2)),
    'b9': WarItem(DefenseMoving(), ActionMoving(first_move=True)),
    'b10': WarItem(DefenseMoving(2), DamageMoving()),
    'b11': WarItem(ActionMoving(), DefenseMoving(2)),
    'c8': WarItem(ActionMoving(), ReverseMoving()),
    'c9': WarItem(DefenseMoving(), WarMoving(first_move=True)),
    'c10': WarItem(MagicDamageMoving(), DoubleMoving()),
    'c11': WarItem(DoubleMoving(first_move=True), ActionMoving()),
    'c12': WarItem(MagicDamageMoving(), DefenseMoving(2)),
}
weaponItems = {
    'a3': WarItem(DamageMoving(), WarMoving()),
    'a4': WarItem(WarMoving(), DamageMoving(2)),
    'a5': WarItem(DoubleMoving(), ActionMoving(2)),
    'a6': WarItem(ActionMoving(first_move=True), DamageMoving(2)),
    'a7': WarItem(ActionMoving(), MagicDamageMoving(2, first_move=True)),
    'b4': WarItem(WarMoving(), DamageMoving(1)),
    'b5': WarItem(WarMoving(first_move=True), DamageMoving(1)),
    'b6': WarItem(ActionMoving(first_move=True), DamageMoving(1)),
    'b7': WarItem(ActionMoving(first_move=True), MagicDamageMoving(1)),
    'b8': WarItem(ReverseMoving(), DamageMoving(3)),
    'c3': WarItem(ActionMoving(), MagicDamageMoving(1)),
    'c4': WarItem(DamageMoving(), ReverseMoving()),
    'c5': WarItem(DefenseMoving(), DamageMoving(first_move=True)),
    'c6': WarItem(DamageMoving(), ActionMoving(2)),
    'c7': WarItem(DamageMoving(2, first_move=True), DefenseMoving(1)),
    'd4': WarItem(DamageMoving(), ReverseMoving(first_move=True)),
}
backpackItems = {
    'a1': WarItem(WarMoving(), ReverseMoving(first_move=True)),
    'a2': WarItem(MagicDamageMoving(), ActionMoving(1)),
    'b1': WarItem(MagicDamageMoving(), ReverseMoving()),
    'b2': WarItem(ActionMoving(), ReverseMoving()),
    'b3': WarItem(DamageMoving(), ReverseMoving()),
    'c1': WarItem(DoubleMoving(), ActionMoving(1)),
    'c2': WarItem(ActionMoving(2, first_move=True), DoubleMoving()),
}
heroesItems = {
    'Korbin': [
        WarItem(DamageMoving(2), ActionMoving()),
        WarItem(DamageMoving(first_move=True), DefenseMoving()),
        WarItem(ReverseMoving(), DamageMoving()),
    ],
    'Laurel': [
        WarItem(DamageMoving(2), ActionMoving()),
        WarItem(DefenseMoving(), DamageMoving(first_move=True)),
        WarItem(ActionMoving(first_move=True), ReverseMoving()),
    ],
    'Lissa': [
        WarItem(DamageMoving(2), DefenseMoving()),
        WarItem(MagicDamageMoving(first_move=True), ReverseMoving()),
        WarItem(ReverseMoving(first_move=True), ActionMoving(first_move=True)),
    ],
    'Hotorn': [
        WarItem(DamageMoving(2), DefenseMoving()),
        WarItem(DamageMoving(first_move=True), ReverseMoving()),
        WarItem(DamageMoving(first_move=True), WarMoving()),
    ],
    'Mok': [
        WarItem(MagicDamageMoving(2), DoubleMoving()),
        WarItem(ReverseMoving(first_move=True), DefenseMoving()),
        WarItem(ActionMoving(first_move=True), DamageMoving()),
    ],
    'Torn': [
        WarItem(ActionMoving(2), MagicDamageMoving()),
        WarItem(DoubleMoving(), MagicDamageMoving(first_move=True)),
        WarItem(ReverseMoving(first_move=True), MagicDamageMoving()),
    ],
}

mobBasic = [
    WarItem(DamageMoving(), DefenseMoving()),
    WarItem(DamageMoving(), ReverseMoving()),
    WarItem(ActionMoving(), DamageMoving(first_move=True)),
    WarItem(WarMoving(first_move=True), DamageMoving()),
    WarItem(WarMoving(first_move=True), DoubleMoving()),
]

mobStrong = mobBasic + [
    WarItem(ActionMoving(first_move=True), DamageMoving(2)),
]

Vorakesh = mobStrong + [
    WarItem(ActionMoving(2), DamageMoving())
]
Morgat = mobStrong + [
    WarItem(DamageMoving(2), ActionMoving())
]


class Action:
    """ Базовый класс действий """
    minPoints = 1
    hero = False
    active = True

    def __init__(self, min_points=1):
        self.minPoints = min_points

    def set_hero(self, hero):
        self.hero = hero

    def do(self, item_ids=None, action_points=1):
        if not item_ids:
            item_ids = []
        if action_points >= self.minPoints:
            for itemID in item_ids:
                self.hero.get_item_by_id(itemID).deactivate()
            return self.calculate(item_ids, action_points)

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

    def calculate(self, itemIDs, action_points):
        pass

    # def do(self, heroTarget, actionPoints=1, itemIDs=[]):
    #     None


class LaurelNative(Action):
    minPoints = 1

    def __init__(self, min_points=1):
        super().__init__(min_points)

    def calculate(self, itemIDs=None, action_points=1):
        if not itemIDs:
            itemIDs = []
        if len(itemIDs) > 0:
            itemID = itemIDs[0]
        else:
            return
        self.hero.get_item_by_id(itemID).random_state()
        self.hero.get_item_by_id(itemID).activate()


class MokNative(Action):
    minPoints = 2

    def calculate(self, item_ids=None, action_points=1):
        item_ids = item_ids or []
        value = self.hero.check_card_block(max_cards=self.hero.get_wisdom + 1, count=True)[0]
        return {"value": value, "type": DefenseMoving}


class HotornNative(Action):
    minPoints = 0

    def __init__(self, min_points=0):
        super().__init__(min_points)

    def calculate(self, item_ids=None, action_points=0):
        item_ids = item_ids or []
        for itemID in item_ids:
            self.hero.get_item_by_id(itemID).random_state()
            self.hero.get_item_by_id(itemID).activate()
        # return {"value": value, "type": defenseMoving}
        None


class KorbinNative(Action):
    minPoints = 1

    def calculate(self, item_ids=None, action_points=0):
        item_ids = item_ids or []
        return {"value": action_points, "type": ActionMoving}

    def block(self, item):
        pass


class Skill:
    """ Применение навыка """
    cost = {'fight': 0, 'adventure': 0, 'mail': 0, 'any': 0}
    success = False
    active = True

    def __init__(self, fight=0, adventure=0, mail=0, any=0, success=False):
        self.cost['fight'] = fight
        self.cost['adventure'] = adventure
        self.cost['mail'] = mail
        self.cost['any'] = any
        self.success = success

    def disable(self):
        self.active = False


skills = [
    {'id': 1, 'card': Skill(fight=1)},
    {'id': 2, 'card': Skill(fight=1, success=True)},
    {'id': 3, 'card': Skill(fight=1)},
    {'id': 4, 'card': Skill(fight=1)},
    {'id': 5, 'card': Skill(fight=1)},
    {'id': 6, 'card': Skill(fight=1)},
    {'id': 7, 'card': Skill(fight=1)},
    {'id': 8, 'card': Skill(fight=1, success=True)},
    {'id': 9, 'card': Skill(fight=1)},
    {'id': 10, 'card': Skill(fight=1)},
    {'id': 11, 'card': Skill(fight=1)},
    {'id': 12, 'card': Skill(fight=1)},
    {'id': 13, 'card': Skill(fight=1)},
    {'id': 14, 'card': Skill(fight=1)},
    {'id': 15, 'card': Skill(fight=1, success=True)},
    {'id': 16, 'card': Skill(fight=1, success=True)},
    {'id': 17, 'card': Skill(fight=1, success=True)},
    {'id': 18, 'card': Skill(fight=1, success=True)},
    {'id': 19, 'card': Skill(fight=1)},
    {'id': 20, 'card': Skill(fight=1, success=True)},
    {'id': 21, 'card': Skill(fight=1)},
    {'id': 22, 'card': Skill(fight=1)},
    {'id': 23, 'card': Skill(fight=1)},
    {'id': 24, 'card': Skill(fight=1)},
    {'id': 25, 'card': Skill(fight=1)},
    {'id': 26, 'card': Skill(fight=1)},
    {'id': 27, 'card': Skill(fight=1)},
    {'id': 28, 'card': Skill(fight=1)},
    {'id': 29, 'card': Skill(fight=1)},
    {'id': 30, 'card': Skill(fight=1, success=True)},
    {'id': 31, 'card': Skill(fight=1, success=True)},
    {'id': 32, 'card': Skill(fight=1)},
    {'id': 33, 'card': Skill(fight=1)},
    {'id': 34, 'card': Skill(fight=1)},
    {'id': 35, 'card': Skill(fight=1)},
    {'id': 36, 'card': Skill(fight=1)},
    {'id': 37, 'card': Skill(fight=1)},
    {'id': 38, 'card': Skill(fight=1)},
    {'id': 39, 'card': Skill(fight=1)},
    {'id': 40, 'card': Skill(fight=1)},
    {'id': 41, 'card': Skill(fight=1)},
    {'id': 42, 'card': Skill(fight=1)},
    {'id': 43, 'card': Skill(fight=1)},
    {'id': 44, 'card': Skill(fight=1)},
    {'id': 45, 'card': Skill(fight=1)},
    {'id': 46, 'card': Skill(fight=1)},
    {'id': 47, 'card': Skill(fight=1)},
    {'id': 48, 'card': Skill(fight=1)},
    {'id': 49, 'card': Skill(fight=1)},
    {'id': 50, 'card': Skill(fight=1)},
    {'id': 51, 'card': Skill(fight=1)},
    {'id': 52, 'card': Skill(fight=1)},
    {'id': 53, 'card': Skill(fight=1)},
    {'id': 54, 'card': Skill(fight=1)},
    {'id': 55, 'card': Skill(fight=1)},
    {'id': 56, 'card': Skill(fight=1)},
    {'id': 57, 'card': Skill(fight=1)},
    {'id': 58, 'card': Skill(fight=1, success=True)},
    {'id': 59, 'card': Skill(fight=1)},
    {'id': 60, 'card': Skill(fight=1)},
]


class SkillBlock():
    state = skills
    disabled_cards = []

    def __init__(self):
        self.mix()

    def mix(self):
        random.shuffle(self.state)

    def get_card(self):
        card = self.state.pop()
        return card

    def get_size(self):
        return len(self.state)

    def throw_card(self, card):
        self.disabled_cards.append(card)

    def check(self, max_cards=1, count=False):
        checked_cards = []
        value = False
        for i in range(max_cards):
            card = self.get_card()
            checked_cards.append(card)
            self.throw_card(card)
            if card["card"].success:
                if not count:
                    return True, checked_cards
                else:
                    value += 1
        print(f"Вытащены карты {checked_cards}")
        return value, checked_cards

