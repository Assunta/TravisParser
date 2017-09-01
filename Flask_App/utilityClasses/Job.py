from analisys.completeParser import getRefreshBuilds
from utility.storeObject import restore, store


def addBackgroundFunction(username, reponame):
    filename=username + "_" +reponame.replace("/", "_")
    builds=restore(filename)
    result = getRefreshBuilds(username,reponame, builds)
    # remove duplicate if present
    all = result
    if result.__len__() > 0:
        index = result[-1].getBuildID()
        for item in builds:
            if int(item["idBuild"]) < int(index):
                result.append(item)
        store(all, filename)

