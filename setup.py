import setuptools

try:
    import pypandoc
    LONG_DESC = pypandoc.convert("README.md", "rst")
except(IOError, ImportError, RuntimeError):
    LONG_DESC = open('README.md').read()

setuptools.setup(
    name="tvtid",
    version="0.2.0",
    author="Christian Kirkegaard",
    author_email="christian@lowpoly.dk",
    description="Library and cli tool for querying tvtid.dk",
    long_description=LONG_DESC,
    license="MIT",
    url="https://github.com/kirkegaard/tvtid.py",
    download_url="https://github.com/kirkegaard/tvtid.py",
    install_requires=[
        'python-dateutil',
        'fuzzywuzzy[speedup]',
        'requests',
        'requests_cache'
    ],
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    py_modules=["tvtid"],
    entry_points={
        "console_scripts": [
            "tvtid=tvtid:main"
        ]
    },
    python_requires=">=3.5",
    include_package_data=True
)
