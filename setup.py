from setuptools import setup

setup(
    name="clav",
    version="1.0",
    py_modules=["main", "lexer", "parser", "interpreter", "nodes", "tokens", "keywords"],
    entry_points={
        "console_scripts": [
            "clav=main:main",
        ],
    },
)