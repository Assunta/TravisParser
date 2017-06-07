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

reponame="richpeck/exception_handler"
f = open('logs\\ruby\\exception_handler\\exception_handler-1264-168008434.txt', 'r')
# f = open('logs\\ruby\\samson-7945-175559529.txt', 'r')
#f = open('logs\\ruby\\github-services-662-175477697.txt', 'r')
# reponame="psu-stewardship/scholarsphere"
# f = open('logs\\ruby\\scholarsphere-4009-175444902.txt', 'r')
# f=open('logs\\ruby\\octopress-963-145287347.txt','r')
# f = open('logs\\ruby\\wraith-967-164825319.txt', 'r')


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