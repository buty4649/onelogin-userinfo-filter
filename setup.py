from setuptools import setup, find_packages

setup(
    name='onelogin_userinfo_filter',
    version='0.1',
    packages=find_packages(),
    entry_points={
      'paste.filter_factory': [
         'userinfo=onelogin_userinfo_filter:OneloginUserinfo.factory'
      ]
    }
)
