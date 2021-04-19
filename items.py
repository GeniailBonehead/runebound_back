import random
# фиксация рандомизатора,убрать в релизе!
# random.seed(3)

class warMoving:
    """Действие, написанное на жетоне или сгенерированное иным способом"""
    typ = "-"
    value = 1
    firstMove = False

    def __init__(self, typ="-", value=1, firstMove=False):
        self.typ = typ
        self.value = value
        self.firstMove = firstMove

    def tellTyp(self):
        return self.typ

    def do(self, player, targetItemID, koef, toEnemy=True):
        None

    def extraMove(self, koef):
        return {"value": self.value * koef, "type": type(self)}


class defenseMoving(warMoving):
    """Защита от удара"""

    def __init__(self, value=1, firstMove=False):
        self.typ = "defense"
        self.value = value
        self.firstMove = firstMove


class magicDamageMoving(warMoving):
    """Нанесение урона"""
    block = defenseMoving

    def __init__(self, value=1, block=defenseMoving, firstMove=False):
        self.typ = "magic_damage"
        self.value = value
        self.block = block
        self.firstMove = firstMove

    def do(self, player, targetItemID, koef, toEnemy=True):
        # player.getHit(self.value * koef)
        return {"value": self.value * koef, "type": self.block}


class damageMoving(warMoving):
    """Нанесение урона"""
    block = defenseMoving

    def __init__(self, value=1, block=defenseMoving, firstMove=False):
        self.typ = "damage"
        self.value = value
        self.block = block
        self.firstMove = firstMove

    def do(self, player, targetItemID, koef, toEnemy=True):
        # player.getHit(self.value * koef)
        return {"value": self.value * koef, "type": self.block}


class reverseMoving(warMoving):
    """Переворот жетона"""

    def __init__(self, firstMove=False):
        self.typ = "reverse"
        self.firstMove = firstMove

    def do(self, player, targetItemID, koef, toEnemy=True):
        if toEnemy:
            player.getItemByID(targetItemID).randomState()
        else:
            player.getItemByID(targetItemID).reverse()


class doubleMoving(warMoving):
    """Удвоение жетона"""

    def __init__(self, firstMove=False):
        self.typ = "double"
        self.firstMove = firstMove

    def do(self, player, targetItemID, koef, toEnemy=False):
        player.getItemByID(targetItemID).koef *= 2


class deleteMoving(warMoving):
    """убрать жетон"""

    def __init__(self, firstMove=False):
        self.typ = "delete"
        self.firstMove = firstMove

    def do(self, player, targetItemID, koef, toEnemy=True):
        player.getItemByID(targetItemID).active = False


class actionMoving(warMoving):
    """Особое действие"""

    def __init__(self, value=1, firstMove=False):
        self.typ = "action"
        self.value = value
        self.firstMove = firstMove

    def do(self, player, targetItemID, koef, toEnemy=False):
        return self.value * koef


class activateMoving(warMoving):
    """Особое действие"""

    def __init__(self, firstMove=False):
        self.typ = "activate"
        self.firstMove = firstMove

    def do(self, player, targetItemID, koef, toEnemy=True):
        player.getItemByID(targetItemID).active = True


class warItem:
    """Игровой жетон"""
    item = [None, None]
    state = 0
    active = True
    koef = 1        # коеффициент усиления

    def __init__(self, side1, side2):
        self.item = [side1, side2]
        self.randomState()

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

    def setState(self, state):
        """Установить сторону жетона"""
        self.state = bool(state)

    def randomState(self):
        """Переброс/бросок жетона"""
        self.state = random.randint(0, 1)

    def getItemState(self):
        return self.item[self.state]

    def reverse(self):
        """перевернуть жетон"""
        self.state = not self.state

    def do(self, player, targetItemID, toEnemy=True):
        if not self.active:
            return None
        else:
            return self.item[self.state].do(player, targetItemID, self.koef, toEnemy=toEnemy)

    def extraMove(self):
        """Действие в ответ (защита от удара)"""
        self.active = False
        return self.item[self.state].extraMove(self.koef)


armourItems = {
    'a8': warItem(defenseMoving(), warMoving(firstMove=True)),
    'a9': warItem(warMoving(), reverseMoving()),
    'a10': warItem(defenseMoving(), warMoving()),
    'a11': warItem(magicDamageMoving(firstMove=True), actionMoving(2)),
    'b9': warItem(defenseMoving(), actionMoving(firstMove=True)),
    'b10': warItem(defenseMoving(2), damageMoving()),
    'b11': warItem(actionMoving(), defenseMoving(2)),
    'c8': warItem(actionMoving(), reverseMoving()),
    'c9': warItem(defenseMoving(), warMoving(firstMove=True)),
    'c10': warItem(magicDamageMoving(), doubleMoving()),
    'c11': warItem(doubleMoving(firstMove=True), actionMoving()),
    'c12': warItem(magicDamageMoving(), defenseMoving(2)),
}
weaponItems = {
    'a3': warItem(damageMoving(), warMoving()),
    'a4': warItem(warMoving(), damageMoving(2)),
    'a5': warItem(doubleMoving(), actionMoving(2)),
    'a6': warItem(actionMoving(firstMove=True), damageMoving(2)),
    'a7': warItem(actionMoving(), magicDamageMoving(2, firstMove=True)),
    'b4': warItem(warMoving(), damageMoving(1)),
    'b5': warItem(warMoving(firstMove=True), damageMoving(1)),
    'b6': warItem(actionMoving(firstMove=True), damageMoving(1)),
    'b7': warItem(actionMoving(firstMove=True), magicDamageMoving(1)),
    'b8': warItem(reverseMoving(), damageMoving(3)),
    'c3': warItem(actionMoving(), magicDamageMoving(1)),
    'c4': warItem(damageMoving(), reverseMoving()),
    'c5': warItem(defenseMoving(), damageMoving(firstMove=True)),
    'c6': warItem(damageMoving(), actionMoving(2)),
    'c7': warItem(damageMoving(2, firstMove=True), defenseMoving(1)),
    'd4': warItem(damageMoving(), reverseMoving(firstMove=True)),
}
backpackItems = {
    'a1': warItem(warMoving(), reverseMoving(firstMove=True)),
    'a2': warItem(magicDamageMoving(), actionMoving(1)),
    'b1': warItem(magicDamageMoving(), reverseMoving()),
    'b2': warItem(actionMoving(), reverseMoving()),
    'b3': warItem(damageMoving(), reverseMoving()),
    'c1': warItem(doubleMoving(), actionMoving(1)),
    'c2': warItem(actionMoving(2, firstMove=True), doubleMoving()),
}
heroesItems = {
    'Korbin': [
        warItem(damageMoving(2), actionMoving()),
        warItem(damageMoving(firstMove=True), defenseMoving()),
        warItem(reverseMoving(), damageMoving()),
    ],
    'Laurel': [
        warItem(damageMoving(2), actionMoving()),
        warItem(defenseMoving(), damageMoving(firstMove=True)),
        warItem(actionMoving(firstMove=True), reverseMoving()),
    ],
    'Lissa': [
        warItem(damageMoving(2), defenseMoving()),
        warItem(magicDamageMoving(firstMove=True), reverseMoving()),
        warItem(reverseMoving(firstMove=True), actionMoving(firstMove=True)),
    ],
    'Hotorn': [
        warItem(damageMoving(2), defenseMoving()),
        warItem(damageMoving(firstMove=True), reverseMoving()),
        warItem(damageMoving(firstMove=True), warMoving()),
    ],
    'Mok': [
        warItem(magicDamageMoving(2), doubleMoving()),
        warItem(reverseMoving(firstMove=True), defenseMoving()),
        warItem(actionMoving(firstMove=True), damageMoving()),
    ],
    'Torn': [
        warItem(actionMoving(2), magicDamageMoving()),
        warItem(doubleMoving(), magicDamageMoving(firstMove=True)),
        warItem(reverseMoving(firstMove=True), magicDamageMoving()),
    ],
}

mobBasic = [
    warItem(damageMoving(), defenseMoving()),
    warItem(damageMoving(), reverseMoving()),
    warItem(actionMoving(), damageMoving(firstMove=True)),
    warItem(warMoving(firstMove=True), damageMoving()),
    warItem(warMoving(firstMove=True), doubleMoving()),
]

mobStrong = mobBasic + [
    warItem(actionMoving(firstMove=True), damageMoving(2)),
]

Vorakesh = mobStrong + [
    warItem(actionMoving(2), damageMoving())
]
Morgat = mobStrong + [
    warItem(damageMoving(2), actionMoving())
]


class action():
    minPoints = 1
    hero = False
    active = True

    def __init__(self, minPoints=1):
        self.minPoints = minPoints

    def setHero(self, hero):
        self.hero = hero

    def do(self, itemIDs=[], actionPoints=1):
        if actionPoints >= self.minPoints:
            for itemID in itemIDs:
                self.hero.getItemByID(itemID).deactivate()
            return self.calculate(itemIDs, actionPoints)

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

    def calculate(self, itemIDs, actionPoints):
        None

    # def do(self, heroTarget, actionPoints=1, itemIDs=[]):
    #     None


class LaurelNative(action):
    minPoints = 1

    def __init__(self, minPoints=1):
        self.minPoints = minPoints

    def calculate(self, itemIDs=[], actionPoints=1):
        if len(itemIDs) > 0:
            itemID = itemIDs[0]
        else:
            return None
        self.hero.getItemByID(itemID).randomState()
        self.hero.getItemByID(itemID).activate()


class MokNative(action):
    minPoints = 2

    def calculate(self, itemIDs=[], actionPoints=1):
        value = self.hero.checkCardsBlock(max_cards=self.hero.getWisdom()+1, count=True)[0]
        return {"value": value, "type": defenseMoving}


class HotornNative(action):
    minPoints = 0

    def __init__(self, minPoints=0):
        self.minPoints = minPoints

    def calculate(self, itemIDs=[], actionPoints=0):
        for itemID in itemIDs:
            self.hero.getItemByID(itemID).randomState()
            self.hero.getItemByID(itemID).activate()
        # return {"value": value, "type": defenseMoving}
        None


class KorbinNative(action):
    minPoints = 1

    def calculate(self, itemIDs=[], actionPoints=0):
        return {"value": actionPoints, "type": actionMoving}

    def block(self, item):
        None

class skill():
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
    {'id': 1, 'card': skill(fight=1)},
    {'id': 2, 'card': skill(fight=1, success=True)},
    {'id': 3, 'card': skill(fight=1)},
    {'id': 4, 'card': skill(fight=1)},
    {'id': 5, 'card': skill(fight=1)},
    {'id': 6, 'card': skill(fight=1)},
    {'id': 7, 'card': skill(fight=1)},
    {'id': 8, 'card': skill(fight=1, success=True)},
    {'id': 9, 'card': skill(fight=1)},
    {'id': 10, 'card': skill(fight=1)},
    {'id': 11, 'card': skill(fight=1)},
    {'id': 12, 'card': skill(fight=1)},
    {'id': 13, 'card': skill(fight=1)},
    {'id': 14, 'card': skill(fight=1)},
    {'id': 15, 'card': skill(fight=1, success=True)},
    {'id': 16, 'card': skill(fight=1, success=True)},
    {'id': 17, 'card': skill(fight=1, success=True)},
    {'id': 18, 'card': skill(fight=1, success=True)},
    {'id': 19, 'card': skill(fight=1)},
    {'id': 20, 'card': skill(fight=1, success=True)},
    {'id': 21, 'card': skill(fight=1)},
    {'id': 22, 'card': skill(fight=1)},
    {'id': 23, 'card': skill(fight=1)},
    {'id': 24, 'card': skill(fight=1)},
    {'id': 25, 'card': skill(fight=1)},
    {'id': 26, 'card': skill(fight=1)},
    {'id': 27, 'card': skill(fight=1)},
    {'id': 28, 'card': skill(fight=1)},
    {'id': 29, 'card': skill(fight=1)},
    {'id': 30, 'card': skill(fight=1, success=True)},
    {'id': 31, 'card': skill(fight=1, success=True)},
    {'id': 32, 'card': skill(fight=1)},
    {'id': 33, 'card': skill(fight=1)},
    {'id': 34, 'card': skill(fight=1)},
    {'id': 35, 'card': skill(fight=1)},
    {'id': 36, 'card': skill(fight=1)},
    {'id': 37, 'card': skill(fight=1)},
    {'id': 38, 'card': skill(fight=1)},
    {'id': 39, 'card': skill(fight=1)},
    {'id': 40, 'card': skill(fight=1)},
    {'id': 41, 'card': skill(fight=1)},
    {'id': 42, 'card': skill(fight=1)},
    {'id': 43, 'card': skill(fight=1)},
    {'id': 44, 'card': skill(fight=1)},
    {'id': 45, 'card': skill(fight=1)},
    {'id': 46, 'card': skill(fight=1)},
    {'id': 47, 'card': skill(fight=1)},
    {'id': 48, 'card': skill(fight=1)},
    {'id': 49, 'card': skill(fight=1)},
    {'id': 50, 'card': skill(fight=1)},
    {'id': 51, 'card': skill(fight=1)},
    {'id': 52, 'card': skill(fight=1)},
    {'id': 53, 'card': skill(fight=1)},
    {'id': 54, 'card': skill(fight=1)},
    {'id': 55, 'card': skill(fight=1)},
    {'id': 56, 'card': skill(fight=1)},
    {'id': 57, 'card': skill(fight=1)},
    {'id': 58, 'card': skill(fight=1, success=True)},
    {'id': 59, 'card': skill(fight=1)},
    {'id': 60, 'card': skill(fight=1)},
]


class skill_block():
    state = skills
    disabled_cards = []

    def __init__(self):
        self.mix()

    def mix(self):
        random.shuffle(self.state)

    def getCard(self):
        card = self.state.pop()
        return card

    def getSize(self):
        return len(self.state)

    def throwCard(self, card):
        self.disabled_cards.append(card)

    def check(self, max_cards=1, count=False):
        checked_cards = []
        value = False
        for i in range(max_cards):
            card = self.getCard()
            checked_cards.append(card)
            self.throwCard(card)
            if card["card"].success:
                if not count:
                    return True, checked_cards
                else:
                    value += 1
        print("Вытащены карты ", checked_cards)
        return value, checked_cards

