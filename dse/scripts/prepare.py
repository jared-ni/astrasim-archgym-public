import os

astrasim_dir = "../../astra-sim"
results_dir = '../results'

if __name__ == '__main__':
    os.system("rm -rf %s" % (os.path.join(astrasim_dir, "build/astra_analytical/build"),))
    os.system("bash %s -c" % (os.path.join(astrasim_dir, "build/astra_analytical/build.sh"),))
    os.system("rm -rf %s/*" % (results_dir,))
    