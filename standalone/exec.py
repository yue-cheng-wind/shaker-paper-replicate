from sys import argv
import random
import subprocess
from glob import glob
import os
import re
import copy
import time

REAL_DIR = glob(os.getcwd())[0]
OUT_DIR = REAL_DIR + '/outputs/'
shouldprint = False
showln = False
testsFound = {}


def save_fail_tests(dictFail):
    os.chdir(REAL_DIR)

    with open(f'{NAME_APP}_shaker.csv', 'w') as f:
        f.write('name, count\n')
        for test in dictFail:
            f.write('%s, %d\n' % (test, dictFail[test]))


def parserTests(path):
    testsFails = {}
    allTests = {}
    # change to dir
    files = glob(path + f'/out.*.txt')  # all log files
    for file in files:
        with open(file, "r") as reader:
            ln = 0
            for line in reader:
                lastName = ''
                ln = ln + 1
                stripped_line = line.strip()
                if stripped_line == 'INSTRUMENTATION_RESULT: stream=':  # if is log for tests fails
                    count = 1
                    for line in reader:
                        ln = ln + 1
                        stripped_line = line.strip()
                        if stripped_line.startswith('INS'):
                            break  # leaves the inner loop
                        failLine = f'{count}) '
                        if stripped_line.startswith(failLine):
                            count += 1
                            if showln:
                                print('line %d -> fail: %s' %
                                      (ln, stripped_line))
                            test = line[3:]  # retire the '1) '
                            test = test.strip()  # for cases '10) '
                            position = test.index('(')
                            # remove the package for test name
                            test = test[:position]
                            if shouldprint:
                                print(f'new tst: {test}. line: {ln}')
                            try:
                                testsFails[test] += 1
                            except KeyError as _:
                                testsFails[test] = 1

                # if is the name of test
                if stripped_line.startswith('INSTRUMENTATION_STATUS: test='):
                    name = stripped_line[29:]  # get only name
                    if name is not lastName:  # for some logs followed in the same test name
                        lastName = name
                        allTests[name] = 1

    return allTests, testsFails  # now, de allTests is de passTests


# cont is the name of outuput file-> out.{count}.txt
def parserData(output, path):
    global testsFound
    path = OUT_DIR + path + '/' + f'{output}'
    os.chdir(path)
    if shouldprint:
        print(path)

    dictPass, dictFail = parserTests(path)

    for test in dictFail.keys():
        try:
            testsFound[test] += dictFail[test]
        except KeyError as _:
            testsFound[test] = dictFail[test]

    for t in testsFound:
        print('%s - %d' % (t, testsFound[t]))
    print('\n')

    save_fail_tests(testsFound)


def runTests(config, cont):
    os.chdir(REAL_DIR)
    test = f'./exec.sh {config[0]} {config[1]} {config[2]} {config[3]} {config[4]} {config[5]} {cont} {NAME_APP} {PID}'

    print("runing %s" % test)
    process = subprocess.Popen(test, stdout=subprocess.PIPE, shell=True)
    stdout = process.communicate()[0].decode("utf-8")
    if shouldprint:
        print(stdout)


def main():  # MHS
    for i in range(NUMBER_RANGE):
        print('-------------> MHS in loop %s <-------------------' % (i+1))
        configs = [[i, 2, 2, 1, 21, 2], [i, 1, 58, 1, 33, 2],
                   [i, 1, 61, 1, 73, 4], [i, 1, 34, 1, 37, 1]]
        cont = 0  # out.{cont}.txt
        for config in configs:
            cont += 1
            runTests(config, cont)
        parserData(i, NAME_APP)


if __name__ == "__main__":
    if len(argv) == 4:
        NUMBER_RANGE = int(argv[1])
        NAME_APP = argv[2]
        PID = int(argv[3])
        print('**Running SHAKER**\nnumber of repetitions is %d\nname app is %s\nPID emulator is %d' %
              (NUMBER_RANGE, NAME_APP, PID))
        main()
    else:
        print("Error: please read the README.md")
        exit(1)
