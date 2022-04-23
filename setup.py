from setuptools import setup

'''
setup.py
src/
    mypkg/
        __init__.py
        module.py     
        data/              # 서브 폴더는 추가되지 않음 이건 따로 처리 필요
            tables.dat
            spoons.dat
            forks.dat

setup(...,
      packages=['mypkg'],
      package_dir={'mypkg': 'src/mypkg'}, # 소스의 위치를 나타낸다. __init__.py 를 찾는다. 그외에 같은 경로에 있는 파일들은 같이 포함됨
      package_data={'mypkg': ['data/*.dat']},
      ...
      )

원하는 패키지가 있다면 아래 내용 사용
install_requires=requirements,
'''

requirements=[
'PyYAML>=1.0',
]

setup(
    name='mygithub', # pip install/uninstall 설치 삭제시 사용하는 이름
    version='0.1.0',
    author='j',
    packages=['mypkg'], # import 할때 사용하게되는 이름
    package_dir={'mypkg': 'python/example/_41_github_install_pkg'},
    license='LICENSE.txt',
    description='installing python package ',
    python_requires='>=3.6',
    install_requires=requirements,
)


# for local test 
# python setup.py install

'''
running install
running bdist_egg
running egg_info
creating mygithub.egg-info
writing mygithub.egg-info/PKG-INFO
writing dependency_links to mygithub.egg-info/dependency_links.txt
writing top-level names to mygithub.egg-info/top_level.txt
writing manifest file 'mygithub.egg-info/SOURCES.txt'
reading manifest file 'mygithub.egg-info/SOURCES.txt'
writing manifest file 'mygithub.egg-info/SOURCES.txt'
installing library code to build/bdist.win-amd64/egg
running install_lib
running build_py
creating build
creating build/lib
creating build/lib/mypkg
copying python/example/_41_github_install_pkg/__init__.py -> build/lib/mypkg
creating build/bdist.win-amd64
creating build/bdist.win-amd64/egg
creating build/bdist.win-amd64/egg/mypkg
copying build/lib/mypkg/__init__.py -> build/bdist.win-amd64/egg/mypkg
byte-compiling build/bdist.win-amd64/egg/mypkg/__init__.py to __init__.cpython-38.pyc
creating build/bdist.win-amd64/egg/EGG-INFO
copying mygithub.egg-info/PKG-INFO -> build/bdist.win-amd64/egg/EGG-INFO
copying mygithub.egg-info/SOURCES.txt -> build/bdist.win-amd64/egg/EGG-INFO
copying mygithub.egg-info/dependency_links.txt -> build/bdist.win-amd64/egg/EGG-INFO
copying mygithub.egg-info/top_level.txt -> build/bdist.win-amd64/egg/EGG-INFO
zip_safe flag not set; analyzing archive contents...
creating dist
creating 'dist/mygithub-0.1.0-py3.8.egg' and adding 'build/bdist.win-amd64/egg' to it
removing 'build/bdist.win-amd64/egg' (and everything under it)
Processing mygithub-0.1.0-py3.8.egg
Copying mygithub-0.1.0-py3.8.egg to c:/users/user/appdata/local/programs/python/python38/lib/site-packages
Adding mygithub 0.1.0 to easy-install.pth file

Installed c:/users/user/appdata/local/programs/python/python38/lib/site-packages/mygithub-0.1.0-py3.8.egg
Processing dependencies for mygithub==0.1.0
Finished processing dependencies for mygithub==0.1.0
'''


# installed package
# > pip freeze
'''
...
mygithub==0.1.0
...
'''

# uninstall package
# > pip uninstall mygithub

# github
# pip install git+https://github.com/my_username/my_repo



