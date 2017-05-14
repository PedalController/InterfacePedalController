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
Pedal Pi management over REST + WebSocket.

WebService also supports auto discover: by publishing to the network using *zeroconf*,
it offers a certain level of location transparency, allowing applications to connect to
the WebService with minimal user effort.

**Documentation:**
   http://pedalpi.github.io/WebService/

**Code:**
   https://github.com/PedalPi/WebService

**Python Package Index:**
   https://pypi.org/project/PedalPi-WebService

**License:**
   `Apache License 2.0`_

.. _Apache License 2.0: https://github.com/PedalPi/WebService/blob/master/LICENSE


Use
---

Installation and dependencies
*****************************

Most dependencies will be installed through `pip`

.. code-block:: bash

    pip install PedalPi-WebService

WebService, for its publication in the network for auto discover, needs the installation
of `pybonjour-python3`_. On debian/ubuntu-based systems, run:

.. code-block:: bash

    sudo apt-get install libavahi-compat-libdnssd1
    pip3 install git+https://github.com/depl0y/pybonjour-python3

.. _pybonjour-python3: https://github.com/depl0y/pybonjour-python3

Configuring the component
*************************

PedalPi components enable the extension of `Pedal Pi - Application`_.
Through them, opening services are offered. A list of components can be found in the `Components repository`_.

To use this component, two steps are required:

.. _Pedal Pi - Application: http://pedalpi-application.readthedocs.io/en/latest/
.. _Components repository: https://github.com/PedalPi/Components#list

1. Registering the webservice in Application
++++++++++++++++++++++++++++++++++++++++++++

The registration must occur before application initialization (``application.start``)

.. code-block:: python

    from application.application import Application
    application = Application(path_data="data/", address='localhost')

    from webservice.webservice import WebService
    application.register(WebService(application, port))

2. Initialization of the web server
+++++++++++++++++++++++++++++++++++

The Application documentation suggests using `signal.pause` so
that the program does not terminate at the end of initialization:
`signal.pause` causes the program to be terminated only when it is
requested (`Ctrl + C`).

When we use PedalPi-WebService, we must replace the use of `signal.pause`
by initializing the web server. This is done using the following
lines of code:

.. code-block:: python

    application.start()

    import tornado
    tornado.ioloop.IOLoop.current().start()

    # Not more necessary
    #from signal import pause
    #pause()

Config file
+++++++++++

The code for starting the Application using the WebService component
look like the following code:

.. code-block:: python

    from application.application import Application
    application = Application(path_data="data/", address='localhost')

    from webservice.webservice import WebService
    application.register(WebService(application, port))

    application.start()

    import tornado
    tornado.ioloop.IOLoop.current().start()

API
---

Rest
****

API documentation can be found at http://pedalpi.github.io/WebService/

WebSocket
*********

Communication via WebService basically consists of receiving updates
about the state of the application. The message types will be
documented in the future and listed at http://pedalpi.github.io/WebService/.

Currently, information about the messages can be found
in the `source code of this project`_.

.. _source code of this project: https://github.com/PedalPi/WebService/tree/master/webservice/websocket/updates_observer_socket.py

Using in your client
--------------------

WebService disposes the Application features in a web service. These projects uses it for control:

 * `Apk`_: App controller for smart devices and navigators.

.. _Apk: https://github.com/PedalPi/Apk

If you are using too, please, send a pull request for this project.


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

.. code-block:: bash

    coverage3 run --source=webservice wstest/config.py test
    coverage3 report
    coverage3 html
    firefox htmlcov/index.html
