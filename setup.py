from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='lsdo_project_template',
    version='0.1.0',
    author='Author name',
    author_email='author@gmail.com',
    license='LGPLv3+',
    keywords='python project template repository package',
    url='http://github.com/LSDOlab/lsdo_project_template',
    download_url='http://pypi.python.org/pypi/lsdo_project_template',
    description='A template repository/package for LSDOlab projects',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.7',
    platforms=['any'],
    install_requires=[
        'numpy',
        'scipy',
        'pytest',
        'myst-nb',
    #     'sphinx_rtd_theme',
    #     'sphinx-copybutton',
    #     'sphinx-autoapi',
    #     'numpydoc',
    #     'gitpython',
    #     # 'sphinxcontrib-collections @ git+https://github.com/anugrahjo/sphinx-collections.git', # 
    #     'sphinx-collections',
    #     'sphinxcontrib-bibtex',
    #     'setuptools',
    #     'wheel',
    #     'twine',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
    ],
    entry_points="""
        [console_scripts]
        lsdo_test=lsdo_test.main:lsdo_test_command
    """,
)
