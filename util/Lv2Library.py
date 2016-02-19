import commands
import re

class Extractor:
    def extract(self, file):
        stringPorts = self.stringPortsOf(file)
        
        data = {
            "ports":{}
        }
        
        for stringPort in stringPorts:
            port = self.extractJsonOf(stringPort)
            data["ports"][port["Name"]] = port
        
        return data

    def stringPortsOf(self, file):
        ports = []

        for port in file.split("Port "):
            if self.isPort(port):
                ports.append(port)

        return ports

    def isPort(self, possiblePort):
        return "Type:" in possiblePort
    
    def extractJsonOf(self, stringParam):
        params = {}
        lines = stringParam.split("\n")

        paramRegex = r"^(?:\t)(?:\t)(?:\w)+"
        valueRegex = r"(?:\:)(?:\s)+"

        paramName = None
        paramValue = None

        for line in lines[1:]:
            paramRegexResult = re.search(paramRegex, line) #paramRegex.exec(line)

            containsParamName = paramRegexResult != None
            if containsParamName:
                paramName = paramRegexResult.group(0).replace('\t\t', '').replace('\r', '')
                paramValue = line.replace(paramRegexResult.group(0), '').replace('\r', '')

                valueRegexResult = re.search(valueRegex, paramValue) #valueRegex.exec(paramValue)
                if valueRegexResult != None:
                    params[paramName] = paramValue.replace(valueRegexResult.group(0), '')
                else:
                    params[paramName] = None


            else:
                isSubObject = "=" in line

                line = line.strip().replace('\r', '')
                if line == '':
                    continue

                params[paramName] = self.multipleLineParamValueDefault(params[paramName], isSubObject)

                # Add value
                if isSubObject:
                    param = line.split("=")
                    params[paramName][param[0].strip()] = param[1].strip().replace('"', '')

                else:
                    params[paramName].append(line)

        return params
    
    def multipleLineParamValueDefault(self, param, isSubObject):
        isTypeSubobject = param == None and isSubObject
        isTypeList = type(param) is str

        if isTypeSubobject:
            return {}

        elif isTypeList:
            return [param]

        else:
            return param


def execute(command):
    return commands.getstatusoutput(command)[1]

def getPlugins():
    return execute("lv2ls").split("\n")

def getPluginInfo(lv2Plugin):
    return execute("lv2info " + lv2Plugin)

class Lv2Library:
    plugins = {}
    errors = []
    
    def __init__(self):
        extractor = Extractor()

        for lv2Plugin in getPlugins():
            try:
                self.plugins[lv2Plugin] = extractor.extract(getPluginInfo(lv2Plugin))
            except Exception as e:
                self.errors.append(lv2Plugin)

if __name__ == "__main__":
    lib = Lv2Library()
    print(lib.plugins.keys())
    print(lib.plugins["http://guitarix.sourceforge.net/plugins/gx_studiopre_st#studiopre_st"])