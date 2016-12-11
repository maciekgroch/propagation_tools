from setuptools import setup


def readme():
    """
    This function just return the content of README.md
    """
    with open('README.md') as f:
        return f.read()


setup(
    name='propagation_tools',
    version='0.01',
    description='Tools to apply light propagation algorithms',
    long_description=readme(),
    classifiers=[
        'Programming Language :: Python :: 3.+',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics'
    ],
    keywords='fourier_optics light_propagation ',
    url='https://github.com/maciekgroch/propagation_tools',
    author='Maciej Grochowicz',
    author_email='maciekgroch@gmail.com',
    license='?',
    packages=['propagation_tools'],
    install_requires=[
        'matplotlib',
        'numpy',
        'pillow',
        'poppy',
        'Sphinx>=1.4',
    ],
    include_package_data=True,
    zip_safe=False
)
