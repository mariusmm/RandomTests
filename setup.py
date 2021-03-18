from setuptools import setup

setup(
    name='app',
    entry_points={
        'paste.app_factory': [
            'main = app:main'
        ],
    },
)
