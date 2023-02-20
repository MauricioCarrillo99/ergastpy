from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='erpy2set',
    url='https://github.com/maxelOA/py_erpy2set',
    author='Mauricio Carrillo',
    author_email='mury_cpineda@hotmail.com',
    packages=['erpy2set'],
    install_requires=['numpy','pandas','requests','json'],
    version='1.0',
    license='MIT',
    description='A extension of ergast developer API',
    long_description=open('README.txt').read(),
)
