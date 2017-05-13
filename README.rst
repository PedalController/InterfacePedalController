Pedal Pi - WebService
=====================

.. image:: https://travis-ci.org/PedalPi/WebService.svg?branch=master
    :target: https://travis-ci.org/PedalPi/WebService
    :alt: Build Status

.. image:: https://codecov.io/gh/PedalPi/WebService/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/PedalPi/WebService
    :alt: Code coverage

.. image:: https://landscape.io/github/PedalPi/WebService/master/landscape.svg?style=flat
    :target: https://landscape.io/github/PedalPi/WebService/master
    :alt: Code Health

**Pedal Pi - WebService** is a Pedal Pi component that offers a
Pedal Pi management over REST + WebSocket

**Documentation:**
   http://pedalpi.github.io/WebService/

**Code:**
   https://github.com/PedalPi/WebService

**Python Package Index:**
   https://pypi.org/project/PedalPi-WebService

**License:**
   `Apache License 2.0`_

.. _Apache License 2.0: https://github.com/PedalPi/Application/blob/master/LICENSE


Use
---

Dependencies
************

This project requires [PedalPi/Application](http://github.com/PedalPi/Application) project. See the [Application documentation](http://pedalpi-application.readthedocs.io/en/latest/#extending) for mode details.

This project requires dependencies too, like `Tornado` and `Requests` (for tests).
For the full list, see [`requirements.txt`](https://github.com/PedalPi/WebService/blob/master/requirements.txt)

For a `config.py` example, see [`test/config.py`](https://github.com/PedalPi/WebService/blob/master/test/config.py)

For the bonjour support for auto discover this web-service, it's necessary install [pybonjour-python3](https://github.com/depl0y/pybonjour-python3) and your system lib dependencies.

.. code-block:: bash

    sudo apt-get install libavahi-compat-libdnssd1
    pip3 install git+https://github.com/depl0y/pybonjour-python3


API
---

Rest
****

`Access the documentation`_ for API details.

.. _Access the documentation:http://pedalpi.github.io/WebService/

WebSocket
*********

View ```websocker/UpdatesObserverSocket``` for the details

Using in your client
--------------------

This code disposes the Application features in a WebService. These projects uses it for control.

* [Apk](https://github.com/PedalPi/Apk): App controller for smart devices and navigators.

If you are using too, please, send a pull request for this project.

## Project configuration

Maintenance
-----------

Documentation
*************

.. code-block:: bash

    # Installing dependencies
    npm install -g aglio

    # Generate doc
    cd docs/
    aglio -i documentation.apib --theme-variables streak --theme-template triple -o index.html

    # View documentation
    firefox index.html

Test
****

After started the a `Application` with `WebService` component, excute:

.. code-block:: bash

    # Test by documentation
    npm install -g dredd
    dredd

.. code-block:: bash

    # Test by code implemented
    # (it necessary start a WebService server before)
    coverage3 run --source=webservice setup.py test
    coverage3 report
    coverage3 html
    firefox htmlcov/index.html
