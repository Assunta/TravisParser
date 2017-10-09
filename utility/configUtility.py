import os
def getKeyValueRuby():
    var={}
    current_file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
    other_file_path = current_file_dir+ "\\config\\ruby.config"
    with open(other_file_path) as file:
        for line in file:
            name, value=line.partition("=")[::2]
            var[name.strip()]=value
    return var

def getKeyValueMaven():
    var={}
    current_file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    other_file_path = current_file_dir + "\\config\\maven.config"
    with open(other_file_path) as file:
        for line in file:
            name, value=line.partition("=")[::2]
            var[name.strip()]=value
    return var

def getKeyValueGradle():
    var={}
    current_file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    other_file_path = current_file_dir + "\\config\\gradle.config"
    with open(other_file_path) as file:
        for line in file:
            name, value=line.partition("=")[::2]
            var[name.strip()]=value
    return var
