#!/usr/bin/python
#filename:q0002.py

import MySQLdb

conn = MySQLdb.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        passwd = '1234',
        db = 'inviteCodeRepo',
    )

cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS inviteCode(id INT PRIMARY KEY AUTO_INCREMENT,code VARCHAR(32))")

f = file('./invite_code.txt','r')
line = f.readline()
while len(line) > 0:
    cmd = ['INSERT INTO inviteCode(code) values("',line,'");']
    cur.execute(''.join(cmd))
#    print ''.join(cmd)
    line = f.readline()
else:
    print "File read end. close it!"
    f.close()

cur.close()

conn.commit()

conn.close()
