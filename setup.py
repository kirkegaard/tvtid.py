import setuptools


setuptools.setup(
    name="tvtid",
    version="0.1.0",
    author="Christian Kirkegaard",
    author_email="christian@lowpoly.dk",
    description="Shows you the TV Program",
    license="MIT",
    url="https://github.com/kirkegaard/tvtid.py",
    download_url="https://github.com/kirkegaard/tvtid.py",
    install_requires=[
        'requests',
        'requests_cache'
    ],
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux :: macos",
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
