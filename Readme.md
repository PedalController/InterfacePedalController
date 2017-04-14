# WebService - Rest v0.2.0

[![Build Status](https://travis-ci.org/PedalPi/WebService.svg?branch=master)](https://travis-ci.org/PedalPi/WebService) [![Code Health](https://landscape.io/github/PedalPi/WebService/master/landscape.svg?style=flat)](https://landscape.io/github/PedalPi/WebService/master) [![codecov](https://codecov.io/gh/PedalPi/WebService/branch/master/graph/badge.svg)](https://codecov.io/gh/PedalPi/WebService)


## Use

This project requires [PedalPi/Application](http://github.com/PedalPi/Application) project. See the [Application documentation](http://pedalpi-application.readthedocs.io/en/latest/#extending) for mode details.

This project requires dependencies too, like `Tornado` and `Requests` (for tests). For the full list, see [`requirements.txt`](https://github.com/PedalPi/WebService/blob/master/requirements.txt)

For a `config.py` example, see [`test/config.py`](https://github.com/PedalPi/WebService/blob/master/test/config.py)

## Rest

### Auth

Not implemented

### Plugins

* ```/effects```:
  * **GET** all plugins effects instaled
* ```/effect/(?P<pluginUri>[^/]+)```:
  * **GET** specific plugin data by
  * Params
    * **pluginUri**: URI of plugin required

### Banks

* ```/banks```
  *  **GET** all banks

### Bank

* ```/bank```
  * **POST** a new bank.
  * Returns the new bank index
* ```/bank/(?P<bankIndex>[0-9]+)```
  * **GET** a bank
  * **PUT** for update a bank
  * **DELETE** a bank
  * Params
    * **bankIndex**

### Pedalboard

* ```/bank/(?P<bankIndex>[0-9]+)/pedalboard```
  * **POST** a new pedalboard.
  * Returns the pedalboard index
  * Params
    * **bankIndex**
* ```/bank/(?P<bankIndex>[0-9]+)/pedalboard/(?P<pedalboardIndex>[0-9]+)```
  * **GET** a pedalboard
  * **PUT** for update a pedalboard
  * **DELETE** a pedalboard
  * Params
    * **bankIndex**
    * **pedalboardIndex**

### Effect

* ```/bank/(?P<bankIndex>[0-9]+)/pedalboard/(?P<pedalboardIndex>[0-9]+)/effect```
  * **POST** a new effect.
  * Returns the effect index
  * Params
    * **bankIndex**
    * **pedalboardIndex**
* ```/bank/(?P<bankIndex>[0-9]+)/pedalboard/(?P<pedalboardIndex>[0-9]+)/effect/(?P<effectIndex>[0-9]+)```
  * **GET** a effect
  * **DELETE** for remove a effect
  * Params
    * **bankIndex**
    * **pedalboardIndex**
    * **effectIndex**

### Param

* ```/bank```
  * **POST** a new bank.
  * Returns the bank index
* ```/bank/(?P<bankIndex>[0-9]+)/pedalboard/(?P<pedalboardIndex>[0-9]+)/effect/(?P<effectIndex>[0-9]+)/param/(?P<paramIndex>[0-9]+)```
  * **GET** a parameter value
  * **PUT** for update a parameter value
  * Params
    * **bankIndex**
    * **pedalboardIndex**
    * **effectIndex**
    * **paramIndex**

### Current

* ```/current```
  * **GET** the current _bank index_ and the current _pedalboard index_
* ```/current/data```
  * **GET** the current _bank data_ and the current _pedalboard index_
* ```/current/bank/(?P<bankIndex>[0-9]+)/pedalboard/(?P<pedalboardIndex>[0-9]+)```
  * **PUT** the current _bankIndex_ and the current _pedalboardIndex_
* ```/current/effect/(?P<effect>[0-9]+)```
  * **PUT** for toggle effect status (active for bypassed or bypassed for active) of the current pedalboard

### Connections

* ```/bank/(?P<bank_index>[0-9]+)/pedalboard/(?P<pedalboard_index>[0-9]+)/connect```
  * **PUT** a new connection for the specified pedalboard
    * Data - JSON connection information
* ```/current/data```
  * **POST** for disconnect the specified_pedalboard
    * Data - JSON connection information

### WebSocket

View ```websocker/UpdatesObserverSocket``` for details

## Applications

This code disposes the Application features in a WebService. These projects uses it for control.

* [Apk](https://github.com/PedalPi/Apk): App controller for smart devices and navigators.

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
