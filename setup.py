from setuptools import setup
from setuptools import find_packages


install_requires = [
    'setuptools',
    'Flask',
    'SQLAlchemy',
    'flask-sqlalchemy',
    'openpyxl',
]

packages = [
    'app'
]
console_scripts = [
    'myapp=run:main',
]

setup(
    name='myapp',
    version='0.1',
    packages=find_packages(exclude=packages),
    install_requires=install_requires,
    entry_points={'console_scripts': console_scripts},
)
