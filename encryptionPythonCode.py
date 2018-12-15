#-*-coding:utf-8-*-

"""
first step, read the current structure of the source code
second step, generate "setup.py"
third step, call "python setup.py build_ext --inplace"
fourth step, rename the generated .so file to .py file
"""

import os
import logging
import argparse

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.DEBUG)


parser = argparse.ArgumentParser("")
parser.add_argument("--entry")
args = parser.parse_args()
entryFileName = args.entry

rootPath = os.getcwd()

setupHeadString = '''from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize('''
setupTailString = '''))\n'''

setupFileName = 'mysetup.py'

allFiles = []

def mymkdir(path):
    if os.path.exists(path) is False:
        os.mkdir(path)


def readFileStructure(rootPath):
    currentLevelAllFiles = os.listdir(rootPath)
    print "currentLevelAllFiles : ",currentLevelAllFiles
    for aFile in currentLevelAllFiles:
        if aFile.endswith(".py"):
            if aFile == setupFileName or aFile == __file__:
                continue
            allFiles.append(rootPath + os.sep + aFile)
        elif os.path.isdir(rootPath + os.sep + aFile):
            readFileStructure(rootPath + os.sep + aFile)



def generateSetupFile():
    setupFile = open(setupFileName,'w')
    setupFile.write(setupHeadString)
    setupFile.write(str(allFiles))
    setupFile.write(setupTailString)



def generateSoFiles():
    cmd = 'python ' + setupFileName + " build_ext --inplace"
    os.system(cmd)


def releaseAndCleanupFiles(srcRootPath,desRootPath):
    logging.debug(os.listdir(srcRootPath))
    for fi in os.listdir(srcRootPath):
        if fi == 'release':
            continue
        if fi.endswith(".so"):
            if fi == '__init__.so':
                cmd = 'cp ' + srcRootPath + os.sep + '__init__.py' + ' ' + desRootPath + os.sep
                os.system(cmd)
                continue

            cmd = 'mv ' + srcRootPath + os.sep + fi + ' ' + desRootPath + os.sep + fi
            os.system(cmd)

        elif fi.endswith(".c"):
            os.remove(srcRootPath + os.sep + fi)
        elif os.path.isdir(srcRootPath + os.sep + fi):
            mymkdir(desRootPath + os.sep + fi)
            releaseAndCleanupFiles(srcRootPath + os.sep + fi,desRootPath + os.sep + fi)


    if entryFileName is not None:
        os.system('cp ' + entryFileName + ' ' + 'release/')
    else:
        logging.warning("use python encryptionPythonCode.py --entry filename")
    if os.path.exists(setupFileName) is True:
        logging.debug('setupfilename exist')
        os.remove(setupFileName)





if __name__ == '__main__':
    readFileStructure(rootPath)
    logging.debug(allFiles)
    generateSetupFile()
    generateSoFiles()
    mymkdir('release')
    if os.path.exists('build') is True:
        os.system('rm -rf build')
    releaseAndCleanupFiles(rootPath,'release')