import pygame
import time
import gladosMove as g


pygame.init()
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("Aucun joystick trouvé.")
    quit()
joystick1 = pygame.joystick.Joystick(0)
joystick1.init()

lastx = 0
lasty = 0
lastz = 0

color = [255,100,0]
bright = 1
lastB = 1

tb1 = False
tb1l = False
tb2 = False
tb2l = False
tg2 = 0

dernier_temps = time.time()

def temps_ecoule():
    global dernier_temps
    temps_actuel = time.time()
    temps_passe = temps_actuel - dernier_temps
    dernier_temps = temps_actuel
    return temps_passe


def ecrire_valeurs_fichier(axe_1, axe_2, axe_3, temps, nom_fichier):
    try:
        with open(nom_fichier, "a") as f:
            ligne = "{} {} {} {}\n".format(axe_1, axe_2, axe_3, temps)
            f.write(ligne)
    except FileNotFoundError:
        with open(nom_fichier, "w") as f:
            ligne = "{} {} {} {}\n".format(axe_1, axe_2, axe_3, temps)
            f.write(ligne)

def lire_valeurs_fichier(nom_fichier):
    with open(nom_fichier, "r") as f:
        lignes = f.readlines()
        valeurs = []
        for ligne in lignes:
            valeurs_ligne = ligne.strip().split()
            valeurs.append((float(valeurs_ligne[0]), float(valeurs_ligne[1]), float(valeurs_ligne[2])))
        return valeurs


# Boucle principale
running = True
#g.talk(1)
g.talkLed()
g.RingCol(color[0]*bright,color[1]*bright,color[2]*bright)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    axis_x = joystick1.get_axis(0)
    axis_y = joystick1.get_axis(1)
    axis_z = -joystick1.get_axis(3)
    bright = (1+joystick1.get_axis(5))/2
    tb1 = joystick1.get_button(0)
    tb2 = joystick1.get_button(1)
    time.sleep(0.05)

    x = int(50 + 50*axis_x)
    y = int(50 + 50*axis_y)
    z = int(50 + 50*axis_z)

    if tb1 != tb1l :
        if tb1 == True:
            color[1] = 100-color[1]
        g.RingCol(color[0]*bright,color[1]*bright,color[2]*bright)
        tb1l = tb1

    if tb2 != tb2l :
        if tb2 == True:
            tg2 = 1-tg2
            print("talk mode :" + str(tg2))
        g.talk(tg2)
        tb2l = tb2

    if joystick1.get_button(2):
        g.awakeLed()

    if joystick1.get_button(3):
        g.processRecordLed()

    if joystick1.get_button(6):
        g.sleepLed()

    if joystick1.get_button(7):
        g.off()
        g.talk(0)


    if x != lastx:
        g.turn(x)
        lastx = x
        print("Axe X:", x)
    if y != lasty:
        g.tilt(y)
        lasty = y
        print("Axe Y:", y)
    if z != lastz:
        g.trans(z)
        lastz = z
        print("Axe Z:", z)
    if bright != lastB:
        g.RingCol(color[0]*bright,color[1]*bright,color[2]*bright)
        lastB = bright
        print("bright :", bright)


    # Pause pour éviter une utilisation excessive du processeur
    #pygame.time.Clock().tick(50)


# Quitter pygame
pygame.quit()