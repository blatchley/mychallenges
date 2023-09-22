import os
import sys
import time
import gmpy2
import random

SIZE = 1024

FLAG = open('drapeau.txt', 'r').read().strip()

def nombre_premier():
    p = int.from_bytes(os.urandom(SIZE // 16), 'big') | 1 | 2**(SIZE // 2)
    while 1:
        p += 2
        if not gmpy2.is_prime(p): continue
        if not gmpy2.is_prime(2*p+1): continue
        return p

def tx(s, speed=0.001):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(speed)

def rx():
    return input()

def enc(n, g, m): # clé publique et message
    r = int.from_bytes(os.urandom(SIZE // 8), 'big') % n
    n2 = n * n
    c  = pow(g, m, n2) * pow(r, n, n2)
    return c % n2

def dec(l, n, u, c):
    n2 = n * n
    pt = (pow(c, l, n2) - 1) // n
    return (pt * u) % n

def le_prix_de_paris():
    return int.from_bytes(os.urandom(2), 'big')

FROMAGE = [
    'Beaufort Chalet d’Alpage',
    'Carre Corse',
    'Rovethym',
    'Cremeux du Mont Saint-Michel',
    'Fleur du Maquis',
    'Soumaintrain',
    'Taupiniere',
    'Saint-Marcellin',
    'Hercule',
    'Camembert de Normandie'
]

into = '''
                                                                                                                       ▄▄              ▄▄                  ▄▄
▀███▀▀▀███                                                              ▄█▀▀▀█▄█                    ▀████▄     ▄███▀ ██              ██   ██           ▀███
  ██    ▀█                                                             ▄██    ▀█                      ████    ████                        ██             ██
  ██   █ ▀███▄███  ▄██▀██▄▀████████▄█████▄  ▄█▀██▄  ▄█▀█████ ▄▄█▀██    ▀███▄   ▀███  ▀███ ▀███▄███    █ ██   ▄█ ██ ▀███ ▀████████▄ ▀███ ██████  ▄▄█▀██   ██
  ██▀▀██   ██▀ ▀▀ ██▀   ▀██ ██    ██    ██ ██   ██ ▄██  ██  ▄█▀   ██     ▀█████▄ ██    ██   ██▀ ▀▀    █  ██  █▀ ██   ██   ██    ██   ██   ██   ▄█▀   ██  ██
  ██   █   ██     ██     ██ ██    ██    ██  ▄█████ ▀█████▀  ██▀▀▀▀▀▀   ▄     ▀██ ██    ██   ██        █  ██▄█▀  ██   ██   ██    ██   ██   ██   ██▀▀▀▀▀▀  ██
  ██       ██     ██▄   ▄██ ██    ██    ██ ██   ██ ██       ██▄    ▄   ██     ██ ██    ██   ██        █  ▀██▀   ██   ██   ██    ██   ██   ██   ██▄    ▄  ██
▄████▄   ▄████▄    ▀█████▀▄████  ████  ████▄████▀██▄███████  ▀█████▀   █▀█████▀  ▀████▀███▄████▄    ▄███▄ ▀▀  ▄████▄████▄████  ████▄████▄ ▀████ ▀█████▀▄████▄
                                                   █▀     ██
                                                   ██████▀

=============================================================================================================================================================

'''
tx(into)

tx('Mise en place "La Fromagerie de Monsieur Paillier", S\'il Vous Plait Tenez Madame...\n\n')

p = nombre_premier()
q = nombre_premier()
n = p * q
l = gmpy2.lcm(p-1, q-1)
g = 0xf00d
u = gmpy2.invert((pow(g, l, n*n) - 1) // n, n)

# Verification sanitaire
pt = random.randrange(0, 2**SIZE)
c = enc(n, g, pt)
assert pt == dec(l, n, u, c)

tx('Le nombre pseudo premier de Fromagerie cryptée : n = 0x%x\n' % n)
tx('Et Le Générateur                               : g = 0x%x\n' % g)
tx('\n'*1, 0.5)
tx('Prix d\'Impression:\n\n', 0.05)

prix = [le_prix_de_paris() for _ in FROMAGE]

for nombre, fromage in enumerate(FROMAGE):
    tx('   %30s : 0x%x\n' % (fromage, enc(n, g, prix[nombre])))


liste_de_courses = [random.randrange(0, 64) for _ in FROMAGE]

tx('\n'*1, 0.5)
tx('Fromage à Acheter:\n\n', 0.05)

prix_total = 0

for nombre, fromage in enumerate(FROMAGE):
    tx('   %30s x %d\n' % (fromage, liste_de_courses[nombre]), 0.01)
    prix_total += liste_de_courses[nombre] * prix[nombre]

vin = le_prix_de_paris()
prix_total += vin

tx('                       Plus vin : + %d\n' %  vin)
tx('\n'*1, 0.5)

tx('Veuillez Entrer le Prix Crypté (En Hexadécimal): ')
try:
    ct = int(rx(), 16)
except ValueError:
    tx('Veuillez Fournir un Numéro, Madame\n', 0.05)
    exit(0)

tx('Merci. ', 0.05)
tx('\n', 1)

tx('Vérifier', 0.05)
tx('...', 1)
tx('\n', 1)

pt = dec(l, n, u, ct)

if prix_total == pt:
    tx('Votre Drapeau, Madame: ', 0.05)
    tx(FLAG, 0.3)
    tx('\n')
else:
    tx('Ce n\'est Pas Correct, Madame', 0.05)
    tx(' ', 1)
    tx(':(\n', 0.3)
