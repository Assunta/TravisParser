class GoalRow:
    def __init__(self, goal, snapshot, INTERNET):
        if(INTERNET):
            self.name= goal.getName()
            self.catgory= goal.getCategory()
            self.snapshot=snapshot
        else:
            self.name= goal["name"]
            self.category= goal["category"]
            self.snapshot= snapshot
