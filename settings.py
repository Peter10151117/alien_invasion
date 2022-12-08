class Settings:
    def __init__(self):
        self.screen_width = 2000
        self.screen_height = 1000
        self.bg_color = (150,0,0)

        self.car_speed = 9.0
        self.car_limit = 3

        # self.bullet_speed = 1.0
        self.bullet_width = 3.0
        self.bullet_height = 15.0
        self.bullet_color = (50,160,20)
        self.bullets_allowed = 10

        self.cone_drop_speed = 2.0

        self.speedup_scale = 1.1

        self.fleet_direction = 1
        # self.initialize_dynamic_settings()

    # def initialize_dynamic_settings(self):
    #     self.car_speed = 1.5
        self.bullet_speed = 20.0
        self.cone_speed = 3.0

    def increase_speed(self):
        self.car_speed *= self.speedup_scale
        # self.bullet_speed *= self.speedup_scale
        self.cone_speed *= self.speedup_scale
