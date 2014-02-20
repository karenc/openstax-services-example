openstax-services-example
=========================

This is an example python wsgiref app that connects to openstax/services.

INSTALL
-------

0. Install ``virtualenv``

1. ``virtualenv .``

2. ``./bin/python setup.py install``

3. Set up openstax/services (See karenc/openstax-setup)

4. Register this app with openstax/services

5. Copy development.ini.example to development.ini and change the values

6. Start the app by ``./bin/python openstax_services_example.py development.ini``
