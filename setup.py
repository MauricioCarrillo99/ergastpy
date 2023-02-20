from setuptools import setup

setuptools.setup(
	name='py_erpy2set',
	version='1.0',
	url='https://github.com/maxelOA/py_erpy2set.git'
	description='ergast-python-2-set',
	author='Mauricio Carrillo',
	author_email='mury_cpineda@hotmail.com',
	packages=['py_erpy2set'],
	scripts=['bin/erpy2set']
	zip_safe=False,
	install_requires=['numpy',
                        'pandas',
                        'requests',
                        'json',
                        'pdp'
	],
)
