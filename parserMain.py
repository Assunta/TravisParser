from domain.GradleLog import GradleLog
from domain.MavenLog import MavenLog
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
# reponame="simpligility/android-maven-plugin"
# f = open('logs\\maven\\android-maven-plugin\\android-maven-plugin-1233-156907093.txt', 'r')
# reponame="opf/openproject"
# f = open('logs\\ruby\\openproject\\openproject-22428-176253633.txt', 'r')
# reponame="jhy/jsoup"
# f = open('logs\\maven\\jsoup\\jsoup-406-176552717.txt', 'r')
# reponame="JodaOrg/joda-time"
# f = open('logs\\maven\\JodaOrg_joda-time\\joda-time-415-175370840.txt', 'r')
# reponame="bitcoinj/bitcoinj"
# f = open('logs\\maven\\bitcoinj_bitcoinj\\bitcoinj-1844-174824456.txt', 'r')
# reponame="languagetool-org/languagetool"
# f = open('logs\\maven\\languagetool-org_languagetool\\languagetool-4133-177081242.txt', 'r')
# reponame="google/error-prone"
# f = open('logs\\maven\\google_error-prone\\error-prone-523-174617444.txt', 'r')
# reponame="spotify/helios"
# f = open('logs\\maven\\spotify_helios\\helios-784-25695663.txt', 'r')
#
#gradle
# reponame="jakenjarvis/Android-OrmLiteContentProvider"
# f = open('logs\\Android-OrmLiteContentProvider-153-42729444.txt', 'r')
# reponame="codecov/example-android"
# f = open('logs\\gradle\\square_picasso\\square_picasso-1351-174648005.txt', 'r')
# reponame="Assunta/example"
# f = open('logs\\old\\example.txt', 'r')
# reponame="rockerhieu/emojicon"
# f = open('logs\\gradle\\rockerhieu_emojicon\\emojicon-142-113999428.txt', 'r')
# reponame="wasabeef/recyclerview-animators"
# f = open('logs\\gradle\\wasabeef_recyclerview-animators\\recyclerview-animators-180-80950913.txt', 'r')
reponame="square/picasso"
f = open('logs\\gradle\\square_picasso\\picasso-1352-174661345.txt', 'r')


# reponame="oblac/jodd"
# f = open('logs\\gradle\\oblac_jodd\\jodd-738-171756800.txt', 'r')


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
# reponame="travis-ci/travis-cookbooks"
# f = open('logs\\ruby\\travis-cookbook\\travis-cookbooks-3486-175761182.txt', 'r')




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
#TODO c'e' il caso di language: generic   -.-'
if linguaggio== "ruby":
    #supponiamo che si usa solo rake e che non usano maven
    parserRake(f)
else:
    tool=checkGradleMaven(f)
    if(tool=="maven"):
        #TODO prendere anche lo in mavenLog status....
        mavenLog=maven_parser(f, MavenLog(reponame))
        print mavenLog
    elif(tool=="gradle"):
        gradleLog=gradle_parser(f, GradleLog(reponame))
print ("PARSE END")