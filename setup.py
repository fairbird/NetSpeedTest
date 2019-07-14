from distutils.core import setup

pkg = 'SystemPlugins.NetSpeedTest'
setup (name = 'enigma2-plugin-systemplugins-netspeedtest',
       version = '1.0',
       description = 'Plugin For Test Internet Speed.',
       packages = [pkg],
       package_dir = {pkg: 'plugin'},
       package_data = {pkg: ['plugin.png', '*/*.png', 'locale/*/LC_MESSAGES/*.mo']},
      )
