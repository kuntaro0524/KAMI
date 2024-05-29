from setuptools import setup, find_packages

setup(
    name='kami',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-cors'
    ],
    entry_points={
        'console_scripts': [
            'kami=kami:app.run'
        ]
    },
)

