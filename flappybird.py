import os
import pygame
import random

_image_library = {}

gamestart = False
tutorial = False
screenwidth = 288
screenheight = 512
framecount = 0
currentpipe = None
gameover = False

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
                img = '/Users/nplotkin/PycharmProjects/FlappyBird/{}.png'.format(num)
                if c == 0:
                    screen.blit(get_image(img), (self.x, self.y))
                else:
                    if dignum == 1:
                        screen.blit(get_image(img), (self.x - 13, self.y))
                    else:
                        screen.blit(get_image(img), (self.x + 10, self.y))

class pipe:
    VEL = 2.5

    def __init__(self, x, y):
        self.counted = False
        self.y = y
        self.y1 = y - 70 - 320
        self.x = x

        self.image = get_image('/Users/nplotkin/PycharmProjects/FlappyBird/greenpipe.png')

        self.rect = self.image.get_rect()
        self.rect1 = self.image.get_rect()

    def getrects(self):
        return (self.rect, self.rect1)

    def getcounted(self):
        return self.counted

    def getx(self):
        return self.x

    def draw(self):
        #set each rect coords and blit
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.image, (self.x, self.y))

        self.rect1.x = self.x
        self.rect1.y = self.y1
        screen.blit(pygame.transform.flip(self.image, False, True), (self.x, self.y1))

    def move(self):
        if not gameover:
            self.x -= self.VEL
            if self.x <= 0-52:
                self.x = 288+199-26
                self.counted = False
                self.y = random.randint(150, 350)
                self.y1 = self.y - 70 - 320
            if self.x <= screenwidth / 2 - 20 - 32 and not self.counted:
                self.counted = True
                return True
            else:
                return False

class base:
    WIDTH = 336
    VEL = 2.5

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        if not gameover:
            self.x1 -= self.VEL
            self.x2 -= self.VEL

            if self.x1 + self.WIDTH < 0:
                self.x1 = self.x2 + self.WIDTH

            if self.x2 + self.WIDTH < 0:
                self.x2 = self.x1 + self.WIDTH

    def draw(self):
        screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappyground.png'), (self.x1, self.y))
        screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappyground.png'), (self.x2, self.y))

class bird(pygame.sprite.Sprite):
    def __init__(self, flapping, x, y):
        self.flapping = flapping
        self.x = x
        self.y = y
        self.vel = 0
        self.image = get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappybird2.png')
        self.rect = self.image.get_rect()

    def getrect(self):
        return self.rect

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
                self.image = get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappybird2.png')
                screen.blit(self.image, (self.x, self.y))
            else:
                self.y -= 0.25
                screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappybird1.png'), (self.x, self.y))

        # When game starts
        else:
            #if game not over
            if not gameover:
                #update rect pos
                self.rect.x = self.x
                self.rect.y = self.y

                # if velocity is not zero, reduce velocity every 10 frames
                if framecount % 10 == 0:
                    if self.vel >= 0:
                        self.vel -= 0.75
                    else:
                        self.vel *= 3

                # when velocity gets to zero or below set flapping to false
                if self.vel <= 0:
                    self.flapping = False

                # add downwards velocity to y
                self.y -= self.vel

                # If flapping, blit flapping animation
                if self.flapping:
                    screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappybird1.png'), (self.x, self.y))
                # If not flapping, blit nonflapping animation
                else:
                    screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappybird2.png'), (self.x, self.y))
            else:
                if self.y <= screenheight-112:
                    if framecount % 10 == 0:
                        if self.vel >= 0:
                            self.vel -= 2
                        else:
                            self.vel *= 3

                    # when velocity gets to zero or below set flapping to false
                    if self.vel <= 0:
                        self.flapping = False

                    # add downwards velocity to y
                    self.y -= self.vel
                    # If flapping, blit flapping animation
                    if self.flapping:
                        screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappybird1.png'),
                                    (self.x, self.y))
                    # If not flapping, blit nonflapping animation
                    else:
                        screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappybird2.png'),
                                    (self.x, self.y))

    # jump method
    def flap(self):
        if not gameover:
            # if not already flapping
            # set jumping to true
            self.flapping = True
            # add jump to velocity
            self.vel = 2

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

#Initialize 3 pipes
pipe1 = pipe(288, 200)
pipe2 = pipe(288+199-26, 200)
pipe3 = pipe(288+199-26+199-26, 200)
currentpipe = pipe1
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
                flappybird.setx((screenwidth / 2 - 20)-60)
                flappybird.sety((flappybird.gety()))
            else:
                gamestart = True
        if gamestart and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            flappybird.flap()
            count.draw()
    framecount += 1
    # dt = clock.tick()
    # time_since_last_action += dt

    screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/background1.png'), (0, 0))
    screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappyground.png'),
                (0, screenheight - 112))

    if gamestart == False and tutorial == False:
        #intro
        screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/buttongroup.png'),
                    (27, screenheight * 2 / 3 - 64))
        screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/flappytitle.png'), (55, screenheight / 4))
        flappybird.draw()
    elif tutorial == True and gamestart == False:
        # tutorial
        flappybird.draw()
        count.draw()
        screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/instruction.png'), (88, screenheight / 3 + 26))
    else:

        #game
        pipe1.draw()
        if pipe1.getx() <= screenwidth / 2 + 20 - 32 and not pipe1.getcounted():
            currentpipe = pipe1
        pipe2.draw()
        if pipe2.getx() <= screenwidth / 2 + 20 - 32 and not pipe2.getcounted():
            currentpipe = pipe2
        pipe3.draw()
        if pipe3.getx() <= screenwidth / 2 +  20 - 32 and not pipe3.getcounted():
            currentpipe = pipe3
        flappybird.draw()

        if currentpipe != None:
            #print("got here")
            currentrects = currentpipe.getrects()
            birdrect = flappybird.getrect()
            #print("birdrect x and y = " + birdrect.x + " " + birdrect.y)
            if birdrect.collidelist(currentrects) != -1 and not gameover:
                pygame.mixer.music.load('/Users/nplotkin/PycharmProjects/FlappyBird/punchsound.wav')
                pygame.mixer.music.play(1)
                gameover = True

        if pipe1.move():
            pygame.mixer.music.load('/Users/nplotkin/PycharmProjects/FlappyBird/flappybirdsound.wav')
            pygame.mixer.music.play(1)
            count.increment()
        if pipe2.move():
            pygame.mixer.music.load('/Users/nplotkin/PycharmProjects/FlappyBird/flappybirdsound.wav')
            pygame.mixer.music.play(1)
            count.increment()
        if pipe3.move():
            pygame.mixer.music.load('/Users/nplotkin/PycharmProjects/FlappyBird/flappybirdsound.wav')
            pygame.mixer.music.play(1)
            count.increment()
        count.draw()

        if gameover:
            screen.blit(get_image('/Users/nplotkin/PycharmProjects/FlappyBird/gameover.png'), (50, 90))

    gamebase.draw()
    gamebase.move()






    # Flip the display
    pygame.display.flip()

    # tick the clock
    clock.tick(60)

# Done! Time to quit.
pygame.quit()
