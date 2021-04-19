from copy import copy
from items import actionMoving

class generateCreature:
    hp = 1
    items = []
    firstMove = False
    actions = []
    ID = 0
    card_block = False
    wisdom = 1
    strench = 1
    eye = 1

    def __init__(self, hp, items, actions, firstMove, card_block, ID=0):
        self.hp = hp
        self.items = items
        self.firstMove = firstMove
        for action in actions:
            action.setHero(self)
        self.actions = actions
        self.ID = ID
        self.card_block = card_block

    def getHit(self, damage):
        self.hp -= damage
        if self.hp < 1:
            self.die()

    def die(self):
        return "dead"

    def activateActions(self):
        None

    def getActiveItems(self):
        res = []
        for item in self.items:
            if item.active:
                res.append(item.getItemState())
        return res

    def getActiveActions(self):
        res = []
        for action in self.actions:
            if action.active:
                res.append(action)
        return res

    def getItemByID(self, id):
        if len(self.items) > id:
            return self.items[id]

    def getActionByID(self, id):
        if len(self.actions) > id:
            return self.actions[id]

    def randomize(self):
        for item in self.items:
            item.randomState()

    def getIni(self):
        ini = 0
        for item in self.items:
            # print(type(item))
            ini += item.item[item.state].firstMove
        return ini

    def getWisdom(self):
        return self.wisdom

    def getStrench(self):
        return self.strench

    def getEye(self):
        return self.eye

    def activateAll(self):
        for item in self.items:
            item.activate()
        for action in self.actions:
            action.activate()

    def checkCardsBlock(self, max_cards=1, count=False):
        return self.card_block.check(max_cards=max_cards, count=count)


class Battle:
    player1 = None
    player2 = None
    round = 0
    moveDone = False
    activeHero = None
    tempGotDMG = {"value": 0, "type": None}

    def setIniScale(self, first, second):
        ini1 = first.getIni()
        ini2 = second.getIni()
        if ini1 > ini2:
            self.player1 = first
            self.player2 = second
        elif ini1 < ini2:
            self.player1 = second
            self.player2 = first
        else:
            if first.firstMove:
                self.player1 = first
                self.player2 = second
            else:
                self.player1 = second
                self.player2 = first

    def __init__(self, first, second):
        """Первый ход, может татарское решение, ХЗ"""
        self.setIniScale(first, second)
        self.turn()

    def turn(self):
        """новый круг"""
        self.player1.randomize()
        self.player2.randomize()
        self.round += 1
        self.moveDone = False
        self.setIniScale(self.player1, self.player2)
        self.player1.activateAll()
        self.player2.activateAll()
        print("-------------round {}, fight!-----------------".format(self.round))

    def getActiveHeroID(self):
        if not self.moveDone:
            if len(self.player1.getActiveItems()) == 0 and len(self.player1.getActiveActions()) == 0:
                if len(self.player2.getActiveItems()) == 0 and len(self.player2.getActiveActions()) == 0:
                    self.turn()
                    return self.getActiveHeroID()
                else:
                    return self.player2.ID
            return self.player1.ID
        else:
            if len(self.player2.getActiveItems()) == 0 and len(self.player2.getActiveActions()) == 0:
                if len(self.player1.getActiveItems()) == 0 and len(self.player1.getActiveActions()) == 0:
                    self.turn()
                    return self.getActiveHeroID()
                else:
                    return self.player1.ID
            return self.player2.ID

    def getActivePlayer(self):
        if not self.moveDone:
            if len(self.player1.getActiveItems()) == 0 and len(self.player1.getActiveActions()) == 0:
                if len(self.player2.getActiveItems()) != 0 and len(self.player2.getActiveActions()) == 0:
                    return self.player2
            return self.player1
        else:
            if len(self.player2.getActiveItems()) == 0 and len(self.player2.getActiveActions()) == 0:
                if len(self.player1.getActiveItems()) != 0 and len(self.player1.getActiveActions()) == 0:
                    return self.player1
            return self.player2

    def move(self, movingIDs, action=None, toEnemy=True, itemID=-1, skill=None):
        """Действие, направленное на жетон или на одного из игроков"""
        player = self.getActivePlayer()
        if toEnemy:
            if player == self.player1:
                heroTarget = self.player2
            else:
                heroTarget = self.player1
        print("действие направлено на "+str(heroTarget.ID))

        typ = None
        res = {'value': 0, "type": None}
        # if self.moveDone:
        #     player = self.player2
        # else:
        #     player = self.player1

        if action != None:
            actionPoints = 0
            for movingID in movingIDs:
                if player.getItemByID(movingID).active:
                    if isinstance(player.getItemByID(movingID).getItemState(), actionMoving):
                        actionPoints += player.getItemByID(movingID).do(heroTarget, itemID)
            actionRes = player.getActionByID(action).do(itemIDs=movingIDs, actionPoints=actionPoints)
            player.getActionByID(action).deactivate()
            if actionRes and ("value" in actionRes):
                res["value"] += actionRes["value"]
                res["type"] = actionRes["type"]
        else:
            for movingID in movingIDs:
                if not player.getItemByID(movingID).active:
                    print("Жетон неактивен")
                if not typ:
                    typ = type(player.getItemByID(movingID))
                if not (typ == type(player.getItemByID(movingID))):
                    # Проверка что одинаковые типы
                    return False
                itemRes = player.getItemByID(movingID).do(heroTarget, itemID, toEnemy)
                if itemRes and ("value" in itemRes):
                    res["value"] += itemRes["value"]
                    res["type"] = itemRes["type"]
                player.getItemByID(movingID).deactivate()
        self.moveDone = not self.moveDone
        self.tempGotDMG = res
        return res

    def extraMove(self, movingIDs=None):
        """Защита от действия"""
        if movingIDs == None or len(movingIDs) == 0:
            damage = self.tempGotDMG["value"]
            self.tempGotDMG = {"value": 0, "type": None}
            return damage
        playerMovingID = self.moveDone
        if playerMovingID == False:
            player = self.player1
            # res = self.player1.getItemByID(movingID).extraMove()
        else:
            player = self.player2
            # res = self.player2.getItemByID(movingID).extraMove()
        typ = type(player.getItemByID(movingIDs[0]))
        res = {'value': 0, "type": None}
        for movingID in movingIDs:
            if type(player.getItemByID(movingIDs[0])) != typ:
                return self.tempGotDMG["value"]
            itemRes = player.getItemByID(movingID).extraMove()
            res["value"] += itemRes["value"]
            res["type"] = itemRes["type"]
        damage = self.tempGotDMG["value"]
        if self.tempGotDMG["type"] == res["type"]:
            damage -= res["value"]
        return max(damage, 0)

    def flee(self):
        None

################################################################################
