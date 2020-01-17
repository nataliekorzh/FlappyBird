import os
import pygame

_image_library = {}

gamestart = False
tutorial = False
screenwidth = 288
screenheight = 512
framecount = 0

class counter:

    def __init__(self, number):
        self.number = number

    def increment(self):
        self.number += 1

    def draw(self):
        if self.number % 10 :
            #one digit number
        img = '/Users/nplotkin/PycharmProjects/FlappyBird/{}.png'.format(self.number)
        screen.blit(get_image(), (self.x1, self.y))




class base:
    WIDTH = 336
    VEL = 2.5

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self):
        screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappyground.png'), (self.x1, self.y))
        screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappyground.png'), (self.x2, self.y))



class bird:
    def __init__(self, flapping, x, y):
        self.flapping = flapping
        self.x = x
        self.y = y

    def setx(self, x):
        self.x = x

    def sety(self, y):
        self.y = y

    def gety(self):
        return self.y

    def draw(self):
        if not gamestart:
            print(framecount)
            if framecount % 30 == 0:
                self.flapping = not self.flapping
            if self.flapping:
                self.y += 0.25
                screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappybird2.png'), (self.x, self.y))
            else:
                self.y -= 0.25
                screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappybird1.png'), (self.x, self.y))


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image



#Game starts here
pygame.init()
#Initialize clock
clock = pygame.time.Clock()
# Set up the drawing window
screen = pygame.display.set_mode([screenwidth, screenheight])
# Run until the user asks to quit
done = False

#Initialize bird
flappybird = bird(False, (screenwidth / 2 - 20), (screenheight / 3 + 50))
#Initialize base
gamebase = base((screenheight - 112))

time_since_last_action = 0


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if gamestart == False and event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            tutorial = True
            flappybird.setx((screenwidth / 2 - 20)-75)
            flappybird.sety((flappybird.gety()))
        if gamestart == False and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            gamestart = True
    framecount += 1

    # dt = clock.tick()
    # time_since_last_action += dt

    screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/background1.png'), (0, 0))
    screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappyground.png'),
                (0, screenheight - 112))
    gamebase.draw()
    gamebase.move()

    if gamestart == False and tutorial == False:
        screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/buttongroup.png'),
                    (27, screenheight * 2 / 3 - 64))
        screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappytitle.png'), (55, screenheight / 4))
        flappybird.draw()
    elif tutorial == True and gamestart == False:
        flappybird.draw()
        screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/instruction.png'), (88, screenheight / 3 + 26))
    else:
        flappybird.draw()

    # Flip the display
    pygame.display.flip()

    # tick the clock
    clock.tick(60)
    print

# Done! Time to quit.
pygame.quit()
