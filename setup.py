python setup.py sdist bdist_wheel
python3 setup.py sdist


pip install wheel setuptools pip --upgrade
pip3 install wheel setuptools pip --upgrade

from setuptools import setup

setuptools.setup(
	name='py_erpy2set_tst',
	version='1.0',
	description='ergast-python-2-set',
	author='Mauricio Carrillo',
	author_email='mury_cpineda@hotmail.com',
	packages=['py_erpy2set_tst'],
	scripts=['bin/erpy2set_tst']
	zip_safe=False,
	install_requires=['numpy',
                        'pandas',
                        'requests',
                        'json',
                        'pdp'
	],
)
