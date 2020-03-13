class Player:
    def __init__(self, x, y, size, direction, speed, alignment, gold):
        self.x = x	
        self.y = y
        self.size = size
        self.direction = direction
        self.speed = speed
        self.alignment = alignment
        self.gold = gold
        self.shield_one = 0
        self.shield_two = 0
							
    def change_x(self, new_x):
        self.x = new_x
    
    def change_y(self, new_y):
        self.y = new_y
        
    def change_size(self, new_size):
        self.size = new_size
        
    def change_direction(self, new_direction):
        self.direction = new_direction
        
    def change_speed(self, new_speed):
        self.speed = new_speed
        
    def change_alignment(self, new_alignment):
        self.alignment = new_alignment
        
    def change_gold(self, new_gold):
        self.gold = new_gold
        
    def change_shield_one(self, new_shield_one):
        self.shield_one = new_shield_one
    
    def change_shield_two(self, new_shield_two):
        self.shield_two = new_shield_two