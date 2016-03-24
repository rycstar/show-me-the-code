#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
#Filename:github_transfer.py
import sys
import time
import codecs
import requests
from bs4 import BeautifulSoup
import argparse

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}
github_login_url = 'https://github.com/login'
github_login_post_url = 'https://github.com/session'
#github_issue_list_url = 'https://github.com/noboundary/xGui/issues'
github_domain = 'https://github.com'

#github data
github_login_data = {
    'commit':'Sign in',
    'login':'********',
    'password':'********',
}

github_issue_query_data = {
    'q':'is:issue is:closed',
    'page':1
}

def args_handler(argv):
    p = argparse.ArgumentParser(description='download from github.com')
    p.add_argument('-u','--user',action='store',default=None,type = str,help = 'Input user name')
    p.add_argument('-p','--password',action='store',default=None,type = str,help = 'Input password')
    p.add_argument('-l','--url',action='store',default='https://github.com/noboundary/xGui/issues',type = str,help = 'Input src issue url')
    args = p.parse_args(argv[1:])
    return args

def github_issue_save(href_val,session):
    issue_url = github_domain + href_val
    issues_values_soup = BeautifulSoup(session.get(issue_url).text,'html.parser')
    file_name = href_val.split('/')[-1]
    print file_name
    with codecs.open(file_name,'wb','utf-8') as f:
        f.write(issues_values_soup.prettify())
        f.close() 

def github_login(session,user,password):
    log_soup = BeautifulSoup(session.get(github_login_url).text,'html.parser')
    github_login_data['utf8'] = log_soup.findAll('input',attrs={'name':'utf8'})[0].get('value')
    github_login_data['authenticity_token'] = log_soup.findAll('input',attrs={'name':'authenticity_token'})[0].get('value')
    github_login_data['login'] = user
    github_login_data['password'] = password
    response = session.post(github_login_post_url,data=github_login_data,headers=header)
    print response

def github_issue_read(session,url,close_state):
    if (close_state == False):
        github_issue_query_data['q'] = 'is:open is:issue'
    else:
        github_issue_query_data['q'] = 'is:issue is:closed'

    length = 1
    i = 1
    while (length > 0):
        github_issue_query_data['page'] = i
        issue_list_soup = BeautifulSoup(session.get(url,data = github_issue_query_data).text,'html.parser')
        issue_list = issue_list_soup.body.find_all('a',attrs={'class':'issue-title-link js-navigation-open'})
        print 'close state : {0} issue num:{1},next_page{2}'.format(close_state,len(issue_list),len(issue_list_soup.body.find_all(attrs={'class':'next_page'})))
        for x in xrange(len(issue_list)):
            time.sleep(4)
            github_issue_save(issue_list[x].get('href'),session)
        next_page = issue_list_soup.body.find_all('a',attrs={'class':'next_page'})
        length = len(next_page)
        i = i + 1
        time.sleep(5)

def main(argv):
    args = args_handler(argv)
    print args
    github_session = requests.session()
    github_login(github_session,args.user,args.password)
    time.sleep(2)
    github_issue_read(github_session,args.url,True)
    github_issue_read(github_session,args.url,False)

if __name__ == '__main__':
    argv = sys.argv
    main(argv)

