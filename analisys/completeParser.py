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

reload(sys)
sys.setdefaultencoding('utf-8')

def completeAnalysis(reponame):

    allBuilds = []
    ansi_escape = re.compile(r'\x1b\[[0-9]+(K)?(;[0-9])?(m)?')
    maxnumberbuilds =10
    f = open('C:\\Users\\Assunta\\Desktop\\TESI\\TravisParser\\config\\token.config', 'r')
    token = f.readline()
    t = TravisPy.github_auth(str(token))
    repo = t.repo(reponame)
    builds = t.builds(slug=repo.slug)
    for count in range(0, min(maxnumberbuilds, len(builds))):
        # catch one build
        build = builds[count]
        #obtain general information about the build
        buildUnderAnalysis= generalInfo(repo, build)
        #job analysis
        for job_id in build.job_ids:
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
                mavenLog = parserMaven(fIn, MavenLog(job_id))
                buildUnderAnalysis.addLog(mavenLog)
            elif language == "ruby":
                rubyLog = parserRuby(fIn, RubyLog(job_id))
                buildUnderAnalysis.addLog(rubyLog)
            else:  # (tool == "gradle"):
                gradleLog = parserGradle(fIn, GradleLog(job_id))
                buildUnderAnalysis.addLog(gradleLog)
            fIn.close()
            os.remove(str(job_id)+'.txt')
        #print(buildUnderAnalysis.toJSON())
        allBuilds.append(buildUnderAnalysis)
    return allBuilds



def generalInfo(repo,build):
    commit = build.commit
    b = Build(build.number) #metto il build number perche' l'id non lo posso prendere
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
    #print b.toJSON()
    return b



#check gradle o maven
def checkGradleMavenFile(f):
    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    if s.find ('[INFO] Scanning for projects') != -1:
        return "maven"
    else:
        return "gradle"


# for b in completeAnalysis("languagetool-org/languagetool"):
#     print "*******************************************"
    # print b.toJSON()