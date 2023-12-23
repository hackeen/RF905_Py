from setuptools import setup, Extension

module1 = Extension('spi', sources=['spi.c'])

setup(
    name='PackageName',
    version='1.0',
    description='This is a demo package',
    ext_modules=[module1],
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/PackageName',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: C',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
