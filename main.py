import pygame
import random


# constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500


# counters & font object
wd_counter = 0
sec_counter = 0
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 12)


# Human class extending pygame.sprite.Sprite
class Human(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super(Human, self).__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.surf = pygame.Surface((self.x, self.y))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.bottom = SCREEN_HEIGHT-2

    def update(self):
        self.rect.move_ip(self.speed, 0)

        if self.rect.right > SCREEN_WIDTH:
            self.rect.left = 0


# Waterdrop class extending pygame.sprite.Sprite
class WaterDrop(pygame.sprite.Sprite):
    def __init__(self):
        super(WaterDrop, self).__init__()
        self.surf = pygame.Surface((2, 2))
        self.surf.fill((135, 206, 250))
        self.rect = self.surf.get_rect(
            center = (
                random.randint(0, SCREEN_WIDTH + 100),
                random.randint(-20, 0)
            )
        )
        self.speed = random.randint(10, 20)

    def update(self):
        self.rect.move_ip(-1, self.speed)
        if self.rect.right < 0:
            self.kill()
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# init pygame lib
pygame.init()


# set up drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


# create a custom event for adding waterdrops
ADD_WATERDROP = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_WATERDROP, 1)


# create a custom event for counting seconds
ADD_SECONDS = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_SECONDS, 1000)


# create groups to hold waterdrops and all sprites
#  - waterdrops is used for collision detection and position updates
#  - all_sprites is used for rendering
waterdrops = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


# instance of human
def instantiate_human(speed):
    global human
    human = Human(25, 75, speed)
    all_sprites.add(human)


# setup the clock for framerates
clock = pygame.time.Clock()


def testloop(sec_to_test, sec_counter, wd_counter, running):

    while running:

        # did the close button clicked?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            # add a new waterdrop?
            if event.type == ADD_WATERDROP:
                new_waterdrop = WaterDrop()
                waterdrops.add(new_waterdrop)
                all_sprites.add(new_waterdrop)
            # sec counter
            if event.type == ADD_SECONDS:
                sec_counter += 1

        # update the human sprite & the waterdrops
        human.update()
        waterdrops.update()

        # fill the background
        screen.fill((0, 0, 0))

        # draw the human to screen
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # check collisions
        if pygame.sprite.spritecollideany(human, waterdrops):
            pygame.sprite.spritecollideany(human, waterdrops).rect.top = SCREEN_HEIGHT
            waterdrops.remove(pygame.sprite.spritecollideany(human,waterdrops))
            all_sprites.remove(pygame.sprite.spritecollideany(human,waterdrops))
            wd_counter += 1

        # text surface object
        text = font.render("Waterdops collided: {}".format(wd_counter), True, (255, 255, 255))
        text2 = font.render("Seconds: {}".format(sec_counter), True, (255, 255, 255))
        screen.blit(text,(5, 5))
        screen.blit(text2,(5, 25))

        # flip the display
        pygame.display.flip()

        # maintaining fps
        clock.tick(60)

        # quit after 30 seconds
        if sec_counter == sec_to_test:
            running = False
    #---------end of loop---------#

    # statistics
    print("\n---------STATISTICS---------")
    print("Seconds simulated: {}".format(sec_counter))
    print("Collisions: {}".format(wd_counter))
    print("Speed: {}".format(human.speed))
    print("Average collisions per seconds: {}".format(wd_counter / max(sec_counter, 1)))


#------you can change the speed of human in the parameter of line 161 instantiate_human() method calling
#------you can change the testing seconds in the first parameter of line 164 testloop() method calling

# create an instance of human: instantiate_human(speed)
instantiate_human(10)

# calling the test function: testloop(sec_to_test, sec_counter, wd_counter)
testloop(10, 0, 0, True)

pygame.quit()