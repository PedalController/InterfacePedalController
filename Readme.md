# WebService - Rest v0.2.0

[![Build Status](https://travis-ci.org/PedalPi/WebService.svg?branch=master)](https://travis-ci.org/PedalPi/WebService) [![Code Health](https://landscape.io/github/PedalPi/WebService/master/landscape.svg?style=flat)](https://landscape.io/github/PedalPi/WebService/master) [![codecov](https://codecov.io/gh/PedalPi/WebService/branch/master/graph/badge.svg)](https://codecov.io/gh/PedalPi/WebService)


## Use

This project requires [PedalPi/Application](http://github.com/PedalPi/Application) project. See the [Application documentation](http://pedalpi-application.readthedocs.io/en/latest/#extending) for mode details.

This project requires dependencies too, like `Tornado` and `Requests` (for tests). For the full list, see [`requirements.txt`](https://github.com/PedalPi/WebService/blob/master/requirements.txt)

For a `config.py` example, see [`test/config.py`](https://github.com/PedalPi/WebService/blob/master/test/config.py)

## Rest

[Access the documentation](http://pedalpi.github.io/WebService/)  for API details.

### WebSocket

View ```websocker/UpdatesObserverSocket``` for details

## Using in your client

This code disposes the Application features in a WebService. These projects uses it for control.

* [Apk](https://github.com/PedalPi/Apk): App controller for smart devices and navigators.

If you are using too, please, send a pull request for this project.

## Project configuration

### Documentation

```bash
# Installing dependencies
npm install -g aglio

# Generate doc
aglio -i documentation.apib --theme-template triple -o index.html

# View documentation
firefox index.html
```

## Testing Rest

After started the a `Application` with `WebService` component, excute:

```bash

npm install -g dredd
dredd docs/documentation.apib http://localhost:3000
dredd docs/plugins.apib http://localhost:3000
dredd

# Run server
#coverage3 run --source=handler setup.py test
#coverage3 report
#coverage3 html
#firefox htmlcov/index.html
```
