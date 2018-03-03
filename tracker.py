from cmd2 import Cmd
from .encounter import *
from .dice import *
from operator import attrgetter

def main_menu():
    print("""
    1. Add Monster
    2. Add NPC Hero
    3. Add PC
    4. Run Encounter
    5. Exit""")

#def add_monster():
#TODO: lookup to table function or custom

ENC = Encounter()


def add_npc():
    name = input("Name: ")
    health = input("Health: ")
    ac = input("Armor Class: ")
    initiative = input("Initiative: ")
    speed = input("Speed: ")
    ENC.add_npc(name, health, ac, initiative, speed)


def add_pc():
    name = input("Name: ")
    health = input("Health: ")
    ac = input("Armor Class: ")
    initiative = input("Initiative: ")
    speed = input("Speed: ")
    player = input("Played By: ")
    ENC.add_player(name, health, ac, initiative, speed, player)



class App(Cmd):
    def do_hello(self, arg):
        print('Hello world')

    def do_add_npc(self, arg):
        name = input("Name: ")
        health = input("Health: ")
        ac = input("Armor Class: ")
        initiative = input("Initiative: ")
        speed = input("Speed: ")
        ENC.add_npc(name, health, ac, initiative, speed)


    def do_print_encounter(self, arg):
        for key, item in ENC.creatures.items():
            item.print()

    def do_add_pc(self, arg):
        name = input("Name: ")
        health = input("Health: ")
        ac = input("Armor Class: ")
        initiative = input("Initiative: ")
        speed = input("Speed: ")
        player = input("Played By: ")
        ENC.add_player(name, health, ac, initiative, speed, player)

    def do_set_initiatives(self):
        die = Dice(1, 20)
        for key, item in ENC.creatures.items():
            roll = 0
            while not roll:
                roll = die.check_roll(input("Enter initiative roll for {0}: ".format(key)))
            item.initiative = roll + item.initiative_bonus
        ENC.creatures = sorted(ENC.creatures, key=attrgetter('initiative_bonus', 'initiative'), reverse=True)

    def do_heal(self, creature, health_up): # too many different ways to heal to do dice validation here
        if health_up > 0:
            ENC.creatures[creature].heal(health_up)

    def do_damage(self, creature, health_down): # too many different ways to damage to do dice validation here
        if health_down > 0:
            ENC.creatures[creature].heal(health_down)


if __name__ == '__main__':
    App().cmdloop()
