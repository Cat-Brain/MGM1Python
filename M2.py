# M2, this is a sequel to a mod(made by me, Jordan Baumann) of a game made by Matthew Tabet.
# Go to https://github.com/Matthew-12525/Create-Your-Own-Adventure for the original game, it's super super different.
"""
Hiya, this 'mod' was written by Jordan Baumann (me),
however this all wouldn't of existed without Matthew's original version of the game (link above ^^^).
I hope that you enjoy this experience, and if you want, maybe you'll even mod this mod! =]
"""

from ast import Delete
from copy import deepcopy # This lets us pass lists that aren't references.
from enum import Enum # This lets me use enum classes, and they look nice. =]
from math import *
import random
import time
from sty import fg, bg, ef, rs
def Col(text : str, r : int, g : int, b : int):
    return fg.red + text + fg.rs

import os
def Clear():
    os.system('cls' if os.name=='nt' else 'clear')














#Classes:

class InflictionType(Enum):
    POISON = 0
    BLEED = 1
    BURNING = 2
    DEADLY_HUG = 3
    STUN = 4
    WET = 5
    STRENGHTEN = 6
    # Insert more status effects here.



class Infliction:
    effect : InflictionType

    def __init__(self, effect : InflictionType):
        self.effect = effect

    def FindDamage(self):
        if self.effect ==  InflictionType.POISON:
            return 2
        elif self.effect == InflictionType.BLEED:
            return 3
        elif self.effect == InflictionType.BURNING:
            return 10
        elif self.effect == InflictionType.DEADLY_HUG:
            return 1
        elif self.effect == InflictionType.STUN:
            return 0
        elif self.effect == InflictionType.WET:
            return 0
        elif self.effect == InflictionType.STRENGHTEN:
            return 0
        else:
            return 0

    def DeathDamage(self):
        if self.effect ==  InflictionType.POISON:
            return 2
        elif self.effect == InflictionType.BLEED:
            return 1
        elif self.effect == InflictionType.BURNING:
            return 5
        elif self.effect == InflictionType.DEADLY_HUG:
            return 10
        elif self.effect == InflictionType.STUN:
            return 0
        elif self.effect == InflictionType.WET:
            return 0
        elif self.effect == InflictionType.STRENGHTEN:
            return 0
        else:
            return 0

    def Reduction(self):
        if self.effect ==  InflictionType.POISON:
            return 0
        elif self.effect == InflictionType.BLEED:
            return 0
        elif self.effect == InflictionType.BURNING:
            return 0
        elif self.effect == InflictionType.DEADLY_HUG:
            return 0
        elif self.effect == InflictionType.STUN:
            return 0
        elif self.effect == InflictionType.WET:
            return 15
        elif self.effect == InflictionType.STRENGHTEN:
            return -10
        else:
            return 0

    def FindName(self):
        if self.effect ==  InflictionType.POISON:
            return f"{fg(0, 255, 0)}poison{fg.rs}"
        elif self.effect == InflictionType.BLEED:
            return f"{fg(255, 0, 0)}bleed{fg.rs}"
        elif self.effect == InflictionType.BURNING:
            return f"{fg(255, 140, 0)}burning{fg.rs}"
        elif self.effect == InflictionType.DEADLY_HUG:
            return f"{fg(0, 100, 100)}deadly hug{fg.rs}"
        elif self.effect == InflictionType.STUN:
            return f"{fg(255, 255, 0)}stun{fg.rs}"
        elif self.effect == InflictionType.WET:
            return f"{fg(0, 0, 255)}wet{fg.rs}"
        elif self.effect == InflictionType.STRENGHTEN:
            return f"{fg(255, 0, 255)}strengthen{fg.rs}"
        else:
            return "NULL INFLICTION TYPE"
    
    """
    0 = independant, 3 + 4 = [3, 4]
    1 = stacks damage and duration, 3 + 4 = (2 <= count, 7)
    2 = stacks damage and chooses highest cooldown, 3 + 4 = (2 <= count, 4)
    """
    def AccumulationType(self):
        if self.effect ==  InflictionType.POISON:
            return 2
        elif self.effect == InflictionType.BLEED:
            return 1
        elif self.effect == InflictionType.BURNING:
            return 2
        elif self.effect == InflictionType.DEADLY_HUG:
            return 0
        elif self.effect == InflictionType.STUN:
            return 2
        elif self.effect == InflictionType.WET:
            return 1
        elif self.effect == InflictionType.STRENGHTEN:
            return 1
        else:
            return 0



class StatusEffect:
    effect : Infliction
    durationLeft : int
    shouldBeDestroyed : bool

    def __init__(self, effect : InflictionType, duration : int):
        self.effect = Infliction(effect)
        self.durationLeft = duration
        self.shouldBeDestroyed = False

    def Update(self):
        self.durationLeft -= 1
        if self.durationLeft <= 0:
            self.shouldBeDestroyed = True
            return self.DeathDamage()
        return self.FindDamage()

    def FindDamage(self):
        return self.effect.FindDamage()

    def DeathDamage(self):
        return self.effect.DeathDamage()

    def Reduction(self):
        return self.effect.Reduction()

    def Name(self):
        return self.effect.FindName()



class HitLocData:
    inflictor : int
    name : str
    leech : float

    def __init__(self, inflictor : int, name : str, leech : float):
        self.inflictor = inflictor
        self.name = name
        self.leech = leech



class Ailment:
    statusEffect : StatusEffect
    data : HitLocData

    def __init__(self, statusEffect : StatusEffect, data : HitLocData):
        self.statusEffect = statusEffect
        self.data = data

    def Update(self):
        return self.statusEffect.Update()

    def FindDamage(self):
        return self.statusEffect.effect.FindDamage()

    def DeathDamage(self):
        return self.statusEffect.effect.DeathDamage()

    def Reduction(self):
        return self.statusEffect.effect.Reduction()

    def Name(self):
        return self.statusEffect.effect.FindName()



class AilmentStackBase:
    inflictors : int
    shouldBeDestroyed : bool
    count : int
    def __init__(self, ailment : Ailment):
        self.effect = ailment.statusEffect.effect
        self.inflictors = [ailment.inflictor]
        self.shouldBeDestroyed = False
        self.count = 1
    
    def AddAilment(self, ailment : Ailment):
        self.count += 1 # self.count++
        print("You shouldn't be seeing this, AilmentStackBase : AddStatusEffect virtal function.")
    
    def Update(self):
        return 0, [], [], 0
    
    def Reduction(self):
        return 0
    
    def Name(self):
        return "NULL"


#region Status Stack sub-classes

class StatusStackType0(AilmentStackBase): # No stacking pretty much. Think of all status effects in M1
    ailments : Ailment

    def __init__(self, ailment : Ailment):
        self.effect = ailment.statusEffect.effect
        self.ailments = [ailment]
        self.shouldBeDestroyed = False
        self.count = 1
    
    def AddAilment(self, ailment : Ailment):
        self.count += 1 # self.count++
        self.ailments.append(ailment)
    
    def Update(self):
        totalDamage = 0
        damageFromSources = [0] * self.count
        damageSources = [0] * self.count

        for i in range(self.count):
            damageSources[i] = self.ailments[i].inflictor
            damageFromSources[i] = self.ailments[i].Update()
            totalDamage += damageFromSources[i]
        removedThisFrame = 0
        index = 0
        while index < len(self.ailments):
            if self.ailments[index].statusEffect.shouldBeDestroyed:
                del self.ailments[index]
                removedThisFrame += 1 # removedThisFrame++
                self.count -= 1 # self.count--
            else:
                index += 1 # index++
        if len(self.ailments) == 0:
            self.shouldBeDestroyed = True
        return totalDamage, damageFromSources, damageSources, removedThisFrame
    
    def Reduction(self):
        return self.statusEffect.Reduction() * len(self.ailments)
    
    def Name(self):
        return self

class StatusStackType1(AilmentStackBase): # Stacks durations and damage, most deadly.
    statusEffect : StatusEffect
    data : HitLocData

    def __init__(self, ailment : Ailment):
        self.effect = ailment.statusEffect.effect
        self.statusEffect = ailment.statusEffect
        self.count = 1
        self.data = [ailment.data]
        self.shouldBeDestroyed = False
        self.count = 1
    
    def AddAilment(self, ailment : Ailment):
        self.statusEffect.durationLeft += ailment.statusEffect.durationLeft
        self.count += 1 # self.count++
        self.data.append(ailment.data)
    
    def Update(self):
        result = self.statusEffect.Update()
        damageSources = [0] * self.count
        for i in range(self.count):
            damageSources[i] = self.data[i].inflictor

        if self.statusEffect.shouldBeDestroyed:
            self.shouldBeDestroyed = True
            return result * self.count, [result] * self.count, damageSources, self.count
        return result * self.count, [result] * self.count, damageSources, 0
    
    def Reduction(self):
        return self.statusEffect.Reduction() * self.count

class StatusStackType2(AilmentStackBase): # Stacks damage and resets duration, second most deadly. RoR2 bleed pretty much.
    statusEffect : StatusEffect
    count : int
    data : HitLocData

    def __init__(self, ailment : Ailment):
        self.effect = ailment.statusEffect.effect
        self.statusEffect = ailment.statusEffect
        self.count = 1
        self.data = [ailment.data]
        self.shouldBeDestroyed = False
    
    def AddAilment(self, ailment : Ailment):
        self.statusEffect.durationLeft = max(self.statusEffect.durationLeft, ailment.statusEffect.durationLeft)
        self.count += 1 # self.count++
        self.data.append(ailment.data)
    
    def Update(self):
        result = self.statusEffect.Update()
        damageSources = [0] * self.count
        for i in range(self.count):
            damageSources[i] = self.data[i].inflictor

        if self.statusEffect.shouldBeDestroyed:
            self.shouldBeDestroyed = True
            return result * self.count, [result] * self.count, damageSources, self.count
        return result * self.count, [result] * self.count, damageSources, 0
    
    def Reduction(self):
        return self.statusEffect.Reduction() * self.count

#endregion

statusStackTypeArray = [StatusStackType0, StatusStackType1, StatusStackType2]



class Ailments:
    stacks : AilmentStackBase
    length : int
    
    def __init__(self):
        self.stacks = []
        self.length = 0
    
    def AddAilment(self, ailment : Ailment):
        self.length += 1 # self.length++
        for i in range(len(self.stacks)):
            if self.stacks[i].effect == ailment.statusEffect.effect:
                self.stacks[i].AddStatusEffect(ailment)
                return
        self.stacks.append(statusStackTypeArray[ailment.statusEffect.effect.AccumulationType()](ailment))
    
    def Update(self):
        damageFromSources = [0] * 10
        damage = 0
        names = []

        for stack in self.stacks:
            dTemp, damageFromSourcesTemp, damageSources, lTemp = stack.Update()
            damage += dTemp
            for i in range(len(damageFromSourcesTemp)):
                damageFromSources[damageSources[i]] += damageFromSources[i]
            self.length -= lTemp
            names.append(stack.effect)
        return damage, damageFromSources
    
    def Reduction(self):
        reduction = 0
        for stack in self.stacks:
            reduction += stack.Reduction()
        return reduction
    
    def FindDataAtIndex(self, index : int):
        offset = 0
        for stack in self.stacks:
            if index < stack.count:
                if type(stack) == StatusStackType0:
                    return stack.ailments[index - offset].info
                else:
                    return stack.data[index - offset]
            offset += stack.count




class Hit:
    damage : int
    ailments : Ailment

    def __init__(self, damage : int, ailments : Ailment):
        self.damage = damage
        self.ailments = ailments



class Attack:
    procs : StatusEffect
    procChances : int # Percent
    damage : int
    damageRand : int
    selfProcs : StatusEffect
    selfProcChances : int # Percent
    selfDamage : int
    selfDamageRand : int
    length : int
    timeSinceStart : int
    name : str
    leech : float

    def __init__(self, procs : StatusEffect, procChances : int, damage : int, damageRand : int,\
        selfProcs : StatusEffect, selfProcChances : int, selfDamage : int, selfDamageRand : int,
        summons, length : int, name : int, leech : float):
        self.procs = procs
        self.procChances = procChances
        self.damage = damage
        self.damageRand = damageRand
        self.selfProcs = selfProcs
        self.selfProcChances = selfProcChances
        self.selfDamage = selfDamage
        self.selfDamageRand = selfDamageRand
        copyOfSummons = []
        for summon in summons:
            copyOfSummons.append(deepcopy(summon))
        self.summons = copyOfSummons
        self.length = length
        self.name = name
        self.timeSinceStart = 0
        self.leech = leech

    def RollDamage(self, currentIndex : int, damageReduction : int):
        ailments = []
        for i in range(len(self.procs)):
            if random.randint(1, 100) <= self.procChances[i]:
                ailments.append(Ailment(self.procs[i], HitLocData(currentIndex, self.name, self.leech)))
        selfAilments = []
        for i in range(len(self.selfProcs)):
            if random.randint(1, 100) <= self.selfProcChances[i]:
                selfAilments.append(Ailment(self.selfProcs[i], HitLocData(currentIndex, self.name, self.leech)))

        unModifiedDamage = max(0, random.randint(self.damage - self.damageRand, self.damage + self.damageRand))
        unModifiedSelfDamage = max(0, random.randint(self.selfDamage - self.selfDamageRand, self.selfDamage + self.selfDamageRand))
        return Hit(max(0, unModifiedDamage - damageReduction), ailments), unModifiedDamage,\
            Hit(max(0, unModifiedSelfDamage - damageReduction), selfAilments), unModifiedSelfDamage



class Unit:
    ailments : Ailments
    name : str
    maxHealth : int
    currentHealth : int
    attacks : Attack
    deathMessage : str
    activeAttack : int
    target : int

    def __init__(self, name : str, startHealth : int, maxHealth : int, attacks : Attack, deathMessage : str):
        self.ailments = []
        self.name = name
        self.currentHealth = startHealth
        self.maxHealth = maxHealth
        self.attacks = attacks
        self.deathMessage = deathMessage

    def Reduction(self):
        return self.ailments.Reduction()
    
    def CurrentAttack(self):
        return self.attacks[self.activeAttack]

    def TakeTurn(self):
        hit : Hit

        if self.CurrentAttack().length <= self.CurrentAttack().timeSinceStart:
            hit, unmodifiedDamage, selfHit, unmodifiedSelfDamage = self.CurrentAttack().RollDamage(0, self.Reduction())
            if hit.damage != 0 or hit.ailments != []:
                if unmodifiedDamage != hit.damage:
                    print(self.name + " does " + self.weapon.CurrentAttack().name + ".\n\
This attack deals " + str(hit.damage) + " damage. It would've done " + str(unmodifiedDamage) + " if it weren't for inflictions.")
                else:
                    print(self.name + " does " + self.weapon.CurrentAttack().name + ".\n\
This attack deals " + str(hit.damage) + " damage.")
                for ailment in hit.ailments:
                    print("This attack inflicts " + ailment.Name() + " for " + str(ailment.durationLeft) + " turns.")
            else:
                if unmodifiedDamage > 0:
                    print(self.name + "'s " + self.CurrentAttack().name + " misses, but it would've done " + str(unmodifiedDamage) + " if it weren't for inflictions.")
                else:
                    print(self.name + "'s " + self.CurrentAttack().name + " misses.")
            
            self.attacks[self.activeAttack].timeSinceStart = 0

            if selfHit.damage != 0 or selfHit.ailments != []:
                healOrDeal = "deals " + str(selfHit.damage) + " damage to"
                if selfHit.damage < 0:
                    healOrDeal = "heals for " + str(-selfHit.damage) + " health points on"

                if unmodifiedSelfDamage != selfHit.damage:
                    print(self.name + " does " + self.CurrentAttack().name + ".\n\
This attack " + healOrDeal + " themselve. It would've done " + str(unmodifiedSelfDamage) + " if it weren't for inflictions.")
                else:
                    print(self.name + " does " + self.CurrentAttack().name + ".\n\
This attack " + healOrDeal + " themselve.")
                for ailment in selfHit.ailments:
                    print("This attack inflicts " + ailment.Name() + " on themselve for " + str(ailment.statusEffect.durationLeft) + " turns.")
                self.ApplyHit(selfHit)


        else:
            hit = Hit(0, [])
            if self.CurrentAttack().length - self.CurrentAttack().timeSinceStart > 1:
                print(self.name + " continues to prepare their " + self.CurrentAttack().name + ". They have " + str(self.CurrentAttack().length - self.CurrentAttack().timeSinceStart) + " turns left.")
            else:
                print(self.name + " continues to prepare their " + self.CurrentAttack().name + ". They will be done next turn.")
            
        self.attacks[self.activeAttack].timeSinceStart += 1

        return hit

    def ApplyHit(self, hit : Hit, dodged : bool):
        self.currentHealth -= hit.damage
        for ailment in deepcopy(hit.ailments):
            if ailment.statusEffect.effect != InflictionType.STUN or not dodged:
                self.ailments.AddAilment(ailment)
            else:
                halfTimeAilment = ailment
                halfTimeAilment.statusEffect.durationLeft = halfTimeAilment.statusEffect.durationLeft // 2
                self.ailments.AddAilment(halfTimeAilment)
                print("Because you blocked get stunned for half as long. Which is in this case " + str(halfTimeAilment.statusEffect.durationLeft) + " turn.")

    def UpdateInflictions(self):
        damageFromSources = [0] * self.ailments.length

        orinalInflictionAttackers = [0] * self.ailments.length
        originalNames = [""] * self.ailments.length
        originalLeech = [0] * self.ailments.length

        for i in range(self.ailments.length):
            tempInfo : HitLocData
            tempInfo = self.ailments.FindDataAtIndex(i)
            orinalInflictionAttackers[i] = tempInfo.inflictor
            originalNames[i] = tempInfo.name
            originalLeech[i] = tempInfo.leech
        

        x = self.ailments.Update()
        


        return orinalInflictionAttackers, damageFromSources, originalNames

    def IsStunned(self):
        for infliction in self.inflictions:
            if infliction.effect.effect == InflictionType.STUN:
                return True
        return False



class Settings:
    sleepTime : int

    def __init__(self, sleepTime : int):
        self.sleepTime = sleepTime

        

















# Functions:


def ChooseDestination(possibilities : str, possibleAnswers : str, firstInputText, badInputText): # Must be in string form even if result should be numeric
    text = ""
    for currentPossibility in possibilities:
        text += currentPossibility + "\n"
    result = input(text + firstInputText).lower()
    badInput = True
    for currentPossibility in possibleAnswers:
        badInput &= currentPossibility != result
    while badInput:
        result = input(text + badInputText).lower()
        for currentPossibility in possibleAnswers:
            badInput &= currentPossibility != result
    return result



def FindSettings():
    global currentSettings
    prompt = input("How many seconds do you want to wait after key events('default' = 1) ").lower()
    badInput = not prompt.isnumeric()
    if not badInput:
        badInput = int(prompt) < 0
    badInput &= prompt != "default"
    while badInput:
        prompt = input("It has to be a number or 'default'. How many seconds do you want to wait after key events('default' = 1) ")
        badInput = not prompt.isnumeric()
        if not badInput:
            badInput = int(prompt) < 0
        badInput &= prompt != "default"
    if prompt == "default":
        currentSettings = Settings(1)
    else:
        currentSettings = Settings(int(prompt))



def PrintUnits(units : Unit):
    for unit in units:
        if unit.name != "NULL":
            print(unit.name)



def CharacterSelect():
    return deepcopy(commanderBob)



def FightSequence():
    print("=]")


























#Variables and game:

#Globalizing variables

specialFightEnding = False
specialFightEndingMonsters = []
allyUnits : Unit
enemyUnits : Unit
currentSettings : Settings

# Constant variables:
# Attacks 
# The syntax for a status effect is:
# StatusEffect(InflictionType.YOURINFLICTION, how long you want it to last)
# The syntax for an attacks is:
# Attack([Status effects], [chance of each status effect happening], damage, damage randomness (how far from the original value the actual value can be), [self inflictions], [self infliction procs], self damage, self damage randomness, [summons], turns to do, name)
# Attacks used by summons
fireBreath = Attack([StatusEffect(InflictionType.BURNING, 4)], [100], 0, 0, [], [], 0, 0, [], 3, "fire breath", 0.0)
heavyBite = Attack([], [], 50, 0, [], [], 0, 0, [], 4, "heavy bite", 0.5)
# Summons.
joshroHead = Unit("Joshro head", 25, 50, [fireBreath, heavyBite], "Killed by the final boss of the ... first game?")
# Normal attacks.
clubBash = Attack([StatusEffect(InflictionType.STUN, 2)], [100], 25, 10, [], [], 0, 0, [], 3, "club bash", 0.0)
punch = Attack([], [], 15, 15, [], [], 0, 0, [], 1, "punch", 0.0)
heavyPunch = Attack([StatusEffect(InflictionType.STUN, 2)], [75], 25, 25, [], [], 0, 0, [], 2, "heavy punch", 0.5)
quickStab = Attack([StatusEffect(InflictionType.POISON, 3)], [50], 5, 5, [], [], 0, 0, [], 1, "quick stab", 0.0)
rockThrow = Attack([StatusEffect(InflictionType.STUN, 1)], [25], 5, 5, [], [], 0, 0, [], 1, "rock throw", 0.0)
slimeHug = Attack([StatusEffect(InflictionType.DEADLY_HUG, 3)], [100], 0, 0, [], [], 0, 0, [], 1, "slime hug", 1.0)
slimeSpike = Attack([StatusEffect(InflictionType.BLEED, 3)], [100], 5, 0, [], [], 0, 0, [], 1, "slime absorb", 2.0)
arrowShoot = Attack([StatusEffect(InflictionType.BURNING, 3), StatusEffect(InflictionType.POISON, 8)], [100, 100], 35, 10, [], [], 0, 0, [], 3, "shoot arrow", 0.0)
chokeHold = Attack([StatusEffect(InflictionType.STUN, 1)], [75], 5, 5, [], [], 0, 0, [], 1, "choke hold", 0.0)
deepCut = Attack([StatusEffect(InflictionType.BLEED, 15), StatusEffect(InflictionType.BLEED, 15), StatusEffect(InflictionType.BLEED, 15)], [100, 50, 25], 0, 0, [], [], 0, 0, [], 1, "deep cut", 0.0)
finisher = Attack([], [], 20, 0, [], [], 0, 0, [], 1, "finisher", 0.0)
heavyBlow = Attack([], [], 100, 0, [], [], 0, 0, [], 5, "heavy blow", 0.0)
quickAttack = Attack([], [], 35, 0, [], [], 0, 0, [], 2, "quick attack", 0.0)
heaviestBlow = Attack([], [], 125, 0, [], [], 0, 0, [], 6, "heaviest blow", 0.0)
splash = Attack([StatusEffect(InflictionType.WET, 5)], [100], 3, 3, [], [], 0, 0, [], 1, "splash", 0.0)
quickClubBash = Attack([StatusEffect(InflictionType.STUN, 2)], [75], 10, 10, [], [], 0, 0, [], 2, "quick club bash", 0.0)
bite = Attack([StatusEffect(InflictionType.POISON, 4), StatusEffect(InflictionType.BLEED, 4)], [50, 50], 5, 5, [], [], 0, 0, [], 4, "bite", 1.0)
scratch = Attack([StatusEffect(InflictionType.BLEED, 4)], [25], 15, 5, [], [], 0, 0, [], 1, "scratch", 0.0)
spare = Attack([], [], 0, 0, [], [], 0, 0, [], 1, "spare", 0.0)
growHead = Attack([], [], 0, 0, [], [], 0, 0, [joshroHead], 2, "grow head", 0.0)
ultraFireBreath = Attack([StatusEffect(InflictionType.BURNING, 3)], [100], 0, 0, [], [], 0, 0, [], 1, "ultra fire breath", 0.0)
# Normal enemies.
# The syntax for enemies is:
# Enemy(start health, max health, [attack1, attack2, ...], "name", leech amount 0 to 1 work best
nullUnit = Unit("NULL", 0, 0, [], "NULL")
joshrosBody = Unit("Joshro's body", 300, 300, [growHead], "Killed by the final boss of the ... first game?")
ogre = Unit("ogre", 100, 100, [clubBash, punch], "Bonk!")
goblin = Unit("goblin", 100, 100, [quickStab, rockThrow], "Praise the almighty stab stab!")
petSlime = Unit("pet slime", 25, 50, [slimeHug], "The deadliest of hugs")
troll = Unit("troll", 125, 125, [quickClubBash, splash], "Quick bonk!")
mutant = Unit("mutant", 200, 200, [punch, heavyPunch], "Heavyeriest punch.")
rat = Unit("rat", 100, 200, [bite, scratch], "Chomp chomp")
babyRat = Unit("baby rat", 25, 50, [bite, scratch, splash], "Chomp splash")
guard = Unit("unloyal guard", 200, 200, [heavyBlow, quickAttack], "Loyal enough to kill you.")
# Playable characters.
commanderBob = Unit("Commander Bob", 200, 200, [quickStab, chokeHold], "Tacticool")























allies = deepcopy([nullUnit] * 10)
opponents = deepcopy([nullUnit] * 10)

def Main():
    global allies, opponents, petSlime, specialFightEnding, restart, currentSettings
    restart = False
    allies[4] = CharacterSelect()
    allies[0] = deepcopy(petSlime)
    allies[1] = deepcopy(petSlime)
    allies[2] = deepcopy(petSlime)
    allies[3] = deepcopy(petSlime)
    allies[5] = deepcopy(petSlime)
    allies[6] = deepcopy(petSlime)
    allies[7] = deepcopy(petSlime)
    allies[8] = deepcopy(petSlime)
    allies[9] = deepcopy(petSlime)
    PrintUnits(allies)













for i in range(7):
    print(Infliction(InflictionType(i)).FindName() + " = " + str(i))

gameRunning = True
while gameRunning:
    result = ChooseDestination(["Begin", "Settings", "End game"], ["begin", "settings", "end game"], "Where do you want to go? ", "It must be one of the 3 options above, sorry. Where do you want to go? ")
    if result == "begin":
        Main()
    elif result == "settings":
        FindSettings()
    else:
        gameRunning = False