#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
#Filename:gitlab.py

import codecs
import requests  
from bs4 import BeautifulSoup

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}
github_login_url = 'https://github.com/login'
github_login_post_url = 'https://github.com/session'

login_data = {
    'commit':'Sign in',
    'login':'rycstar',
    'password':'********',
}



#with requests.session() as res:
#    log_soup = BeautifulSoup(res.get(github_login_url).text,'html.parser')
#    login_data['utf8'] = log_soup.findAll('input',attrs={'name':'utf8'})[0].get('value')
#    login_data['authenticity_token'] = log_soup.findAll('input',attrs={'name':'authenticity_token'})[0].get('value')
#    response = res.post(github_login_post_url,data=login_data,headers=header)
#    print response

    #r = BeautifulSoup(res.get(gitlab_new_issue_url).text,'html.parser')
#    print r
    #new_issue_data['utf8'] = r.findAll('input',attrs={'name':'utf8'})[0].get('value')
    #new_issue_data['authenticity_token'] = r.findAll('meta',attrs={'name':'csrf-token'})[0].get('content')
    #print new_issue_data
    #response = res.post('http://172.16.1.8/fanvil_x6/test_prj/issues',data=new_issue_data,headers=header)
    #res_issue = BeautifulSoup(response.text,'html.parser')

#   print response
#with codecs.open('./new_issue_id.txt','wb','utf-8') as f:
#    f.write(requests.get(github_login_url).text)
#    f.close()

soup = BeautifulSoup(open('new_issue_id.txt'),'lxml')
#print soup.prettify()
#print soup.title
#print soup.head
#print soup.input.name
#print soup.input.attrs
#print len(soup.find_all('input',attrs={'type':'hidden','name':'authenticity_token'}))
#for child in soup.body.children:
#    print child
print soup.body.find_all('div',attrs={'class':'auth-form-body'})[0].find_all('label')