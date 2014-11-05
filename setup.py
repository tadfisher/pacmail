#!/usr/bin/env python

from distutils.core import setup

dfiles = ['LICENSE', 'README', 'ChangeLog', 'AUTHORS']

setup(name='PacMail',
      version='0.1.5',
      license='GPL2',
      description='Daemon that emails users about updates for Arch Linux systems',
      author=['Tad Fisher'],
      author_email=['tadfisher@gmail.com'],
      url='http://code.google.com/p/pacmail/',
      package_dir={'pacmail':'src'},
      packages=['pacmail'],
      scripts=['bin/pacmail'],
      data_files=[('share/pacmail/', dfiles),
	          ('/etc/', ['pacmail.conf'])]
)
