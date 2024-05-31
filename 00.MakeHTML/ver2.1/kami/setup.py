from setuptools import setup, find_packages

setup(
    name='KAMI',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['templates/*.html', 'static/*']
    },
    install_requires=[
        'flask',
        'flask-cors'
    ],
    entry_points={
        'console_scripts': [
            'kami=kami.__main__:main'
        ]
    },
)
