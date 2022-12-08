import sys
from random import randint
from time import sleep
import pygame
from settings import Settings
from racecar import Car
from bullet import Bullet
from cone import Cone
from game_stats import GameStats
from button import Button
from sec_car import SecCar
import sound_effects as se

class racegame:

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)  # , pygame.FULLSCREEN)
        self.pic = pygame.image.load("images/route.png")

        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Race car game")
        self.pic = pygame.transform.scale(self.pic, (self.settings.screen_width, self.settings.screen_height))
        self.i = self.settings.screen_height

        self.stats = GameStats(self)

        self.car = Car(self)
        self.seccar = SecCar(self)
        self.bullets = pygame.sprite.Group()
        self.cones = pygame.sprite.Group()
        self.WIDTH = self.settings.screen_width
        self.HEIGHT = self.settings.screen_height

        self._create_fleet()

        self.play_button = Button(self, "Play")
        se.background_sound.play()

    def run_game(self):
        while True:
            self._check_events()
            # if self.stats.game_active:
            self.car.update()
            self.seccar.update()
            self._update_bullets()
            self._update_cones()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            # self.settings.initialize_dynamic_settings()

            self.stats.reset_stats()
            self.stats.game_active = True

            self.cones.empty()
            self.bullets.empty()
            self._create_fleet()
            self.car.center_car()
            self.seccar.center_seccar()


            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.car.moving_right = True
            self.seccar.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.car.moving_left = True
            self.seccar.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            se.bullet_sound.play()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.car.moving_right = False
            self.seccar.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.car.moving_left = False
            self.seccar.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        print(self.bullets)
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_cone_collisions()

    def _check_bullet_cone_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.cones, True, True)

        if not self.cones:
            print(True)
        #     self.bullets.empty()
        #     self._create_fleet()
        #     # self.settings.increase_speed()

    def _update_cones(self):
        self._check_fleet_edges()
        self.cones.update()

        if pygame.sprite.spritecollideany(self.car, self.cones):
            self._car_hit()
        self._check_cone_bottom()

        if pygame.sprite.spritecollideany(self.seccar, self.cones):
            self._seccar_hit()
        self._check_cone_bottom()

    def _check_cone_bottom(self):
        screen_rect = self.screen.get_rect()
        for cone in self.cones.sprites():
            if cone.rect.bottom >= screen_rect.bottom:
                # self._car_hit()
                self._seccar_hit()
                break

    def _car_hit(self):
        if self.stats.cars_left > 0:
            self.stats.cars_left -= 1

            self.cones.empty()
            self.bullets.empty()

            self._create_fleet()
            self.cone.center_cone()
            sleep(0.5)
        else:
            self.stats.game_active = False

        if self.stats.seccars_left > 0:
            self.stats.seccars_left -= 1

            self.cones.empty()
            self.bullets.empty()

            self._create_fleet()
            self.cone.center_cone()
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _create_fleet(self):

        cone = Cone(self)
        cone_width, cone_height = cone.rect.size
        available_space_x = self.settings.screen_width - (2 * cone_width)
        number_cones_x = available_space_x // (2 * cone_width)

        car_height = self.car.rect.height
        seccar_height = self.seccar.rect.height
        available_space_y = (self.settings.screen_height - (3 * cone_height) - car_height)
        number_rows = available_space_y // (2 * cone_height)

        for row_number in range(number_rows):
            for cone_number in range(number_cones_x):
                self._create_cone(cone_number, row_number)

    def _create_cone(self, cone_number, row_number):
        cone = Cone(self)

        cone_width, cone_height = cone.rect.size
        cone.x = cone_width + 2 * cone_width * cone_number
        cone.rect.x = cone.x + randint(-int(0.5*cone_width), int(0.5*cone_width))
        cone.rect.y = cone.rect.height + 2 * cone.rect.height * row_number
        self.cones.add(cone)

    def _check_fleet_edges(self):
        for cone in self.cones.sprites():
            if cone.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for cone in self.cones.sprites():
            cone.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def check_boundaries(self):
        if self.car.x >= 40:
            self.car_boundary = True
            self.car.x = self.screen_width
        if self.car.x <= -300:
            self.car_boundary = True
            self.car.x = 0

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill((0,0,0))
        self.i -= self.settings.cone_speed
        val = self.settings.screen_height - self.i
        val = val % self.settings.screen_height
        val2 = val - int(1 * self.settings.screen_height)
        self.screen.blit(self.pic, (0,val))
        self.screen.blit(self.pic, (0, val2))
        self.car.blitme()
        self.seccar.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.cones.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = racegame()
    ai.run_game()