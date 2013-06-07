from distutils.core import setup

setup(
    name = "nontemplate",
    version = "0.12",
    author = "Nick Moore",
    author_email = "nick@zoic.org",
    url = "http://code.zoic.org/nontemplate/",
    description = "Nontemplate is not a Templating Language",
    download_url = "http://code.zoic.org/nontemplate/dist/nontemplate-0.12.tar.gz",
    keywords = ["xml", "html", "template"],
    license = "MIT",
    classifiers=[
      'Programming Language :: Python :: 2.6',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Development Status :: 2 - Pre-Alpha',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
    ],
    py_modules = ['nontemplate'],
    long_description = open('README.txt').read(),
)
