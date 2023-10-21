import os
import numpy as np

template = "MICRO \n\
1 \n\
conv1 -1 5 NONE 0 5 NONE 0 5 ALLREDUCE %d 5"

filename_template = "allreduce_%.2f.txt"

giga = 1024*1024*1024

collective_sizes = np.arange(0.1, 1, 0.05)
for size in collective_sizes:
    f = open(filename_template%(size,), 'w')
    print(template % (int(giga*size),), file=f)
    f.close()


