from setuptools import setup, find_packages
 
setup(
    name='csvexporter',
    version=__import__('csvexporter').__version__,
    description='filter and export data from django admin',
    author='Klemens Mantzos',
    author_email='klemens@fetzig.at',
    url='http://github.com/fetzig/django-csv-exporter',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
)