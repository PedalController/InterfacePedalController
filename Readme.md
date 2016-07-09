# WebService - Rest v0.2.0

[![Build Status](https://travis-ci.org/PedalPi/WebService.svg?branch=master)](https://travis-ci.org/PedalPi/WebService) [![Code Health](https://landscape.io/github/PedalPi/WebService/master/landscape.svg?style=flat)](https://landscape.io/github/PedalPi/WebService/master) [![codecov](https://codecov.io/gh/PedalPi/WebService/branch/master/graph/badge.svg)](https://codecov.io/gh/PedalPi/WebService)

## Rest

### Auth

Not implemented

### Plugins

* ```/plugins```: 
  * **GET** all plugins effects instaled
* ```/plugin/(?P<pluginUri>[^/]+)```:
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

* ```/current/bank/(?P<bank>[0-9]+)```
 * **PUT** the current bank
* ```/current/patch/(?P<patch>[0-9]+)```
 * **PUT** the current patch
* ```/current/effect/(?P<effect>[0-9]+)```
 * **PUT** for toggle effect status (actived for bypassed or bypassed for actived) of the current patch
* ```/current/effect/(?P<effect>[0-9]+)/param/(?P<param>[0-9]+)```
 * **PUT** for set a parameter value for a effect of the current patch

### Connections

Not implemented

### Peripheral

Not implemented

### WebSocket

View ```websocker/UpdatesObserverSocket``` for details

## To install

```
sudo pip3 install virtualenv

virtualenv PedalPi-WS
source ./PedalPi-WS/bin/activate

pip3 install -r requirements.txt
```

## To run

```
source ./PedalPi-WS/bin/activate
python3 init.py
``` 

## To test Rest

```
# Run server
coverage3 run --source=handler setup.py test
coverage3 report
coverage3 html
firefox htmlcov/index.html
```
