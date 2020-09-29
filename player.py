class player(object):
    def __init__(self,num_player,move):
        self.color = color_list[num_player]
        self.width = 4
        self.dir = random.randint(1,360)
        self.posx = random.randint(200,700)
        self.posy = random.randint(200,700)  
        self.is_playing = True
        self.points = 0
        self.left= move[0]
        self.right = move[1]
        self.mult_forward_move = self.width + 2

    def legal_move(self, screen):
        
        if self.is_border_touched():
            return False        
        posx = self.posx + math.cos(self.dir) * self.mult_forward_move
        posy = self.posy + math.sin(self.dir) * self.mult_forward_move
        color = screen.get_at((round(posx),round(posy)))
        if color != BLACK:
            return False
        return True

    def move(self):
        self.posx += math.cos(self.dir)
        self.posy += math.sin(self.dir)

    def update_dir(self, num):
        self.dir += num

    def is_border_touched(self):
        if self.posx > 895 or self.posx < 5 or self.posy > 895 or self.posy < 5:
            return True
        return False