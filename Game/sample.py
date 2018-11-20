import pygame as pg


class Player(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((30, 50))
        self.image.fill(pg.Color('dodgerblue1'))
        self.rect = self.image.get_rect(center=pos)
        # Give the sprite another rect for the collision detection.
        # Scale it to the desired size.
        self.hitbox = self.rect.inflate(100, 100)

    def update(self):
        # Update the position of the hitbox.
        self.hitbox.center = self.rect.center


class Enemy(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((30, 50))
        self.image.fill(pg.Color('sienna1'))
        self.rect = self.image.get_rect(center=pos)


def hitbox_collision(sprite1, sprite2):
    """Check if the hitbox of the first sprite collides with the
    rect of the second sprite.

    `spritecollide` will pass the player object as `sprite1`
    and the sprites in the enemies group as `sprite2`.
    """
    return sprite1.hitbox.colliderect(sprite2.rect)


def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    enemies = pg.sprite.Group()

    player = Player((100, 300), all_sprites)
    enemy = Enemy((320, 240), all_sprites, enemies)

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.MOUSEMOTION:
                player.rect.center = event.pos

        all_sprites.update()
        collided_sprites = pg.sprite.spritecollide(
            player, enemies, False, collided=hitbox_collision)
        for enemy_sprite in collided_sprites:
            print(enemy_sprite)

        screen.fill((30, 30, 30))
        all_sprites.draw(screen)
        pg.draw.rect(screen, (0, 255, 0), player.rect, 1)
        pg.draw.rect(screen, (255, 0, 0), player.hitbox, 1)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()