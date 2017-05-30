from parserGradleJava import *


reponame="square/picasso"
f = open('logs\\picasso.txt', 'r')


common_parse(reponame)
check=checkGradleMaven()
if check== "maven":
    print "parser maven"
else:
    gradle_parse(f)