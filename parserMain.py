from parserGeneral import *
from parserGradle import *
from parserMaven import maven_parser



#maven
# reponame="springside/springside4"
# f = open('logs\\springside4-442-153294230.txt', 'r')
reponame="pulse00/Twig-Eclipse-Plugin"
f = open('logs\\Twig-Eclipse-Plugin-137-168865827.txt', 'r')
# reponame="Assunta/example2"
# f = open('logs\\example2-6-173560799.txt', 'r')
#
#gradle
# reponame="jakenjarvis/Android-OrmLiteContentProvider"
# f = open('logs\\Android-OrmLiteContentProvider-153-42729444.txt', 'r')
# reponame="codecov/example-android"
# f = open('logs\\example-android-48-67063849.txt', 'r')

#per prendere l'id purtoppo non c'e' un metodo di build e quindi dobbiamo leggerlo dal log.........
# problema: non i tutti i log ci sta build_id....
#come si fa?
#TODO sistemare
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



common_parse(reponame, getBuildId(f))
tool=checkGradleMaven(f)
if(tool=="maven"):
    maven_parser(f)
elif(tool=="gradle"):
    gradle_parser(f)
print ("PARSE END")