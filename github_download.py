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
    p.add_argument('-f','--fullmode',action='store',default=0,type = int,help = '1 == Down the whole issue html, 0 == down the title and comment only')
    p.add_argument('-l','--url',action='store',default='https://github.com/noboundary/xGui/issues',type = str,help = 'Input src issue url')
    args = p.parse_args(argv[1:])
    return args

def github_issue_save(href_val,session,full_mode,close_state):
    issue_url = github_domain + href_val
    issues_values_soup = BeautifulSoup(session.get(issue_url).text,'html.parser')
    file_name = href_val.split('/')[-1]+'_issue.html'
    print 'filename:{0},full_mode:{1}'.format(file_name,full_mode)
    with codecs.open(file_name,'wb','utf-8') as f:
        if not full_mode:
            issue_title = issues_values_soup.find_all('div',attrs={'class':'gh-header-show'})[0]
            issue_state = issues_values_soup.find_all('div',attrs={'class':'flex-table gh-header-meta'})[0]
            f.write(issue_title.prettify())
            f.write(issue_state.prettify())
            issue_comment = issues_values_soup.body.find_all('div',attrs={'class':'edit-comment-hide'})
            issue_timeline = issues_values_soup.body.find_all('div',attrs={'class':'timeline-comment-header-text'})
            issue_assignee = issues_values_soup.body.find_all('div',attrs={'class':'discussion-sidebar-item sidebar-assignee js-discussion-sidebar-item'})
            issue_labels = issues_values_soup.body.find_all('div',attrs={'class':'discussion-sidebar-item sidebar-labels js-discussion-sidebar-item'})
            issue_milestone = issues_values_soup.body.find_all('div',attrs={'class':'discussion-sidebar-item sidebar-milestone js-discussion-sidebar-item'})
            if len(issue_comment) == len(issue_timeline):
                for x in xrange(len(issue_comment)):
                    f.write(issue_comment[x].prettify())
            else:
                print 'timeline number is not same as comment, error! discard {0}'.format(file_name)
            f.write(issue_labels[0].prettify())
            f.write(issue_milestone[0].prettify())
            f.write(issue_assignee[0].prettify())
        else:
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

def github_issue_read(session,url,close_state,full_mode):
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
            github_issue_save(issue_list[x].get('href'),session,full_mode,close_state)
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
    github_issue_read(github_session,args.url,True,args.fullmode)
    github_issue_read(github_session,args.url,False,args.fullmode)

if __name__ == '__main__':
    argv = sys.argv
    main(argv)

