from parserGeneral import *
from parserGradle import *
from parserMaven import maven_parser
from parserRake import parserRake


#maven
# reponame="springside/springside4"
# f = open('logs\\springside4-442-153294230.txt', 'r')

# reponame="pulse00/Twig-Eclipse-Plugin"
# f = open('logs\\Twig-Eclipse-Plugin-137-168865827.txt', 'r')
# reponame="Assunta/example2"
# f = open('logs\\example2-6-173560799.txt', 'r')
#
#gradle
# reponame="jakenjarvis/Android-OrmLiteContentProvider"
# f = open('logs\\Android-OrmLiteContentProvider-153-42729444.txt', 'r')
# reponame="codecov/example-android"
# f = open('logs\\example-android-48-67063849.txt', 'r')

#ruby
# reponame="zendesk/samson"
# f = open('logs\\ruby\\samson\\samson-7987-175874498.txt', 'r')
# reponame="ManageIQ/manageiq"
# f = open('logs\\ruby\\ManageIQ\\manageiq-59083-175928155.txt', 'r')
# rapid7/metasploit-framework
# reponame="rapid7/metasploit-framework"
# f = open('logs\\ruby\\metasploit-framework\\metasploit-framework-20590-175876290.txt', 'r')
# reponame="richpeck/exception_handler"
# f = open('logs\\ruby\\exception_handler\\exception_handler-1264-168008434.txt', 'r')
reponame="travis-ci/travis-cookbooks"
f = open('logs\\ruby\\travis-cookbook\\travis-cookbooks-3486-175761182.txt', 'r')




#per prendere l'id purtoppo non c'e' un metodo di build e quindi dobbiamo leggerlo dal log.........
#TODO gestire il caso in cui il numero di build non c'e' nel file
def getBuildId(f):
    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    index= s.find('Build id:')
    if index !=-1:
        s.seek(index)
        id=s.readline().split(":")[1].strip()
        return id
    else:
        print "Error: non e' possibile prendere la build id dal log......"
        return -1



linguaggio=common_parse(reponame, getBuildId(f))
print "\nLOG"
if linguaggio== "ruby":
    #supponiamo che si usa solo rake e che non usano maven
    parserRake(f)
else:
    tool=checkGradleMaven(f)
    if(tool=="maven"):
        maven_parser(f)
    elif(tool=="gradle"):
        gradle_parser(f)
print ("PARSE END")