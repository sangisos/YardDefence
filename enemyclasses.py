# encoding: utf-8
from enemybaseclasses import *

# Normal enemies inherits the Enemy class

class enemy2(Enemy):
    '''Enemy 2'''
    level=1

class enemy3(Enemy):
    '''Enemy 3'''
    level=1

class enemy4(Enemy):
    '''Enemy 4'''
    level=1
    hp=2

class enemy5(Enemy):
    '''Enemy 5'''
    level=2
    hp=4

class enemy6(Enemy):
    '''Enemy 6'''
    level=2
    hp=5

class enemy7(Enemy):
    '''Enemy 7'''
    level=2
    hp=7

class enemy8(Enemy):
    '''Enemy 8'''
    level=3
    hp=8

class enemy9(Enemy):
    '''Enemy 9'''
    level=3
    hp=8

class enemy10(Enemy):
    '''Enemy 10'''
    level=3
    hp=8

# Bosses inherits the Boss class 

class boss1(Boss):
    '''Boss 1'''
    level=1
    hp=10

class boss2(Boss):
    '''Boss 2'''
    level=2
    hp=25

class boss3(Boss):
    '''Boss 3'''
    level=3
    hp=50

for lev in range(1,4):
    for ec in getEnemyClasses(lev):
        ec.classTag="class"+str(ec.__name__)
