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

        self._rects = []
        self._vels = []

        for i in range(100):
            self._rects.append(pg.shapes.Rectangle(self.height / 2, self.height / 2, self.width / 10, self.height / 10,
                                color = self.randColor(),
                                batch = self._batch))
                            
            self.insert_vel()

        pg.clock.schedule_interval(self.update, 1 / 120)

    def randColor(self):
        return (randint(0,255), randint(0,255), randint(0,255))

    def update(self, dt):
        for rect in self._rects:
            rect.x += self._vels[self._rects.index(rect)]['x'] * dt
            rect.y += self._vels[self._rects.index(rect)]['y'] * dt

            if rect.x <= 0:
                rect.x = 0
                self._vels[self._rects.index(rect)]['x'] = -self._vels[self._rects.index(rect)]['x']
                rect.color = self.randColor()

            if rect.x >= self.width - rect.width:
                rect.x = self.width - rect.width
                self._vels[self._rects.index(rect)]['x'] = -self._vels[self._rects.index(rect)]['x']
                rect.color = self.randColor()

            if rect.y <= 0:
                rect.y = 0
                self._vels[self._rects.index(rect)]['y'] = -self._vels[self._rects.index(rect)]['y']
                rect.color = self.randColor()
            
            if rect.y >= self.height - rect.height:
                rect.y = self.height - rect.height
                self._vels[self._rects.index(rect)]['y'] = -self._vels[self._rects.index(rect)]['y']
                rect.color = self.randColor()

    def velRand(self):
        x = randint(-self.width // 2, self.width // 2)
        y = randint(-self.height // 2, self.height // 2)

        return x, y
    
    def insert_vel(self):
        x, y = self.velRand()

        self._vels.append({'x': x, 'y': y})
    
    def replace_vel(self):
        x, y = self.velRand()

        for vel in self._vels:
            x, y = self.velRand()
            self._vels.pop(0)

            self._vels.append({'x': x, 'y': y})

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pg.window.mouse.LEFT:
            for rect in self._rects:
                if x > rect.x and x < rect.x + rect.width and y > rect.y and y < rect.y + rect.height:
                    self._vels[self._rects.index(rect)]['x'] = 0
                    self._vels[self._rects.index(rect)]['y'] = 0

                    self._rect = rect

                    self._click_x = x
                    self._click_y = y

                    self._dx_rect_click = rect.x - x
                    self._dy_rect_click = rect.y - y

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pg.window.mouse.LEFT:
            try:
                if self._dx_rect_click or  self._dy_rect_click:    
                    self._vels[self._rects.index(self._rect)]['x'] = (self._click_x - x) * 2
                    self._vels[self._rects.index(self._rect)]['y'] = (self._click_y - y) * 2

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
        if symbol in [pg.window.key.LEFT, pg.window.key.RIGHT, pg.window.key.DOWN, pg.window.key.UP, pg.window.key.SPACE]:
            if symbol == pg.window.key.LEFT:
                for rect in self._rects:
                    if self._vels[self._rects.index(rect)]['x'] > 0:
                        self._vels[self._rects.index(rect)]['x'] = -self._vels[self._rects.index(rect)]['x']

                        rect.color = self.randColor()

            if symbol == pg.window.key.UP:
                for rect in self._rects:
                    if self._vels[self._rects.index(rect)]['y'] < 0:
                        self._vels[self._rects.index(rect)]['y'] = -self._vels[self._rects.index(rect)]['y']

                        rect.color = self.randColor()

            if symbol == pg.window.key.RIGHT:
                for rect in self._rects:
                    if self._vels[self._rects.index(rect)]['x'] < 0:
                        self._vels[self._rects.index(rect)]['x'] = -self._vels[self._rects.index(rect)]['x']

                        rect.color = self.randColor()

            if symbol == pg.window.key.DOWN:
                for rect in self._rects:
                    if self._vels[self._rects.index(rect)]['y'] > 0:
                        self._vels[self._rects.index(rect)]['y'] = -self._vels[self._rects.index(rect)]['y']
                            
                        rect.color = self.randColor()

            if symbol == pg.window.key.SPACE:
                for rect in self._rects:
                    self.replace_vel()
                    rect.color = self.randColor()

        if modifiers & pg.window.key.MOD_CTRL:
            for rect in self._rects:
                self._vels[self._rects.index(rect)]['x'] = 0
                self._vels[self._rects.index(rect)]['y'] = 0

    def on_resize(self, width, height):
        super().on_resize(width, height)
        
        for rect in self._rects:
            rect.width = self.height / 10
            rect.height =  self.height / 10

            rect.x = width / 2 - rect.width / 2
            rect.y = height / 2 - rect.height / 2

    def on_draw(self):
        self.clear()
        self._batch.draw()

if __name__ == '__main__':
    window = App(resizable = True)
    pg.app.run()
