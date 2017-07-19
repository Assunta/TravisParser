
#count the status of all builds
def countStatStatus(results):
    #passed, failed, errored
    stats=[0.0,0.0,0.0]
    n= results.__len__()
    for build in results:
        status=build.getStatus()
        if status=="passed":
            stats[0]= stats[0]+1
        elif status=="failed":
            stats[1]=stats[1]+1
        else:
            stats[2]=stats[2]+1
    return [stats[0]/n*100, stats[1]/n*100,stats[2]/n*100]

#count the reasons of failures
def countReason(results):
    reason= {}


