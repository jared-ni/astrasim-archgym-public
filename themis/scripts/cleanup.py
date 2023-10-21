import os

results_dir = '../results'

if __name__ == '__main__':
    os.system("rm -rf %s/*" % (results_dir,))
    