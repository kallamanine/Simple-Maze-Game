from pygame import *

# parent class for other sprites
class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(
            image.load(player_image),
            (size_x, size_y)
        )

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# class of the main player
class Player(GameSprite):

    def __init__(
        self,
        player_image,
        player_x,
        player_y,
        size_x,
        size_y,
        player_x_speed,
        player_y_speed
    ):
        GameSprite.__init__(
            self,
            player_image,
            player_x,
            player_y,
            size_x,
            size_y
        )

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):

        # horizontal movement
        if (
            self.rect.x <= win_width - 80 and self.x_speed > 0
        ) or (
            self.rect.x >= 0 and self.x_speed < 0
        ):
            self.rect.x += self.x_speed

        # collision with walls
        platforms_touched = sprite.spritecollide(
            self,
            barriers,
            False
        )

        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(
                    self.rect.right,
                    p.rect.left
                )

        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(
                    self.rect.left,
                    p.rect.right
                )

        # vertical movement
        if (
            self.rect.y <= win_height - 80 and self.y_speed > 0
        ) or (
            self.rect.y >= 0 and self.y_speed < 0
        ):
            self.rect.y += self.y_speed

        # collision with walls
        platforms_touched = sprite.spritecollide(
            self,
            barriers,
            False
        )

        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = p.rect.top
                self.y_speed = 0

        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = p.rect.bottom
                self.y_speed = 0

    # shooting
    def fire(self):
        bullet = Bullet(
            'bullet (1).png',
            self.rect.right,
            self.rect.centery,
            15,
            20,
            15
        )

        bullets.add(bullet)


# enemy sprite class
class Enemy(GameSprite):

    side = "left"

    def __init__(
        self,
        player_image,
        player_x,
        player_y,
        size_x,
        size_y,
        player_speed
    ):
        GameSprite.__init__(
            self,
            player_image,
            player_x,
            player_y,
            size_x,
            size_y
        )

        self.speed = player_speed

    def update(self):

        if self.rect.x <= 420:
            self.side = "right"

        if self.rect.x >= win_width - 85:
            self.side = "left"

        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


# bullet sprite class
class Bullet(GameSprite):

    def __init__(
        self,
        player_image,
        player_x,
        player_y,
        size_x,
        size_y,
        player_speed
    ):
        GameSprite.__init__(
            self,
            player_image,
            player_x,
            player_y,
            size_x,
            size_y
        )

        self.speed = player_speed

    def update(self):

        self.rect.x += self.speed

        # disappears after reaching edge of screen
        if self.rect.x > win_width + 10:
            self.kill()


# Creating window
win_width = 700
win_height = 500

display.set_caption("Pac-Man")

window = display.set_mode(
    (win_width, win_height)
)

back = (119, 210, 223)


# group for walls
barriers = sprite.Group()

# group for bullets
bullets = sprite.Group()

# group for monsters
monsters = sprite.Group()


# creating walls
w1 = GameSprite(
    'platform2 (1).png',
    win_width / 2 - win_width / 3,
    win_height / 2,
    300,
    50
)

w2 = GameSprite(
    'platform2_v (1).png',
    370,
    100,
    50,
    400
)


# adding walls
barriers.add(w1)
barriers.add(w2)


# creating player
packman = Player(
    'pac-1 (1).png',
    5,
    win_height - 80,
    80,
    80,
    0,
    0
)


# creating finish
final_sprite = GameSprite(
    'pac-1 (1).png',
    win_width - 85,
    win_height - 100,
    80,
    80
)


# function to create a new enemy
def create_enemy():

    enemy = Enemy(
        'cyborg (1).png',
        win_width - 80,
        150,
        80,
        80,
        5
    )

    monsters.add(enemy)


# create first enemy
create_enemy()


# function to restart the game
def restart_game():

    # reset player position
    packman.rect.x = 5
    packman.rect.y = win_height - 80

    # stop player movement
    packman.x_speed = 0
    packman.y_speed = 0

    # remove all bullets
    bullets.empty()

    # remove all monsters
    monsters.empty()

    # create new monster
    create_enemy()


# variable responsible for game ending
finish = False


# game loop
run = True

while run:

    time.delay(50)

    # checking events
    for e in event.get():

        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:

            if e.key == K_LEFT:
                packman.x_speed = -5

            elif e.key == K_RIGHT:
                packman.x_speed = 5

            elif e.key == K_UP:
                packman.y_speed = -5

            elif e.key == K_DOWN:
                packman.y_speed = 5

            elif e.key == K_SPACE:
                packman.fire()

        elif e.type == KEYUP:

            if e.key == K_LEFT:
                packman.x_speed = 0

            elif e.key == K_RIGHT:
                packman.x_speed = 0

            elif e.key == K_UP:
                packman.y_speed = 0

            elif e.key == K_DOWN:
                packman.y_speed = 0


    # checking that game is not finished
    if not finish:

        # background
        window.fill(back)

        # update player
        packman.update()

        # update bullets
        bullets.update()

        # draw player
        packman.reset()

        # draw bullets
        bullets.draw(window)

        # draw walls
        barriers.draw(window)

        # draw finish
        final_sprite.reset()

        # bullet hits monster
        sprite.groupcollide(
            monsters,
            bullets,
            True,
            True
        )

        # update monsters
        monsters.update()

        # draw monsters
        monsters.draw(window)

        # bullet hits wall
        sprite.groupcollide(
            bullets,
            barriers,
            True,
            False
        )


        # player hits monster
        if sprite.spritecollide(
            packman,
            monsters,
            False
        ):

            finish = True

            img = image.load(
                'game-over_1 (1).png'
            )

            d = img.get_width() // img.get_height()

            window.fill(
                (255, 255, 255)
            )

            window.blit(
                transform.scale(
                    img,
                    (
                        win_height * d,
                        win_height
                    )
                ),
                (90, 0)
            )

            display.update()

            # wait 2 seconds
            time.delay(2000)

            # restart game
            restart_game()

            finish = False


        # player reaches finish
        if sprite.collide_rect(
            packman,
            final_sprite
        ):

            finish = True

            img = image.load(
                'thumb (1).jpg'
            )

            window.fill(
                (255, 255, 255)
            )

            window.blit(
                transform.scale(
                    img,
                    (
                        win_width,
                        win_height
                    )
                ),
                (0, 0)
            )

            display.update()

            # wait 2 seconds
            time.delay(2000)

            # restart game
            restart_game()

            finish = False


    display.update()


quit()