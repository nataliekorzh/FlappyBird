import os
import pygame

_image_library = {}

gamestart = False
screenwidth = 288
screenheight = 512
flapping = False
framecount = 0

def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([screenwidth, screenheight])

# Run until the user asks to quit
done = False

clock = pygame.time.Clock()

time_since_last_action = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if gamestart == False and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            gamestart = True

    framecount += 1

    #dt = clock.tick()
    #time_since_last_action += dt

    screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/background1.png'), (0, 0))
    screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappyground.png'),
                (0, screenheight-112))
    if gamestart == False:
        print(framecount)
        if framecount % 60 == 0:
            flapping = not flapping
        if flapping == True:
            screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappybird2.png'),
                        (screenwidth / 2 - 20, (screenheight / 3 + 50)))
        else:
            screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappybird1.png'),
                        (screenwidth / 2 - 20, (screenheight / 3 + 50)))
        screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/buttongroup.png'), (27, screenheight*2/3-64))
        screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappytitle.png'), (55, screenheight/4))


    # Flip the display
    pygame.display.flip()

    #tick the clock
    clock.tick(60)
    print

# Done! Time to quit.
pygame.quit()