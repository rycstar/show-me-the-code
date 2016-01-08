#!/usr/bin/python
import random
import string
#invite code is the group of letters and digit,so we defined a letter list.
lettergroup = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

#this function is to get random char according to the bit-true of the input num
#if bit-true, we will random get 2 char from 'A-R', else we get char from 'S-9'
def getRandomChar(num,offset):
    if offset >= 0 and offset < 8 :
        random.seed()
        splitlen = len(lettergroup) >> 1
        if num & (0x01 << offset):
            return random.sample(lettergroup[0:splitlen],2)
        else:
            return random.sample(lettergroup[splitlen:],2)
    return ''
#add file IO to record the inviteCodes.
f = file('./invite_code.txt','w')
for i in range(1,201):
    inviteCode = ''
    for j in range(0,8):
        inviteCode += ''.join(getRandomChar(i,j))
#    print 'inviteCode[%d]:%s' %(i,inviteCode)    
    f.write(inviteCode+'\n');
f.close()
