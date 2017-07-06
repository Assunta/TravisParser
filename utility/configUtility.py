
def getKeyValueRuby():
    var={}
    with open("C:\\Users\\Assunta\\Desktop\\TESI\\TravisParser\\config\\ruby.config") as file:
        for line in file:
            name, value=line.partition("=")[::2]
            var[name.strip()]=value
    return var

def getKeyValueMaven():
    var={}
    with open("C:\\Users\\Assunta\\Desktop\\TESI\\TravisParser\\config\\maven.config") as file:
        for line in file:
            name, value=line.partition("=")[::2]
            var[name.strip()]=value
    return var

def getKeyValueGradle():
    var={}
    with open("C:\\Users\\Assunta\\Desktop\\TESI\\TravisParser\\config\\gradle.config") as file:
        for line in file:
            name, value=line.partition("=")[::2]
            var[name.strip()]=value
    return var
