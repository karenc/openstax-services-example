from setuptools import setup

setup(
        name='openstax-services-example',
        version='0.1',
        description='An example app that connects to openstax/services',
        long_description=open('README.rst').read(),
        author='Karen Chan',
        author_email='karen@karen-chan.com',
        url='http://github.com/karenc/openstax-services-example',
        py_modules=['openstax_services_example'],
        install_requires=['sanction'],
        )
