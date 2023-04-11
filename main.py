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
        super().on_resize(self.width, self.height)

        self._rect = pg.shapes.Rectangle(self.height / 2, self.height / 2, self.height/10, self.height/10,
                            color = (0, 0, 0),
                            batch = self._batch)
                            
        self.velRand()

        pg.clock.schedule_interval(self.update, 1/120.0)

    def update(self, dt):
        self._rect.x += self._velRand_x * dt
        self._rect.y += self._velRand_y * dt

        if self._rect.x <= 0 or self._rect.x >= self.width - self._rect.x:
            self._velRand_x = -self._velRand_x

        if self._rect.y <= 0 or self._rect.y >= self.height - self._rect.y:
            self._velRand_y = -self._velRand_y

    def velRand(self):
        self._velRand_x = randint(-self.width//3, self.width//5)
        self._velRand_y = randint(-self.width//3, self.height//5)

        if self._velRand_x == 0 or self._velRand_y == 0:
            self.velRand()

    def on_key_press(self, symbol, modifiers):
        if symbol in [65361, 65362, 65363, 65364]:
            if symbol == pg.window.key.LEFT:
                if self._velRand_x > 0:
                    self._velRand_x = -self._velRand_x

            if symbol == pg.window.key.UP:
                if self._velRand_y < 0:
                    self._velRand_y = -self._velRand_y

            if symbol == pg.window.key.RIGHT:
                if self._velRand_x < 0:
                    self._velRand_x = -self._velRand_x

            if symbol == pg.window.key.DOWN:
                if self._velRand_y > 0:
                    self._velRand_y = -self._velRand_y

    def on_resize(self, width, height):
        self._rect.width = width/10
        self._rect.height = height/10

        self._rect.x = width/2
        self._rect.y = height/2

        super().on_resize(width, height)

    def on_draw(self):
        self.clear()
        self._batch.draw()

if __name__ == '__main__':
    window = App(resizable = True)
    pg.app.run()
