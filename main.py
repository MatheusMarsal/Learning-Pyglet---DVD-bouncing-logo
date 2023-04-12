from random import randint
import pyglet as pg

class App(pg.window.Window):
    def __init__(self, *kwarg, **kwards):
        super().__init__(*kwarg, **kwards)

        self._style = self.WINDOW_STYLE_TRANSPARENT

        self._batch = pg.graphics.Batch()
        
        self.set_location(0, 30)
        self.width = pg.canvas.Display().get_default_screen().width
        self.height = pg.canvas.Display().get_default_screen().height - 70
        self.maximize()

        self._rect = pg.shapes.Rectangle(self.width / 2, self.height / 2, self.width / 10, self.height / 10,
                            color = (0, 0, 0),
                            batch = self._batch)
                            
        self.velRand()

        pg.clock.schedule_interval(self.update, 1 / 120)

    def update(self, dt):
        self._rect.x += self._vel_x * dt
        self._rect.y += self._vel_y * dt

        if self._rect.x <= 0:
            self._rect.x = 0
            self._vel_x = -self._vel_x

        if self._rect.x >= self.width - self._rect.width:
            self._rect.x = self.width - self._rect.width
            self._vel_x = -self._vel_x

        if self._rect.y <= 0:
            self._rect.y = 0
            self._vel_y = -self._vel_y
        
        if self._rect.y >= self.height - self._rect.height:
            self._rect.y = self.height - self._rect.height
            self._vel_y = -self._vel_y

    def velRand(self):
        self._vel_x = randint(-self.width // 2, self.width // 2)
        self._vel_y = randint(-self.height // 2, self.height // 2)

        if self._vel_x == 0 or self._vel_y == 0:
            self.velRand()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pg.window.mouse.LEFT:
            if x > self._rect.x and x < self._rect.x + self._rect.width and y > self._rect.y and y < self._rect.y + self._rect.height:
                self._vel_x = 0
                self._vel_y = 0

                self._click_x = x
                self._click_y = y

                self._dx_rect_click = self._rect.x - x
                self._dy_rect_click = self._rect.y - y

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pg.window.mouse.LEFT:
            try:
                if self._dx_rect_click or  self._dy_rect_click:
                    self._vel_x = (self._click_x - x) * 2
                    self._vel_y = (self._click_y - y) * 2

                    self._dx_rect_click = 0
                    self._dy_rect_click = 0

            except:
                pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & pg.window.mouse.LEFT:
            try:
                if self._dx_rect_click or self._dy_rect_click:
                    self._rect.x = x + self._dx_rect_click
                    self._rect.y = y + self._dy_rect_click

            except:
                pass

    def on_key_press(self, symbol, modifiers):
        if symbol in [pg.window.key.LEFT, pg.window.key.RIGHT, pg.window.key.DOWN, pg.window.key.UP]:
            if symbol == pg.window.key.LEFT:
                if self._vel_x > 0:
                    self._vel_x = -self._vel_x

            if symbol == pg.window.key.UP:
                if self._vel_y < 0:
                    self._vel_y = -self._vel_y

            if symbol == pg.window.key.RIGHT:
                if self._vel_x < 0:
                    self._vel_x = -self._vel_x

            if symbol == pg.window.key.DOWN:
                if self._vel_y > 0:
                    self._vel_y = -self._vel_y

            if symbol == pg.window.key.NUM_0:
                self._vel_x = 0
                self._vel_y = 0

    def on_resize(self, width, height):
        super().on_resize(width, height)

        self._rect.width = self.width / 10
        self._rect.height =  self.height / 10

        self._rect.x = width / 2 - self._rect.width / 2
        self._rect.y = height / 2 - self._rect.height / 2

    def on_draw(self):
        self.clear()
        self._batch.draw()

if __name__ == '__main__':
    window = App(resizable = True)
    pg.app.run()
