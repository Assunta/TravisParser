class Row:
    def __init__(self, build):
        # if(INTERNET):
        #     self.idBuild= build.getBuildID()
        #     self.Duration= build.getDuration()
        #     self.email= build.getEmail()
        #     self.StartDate= build.getStart()
        #     self.status=build.getStatus()
        #     self.typeOfFailures = list()
        #     count_job_failed = 0
        #     for l in build.getLogs():
        #         if l.getStatus != "passed":
        #             count_job_failed += 1
        #             self.typeOfFailures.append(l.getTypeOfError())
        #     self.numJobFailed = count_job_failed
        # else:
        self.idBuild= build["idBuild"]
        self.Duration= build["Duration"]
        self.email= build["email"]
        self.StartDate= build["StartDate"]
        self.status=build["status"]
        self.typeOfFailures=list()
        count_job_failed=0
        for l in build["Logs"]:
            if l["status"]!="passed":
                count_job_failed+=1
                self.typeOfFailures.append(l["typeOfError"])
        self.typeOfFailures=list(set(self.typeOfFailures))
        self.numJobFailed=count_job_failed