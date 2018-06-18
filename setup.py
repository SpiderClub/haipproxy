from os import path as os_path
from setuptools import setup

import haipproxy


this_directory = os_path.abspath(os_path.dirname(__file__))


def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name='haipproxy',
    python_requires='>=3.4.0',
    version=haipproxy.__version__,
    description="High aviariable proxy pool client for crawlers.",
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    author="Resolvewang",
    author_email='resolvewang@foxmail.com',
    url='https://github.com/SpiderClub/haipproxy',
    packages=[
        'haipproxy',
        'haipproxy.client',
        'haipproxy.config',
        'haipproxy.utils'
    ],
    install_requires=read_requirements('requirements-cli.txt'),
    include_package_data=True,
    license="MIT",
    keywords=['proxy', 'client', 'haipproxy'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)