from setuptools import setup


setup(
    name = "tensormoments",
    version = "0.0.1",
    author = "Florian Thoele",
    author_email = "florian.thoele@gmail.com",
    description = ("Helper functions to deal with output files containing tensor moments"),
    license = "MIT",
    keywords = "",
    url = "",
    packages=['tensormoments'],
    long_description="",
    install_requires=[
        "numpy",
        "pandas",
        "six"
    ],
    )
