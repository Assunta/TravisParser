from parserGradleJava import *


reponame="wasabeef/recyclerview-animators"
f = open('logs\\wasabeef.txt', 'r')


common_parse(reponame)
check=checkGradleMaven()
if check== "maven":
    print "parser maven"
else:
    gradle_parse(f)