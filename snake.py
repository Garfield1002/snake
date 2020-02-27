'''
(\/)
(oO)
c(")(")
Author: Jack
'''


class Snake():
    def __init__(self, snake_id):
        self.x = 0
        self.y = 0
        self.direction = (2, 0)
        self.body = []
        self.grow = False
        self.score = 0
        self.alive = True
        self.id = snake_id
        self.skin = 'O'
        self.beep = 0
