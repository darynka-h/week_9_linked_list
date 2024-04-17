"""
In Minecraft, players explore a blocky, pixelated procedurally 
generated, three-dimensional world with virtually infinite 
terrain. Players can discover and extract raw materials, 
craft tools and items, and build structures, earthworks, 
and machines. Depending on their chosen game mode, 
players can fight hostile mobs, as well as cooperate 
with or compete against other players in the same world.
We will explore it here.
"""
# from minecraft import *

class Entity:
    pass

class Player(Entity):
    __inventory = {'Food': [], 'Armor': [], 'Weapon': []}
    difficulty = 'Normal'

    def __init__(self, name) -> None:
        self.name = name
        self.health = 20
        self.damage = 4
        self.food_level = 20

# assert str(player) == "This is Steve with health 20 and food level 20. He doesn't have armor."
#     assert str([player]) == "[Name: Steve, Health: 20, Food level: 20, Armor: []]"
    def __str__(self) -> str:
        len_amour = len(self.__inventory['Armor'])
        if len_amour == 0:
            return f"This is {self.name} with health {self.health} and food level {self.food_level}. He doesn't have armor."
        if len_amour == 1:
            return f"This is {self.name} with health {self.health} and food level {self.food_level}. His armor: {self.__inventory['Armor'][0].name_armor}."
        arm_names = [el.name_armor for el in self.__inventory['Armor']]
        return f"This is {self.name} with health {self.health} and food level {self.food_level}. His armor: {', '.join(arm_names)}."

    def __repr__(self) -> str:
        if len(self.__inventory['Armor']) == 0:
            return f"Name: {self.name}, Health: {self.health}, Food level: {self.food_level}, Armor: {[]}"
        if len(self.__inventory['Armor']) == 1:
            return f"Name: {self.name}, Health: {self.health}, Food level: {self.food_level}, Armor: {self.__inventory['Armor']}"
        arm_names = [el.name_armor for el in self.__inventory['Armor']]
        return f"Name: {self.name}, Health: {self.health}, Food level: {self.food_level}, Armor: {self.__inventory['Armor']}"
    @property
    def inventory(self):
        return self.__inventory['Weapon'] + self.__inventory['Armor']

    @inventory.setter
    def inventory(self, item):
        return []

    @classmethod
    def add_item(cls, item):
        if isinstance(item, Food):
            cls.__inventory['Food'].append(item)
            return True
        if isinstance(item, Weapon):
            cls.__inventory['Weapon'].append(item)
            return True
        if isinstance(item, Armor):
            cls.__inventory['Armor'].append(item)
            return True
        raise TypeError("I can add only food, armor or weapon.")


class Mob(Entity):
    def __init__(self, name, health, damage) -> None:
        self.name = name
        self.health = health
        self.damage = damage

    def attack(self, player):
        self.player.health -= 5


class Food:
    def __init__(self, item_name, hunger_restore_level) -> None:
        self.item_name = item_name
        self.hunger_restore_level = hunger_restore_level

    def __add__(self, other):
        result = [self, other]
        return result

    def __mul__(self, number):
        if isinstance(number, int):
            result = [self] * number
            return result
        raise TypeError("We can multiply items only by integer")


class Weapon:
    def __init__(self, name_weapon, damage) -> None:
        self.name_weapon = name_weapon
        self.damage = damage

    def __mul__(self, number):
        if isinstance(number, int):
            result = [self] * number
            return result
        raise TypeError("We can multiply items only by integer")
    

class Armor:
    def __init__(self, name_armor, protection) -> None:
        self.name_armor = name_armor
        self.protection= protection

    def __repr__(self) -> str:
        return f"{self.name_armor}"

class Chest:
    def __init__(self, *args) -> None:
        self._items = args

    @property
    def items(self):
        result = []
        for el in self._items:
            if isinstance(el, Armor):
                result.append(el.name_armor)
                Player.add_item(el)
            if isinstance(el, Weapon):
                result.append(el.name_weapon)
                Player.add_item(el)
            if isinstance(el, Food):
                result.append(el.item_name)
                Player.add_item(el)
            if isinstance(el, list):
                result.extend(el)
                for i_ in el:
                    Player.add_item(i_)

        return result


    def __repr__(self) -> str:
        return f"{self.items}"
    
    # def __len__(self):
    #     for 

    
def test_minecraft():
    print("Creating a New Player...")
    # In the game there are two types
    # of entities: players created by users
    # and mobs created by AI.
    assert issubclass(Player, Entity)
    assert issubclass(Mob, Entity)

    # Each entity can attack.
    # Each entity has name, health level
    # and level of damage when attack.
#     # try:
#     #     Entity('Some', 3, 4)
#     #     assert False
#     # except TypeError as e:
#     #     assert e.args[0] == "Can't instantiate abstract class Entity with abstract method attack"

#     # Let's create a player.
    player = Player("Steve")
    assert player.name == 'Steve'
    # The initial level of health 
    # for each player is 20.
    assert player.health == 20
    # The default level of damage
    # for others is 4.
    assert player.damage == 4
    # The initial and maximum level of food
    #  for each player is 20.
    assert player.food_level == 20
    # Each player can have extra food, armor
    # and weapon.
    assert player._Player__inventory == {'Food': [], 'Armor': [], 'Weapon': []}

#     # Other players can see the armor for the player 
#     # and don't see the information
#     # about food and weapon.
    assert player.inventory == []
    assert str(player) == "This is Steve with health 20 and food level 20. He doesn't have armor."
    assert str([player]) == "[Name: Steve, Health: 20, Food level: 20, Armor: []]"

#     # Each minecraft world has its own difficulty for players:
#     # Easy, Normal and Hard.
#     # Default difficulty is normal.
#     # The level of difficulty influence the
#     # intense of fighting (you will see later).
    assert Player.difficulty == 'Normal'
    assert player.difficulty == 'Normal'

#     print("Preparing for the fight...")
#     # Player needs Food for the fight.
#     # Food refers to any consumable items that,
#     # when eaten, restore food level and sometimes
#     # cause status effects.
#     # Each item of the food has different
#     # level of hunger satisfaction
    golden_apple = Food('Golden Apple', 4)
    assert golden_apple.hunger_restore_level == 4
    whole_cake = Food('Cake (whole)', 14)
    assert whole_cake.hunger_restore_level == 14
    player.add_item(golden_apple)
    assert player._Player__inventory == {'Food': [golden_apple], 'Armor': [], 'Weapon': []}
#     try:
#         player.add_item('apple')
#         assert False
#     except TypeError as e:
#         assert e.args[0] == 'I can add only food, armor or weapon.'

#     # All food items and ingredients can be stacked
#     assert golden_apple+golden_apple == [golden_apple, golden_apple]
#     assert golden_apple+whole_cake == [golden_apple, whole_cake]
#     assert golden_apple*4 == [golden_apple, golden_apple, golden_apple, golden_apple] 
#     # we can't multiply food
    try:
        golden_apple * golden_apple
        assert False
    except TypeError as e:
        assert e.args[0] == "We can multiply items only by integer"

#     # Weapons can have different damage
    sword = Weapon('Sword', 7)
    assert sword.damage == 7
    ax1 = Weapon('Ax', 8)
    assert ax1.damage == 8
    assert isinstance(ax1, Weapon)
    player.add_item(sword)
    player.add_item(ax1)
    assert player._Player__inventory == {'Food': [golden_apple], 'Armor': [], 'Weapon': [sword, ax1]}

#     # Armors can protect
#     helmet = Armor('Helmet', 1)
#     assert helmet.protection == 1
#     assert isinstance(helmet, Armor)
#     player.add_item(helmet)
#     assert player._Player__inventory == {'Food': [golden_apple], 'Armor': [helmet], 'Weapon': [sword, ax1]}
#     assert str(player) == 'This is Steve with health 20 and food level 20. His armor: Helmet.'

#     # Let's imagine that we don't have to mine diamonds 
#     # to make tools and armor.
#     # We found chests with resourses in it!
#     chest1 = Chest(Armor('Chestplate', 3), Armor('Boots', 1), Weapon('Sword', 7))
#     # assert str(chest1.items) == '[Chestplate, Boots, Sword]'
#     assert isinstance(chest1.items, list)

#     chest2 = Chest(golden_apple * 4, Weapon('Arrow', 1) * 25, whole_cake)
#     assert len(chest2.items) == 30

#     player.inventory = chest1
#     assert str([player]) == "[Name: Steve, Health: 20, Food level: 20, Armor: [Helmet, Chestplate, Boots]]", str([player])
#     assert str(player) == "This is Steve with health 20 and food level 20. His armor: Helmet, Chestplate, Boots."
#     player.inventory = chest2
#     assert sum(len(items) for items in player._Player__inventory.values()) == 37

#     print("Fighting...")
#     # A mob is an AI-driven game entity resembling a living creature.
#     # Player can kill mobs, mobs can kill players.
#     # There are various mobs.
#     spider = Mob('Spider', 16, 10)
#     assert spider.health == 16
#     assert spider.damage == 10
#     assert player.health == 20
#     # when mob atttacks player
#     # the level of health decrease by 
#     # level of mob's damage. Don't forget to
#     # count all protection level.
#     spider.attack(player)
#     assert player.health == 15
#     # when player atttacks mob
#     # the level of mob's health decrease by 
#     # level of player's damage. The player
#     # also decrease food_level by 1/2/3 depending
#     # on difficulty level: Easy/Normal/Hard. Of course,
#     # we should choose the weapon.
#     player.attack(spider, ax1)
#     assert spider.health == 8
#     assert player.food_level == 18

#     #We can change the difficulty for players
#     Player.change_difficulty("Hard")
#     assert Player.difficulty == "Hard"

#     player.attack(spider, sword)
#     assert spider.health == 1 
#     assert player.food_level == 15

#     # By the way, we can enchant tools/armor to 
#     # increase damage/protection
#     assert isinstance(helmet, EnchantmentMixin)
#     assert isinstance(sword, EnchantmentMixin)
#     helmet.enchant(4)
#     assert helmet.protection == 5

#     spider.attack(player)
#     assert player.health == 14
#     # A player can restore food level
#     # by eating food.
#     player.eat(golden_apple)
#     assert player.food_level == 19

#     try:
#         player.eat('apple')
#         assert False
#     except TypeError as e:
#         assert e.args[0]== 'I can eat only food.'

#     try:
#         player.attack(spider, 'Sword')
#         assert False
#     except WeaponError as e:
#         assert e.message == "Player doesn't have such weapon"

#     print("Congratulations!")


# if __name__ == "__main__":
#     test_minecraft()
