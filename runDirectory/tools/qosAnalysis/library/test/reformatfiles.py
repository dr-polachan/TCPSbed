import numpy as np
import re
def reformatfiles(file_send_data,savefile_read_data,tp):
 with open(file_send_data,'rt') as istream:
  file1 = open(savefile_read_data,'w')
  for L in istream.readlines(): 
   tps = re.search('tp:(.*?) .*', L)
   if tps.group(1)==tp:
    tsn = re.search('time_(.*?):.*', L)
    if tsn.group(1)=="received":
     ts = re.search('time_received:(.*?) .*', L)
     file1.write('%s \t' % ts.group(1))
     se = re.search('seq:(.*?) .*', L)
     file1.write('%s \n' % se.group(1))
    else:
     ts = re.search('time_send:(.*?) .*', L)
     file1.write('%s \t' % ts.group(1))
     se = re.search('seq:(.*?) .*', L)
     file1.write('%s \n' % se.group(1))
#reformatfiles("data_send.txt","codck.txt","tp_server_entry")


