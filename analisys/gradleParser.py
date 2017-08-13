import re

from domain.GradleCommand import GradleCommand
from domain.Task import Task
from utility.configUtility import getKeyValueGradle
from utility.dbUtility import getStatusMessages

status = "passed"
commandList = list()
# default command to safe execution
commandList.append(GradleCommand("DEFAULT"))
errorList = list()
noteList = list()
dependenciesList = list()
statusErrorList = list()

values = getKeyValueGradle()
statusMessage = getStatusMessages()


def parserGradle(f, gradleLog):
    status = "passed"
    commandList = list()
    # default command to safe execution
    commandList.append(GradleCommand("DEFAULT"))
    errorList = list()
    noteList = list()
    dependenciesList = list()
    statusErrorList = list()
    taskList = list()
    for line in f:
        # match gradle command
        if re.match(values["GRADLE_COMMAND"], line):
            # add tasks to old command and create new command
            commandList[-1].addListaTasks(taskList)
            taskList=list()
            commandList.append(GradleCommand(line.split("$")[1].strip()))
        #checkMainInfo(line, taskList)
            # match gradle task
        if re.match(values["TASK"], line):
            task = line.split(" ")[0]
            if task.count(":") == 2:
                # get project name and task name
                module_name = task.split(":")[1]
                task_name = task.split(":")[2]
                if task_name == "":
                    t = Task(module_name)
                else:
                    t = Task(task_name.strip())
                    t.setProjectName(module_name)
            else:
                t = Task(task.replace(":", "").strip())
                t.setProjectName(" ")
            if re.match(values["UP_TO_DATE"], line):
                t.setIsUpdate()
            elif re.match(values["FAILED"], line):
                t.setIsFailed()
            elif re.match(values["SKIPPED"], line):
                t.setIsSkipped()
            # check if a task is present in the list
            if len(taskList) > 0:
                taskOld = taskList.pop(-1)
                if taskOld is not None and not taskOld.__eq__(t):
                    taskList.append(taskOld)
                    taskList.append(t)
                else:
                    taskList.append(t)
            else:
                taskList.append(t)
        elif re.match(values["NOTE"], line):
            try:
                noteList.append(taskList[-1].getName() + "\t" + line.strip())
            except IndexError:
                noteList.append("NO_TASK" + "\t" + line.strip())
        elif re.match(values["SKIPPED_TASK"], line):
            taskList[-1].setIsSkipped()
            # error messages
        elif re.match(values["ERROR"], line):
            try:
                errorList.append(taskList[-1].getName() + "\t" + taskList[-1].getCategory() + "\t" + line)
            except IndexError:
                errorList.append("NO_TASK" + "\tother\t" + line)
        elif re.match(values["DEPENDENCIES"], line):
            dependenciesList.append(line.replace("Download", "").strip().split("/")[-1])

        #status = checkStatus(line)
        status = "passed"
        for mess in statusMessage:
            if re.match(mess.get("regex"), line):
                status = mess.get("status")
                statusErrorList.append(line.strip())
                break

    commandList[-1].addListaTasks(taskList)
    gradleLog.addCommands(commandList)
    gradleLog.addErrorList(errorList, list(set(statusErrorList)))
    gradleLog.addListaNote(list(set(noteList)))
    gradleLog.addDependencies(dependenciesList)
    gradleLog.setStatus(status)
    gradleLog.setListaErroriStatus(list(set(statusErrorList)))

    # print gradleLog.toJSON()
    return gradleLog


# # check the presence of commands, tasks, errors, warnings, dependencies
# def checkMainInfo(line, taskList):
#     # match gradle task
#     if re.match(values["TASK"], line):
#         task = line.split(" ")[0]
#         if task.count(":") == 2:
#             # get project name and task name
#             module_name = task.split(":")[1]
#             task_name = task.split(":")[2]
#             t = Task(task_name.strip())
#             t.setProjectName(module_name)
#         else:
#             t = Task(task.replace(":", "").strip())
#             t.setProjectName(" ")
#         if re.match(values["UP_TO_DATE"], line):
#             t.setIsUpdate()
#         elif re.match(values["FAILED"], line):
#             t.setIsFailed()
#         elif re.match(values["SKIPPED"], line):
#             t.setIsSkipped()
#         # check if a task is present in the list
#         if len(taskList) > 0:
#             taskOld = taskList.pop(-1)
#             if taskOld is not None and not taskOld.__eq__(t):
#                 taskList.append(taskOld)
#                 taskList.append(t)
#             else:
#                 taskList.append(t)
#         else:
#             taskList.append(t)
#     elif re.match(values["NOTE"], line):
#         try:
#             noteList.append(taskList[-1].getName() + "\t" + line.strip())
#         except IndexError:
#             noteList.append("NO_TASK" + "\t" + line.strip())
#     elif re.match(values["SKIPPED_TASK"], line):
#         taskList[-1].setIsSkipped()
#     # error messages
#     elif re.match(values["ERROR"], line):
#         try:
#             errorList.append(taskList[-1].getName() + "\t" + taskList[-1].getCategory() + "\t" + line)
#         except IndexError:
#             errorList.append("NO_TASK" + "\tother\t" + line)
#     elif re.match(values["DEPENDENCIES"], line):
#         dependenciesList.append(line.replace("Download", "").strip())
#
#
# def checkStatus(line):
#     status = "passed"
#     for mess in statusMessage:
#         if re.match(mess.get("regex"), line):
#             status = mess.get("status")
#             statusErrorList.append(line.strip())
#             break
#     return status
