import os
import pygame

_image_library = {}

gamestart = False
tutorial = False
screenwidth = 288
screenheight = 512
framecount = 0

class counter:

    digits = [-1, -1]

    def __init__(self, number, x, y):
        self.number = number
        self.x = x
        self.y = y

    def increment(self):
        self.number += 1

    def makeArray(self, num, index):
        if (num / 10) < 1:
            self.digits[index] = num
            return 1
        else:
            current = num / 10
            self.digits[index] = current
            return 0

    def recurseArray(self, dig):
        ind = 0
        val = self.makeArray(dig, ind)
        while val == 0:
            dig = dig % 10
            ind += 1
            val = self.makeArray(dig, ind)

    def draw(self):
        self.recurseArray(self.number)
        c = 0
        dignum = 0

        if self.number / 10 >= 1:
            #mult digits
            c = 1

        for i in self.digits:
            if i >= 0:
                dignum += 1
                num = int(i)
                img = '/Users/nataliekorzh/PycharmProjects/Flappy_Bird/{}.png'.format(num)
                if c == 0:
                    screen.blit(get_image(img), (self.x, self.y))
                else:
                    if dignum == 1:
                        screen.blit(get_image(img), (self.x - 13, self.y))
                    else:
                        screen.blit(get_image(img), (self.x + 10, self.y))

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
        screen.blit(get_image('/Users/nataliekorzh/PycharmProjects/Flappy_Bird/flappyground.png'), (self.x1, self.y))
        screen.blit(get_image('/Users/nataliekorzh/PycharmProjects/Flappy_Bird/flappyground.png'), (self.x2, self.y))

class bird:
    def __init__(self, flapping, x, y):
        self.flapping = flapping
        self.x = x
        self.y = y
        self.vel = 0

    def setx(self, x):
        self.x = x

    def sety(self, y):
        self.y = y

    def gety(self):
        return self.y

    def draw(self):
        # when game hasnt started
        if not gamestart:
            if framecount % 30 == 0:
                self.flapping = not self.flapping
            if self.flapping:
                self.y += 0.25
                screen.blit(get_image('/Users/nataliekorzh/PycharmProjects/Flappy_Bird/flappybird2.png'), (self.x, self.y))
            else:
                self.y -= 0.25
                screen.blit(get_image('/Users/nataliekorzh/PycharmProjects/Flappy_Bird/flappybird1.png'), (self.x, self.y))

        # When game starts
        else:
            # if velocity is not zero, reduce velocity every 10 frames
            if framecount % 10 == 0:
                if self.vel >= 0:
                    self.vel -= 1
                else:
                    self.vel *= 3

            # when velocity gets to zero or below set flapping to false
            if self.vel <= 0:
                self.flapping = False

            # add downwards velocity to y
            self.y -= self.vel

            # If flapping, blit flapping animation
            if self.flapping:
                screen.blit(get_image('/Users/nataliekorzh/PycharmProjects/Flappy_Bird/flappybird1.png'), (self.x, self.y))
            # If not flapping, blit nonflapping animation
            else:
                screen.blit(get_image('/Users/nataliekorzh/PycharmProjects/Flappy_Bird/flappybird2.png'), (self.x, self.y))

    # jump method
    def flap(self):
        # if not already flapping
        #if self.flapping == False:
        # set jumping to true
        self.flapping = True
        # add jump to velocity
        self.vel += 2

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
#Init counter
count = counter(0, (screenwidth) / 2 - 12, (screenheight / 16))

time_since_last_action = 0


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if gamestart == False and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if tutorial == False:
                tutorial = True
                flappybird.setx((screenwidth / 2 - 20)-75)
                flappybird.sety((flappybird.gety()))
            else:
                gamestart = True
        if gamestart == True and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            flappybird.flap()
            count.increment()
    framecount += 1

    # dt = clock.tick()
    # time_since_last_action += dt

    screen.blit(get_image('/Users/nataliekorzh/PycharmProjects/Flappy_Bird/background1.png'), (0, 0))
    screen.blit(get_image('/Users/nataliekorzh/PycharmProjects/Flappy_Bird/flappyground.png'),
                (0, screenheight - 112))
    gamebase.draw()
    gamebase.move()

    if gamestart == False and tutorial == False:
        #intro
        screen.blit(get_image('/Users/nataliekorzh/PycharmProjects/Flappy_Bird/buttongroup.png'),
                    (27, screenheight * 2 / 3 - 64))
        screen.blit(get_image('/Users/nataliekorzh/PycharmProjects/Flappy_Bird/flappytitle.png'), (55, screenheight / 4))
        flappybird.draw()
    elif tutorial == True and gamestart == False:
        # tutorial
        flappybird.draw()
        count.draw()
        screen.blit(get_image('/Users/nataliekorzh/PycharmProjects/Flappy_Bird/instruction.png'), (88, screenheight / 3 + 26))
    else:
        #game
        count.draw()
        flappybird.draw()

    # Flip the display
    pygame.display.flip()

    # tick the clock
    clock.tick(60)

# Done! Time to quit.
pygame.quit()
