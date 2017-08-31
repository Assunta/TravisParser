import re

from domain.Goal import Goal
from domain.snapshot import Snapshot
from utility.configUtility import getKeyValueMaven
from utility.dbUtility import getStatusMessages

warningList=list()
errorList=list()
dependenciesList=list()
snapshotList=list()
statusErrorList=list()
status="passed"
statusMessage= getStatusMessages()
values = getKeyValueMaven()

def parserMaven(username,f, mavenLog):
    warningList = list()
    errorList = list()
    dependenciesList = list()
    snapshotList = list()
    statusErrorList = list()
    status = "passed"
    for line in f:
        #checkMainInfo(line)
        if re.match(values["SNAPSHOT"], line):
            snapshotList.append(Snapshot((line.split("[INFO] Building", 1)[1]).strip()))
        elif re.match(values["GOAL"], line):
            goal = (line.split("---")[1]).split("@")[0].strip()
            # remove num version
            goal = re.sub(":((\d)*\.)*(\d)*:", ":", goal).strip()
            try:
                snapshotList[-1].addGoal(Goal(username,goal.split("(")[0].strip()))
            except IndexError:
                snapshotList.append(Snapshot("EMPTY_SNAPSHOT"))
        # match expressions: # Running test ExampleTest
        elif re.match(values["RUNNING_TEST"], line):
            try:
                snapshotList[-1].addTest(line.replace("[INFO]", "").strip())
            except IndexError:
                snapshotList.append(Snapshot("EMPTY_SNAPSHOT"))
        elif re.match(values["TEST_RESULT"], line):
            if not re.match(values["TEST_EX"], line):
                snapshotList[-1].addTest("Total Tests: \n")
            snapshotList[-1].addTest(line.replace("[INFO]", "").replace("[WARNING]", "").strip())
        elif re.match(values["ERROR"], line):
            try:
                errorList.append((snapshotList[-1].getGoals())[-1].__str__() + line)
            except IndexError:
                errorList.append(line)
        elif re.match(values["WARNING"], line):
            warningList.append(line)
        elif re.match(values["DEPENDENCIES"], line):
            if not (re.match(values["DEPENDENCIES_FILTER"], line)):
                str = line.split(" ")[2].split('/')[-1][:-4]
                dependenciesList.append(str)
        elif re.match(values["DEPENDENCIES_WITHOUT_INFO"], line):
            if not (re.match(values["DEPENDENCIES_FILTER"], line)):
                str = line.split("Downloaded:")[1].strip().split(" ")[0].split('/')[-1][:-4]
                dependenciesList.append(str)

        #status=checkStatus(line)
        for mess in statusMessage:
            if re.match(mess.get("regex"), line):
                status = mess.get("status")
                statusErrorList.append(line.strip())
                break

    warning = set(warningList)
    mavenLog.addErrorList(errorList)
    mavenLog.addSnapshotList(snapshotList)
    mavenLog.addWarningList(list(warning))
    mavenLog.getError()
    mavenLog.setStatus(status)
    mavenLog.setStatusError(list(set(statusErrorList)))
    mavenLog.setDependencies(list(set(dependenciesList)))
    #print mavenLog.toJSON()
    return mavenLog



def checkStatus(line):
    status = "passed"
    for mess in statusMessage:
        if re.match(mess.get("regex"), line):
            status = mess.get("status")
            statusErrorList.append(line.strip())
            break
    return status


# check the presence of a snapshot, goal, test, errors, warnings, dependencies
def checkMainInfo(line):
    if re.match(values["SNAPSHOT"], line):
        snapshotList.append(Snapshot((line.split("[INFO] Building", 1)[1]).strip()))
    elif re.match(values["GOAL"],line):
        goal = (line.split("---")[1]).split("@")[0].strip()
        # remove num version
        goal = re.sub(":((\d)*\.)*(\d)*:", ":", goal).strip()
        try:
            snapshotList[-1].addGoal(Goal(goal.split("(")[0].strip()))
        except IndexError:
            snapshotList.append(Snapshot("EMPTY_SNAPSHOT"))
    # match expressions: # Running test ExampleTest
    elif re.match(values["RUNNING_TEST"],line):
        try:
            snapshotList[-1].addTest(line.replace("[INFO]","").strip())
        except IndexError:
            snapshotList.append(Snapshot("EMPTY_SNAPSHOT"))
    elif re.match(values["TEST_RESULT"],line):
        if not re.match(values["TEST_EX"], line):
            snapshotList[-1].addTest("Total Tests: \n")
        snapshotList[-1].addTest(line.replace("[INFO]","").replace("[WARNING]","").strip())
    elif re.match(values["ERROR"],line):
        try:
            errorList.append((snapshotList[-1].getGoals())[-1].__str__() + line)
        except IndexError:
            errorList.append(line)
    elif re.match(values["WARNING"],line):
        warningList.append(line)
    elif re.match(values["DEPENDENCIES"],line):
        if not (re.match (values["DEPENDENCIES_FILTER"], line)):
            str = line.split(" ")[2].split('/')[-1][:-4]
            dependenciesList.append(str)

