#!/usr/bin/python
# -*- coding: utf-8 -*-
from distutils.core import setup
import setup_translate

pkg = 'SystemPlugins.NetSpeedTest'
setup(name='enigma2-plugin-systemplugins-netspeedtest',
       version='1.1',
       description='Plugin For Test Internet Speed.',
       packages=[pkg],
       package_dir={pkg: 'plugin'},
       package_data={pkg: ['netspeed.jpg', '*/*.jpg', 'locale/*/LC_MESSAGES/*.mo']},
       cmdclass=setup_translate.cmdclass, # for translation
      )
