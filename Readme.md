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

### Patch

* ```/bank/(?P<bankIndex>[0-9]+)/patch```
  * **POST** a new patch.
  * Returns the patch index
  * Params
    * **bankIndex**
* ```/bank/(?P<bankIndex>[0-9]+)/patch/(?P<patchIndex>[0-9]+)```
  * **GET** a patch
  * **PUT** for update a patch
  * **DELETE** a patch
  * Params
    * **bankIndex**
    * **patchIndex**

### Effect

* ```/bank/(?P<bankIndex>[0-9]+)/patch/(?P<patchIndex>[0-9]+)/effect```
  * **POST** a new effect.
  * Returns the effect index
  * Params
    * **bankIndex**
    * **patchIndex**
* ```/bank/(?P<bankIndex>[0-9]+)/patch/(?P<patchIndex>[0-9]+)/effect/(?P<effectIndex>[0-9]+)```
  * **GET** a effect
  * **DELETE** for remove a effect
  * Params
    * **bankIndex**
    * **patchIndex**
    * **effectIndex**

### Param

* ```/bank```
  * **POST** a new bank.
  * Returns the bank index
* ```/bank/(?P<bankIndex>[0-9]+)/patch/(?P<patchIndex>[0-9]+)/effect/(?P<effectIndex>[0-9]+)/param/(?P<paramIndex>[0-9]+)```
  * **GET** a parameter value
  * **PUT** for update a parameter value
  * Params
    * **bankIndex**
    * **patchIndex**
    * **effectIndex**
    * **paramIndex**

### Current

* ```/current```
  * **GET** the current _bank index_ and the current _patch index_
* ```/current/data```
  * **GET** the current _bank data_ and the current _patch index_
* ```/current/bank/(?P<bankIndex>[0-9]+)/patch/(?P<patchIndex>[0-9]+)```
  * **PUT** the current _bankIndex_ and the current _patchIndex_
* ```/current/effect/(?P<effect>[0-9]+)```
  * **PUT** for toggle effect status (active for bypassed or bypassed for active) of the current patch
* ```/current/effect/(?P<effect>[0-9]+)/param/(?P<param>[0-9]+)```
  * **PUT** for set a parameter value for a effect of the current patch

### Connections

Not implemented

### Peripheral

Not implemented

### WebSocket

View ```websocker/UpdatesObserverSocket``` for details

## Applications 

This code disposes the Application features in a WebService. These projects uses it for control.

* [Apk](https://github.com/Apk): App controller for smart devices and navigators.

## Project configuration

### Others

```bash
npm install -g api-designer
api-designer
```

## To test Rest

After started the a `Application` with `WebService` component, excute: 

```bash
# Run server
coverage3 run --source=handler setup.py test
coverage3 report
coverage3 html
firefox htmlcov/index.html
```
