from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    readme = f.read()

requirements = ['nukeuuid', 'deepdiff']
test_requirements = ['pytest', 'pytest-cov',
                     'sphinx', 'sphinx_rtd_theme']

setup(
    name = 'nukedatastore',
    version = '0.1.2',
    description='A library for basic data persistence in Nuke',
    long_description=readme,
    url='https://github.com/florianeinfalt/nukedatastore',
    author='Florian Einfalt',
    author_email='info@florianeinfalt.de',
    license='Apache 2.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    install_requires=requirements,
    tests_require=test_requirements
)
