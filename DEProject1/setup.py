from setuptools import setup, find_packages

setup(
    name='redactor',
    version='1.0.0',
    author='Rushit Varma Gadiraju',
    author_email='vgadiraju@ufl.edu',
    description='A text redaction tool for sensitive information',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/cis6930fa24-project1',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'spacy>=3.0.0,<4.0.0',
        'argparse',
    ],
    extras_require={
        'dev': ['pytest', 'pytest-runner']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'redactor=redactor.redactor:main',
        ],
    },
)