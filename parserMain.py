from parserGradleJava import *
from parserGradle import *



reponame="passy/Android-DirectoryChooser"
f = open('logs\\AndroidDirChooser.txt', 'r')



common_parse(reponame)
tool=checkGradleMaven()
if(tool=="maven"):
    maven_parse(f)
elif(tool=="gradle"):
    gradle_parser(f)
print ("PARSE END")