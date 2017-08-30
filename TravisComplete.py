from travispy import TravisPy

from analisys.gradleParser import parserGradle
from analisys.mavenParser import parserMaven
from analisys.rubyParser import parserRuby
from domain.Build import Build
import re

from domain.GradleLog import GradleLog
from domain.MavenLog import MavenLog
from domain.RubyLog import RubyLog
from parserGeneral import checkGradleMaven


def completeAnalysis(reponame):
    allBuilds=[]
    maxnumberbuilds = 2
    f = open('C:\\Users\\Assunta\\Desktop\\TESI\\TravisParser\\config\\token.config', 'r')
    token = f.readline()
    t = TravisPy.github_auth(str(token))
    repo = t.repo(reponame)
    builds = t.builds(slug=repo.slug)
    for count in range(0, min(maxnumberbuilds, len(builds))):
        # prendo la singola build
        build = builds[count]
        buildAfterAnalysis=completeAnalysisBuild(t, repo, build, reponame)
        allBuilds.append(buildAfterAnalysis)
        print buildAfterAnalysis.toJSON();

    return allBuilds


def completeAnalysisBuild(t, repo, build, reponame):
        ansi_escape = re.compile(r'\x1b\[[0-9]+(K)?(;[0-9])?(m)?')
        # prendo le informazioni generali
        b = common_parse(repo, build)
        #per ogni job faccio l'analisi del log
        for job_id in build.job_ids:
            # print job_id+"*****************************"
            job=t.job(job_id)
            log_text = t.log(job.log_id).body
            log_text = (ansi_escape.sub('', log_text)).split("\n")
            linguaggio= build.config["language"]
            tool = checkGradleMaven(log_text)
            if (tool == "maven"):
                mavenLog = parserMaven(log_text, MavenLog(reponame))
                # print mavenLog.toJSON()
                b.addLog(mavenLog)
            elif linguaggio == "ruby":
                rubyLog=parserRuby(log_text,RubyLog(reponame))
                b.addLog(rubyLog)
            else: #(tool == "gradle"):
                gradleLog = parserGradle(log_text, GradleLog(reponame))
                # print gradleLog.toJSON()
                b.addLog(gradleLog)
        return b


def common_parse(repo,build):
    commit = build.commit
    b = Build(build.number) #metto il build number perche' l'id non lo posso prendere
    b.setStatus(build.state)
    if repo.description is not None:
        b.setDescription(repo.description)
    b.setCommitId(build.commit_id)
    b.setIsPullRequest(build.pull_request)
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
    # print b.toJSON()
    return b

completeAnalysis("Mashape/unirest-java")