from datetime import datetime

INTERNET=False

def getAuthors(results):
    authors = set();
    for build in results:
        if INTERNET:
            authors.add(build.getAuthor());
        else:
            authors.add(build["author"]);
    return list(authors)



#count the status of all builds
def countStatStatus(results):
    #passed, failed, errored, cancled
    stats=[0.0,0.0,0.0, 0.0]
    n= results.__len__()
    for build in results:
        if INTERNET:
        #quando c'e' internet
            status=build.getStatus()
        else:
        #quando non c'e
            status = build["status"]
        if status=="passed":
            stats[0]= stats[0]+1
        elif status=="failed":
            stats[1]=stats[1]+1
        elif status=="errored":
            stats[2]=stats[2]+1
        else:
            stats[3] = stats[3] + 1
    return [stats[0]/n*100, stats[1]/n*100,stats[2]/n*100,stats[3]/n*100]

# count the reasons of failures
def countReason(results):
    reason= {}
    tot=0
    for b in results:
        if INTERNET:
            for log in b.getLogs():
                if log.getStatus()!="passed":
                    tot = tot + 1
                    error = log.getTypeOfError()
                    value = reason.get(error, None)
                    if value is not None:
                        reason[error] = reason.get(error) + 1.0
                    else:
                        reason[error] = 1.0
        else:
            for log in b["Logs"]:
                if  log["status"]!="passed":
                    tot=tot+1
                    error=log["typeOfError"]
                    value= reason.get(error, None)
                    if value is not None:
                        reason[error]= reason.get(error)+1.0
                    else:
                        reason[error]=1.0
    # obtain %
    for key, value in reason.iteritems():
        reason[key]=float(value/tot*100)
    print reason
    return reason


#count the status of all builds
def countStatStatusFilter(results, start, finish, authors):
    #passed, failed, errored, cancled
    stats=[0.0,0.0,0.0, 0.0]
    n= results.__len__()
    for build in results:
        status = build["status"]
        dateObject= datetime.strptime(build["StartDate"], '%Y-%m-%d')
        if not (dateObject<=finish and dateObject>=start):
           n=n-1
        elif build["author"] in authors:
            if status=="passed":
                stats[0]= stats[0]+1
            elif status=="failed":
                stats[1]=stats[1]+1
            elif status=="errored":
                stats[2]=stats[2]+1
            else:
                stats[3] = stats[3] + 1
        else:
             n = n - 1
    return [stats[0]/n*100, stats[1]/n*100,stats[2]/n*100,stats[3]/n*100]


def countReasonFilter (results, start, finish, authors):
    reason = {}
    tot = 0
    for b in results:
        dateObject = datetime.strptime(b["StartDate"], '%Y-%m-%d')
        if  (dateObject <= finish and dateObject >= start):
            if b["author"] in authors:
                for log in b["Logs"]:
                    if log["status"] != "passed":
                        tot = tot + 1
                        error = log["typeOfError"]
                        value = reason.get(error, None)
                        if value is not None:
                            reason[error] = reason.get(error) + 1.0
                        else:
                            reason[error] = 1.0
    # obtain %
    for key, value in reason.iteritems():
        reason[key] = float(value / tot * 100)
    return reason