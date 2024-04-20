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
g.talk(1)
g.talkLed()
g.RingCol(255,100,0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    axis_x = joystick1.get_axis(0)
    axis_y = joystick1.get_axis(1)
    axis_z = -joystick1.get_axis(3)

    x = int(50 + 50*axis_x)
    y = int(50 + 50*axis_y)
    z = int(50 + 50*axis_z)

    if x != lastx or y != lasty or z != lastz:
        #ecrire_valeurs_fichier(x,y,z,temps_ecoule(),"1.txt")
        time.sleep(0.1)


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


    # Pause pour éviter une utilisation excessive du processeur
    #pygame.time.Clock().tick(50)


# Quitter pygame
pygame.quit()