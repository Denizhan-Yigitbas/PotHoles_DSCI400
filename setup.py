from setuptools import setup

setup(
    name='PotHoles_DSCI400',
    version='1.1',
    packages=['potholes', 'potholes.runtime', 'potholes.runtime.util', 'potholes.runtime.dataloader'],
    package_dir={'potholes': ''},
    url='',
    license='',
    package_data={'potholes': ['data/output/*.csv']},
    author='Denizhan Yigitbas',
    author_email='dy22@rice.edu',
    description='Potholes'
)