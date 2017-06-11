from travispy import TravisPy

maxnumberbuilds=10
f = open('token.config', 'r')
token = f.readline()
t = TravisPy.github_auth(str(token))

def common_parse(reponame):
    builds = t.builds(slug=reponame)
    for count in range(0, min(maxnumberbuilds, len(builds))):
        build = builds[count]
        repo= t.repo(reponame)
        commit=build.commit
        print "Nome : "+repo.slug
        print "Stato: " + build.state
        if repo.description is not None:
             print "Descrizione: " +repo.description
        print "Build number: " + build.number
        print "Commit ID: " + str(build.commit_id)
        print "Pull request?: "+str(build.pull_request)
        if(build.pull_request):
            print "Titolo pull request: "+build.pull_request_title
            print "Numero pull request: "+str(build.pull_request_number)
        print "Iniziato a: "+str(build.started_at)
        print "Finito a: "+str(build.finished_at)
        print "Durata: "+'%02d:%02d' % ((build.duration/60),build.duration%60) # build.duration da isecondi
        print "Commit SHA: " + commit.sha
        print "Branch: "+commit.branch
        print "Commit message: "+commit.message
        if commit.committed_at is not None:
            print "Data commit: "+ commit.committed_at
        print "Autore commit: "+ commit.author_name
        print "Email Autore commit: "+ commit.author_email
        #informazioni file travis.yml
        # potremmo estrarre qualche informazione da qui
        print build.config
        print "Language: "+build.config["language"]
        print "Numero jobs: "+str(len(build.job_ids))
        #return build.config["language"]
        print "****************************************************"

common_parse("chef/chef")
