from setuptools import setup, find_packages
from multiuac import VERSION

setup(
    name="multiuac",
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        "PyYAML",
        "arrow",
        "attrs",
        "py3-bencode",
        "redis",
        "sippy-tbs>=2022.7.0",
        "anyio",
        "asyncwebsockets>=0.8.2",
        "hypercorn==0.13.2",
        "quart"
    ],
    entry_points={
        "console_scripts": [
            "multiuac_cli = multiuac.multiuac:main_func"
        ]
    }
)
