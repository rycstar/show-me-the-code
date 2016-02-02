#!/usr/bin/python
#filename:q_alloc_chk.py
import sets

alloc_str = 'alloc addr:'
free_str = 'free addr:'
res = set()

def set_alloc_type(src_str):
    if src_str.find(alloc_str) > 0 :
        res.add(src_str[src_str.find(alloc_str)+len(alloc_str):])
        return 1
    elif src_str.find(free_str) > 0 :
#        res.add(src_str[src_str.find(free_str)+len(free_str):])
#        res.remove(src_str[src_str.find(free_str)+len(free_str):])
        res.discard(src_str[src_str.find(free_str)+len(free_str):])
        return 2
    else:
        return 0

f = file('./alloc_chk.txt','r')
line = f.readline()
while len(line) > 0:
    set_alloc_type(line)
    line = f.readline()
else:
    print "File read end. close it!"
    f.close()
print "The unfreed addr num:(%d)" %len(res)
print res 
