class Game:
    def __init__(self, level, state, high_score):
        self.level = level	
        self.state = state 
        self.high_score = high_score
							
    def change_level(self, new_level):
        self.level = new_level
    
    def change_state(self, new_state):
        self.state = new_state
        
    def change_high_score(self, new_high_score):
        self.high_score = new_high_score
                    