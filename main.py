from classes.game import Person, bgcolor
from classes.magic import Spell
from classes.inventory import Item
import random


# Create Black Magic
Fire = Spell("Fire", 25, 600, "black")
Thunder = Spell("Thunder", 25, 600, "black")
Blizzard = Spell("Blizzard", 25, 600, "black")
Meteor = Spell("Meteor", 40, 1200, "black")
Quake = Spell("Quake", 14, 140, "black")


# Create White Magic
Cure = Spell("Cura", 25, 620, "white")
Cura = Spell("Cura", 50, 1500, "white")
Curaga = Spell("Curaga", 50, 6000, "white")


# Create new Itmes
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi - Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("Mega Elixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


# Instantiate People
player_spells = [Fire, Thunder, Blizzard, Meteor, Cure, Cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5}, {"item": superpotion, "quantity": 5}, {
    "item": elixer, "quantity": 5}, {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

enemy_spells = [Fire, Meteor, Curaga]


# Players
player1 = Person("Valos:", 3400, 140, 301, 34, player_spells, player_items)
player2 = Person("Nicka:", 4500, 178, 325, 34, player_spells, player_items)
player3 = Person("Robot:", 3900, 195, 288, 34, player_spells, player_items)


# Enemies
enemy1 = Person("Imp  ", 3100, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Magus", 11200, 750, 525, 25, enemy_spells, [])
enemy3 = Person("Jack ", 3400, 130, 560, 325, enemy_spells, [])


players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

# Initializing running boolean
running = True
i = 0

print("\n"+ bgcolor.OKBLUE + "                               AN ENEMY ATTACKS" + bgcolor.ENDC)

# Start of the logic and loop
while(running):

    print("================================================================================")

    print("\n")
    print("NAME                   HP                                     MP")


    #For getting players stats
    for player in players:
        player.get_stats()

    print("\n")


    #For getting enemy stats
    for enemy in enemies:
        enemy.get_enemy_stats()


    # Check if Battle is over
    def check_battle_over():

        # CHeck if Player won
        if len(enemies) == 0:
            return 1

        # Check if Enemy won
        elif len(players) == 0:
            return 2
        
        return 0

    
    winner = 0


    #For each players to take actions on the enemies
    for player in players:

        # Choosing your action
        player.choose_action()
        choice = int(input("\nChoose your action:"))
        index = int(choice-1)

        # For attacking the enemy
        if index == 0:
            dmg = player.generate_damage()

            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)

            print(bgcolor.OKGREEN + "\nYou attacked", enemies[enemy].name.replace(" ", ""), "for", dmg, "points of damage" + bgcolor.ENDC)

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", ""), " has died")
                del enemies[enemy]

        # For doing magic on enemy
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print("\nNot Enough MP")
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bgcolor.OKBLUE + "\n" + spell.name + " heals for " + str(magic_dmg) + " HP" + bgcolor.ENDC)

            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)

                print(bgcolor.OKGREEN + "\n" + spell.name + " deals " + str(magic_dmg) + " points of damage to " + enemies[enemy].name.replace(" ", "") + bgcolor.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", ""), " has died")
                    del enemies[enemy]

        # For items
        elif index == 2:
            player.choose_items()
            item_choice = int(input("Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bgcolor.FAIL + "\nNone left" + bgcolor.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bgcolor.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + " HP" + bgcolor.ENDC)

            elif item.type == "elixer":

                if item.name == "Mega Elixer":
                    for i in players:
                        player.hp = player.maxhp
                        player.mp = player.maxmp

                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp

                print(bgcolor.OKGREEN + "\n" + item.name + " Fully restores HP/MP" + bgcolor.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bgcolor.OKBLUE + "\n" + item.name + " deals " + str(item.prop) +" points of damage to " + enemies[enemy].name.replace(" ", "") + bgcolor.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(bgcolor.OKGREEN + enemies[enemy].name.replace(" ", ""), " has died" + bgcolor.ENDC)
                    del enemies[enemy]

        #Calling the battle function
        winner = check_battle_over()
        if winner != 0:
            break
    
    #For checking whether all the players or enemies have died or not after the players attack
    if winner == 1:
        print(bgcolor.OKGREEN + "\nYou Win!!" + bgcolor.ENDC)
        running = False
    elif winner == 2:
        print(bgcolor.FAIL + bgcolor.BOLD + "\nYour Enemies have defeated you!!" + bgcolor.ENDC)
        running = False


    print("\n")


    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)


        #For enemies to attack the players
        if enemy_choice == 0:
            #Chose attack
            target = random.randrange(0, len(players))
            enemy_damage = enemy.generate_damage()

            players[target].take_damage(enemy_damage)
            print(bgcolor.FAIL + bgcolor.BOLD + "\n", enemy.name.replace(" ", ""), "attcks", players[target].name.replace(
                " ", ""), "for", enemy_damage, "points\n" + bgcolor.ENDC)


        #For enemies to do magic on the player
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bgcolor.FAIL + bgcolor.BOLD + spell.name + " heals " + enemy.name +
                      " for " + str(magic_dmg) + " HP" + bgcolor.ENDC)

            elif spell.type == "black":

                #target = random.randrange(0, 3)
                target = random.randrange(0, len(players))
                players[target].take_damage(magic_dmg)

                print(bgcolor.FAIL + bgcolor.BOLD + "\n" + enemy.name.replace(" ", "") + "'s " + spell.name + " deals " + str(
                    magic_dmg) + " points of damage to " + players[target].name.replace(" ", "") + bgcolor.ENDC)

                if players[target].get_hp() == 0:
                    print(bgcolor.WARNING + bgcolor.BOLD + players[target].name.replace(" ", ""), " has died" + bgcolor.ENDC)
                    del players[target]
        

        #Calling the battle function
        winner = check_battle_over()
        if winner != 0:
            break
    

    #For checking whether all the players or enemies have died or not after the enemies attack
    if winner == 1:
        print(bgcolor.OKGREEN + "\nYou Win!!" + bgcolor.ENDC)
        running = False
    elif winner == 2:
        print(bgcolor.FAIL + bgcolor.BOLD + "\nYour Enemies have defeated you!!" + bgcolor.ENDC)
        running = False
