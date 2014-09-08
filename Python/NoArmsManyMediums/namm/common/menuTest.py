import pygame

running = true
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

    # code for our menu 
    ourMenu = ("Start Game",
               "Quit")

    myMenu = Menu(ourMenu)
    myMenu.drawMenu()
  #  pygame.display.flip()
    # main loop for event handling and drawing
    while 1:
        clock.tick(60)

    # Handle Input Events
        for event in pygame.event.get():
            myMenu.handleEvent(event)
            # quit the game if escape is pressed
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                myMenu.activate()
            elif event.type == Menu.MENUCLICKEDEVENT:
                if event.text=="Quit":
                    return
                elif event.item == 0:
                    isGameActive = True
                    myMenu.deactivate()

        screen.blit(background, (0, 0))    
        if myMenu.isActive():
            myMenu.drawMenu()
        else:
            background.fill((0, 0, 0))

        pygame.display.flip()
