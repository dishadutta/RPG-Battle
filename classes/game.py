import random
from .magic import Spell
from .inventory import Item

class bgcolor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RAND1 = '\033[96m'
    RAND2 = '\033[98m'
    RAND3 = '\033[97m'
    RAND4 = '\033[99m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]
        self.name = name

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self,dmg):
        self.hp-= dmg
        if self.hp<0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp>self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_maxhp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_maxmp(self):
        return self.maxmp
    
    def reduce_mp(self,cost):
        self.mp-=cost

    def choose_action(self):
        i=1
        print("\n", "   " + self.name)
        print("\n" + "   " + bgcolor.RAND1 + bgcolor.BOLD +"ACTIONS:" + bgcolor.ENDC)
        for items in self.actions:
            print("     " + str(i) + "." + items)
            i+=1
    
    def choose_magic(self):
        i=1
        print("\n" + "   " + bgcolor.RAND2 + bgcolor.BOLD +"MAGIC" + bgcolor.ENDC)
        for spell in self.magic:
            print("      " + str(i) + ". " + spell.name + " (Cost: " + str(spell.cost) + " )")
            i+=1

    def choose_items(self):
        i=1
        print("\n" + "   " + bgcolor.RAND4 + bgcolor.BOLD + "ITEM" + bgcolor.ENDC)
        for item in self.items:
            print("     " + str(i) + ". " + item["item"].name + ": " + item["item"].description + " (x" + str(item["quantity"]) + ")")
            i+=1


    def choose_target(self, enemies):
        i=1
        print("\n" + "   " + bgcolor.RAND3 + bgcolor.BOLD +"TARGET" + bgcolor.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("     " + str(i) + ". " + enemy.name)
                i+=1

        choice = int(input("Choose Target: "))  - 1
        return choice


    def get_enemy_stats(self):

        #Setting HP bar of enemy
        hp_bar = ""
        bar_ticksh = (self.hp/self.maxhp) * 100/2

        while bar_ticksh > 0:
            hp_bar+= "█"
            bar_ticksh -= 1

        while len(hp_bar) < 50:
            hp_bar+=" "


        #Formatting of the HP spaces for enemy
        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 11:
            decreasedh = 11 - len(hp_string)
        
            while decreasedh > 0:
                current_hp += " "
                decreasedh -= 1

            current_hp += hp_string

        else:
            current_hp = hp_string

        print("                        __________________________________________________")
        print(self.name+"      "+current_hp+" "+"|"+ bgcolor.WARNING + hp_bar+ bgcolor.ENDC +"|")
            

    def get_stats(self):

        #Setting HP bar of player
        hp_bar = ""
        bar_ticksh = (self.hp/self.maxhp) * 100/4

        while bar_ticksh > 0:
            hp_bar+= "█"
            bar_ticksh-=1

        while len(hp_bar) < 25:
            hp_bar+=" "


        #Setting HP bar of player
        mp_bar = ""
        bar_ticksm = (self.mp/self.maxmp) * 100/10

        while bar_ticksm > 0:
            mp_bar+= "█"
            bar_ticksm-=1

        while len(mp_bar) < 10:
            mp_bar+=" "


        #Formatting of the HP spaces for player
        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 9:
            decreasedh = 9 - len(hp_string)
        
            while decreasedh > 0:
                current_hp += " "
                decreasedh -= 1

            current_hp += hp_string

        else:
            current_hp = hp_string


        #Formatting of the MP spaces for player
        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""

        if len(mp_string) < 7:
            decreasedm = 7 - len(mp_string)
        
            while decreasedm > 0:
                current_mp += " "
                decreasedm -= 1

            current_mp += mp_string

        else:
            current_mp = mp_string
        

        print("                       _________________________              __________")
        print(self.name+"      "+current_hp+" "+"|"+ bgcolor.OKGREEN +hp_bar+ bgcolor.ENDC +"|    "+current_mp+" "+"|"+mp_bar+"|")


    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        pct = self.hp/self.maxhp * 100

        if self.mp < spell.cost and spell.type == "white" and pct>50:
            self.choose_enemy_spell()
        return spell, magic_dmg
