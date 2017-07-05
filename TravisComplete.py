from travispy import TravisPy
from domain.Build import Build
import re

from domain.GradleLog import GradleLog
from domain.MavenLog import MavenLog
from parserGeneral import checkGradleMaven
from parserGradle import gradle_parser
from parserMaven import maven_parser
from parserRake import parserRake



def completeAnalysis(reponame):
    ansi_escape = re.compile(r'\x1b\[[0-9]+(K)?(;[0-9])?(m)?')
    maxnumberbuilds = 2
    f = open('C:\\Users\\Assunta\\Desktop\\TESI\\TravisParser\\config\\token.config', 'r')
    token = f.readline()
    t = TravisPy.github_auth(str(token))
    repo = t.repo(reponame)
    builds = t.builds(slug=repo.slug)
    for count in range(0, min(maxnumberbuilds, len(builds))):
        #prendo la singola build
        build = builds[count]
        #prendo le informazioni generali
        b=common_parse(repo,build)
        #per ogni job faccio l'analisi del log
        for job_id in build.job_ids:
            job=t.job(job_id)
            log_text = t.log(job.log_id).body
            log_text = (ansi_escape.sub('', log_text)).split("\n")
            linguaggio= build.config["language"]
            if linguaggio == "ruby":
                # supponiamo che si usa solo rake e che non usano maven
                parserRake(log_text)
            else:
                tool = checkGradleMaven(log_text)
                if (tool == "maven"):
                    # TODO prendere anche lo in mavenLog status....
                    mavenLog = maven_parser(log_text, MavenLog(reponame))
                    print mavenLog.toJSON()
                elif (tool == "gradle"):
                    gradleLog = gradle_parser(log_text, GradleLog(reponame))
                    print gradleLog.toJSON()
    return b


def common_parse(repo,build):
    commit = build.commit
    b = Build(build.number) #metto il build number perche' l'id non lo posso prendere
    b.setStatus(build.state)
    if repo.description is not None:
        b.setDescription(repo.description)
    b.setBuildNumber(build.number)
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
    print b.toJSON()
    return b

# completeAnalysis("Mashape/unirest-java")