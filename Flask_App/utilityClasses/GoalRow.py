class GoalRow:
    def __init__(self, goal, snapshot):
        # self.name= goal.getName()
        # self.catgory= goal.getCategory()
        # self.snapshot=snapshot
        self.name= goal["name"]
        self.category= goal["category"]
        self.snapshot= snapshot
