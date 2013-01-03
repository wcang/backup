#!/usr/bin/python

import sys
import os
import stat
import glob

if len(sys.argv) != 3:
    print "Usage %s configuration destination" % sys.argv[0]
    sys.exit(1)

dest = sys.argv[2]
file_list = []
conf_file =  open(sys.argv[1], 'r')

for line in conf_file.readlines():
    if not line.startswith('#'):
        temp = line.split(',')

        if len(temp) == 3:
            file_list.append({'user': temp[0].strip(), 'group': temp[1].strip(), 
                'list': temp[2].strip()})
        else:
            print "Invalid configuration %s" % line

conf_file.close()

for temp in file_list:
    temp_file = open(temp['list'], 'r')

    for src in [ line.strip() for line in temp_file.readlines() if not line.startswith('#') ]:
        expanded_src = glob.glob(src)

        for individual_src in expanded_src:
            mode = os.stat(individual_src).st_mode
            final_dest = dest + os.path.dirname(individual_src)

            try:
                os.stat(final_dest) #check whether the final destination exists
            except Exception:
                os.makedirs(final_dest) #create one
            finally:
                os.system("rsync -azvv --delete \"%s\" \"%s\"" % 
                        (individual_src, final_dest))

    temp_file.close()
