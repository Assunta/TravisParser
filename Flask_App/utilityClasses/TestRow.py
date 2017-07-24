class TestRow:
    def __init__(self, test, snapshot):
        # self.testClass= test["testClass"]
        # self.skipped= test["skipped"]
        # self.run = test["run"]
        # self.failures = test["failures"]
        # self.time = test["time"]

        self.testClass= test["testClass"]
        self.skipped= test["skipped"]
        self.run = test["run"]
        self.failures = test["failures"]
        self.time = test["time"]

        self.snapshot= snapshot
