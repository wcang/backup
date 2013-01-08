#!/usr/bin/python

import sys
import os
import stat
import glob

if len(sys.argv) != 3:
    print "Usage %s configuration source_prefix" % sys.argv[0]
    sys.exit(1)

src_prefix = sys.argv[2]
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
        expanded_src = glob.glob(src_prefix + src)

        for final_src in expanded_src:
            mode = os.stat(final_src).st_mode
            final_dest = '/' +  final_src[len(src_prefix):]
            final_dir = final_dest

            if not stat.S_ISDIR(mode):
                final_dir = os.path.dirname(final_dest)
            
            try:
                os.stat(final_dir) #check whether the final destination exists
            except Exception:
	        os.makedirs(final_dir) #create one
            finally:
                print "rsync -azvv \"%s\" \"%s\"" % (final_src, os.path.dirname(final_dest))
		os.system("rsync -azvv \"%s\" \"%s\"" % 
                        (final_src, os.path.dirname(final_dest)))
		os.system("chown -R %s:%s \"%s\"" % (temp['user'], temp['group'],
                        final_dest))

    temp_file.close()
