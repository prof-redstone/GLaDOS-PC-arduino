import pygame
import time
import gladosMove as g

# Initialisation de pygame
pygame.init()

# Initialisation du joystick
pygame.joystick.init()

# Vérifier s'il y a des joysticks disponibles
if pygame.joystick.get_count() == 0:
    print("Aucun joystick trouvé.")
    quit()

# Sélectionner le premier joystick disponible
print(pygame.joystick)
joystick1 = pygame.joystick.Joystick(0)
joystick1.init()

lastx = 0
lasty = 0
lastz = 0

# Boucle principale
running = True
g.talk(1)
g.talkLed()
g.RingCol(255,100,0)
while running:
    # Récupérer les événements
    for event in pygame.event.get():
        # Si l'utilisateur quitte, arrêter la boucle
        if event.type == pygame.QUIT:
            running = False

    # Lire les valeurs des axes
    axis_x = joystick1.get_axis(0)
    axis_y = joystick1.get_axis(1)
    axis_z = -joystick1.get_axis(3)

    x = int(50 + 50*axis_x)
    y = int(50 + 50*axis_y)
    z = int(50 + 50*axis_z)

    # Afficher les valeurs des axes
    if x != lastx:
        g.turn(x)
        lastx = x
        print("Axe X:", x)
        time.sleep(0.1)
    if y != lasty:
        g.tilt(y)
        lasty = y
        print("Axe Y:", y)
        time.sleep(0.1)
    if z != lastz:
        g.trans(z)
        lastz = z
        print("Axe Z:", z)
        time.sleep(0.1)


    # Pause pour éviter une utilisation excessive du processeur
    pygame.time.Clock().tick(50)

# Quitter pygame
pygame.quit()