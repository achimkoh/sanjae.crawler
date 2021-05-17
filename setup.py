from setuptools import setup

setup(
    name='opendata_sanjae',
    version='0.0.1',
    description='근로복지공단_산재보험 판례 판결문 조회 서비스 API의 python wrapper',
    author='red112',
    # author_email='',
    # license='',
    packages=['opendata_sanjae'],
    zip_safe=False,
    install_requires=[
        'beautifulsoup4',
        'lxml',
        'requests',
        'pandas'
    ]
)
