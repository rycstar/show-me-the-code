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
        if num & (0x01 << offset):
#            print lettergroup[0:18]
            return random.sample(lettergroup[0:18],2)
        else:
#            print lettergroup[18:]
            return random.sample(lettergroup[18:],2)
    return ''

for i in range(1,201):
    inviteCode = ''
    for j in range(0,8):
        rstr = ''.join(getRandomChar(i,j))
        inviteCode += rstr
    print 'inviteCode[%d]:%s' %(i,inviteCode)    
