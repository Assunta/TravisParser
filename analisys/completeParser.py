import os
import re

import mmap

import sys
from travispy import TravisPy

from analisys.gradleParser import parserGradle
from analisys.mavenParser import parserMaven
from analisys.rubyParser import parserRuby
from domain.Build import Build
from domain.GradleLog import GradleLog
from domain.MavenLog import MavenLog
from domain.RubyLog import RubyLog
from utility.dbUtility import getToken

reload(sys)
sys.setdefaultencoding('utf-8')

def getRefreshBuilds(username,reponame, buildOld):
    allBuilds = []
    ansi_escape = re.compile(r'\x1b\[[0-9]+(K)?(;[0-9])?(m)?')
    # f = open('C:\\Users\\Assunta\\Desktop\\TESI\\TravisParser\\config\\token.config', 'r')
    # token = f.readline()
    token= getToken(username)
    t = TravisPy.github_auth(str(token))
    print reponame
    repo = t.repo(reponame)
    lastBuild= repo.last_build_number
    if(buildOld[0]["idBuild"]==lastBuild):
        print "The project is up to date!!"
        return allBuilds
    else:
        print "last analyzed= "+buildOld[0]["idBuild"]
        print "last build: " + str(lastBuild)
        lastBuild = str(int(lastBuild) + 1)
        builds=completeAnalysis(username,reponame, lastBuild)
        lastBuild=int(builds[-1].getBuildID())
        print "last build: "+str(lastBuild)
        for b in builds:
            print b.getBuildID()
        while (lastBuild>int(buildOld[0]["idBuild"])):
            other_builds=completeAnalysis(username,reponame, lastBuild)
            for b in other_builds:
                builds.append(b)
                print b.getBuildID()
            lastBuild = int(other_builds[-1].getBuildID())
            print "last build: " + str(lastBuild)
        return builds



def getBuilds(username,reponame):
    # f = open('C:\\Users\\Assunta\\Desktop\\TESI\\TravisParser\\config\\token.config', 'r')
    # token = f.readline()
    token = getToken(username)
    t = TravisPy.github_auth(str(token))
    repo = t.repo(reponame)
    lastBuild= repo.last_build_number

    # lastBuild=24
    lastBuild = str(int(lastBuild) + 1)
    print "last build: " + str(lastBuild)
    builds=completeAnalysis(username,reponame, lastBuild)
    lastBuild=int(builds[-1].getBuildID())
    print "last build: "+str(lastBuild)
    for b in builds:
        print b.getBuildID()
    while (lastBuild>1):
        other_builds=completeAnalysis(username,reponame, lastBuild)
        for b in other_builds:
            builds.append(b)
            print b.getBuildID()
        lastBuild = int(other_builds[-1].getBuildID())
        print "last build: " + str(lastBuild)
    return builds





def completeAnalysis(username,reponame, afterBuild):
    allBuilds = []
    ansi_escape = re.compile(r'\x1b\[[0-9]+(K)?(;[0-9])?(m)?')
    maxnumberbuilds =25
    # f = open('C:\\Users\\Assunta\\Desktop\\TESI\\TravisParser\\config\\token.config', 'r')
    # token = f.readline()
    token = getToken(username)
    t = TravisPy.github_auth(str(token))
    repo = t.repo(reponame)
    builds = t.builds(slug=repo.slug, after_number=afterBuild)
    for count in range(0,min(maxnumberbuilds, len(builds))):
        # catch one build
        build = builds[count]
        #obtain general information about the build
        buildUnderAnalysis= generalInfo(repo, build)
        #job analysis
        for job_id in build.job_ids:
            try:
                job = t.job(job_id)
                log_text = t.log(job.log_id).body
                log_text = (ansi_escape.sub('', log_text))
                #I have to write the log into a file because if I analyze the logstring the scripts don't work....
                fOut = open(str(job_id)+'.txt','w+')
                fOut.write(log_text)
                fOut.close()
                #TODO pensare bene qui se ci puo' essere conflitto con il nome del file
                fIn=open(str(job_id)+'.txt','r')
                language = build.config["language"]
                tool = checkGradleMavenFile(fIn)
                if (tool == "maven"):
                    mavenLog = parserMaven(username,fIn, MavenLog(job_id))
                    buildUnderAnalysis.addLog(mavenLog)
                elif language == "ruby":
                    rubyLog = parserRuby(username,fIn, RubyLog(job_id))
                    buildUnderAnalysis.addLog(rubyLog)
                else:  # (tool == "gradle"):
                    gradleLog = parserGradle(username,fIn, GradleLog(job_id))
                    buildUnderAnalysis.addLog(gradleLog)
                fIn.close()
                os.remove(str(job_id)+'.txt')
            except Exception,e:
                print "Some exception"+ str(e)
                try:
                    fIn.close()
                    os.remove(str(job_id) + '.txt')
                except Exception, e2:
                    print str(e2)
        #print(buildUnderAnalysis.toJSON())
        allBuilds.append(buildUnderAnalysis)
    return allBuilds



def generalInfo(repo,build):
    try:
        b = Build(build.number)  # metto il build number perche' l'id non lo posso prendere
        commit = build.commit

        b.setStatus(build.state)
        if repo.description is not None:
            b.setDescription(repo.description)
        b.setCommitId(build.commit_id)
        b.setIsPullRequest(str(build.pull_request))
        if(build.pull_request):
            b.setTitlePull(build.pull_request_title)
            b.setPullId(str(build.pull_request_number))
        b.setStart(str(build.started_at))
        b.setFinish(str(build.finished_at))
        if build.duration is not None:
            b.setDuration(build.duration)
        b.setCommitSHA(commit.sha)
        b.setBranch(commit.branch)
        b.setCommit(commit.message)
        if commit.committed_at is not None:
            b.setCommitDate(commit.committed_at)
        b.setAuthor(commit.author_name)
        b.setEmail(commit.author_email)
        b.setLanguage(build.config["language"])
        b.setNumJobs(len(build.job_ids))
    except Exception, e:
        print "Some exception" + str(e)
    #print b.toJSON()
    return b



#check gradle o maven
def checkGradleMavenFile(f):
    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    if s.find ('[INFO] Scanning for projects') != -1:
        return "maven"
    else:
        return "gradle"

