"use strict";

const fs = require('fs');
const execSync = require('child_process').execSync;


class Extractor {
    extract(file) {
        let stringPorts = this.stringPortsOf(file);

        let data = {
            ports : {}
        };

        for (let stringPort of stringPorts) {
            let port = this.extractJsonOf(stringPort);
            data.ports[port['Name']] = port;
        }

        return data;
    }

    stringPortsOf(file) {
        let ports = [];

        for (let port of file.split("Port "))
            if (this.isPort(port))
                ports.push(port);

        return ports;
    }

    isPort(possiblePort) {
        return possiblePort.includes("Type:");
    }

    extractJsonOf(stringParam) {
        let params = {};
        let lines = stringParam.split("\n");

        let paramRegex = /^(?:\t)(?:\t)(?:\w)+/;
        let valueRegex = /(?:\:)(?:\s)+/;

        let paramName = null;
        let paramValue = null;

        for (let i = 1; i<lines.length; i++) {
            let line = lines[i];
            console.log(line)
            return

            let paramRegexResult = paramRegex.exec(line);

            let containsParamName = paramRegexResult != null;
            if (containsParamName) {
                paramName = paramRegexResult[0].replace('\t\t', '').replace('\r', '');
                paramValue = line.replace(paramRegexResult[0], '').replace('\r', '');

                let valueRegexResult = valueRegex.exec(paramValue);
                if (valueRegexResult != null)
                    params[paramName] = paramValue.replace(valueRegexResult[0], '');
                else
                    params[paramName] = null;


            } else {
                let isSubObject = line.includes("=");

                line = line.trim().replace('\r', '');
                if (line == '')
                    continue;

                params[paramName] = this.multipleLineParamValueDefault(
                    params[paramName],
                    isSubObject
                );

                // Add value
                if (isSubObject) {
                    let param = line.split("=");
                    params[paramName][param[0].trim()] = param[1].trim(0).replace('"', '');

                } else
                    params[paramName].push(line);
            }
        }

        return params;
    }

    multipleLineParamValueDefault(param, isSubObject) {
        let isTypeSubobject = param == null && isSubObject;
        let isTypeList = typeof param == 'string';

        if (isTypeSubobject)
            return {};

        else if (isTypeList)
            return [param];

        else
            return param;
    }
}

let extractor = new Extractor();

/*
let file = fs.readFileSync("./lib/example.txt", 'utf8');
let effectData = extractor.extract(file);
effectData.uri = "example";
fs.writeFileSync(
    `./lib/plugins/example.json`,
    JSON.stringify(effectData)
);
*/



for (let lv2Plugin of execSync('lv2ls').toString().split('\n')) {
    if (lv2Plugin == '')
        return;

    let data = execSync('lv2info ' + lv2Plugin).toString();
    let effectData = extractor.extract(data);
    effectData.uri = lv2Plugin;

    let name = lv2Plugin.split('/');
    name = name[name.length-1];

    fs.writeFileSync(`./plugins/${name}.json`, JSON.stringify(effectData));
}