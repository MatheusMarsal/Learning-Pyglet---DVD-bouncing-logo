from random import randint
import pyglet as pg

class App(pg.window.Window):
    def __init__(self, *kwarg, **kwards):
        super().__init__(*kwarg, **kwards)

        self._beep = pg.media.load('Beep.mp3', streaming=False)
        self._style = self.WINDOW_STYLE_TRANSPARENT

        self._batch = pg.graphics.Batch()
        
        self.set_location(0, 30)
        self.width = pg.canvas.Display().get_default_screen().width
        self.height = pg.canvas.Display().get_default_screen().height - 70
        self.maximize()

        self._rects = []
        self._vels = []

        for i in range(6):
            self._rects.append(pg.shapes.Rectangle(self.width // 2, self.width // 2, self.width // 10, self.height // 10,
                                color = (0, 0, 0),
                                batch = self._batch))

            self.append_velRand()
        
        pg.clock.schedule_interval(self.update, 1/120)

    def border_collision(self, rect):
        if rect.x <= 0:
            rect.x = 0
            self._vels[self._rects.index(rect)]['x'] = -self._vels[self._rects.index(rect)]['x']

        if rect.x >= self.width - rect.width:
            rect.x = self.width - rect.width
            self._vels[self._rects.index(rect)]['x'] = -self._vels[self._rects.index(rect)]['x']

        if rect.y <= 0:
            rect.y = 0
            self._vels[self._rects.index(rect)]['y'] = -self._vels[self._rects.index(rect)]['y']
        
        if rect.y >= self.height - rect.height:
            rect.y = self.height - rect.height
            self._vels[self._rects.index(rect)]['y'] = -self._vels[self._rects.index(rect)]['y']

    def collision_rects(self, rect1, rect2):
        if  self._vels[rect1]['x'] > 0 and self._vels[rect2]['x'] < 0 or \
            self._vels[rect1]['x'] < 0 and self._vels[rect2]['x'] > 0:
            self._vels[rect1]['x'] = -self._vels[rect1]['x']
            self._vels[rect2]['x'] = -self._vels[rect2]['x']
            
        else:
            vel_pivot = self._vels[rect1]['x']
            self._vels[rect1]['x'] = self._vels[rect2]['x']
            self._vels[rect2]['x'] = vel_pivot

        if  self._vels[rect1]['y'] > 0 and self._vels[rect2]['y'] < 0 or \
            self._vels[rect1]['y'] < 0 and self._vels[rect2]['y'] > 0:
            self._vels[rect1]['y'] = -self._vels[rect1]['y']
            self._vels[rect2]['y'] = -self._vels[rect2]['y']
        
        else:
            vel_pivot = self._vels[rect1]['y']
            self._vels[rect1]['y'] = self._vels[rect2]['y']
            self._vels[rect2]['y'] = vel_pivot

    def collision_botton_right(self, rect1, rect2):
        if  self._rects[rect1].x + self._rects[rect1].width >= self._rects[rect2].x and \
            self._rects[rect1].x + self._rects[rect1].width <= self._rects[rect2].x + (self._rects[rect2].width * 0.3) and  \
            self._rects[rect1].y >= self._rects[rect2].y and \
            self._rects[rect1].y <= self._rects[rect2].y + self._rects[rect2].height:

            self.collision_rects(rect1, rect2)
            self._beep.play()

    def collision_top(self, rect1, rect2):
        if  self._rects[rect1].x + self._rects[rect1].width >= self._rects[rect2].x and \
            self._rects[rect1].x + self._rects[rect1].width <= self._rects[rect2].x + self._rects[rect2].width and  \
            self._rects[rect1].y >= self._rects[rect2].y + (self._rects[rect2].height * 0.7)  and \
            self._rects[rect1].y <= self._rects[rect2].y + self._rects[rect2].height:
            
            self.collision_rects(rect1, rect2)
            self._beep.play()

    def collision_top_right(self, rect1, rect2):
        if  self._rects[rect1].x + self._rects[rect1].width >= self._rects[rect2].x and \
            self._rects[rect1].x + self._rects[rect1].width <= self._rects[rect2].x + (self._rects[rect2].width * 0.3) and  \
            self._rects[rect1].y + self._rects[rect1].height >= self._rects[rect2].y and \
            self._rects[rect1].y + self._rects[rect1].height <= self._rects[rect2].y + self._rects[rect2].height:
            
            self.collision_rects(rect1, rect2)
            self._beep.play()

    def collision_botton(self, rect1, rect2):
        if  self._rects[rect1].x + self._rects[rect1].width >= self._rects[rect2].x and \
            self._rects[rect1].x + self._rects[rect1].width <= self._rects[rect2].x + self._rects[rect2].width and  \
            self._rects[rect1].y + self._rects[rect1].height >= self._rects[rect2].y and \
            self._rects[rect1].y + self._rects[rect1].height <= self._rects[rect2].y + (self._rects[rect2].height * 0.3):
            
            self.collision_rects(rect1, rect2)
            self._beep.play()

    def rects_sensor(self):
        for rect1 in range(len(self._rects)):
            for rect2 in range(len(self._rects)):
                if rect2 != rect1:
                    self.collision_botton_right(rect1, rect2)
                    self.collision_top_right(rect1, rect2)
                    self.collision_top(rect1, rect2)
                    self.collision_botton(rect1, rect2)

    def update(self, dt):
        for rect in self._rects:
            rect.x += self._vels[self._rects.index(rect)]['x'] * dt
            rect.y += self._vels[self._rects.index(rect)]['y'] * dt

            self.border_collision(rect)

        self.rects_sensor()

    def velRand(self):
        vel_x = randint(-self.width // 2, self.width // 2)
        vel_y = randint(-self.width // 2, self.width // 2)

        return vel_x, vel_y

    def append_velRand(self):
        vel_x, vel_y = self.velRand()

        self._vels.append({'x': 0, 'y': 0})

    def replace_velRand(self):
        for vel in self._vels:
            vel_x, vel_y = self.velRand()

            self._vels.pop(0)
            self._vels.append({'x': vel_x, 'y': vel_y})

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
        if symbol in [pg.window.key.LEFT, pg.window.key.RIGHT, pg.window.key.DOWN, pg.window.key.UP, pg.window.key.NUM_0, pg.window.key.SPACE]:
            if symbol == pg.window.key.LEFT:
                for rect in self._rects:
                    if self._vels[self._rects.index(rect)]['x'] > 0:
                        self._vels[self._rects.index(rect)]['x'] = -self._vels[self._rects.index(rect)]['x']

            if symbol == pg.window.key.UP:
                for rect in self._rects:
                    if self._vels[self._rects.index(rect)]['y'] < 0:
                        self._vels[self._rects.index(rect)]['y'] = -self._vels[self._rects.index(rect)]['y']

            if symbol == pg.window.key.RIGHT:
                for rect in self._rects:
                    if self._vels[self._rects.index(rect)]['x'] < 0:
                        self._vels[self._rects.index(rect)]['x'] = -self._vels[self._rects.index(rect)]['x']

            if symbol == pg.window.key.DOWN:
                for rect in self._rects:
                    if self._vels[self._rects.index(rect)]['y'] > 0:
                        self._vels[self._rects.index(rect)]['y'] = -self._vels[self._rects.index(rect)]['y']

            if symbol == pg.window.key.NUM_0:
                for rect in self._rects:
                    self._vels[self._rects.index(rect)]['x'] = 0
                    self._vels[self._rects.index(rect)]['y'] = 0
                
            if symbol == pg.window.key.SPACE:
                self.replace_velRand()

        if modifiers & pg.window.key.MOD_CTRL:
            for rect in self._rects: 
                rect.color = (0, 0, 0)

    def on_resize(self, width, height):
        super().on_resize(width, height)

        count = 0
        for rect in self._rects:
            rect.width = self.height // 10
            rect.height =  self.height // 10

            rect.x = 0 + rect.width // 2 + 200 * count
            rect.y = height / 2 - rect.height // 2 
            count += 1

    def on_draw(self):
        self.clear()
        self._batch.draw()

if __name__ == '__main__':
    window = App(resizable = True)
    pg.app.run()
