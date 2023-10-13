from setuptools import setup, find_packages

setup(
    name='lilo',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'lilo=lilo.lilo:main',
        ],
    },
    package_data={
        'lilo': [
            'schemes/ASFV/ASFV.scheme.bed',
            'schemes/ASFV/ASFV.reference.fasta',
            'schemes/ASFV/ASFV.primers.csv',
            'schemes/SCoV2/SCoV2.scheme.bed',
            'schemes/SCoV2/SCoV2.reference.fasta',
            'schemes/SCoV2/SCoV2.primers.csv',
            'config.file'
        ]
    },
)
