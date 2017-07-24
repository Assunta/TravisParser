class Row:
    def __init__(self, build):
        # self.idBuild= build.getBuildID()
        # self.Duration= build.getDuration()
        # self.email= build.getEmail()
        # self.StartDate= build.getStart()
        # self.status=build.getStatus()
        self.idBuild= build["idBuild"]
        self.Duration= build["Duration"]
        self.email= build["email"]
        self.StartDate= build["StartDate"]
        self.status=build["status"]