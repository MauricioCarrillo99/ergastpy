python setup.py sdist bdist_wheel
python3 setup.py sdist


pip install wheel setuptools pip --upgrade
pip3 install wheel setuptools pip --upgrade

from setuptools import setup

setuptools.setup(
	name='erpy2set',
	version='1.0',
	description='ergast-python-2-set',
	author='Mauricio Carrillo',
	author_email='jdoe@example.com',
	packages=['erpy2set'],
	install_requires=['numpy',
                        'pandas',
                        'requests',
                        'json',
                        'pdp'
	],
)
