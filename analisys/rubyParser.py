import re

from domain.Error import Error
from utility.configUtility import getKeyValueRuby
from utility.dbUtility import getStatusMessages, getRubyTools, getRubyTestMessages, getRubyErrors



#set this like a global variable so i open the connection with the db only once and store the items into the list


def parserRuby(username,f, log):
    statusMessage = getStatusMessages()
    tools = getRubyTools(username)
    testMessages = getRubyTestMessages(username)
    errors = getRubyErrors(username)
    errorList = list()
    dependenciesList = list()
    commandList = ["no command"]
    testList = list()
    warningList = list()
    toollist = list()
    status = "passed"
    listStatusMessages = list()
    for line in f:
            #checkMainInfo(line)
            values = getKeyValueRuby()
            if re.match(values["DEPENDENCIES"], line):
                try:
                    dependenciesList.append(line.split(" ")[1].strip() + " " + line.split(" ")[2].strip())
                except:
                    dependenciesList.append(line.split(" ")[1].strip())
            elif re.match(values["GEM_COMPLEATE"], line):
                dependenciesList.append((line.strip()))
            elif re.match(values["COMMANDS"], line):
                if not re.match(values["COMMANDS_EX"], line):
                    commandList.append(line.split("$", 1)[1].strip())
            elif re.match(values["WARNING"], line):
                warningList.append(line.strip())
            #checkOtherTools(line)
            for tool in tools:
                if re.match(tool.get("regex"), line):
                    toollist.append(tool.get("tool"))
                    break
            #status=checkStatus(line)
            for mess in statusMessage:
                if re.match(mess.get("regex"), line):
                    status = mess.get("status")
                    listStatusMessages.append(line.strip())
                    break
            #checkTestingMessages(line)
            for msg in testMessages:
                if re.match(msg.get("regex"), line):
                    testList.append(msg.get("category") + ":" + line.strip().replace("......", ""))
                    break
            #checkErrors(line)
            for msg in errors:
                if re.match(msg.get("regex"), line):
                    error = Error(line.strip())
                    error.setTask(commandList[-1])
                    error.setCategory(msg.get("category"))
                    errorList.append(error)
                    break

    log.setDependencies(list(set(dependenciesList)))
    log.addErrorList(errorList)
    log.setTest(testList)
    log.setCommand(commandList)
    log.setStatus(status)
    log.setWarning(list(set(warningList)))
    log.setTool(list(set(toollist)))
    log.setStatusMessages(listStatusMessages)
    #print log.toJSON()
    return log

# #check the presence of a command, warnings or dependencies
# def checkMainInfo(line):
#     values=getKeyValueRuby()
#     if re.match(values["DEPENDENCIES"],line):
#         try:
#             dependenciesList.append(line.split(" ")[1].strip() + " " + line.split(" ")[2].strip())
#         except:
#             dependenciesList.append(line.split(" ")[1].strip())
#     elif re.match(values["GEM_COMPLEATE"], line):
#         dependenciesList.append((line.strip()))
#     elif re.match(values["COMMANDS"],line):
#         if not re.match(values["COMMANDS_EX"], line):
#             commandList.append(line.split("$", 1)[1].strip())
#     elif re.match(values["WARNING"],line):
#         warningList.append(line.strip())
#
#
# #check the usage of tools
# def checkOtherTools(line):
#     for tool in tools:
#         if re.match(tool.get("regex"), line):
#             toollist.append(tool.get("tool"))
#             break
#
#
# #check line to discover status message and set the status of the job
# def checkStatus(line):
#     status="passed"
#     for mess in statusMessage:
#         if re.match(mess.get("regex"), line):
#             status = mess.get("status")
#             listStatusMessages.append(line.strip())
#             break
#     return status
#
# #check message of testing executed
# def checkTestingMessages(line):
#     for msg in testMessages:
#         if re.match(msg.get("regex"), line):
#             testList.append(msg.get("category") + ":" + line.strip().replace("......", ""))
#             break
#
# #check for error messages
# def checkErrors(line):
#     for msg in errors:
#         if re.match(msg.get("regex"), line):
#             error = Error(line.strip())
#             error.setTask(commandList[-1])
#             error.setCategory(msg.get("category"))
#             errorList.append(error)
#             break
