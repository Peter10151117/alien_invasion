import pygame

class SecCar:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.healthy_image = pygame.image.load('images/car2.png')
        self.light_damage_image = pygame.image.load('images/damagedcar.png')
        self.heavy_damage_image = pygame.image.load('images/wreckedcar.png')

        self.image = self.healthy_image
        self.rect = self.image.get_rect()

        self.health = 3

        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        mouse_pos = pygame.mouse.get_pos() #, self.x = mouse_pos[0], self.x = mouse_pos[1]
        self.x = mouse_pos[0]
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.car_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.car_speed

        self.rect.x = self.x
        print(self.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_car(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)