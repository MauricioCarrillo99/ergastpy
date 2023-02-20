from setuptools import setup

setup(
    name="erpy2set",
    url="https://github.com/maxelOA/erpy2set.git",
    author="Mauricio Carrillo",
    author_email="mury_cpineda@hotmail.com",
    packages=['erpy2set'],
    package_dir={"erpy2set":"erpy2set"},
    install_requires=["numpy >=1.21.6","pandas >= 1.3.5","requests >=2.25.1","json >= 2.0.9"],
    version="1.0",
    license="unlicense",
    description="A extension of ergast developer API",
    long_description=open('README.txt').read()
)
