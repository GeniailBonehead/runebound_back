from items import ActionMoving


class GenerateCreature:
    """ Базовый класс создания существ """
    hp = 1
    items = []
    firstMove = False
    actions = []
    id = 0
    card_block = False
    wisdom = 1
    strength = 1
    eye = 1

    def __init__(self, hp, items, actions, first_move, card_block, id=0):
        self.hp = hp
        self.items = items
        self.firstMove = first_move
        for action in actions:
            action.set_hero(self)
        self.actions = actions
        self.id = id
        self.card_block = card_block

    def get_hit(self, damage):
        """ Обработка получения урона """
        self.hp -= damage
        if self.hp < 1:
            self.die()

    def die(self):
        """ Обработка смерти """
        return "dead"

    def activate_actions(self):
        pass

    def get_active_items(self):
        """ Текущие предметы  """
        res = []
        for item in self.items:
            if item.active:
                res.append(item.get_item_state())
        return res

    def get_active_actions(self):
        """ Текущие активные жетоны """
        res = []
        for action in self.actions:
            if action.active:
                res.append(action)
        return res

    def get_item_by_id(self, id):
        """ Получить предмет по идентификатору """
        if len(self.items) > id:
            return self.items[id]

    def get_action_by_id(self, id):
        """ Получить действие по идентификатору """
        if len(self.actions) > id:
            return self.actions[id]

    def randomize(self):
        """ Случайный бросок всех предметов """
        for item in self.items:
            item.random_state()

    @property
    def ini(self):
        ini = 0
        for item in self.items:
            # print(type(item))
            ini += item.item[item.state].first_move
        return ini

    @property
    def get_wisdom(self):
        return self.wisdom

    @property
    def get_strength(self):
        return self.strength

    @property
    def get_eye(self):
        return self.eye

    def activate_all(self):
        """ Активировать все предметы """
        for item in self.items:
            item.activate()
        for action in self.actions:
            action.activate()

    def check_card_block(self, max_cards=1, count=False):
        return self.card_block.check(max_cards=max_cards, count=count)


class Battle:
    """ Базовый класс битвы """
    player1 = None
    player2 = None
    round = 0
    moveDone = False
    activeHero = None
    tempGotDMG = {"value": 0, "type": None}

    def set_ini_scale(self, first, second):
        """ Установить шкалу инициативы """
        ini1 = first.ini()
        ini2 = second.ini()
        if ini1 > ini2:
            self.player1 = first
            self.player2 = second
        elif ini1 < ini2:
            self.player1 = second
            self.player2 = first
        else:
            if first.first_move:
                self.player1 = first
                self.player2 = second
            else:
                self.player1 = second
                self.player2 = first

    def __init__(self, first, second):
        """ Первый ход, может татарское решение, ХЗ """
        self.set_ini_scale(first, second)
        self.turn()

    def turn(self):
        """ Новый круг """
        self.player1.randomize()
        self.player2.randomize()
        self.round += 1
        self.moveDone = False
        self.set_ini_scale(self.player1, self.player2)
        self.player1.activate_all()
        self.player2.activate_all()
        print("-------------round {}, fight!-----------------".format(self.round))

    def get_active_hero_id(self):
        """ Получить идентификатор текущего героя """
        if not self.moveDone:
            if len(self.player1.get_active_items()) == 0 and len(self.player1.get_active_actions()) == 0:
                if len(self.player2.get_active_items()) == 0 and len(self.player2.get_active_actions()) == 0:
                    self.turn()
                    return self.get_active_hero_id()
                else:
                    return self.player2.id
            return self.player1.id
        else:
            if len(self.player2.get_active_items()) == 0 and len(self.player2.get_active_actions()) == 0:
                if len(self.player1.get_active_items()) == 0 and len(self.player1.get_active_actions()) == 0:
                    self.turn()
                    return self.get_active_hero_id()
                else:
                    return self.player1.id
            return self.player2.id

    def get_active_player(self):
        if not self.moveDone:
            if len(self.player1.get_active_items()) == 0 and len(self.player1.get_active_actions()) == 0:
                if len(self.player2.get_active_items()) != 0 and len(self.player2.get_active_actions()) == 0:
                    return self.player2
            return self.player1
        else:
            if len(self.player2.get_active_items()) == 0 and len(self.player2.get_active_actions()) == 0:
                if len(self.player1.get_active_items()) != 0 and len(self.player1.get_active_actions()) == 0:
                    return self.player1
            return self.player2

    def move(self, moving_ids, action=None, to_enemy=True, item_id=-1, skill=None):
        """ Действие, направленное на жетон или на одного из игроков """
        player = self.get_active_player()
        hero_target = None
        if to_enemy:
            hero_target = self.player2 if player == self.player1 else self.player1
        print(f"действие направлено на {hero_target.ID}")

        typ = None
        res = {'value': 0, "type": None}
        # if self.moveDone:
        #     player = self.player2
        # else:
        #     player = self.player1

        if action is not None:
            action_points = 0
            for movingID in moving_ids:
                if player.get_item_by_id(movingID).active:
                    if isinstance(player.get_item_by_id(movingID).get_item_state(), ActionMoving):
                        action_points += player.get_item_by_id(movingID).do(hero_target, item_id)
            action_res = player.getActionByID(action).do(item_ids=moving_ids, action_points=action_points)
            player.getActionByID(action).deactivate()
            if action_res and ("value" in action_res):
                res["value"] += action_res["value"]
                res["type"] = action_res["type"]
        else:
            for movingID in moving_ids:
                if not player.get_item_by_id(movingID).active:
                    print("Жетон неактивен")
                if not typ:
                    typ = type(player.get_item_by_id(movingID))
                if not isinstance(typ, type(player.get_item_by_id(movingID))):
                    # Проверка что одинаковые типы
                    return False
                itemRes = player.get_item_by_id(movingID).do(hero_target, item_id, to_enemy)
                if itemRes and ("value" in itemRes):
                    res["value"] += itemRes["value"]
                    res["type"] = itemRes["type"]
                player.get_item_by_id(movingID).deactivate()
        self.moveDone = not self.moveDone
        self.tempGotDMG = res
        return res

    def extra_move(self, moving_ids=None):
        """ Защита от действия """
        if moving_ids is None or len(moving_ids) == 0:
            damage = self.tempGotDMG["value"]
            self.tempGotDMG = {"value": 0, "type": None}
            return damage
        player_moving_id = self.moveDone
        player = self.player2 if player_moving_id else self.player1
        typ = type(player.get_item_by_id(moving_ids[0]))
        res = {'value': 0, "type": None}
        for movingID in moving_ids:
            if type(player.get_item_by_id(moving_ids[0])) != typ:
                return self.tempGotDMG["value"]
            item_res = player.get_item_by_id(movingID).extra_move()
            res["value"] += item_res["value"]
            res["type"] = item_res["type"]
        damage = self.tempGotDMG["value"]
        if self.tempGotDMG["type"] == res["type"]:
            damage -= res["value"]
        return max(damage, 0)

    def flee(self):
        pass
