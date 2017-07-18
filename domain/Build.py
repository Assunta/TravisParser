import json
class Build():
    def __init__(self,idBuild):
        self.idBuild=idBuild
        self.status =""
        self.description=""
        self.commitId=""
        self.isPullRequest=False
        self.TitlePull=""
        self.PullId=""
        self.StartDate =""
        self.StartHour =""
        self.FinishDate = ""
        self.FinishHour = ""
        self.Duration=""
        self.Sha=""
        self.Branch=""
        self.Commit = ""
        self.CommitData =""
        self.commitHour=""
        self.author = ""
        self.email = ""
        self.Language = ""
        self.NumJobs = 0

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


    def setStatus(self, status):
        self.status=status

    def setDescription(self, desc):
        self.description=desc

    def setCommitId(self, commitId):
        self.commitId=commitId

    def setIsPullRequest(self, bool):
        self.isPullRequest=bool

    def setTitlePull(self, t):
        self.TitlePull=t

    def setPullId(self, n):
        self.PullId=n

    def setStart(self, start):
        self.StartDate= start.split("T")[0]
        self.StartHour= start.split("T")[1].replace("Z","")

    def setFinish(self, start):
        self.FinishDate = start.split("T")[0]
        self.FinishHour = start.split("T")[1].replace("Z","")

    def setDuration(self, d):
        self.Duration= '%02d:%02d' % ((d/ 60), d % 60)  # build.duration da isecondi

    def setCommitSHA(self, sha):
        self.Sha=sha

    def setBranch(self, b):
        self.Branch=b

    def setCommit(self, commit):
        self.Commit=commit

    def setCommitDate(self, d):
        self.commitData = d.split("T")[0]
        self.commitHour = d.split("T")[1].replace("Z", "")

    def setAuthor(self,a):
        self.author=a

    def setEmail(self, email):
        self.email=email

    def setLanguage(self, l):
        self.Language=l

    def setNumJobs(self, n):
        self.NumJobs=n

    def getStatus(self):
        return self.status

    def getDescription(self):
        return self.description

    def getCommitId(self):
        return self.commitId

    def getIsPullRequest(self):
        return self.isPullRequest

    def getTitlePull(self):
        return self.TitlePull

    def getPullId(self):
        return self.PullId

    def getStart(self):
        return[self.StartDate,
        self.StartHour]

    def getFinish(self):
        return[self.FinishDate,
        self.FinishHour]

    def getDuration(self):
        return self.Duration

    def getCommitSHA(self):
        return self.Sha

    def getBranch(self):
        return self.Branch

    def getCommit(self):
        return self.Commit

    def getCommitDate(self):
        return [self.CommitData, self.commitHour]

    def getAuthor(self):
        return self.author

    def getEmail(self):
        return self.email

    def getLanguage(self):
        return self.Language

    def getNumJobs(self):
        return self.NumJobs
