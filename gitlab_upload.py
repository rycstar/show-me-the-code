#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
#Filename:gitlab_upload.py
import sys
import os
import time
import codecs
import requests
from bs4 import BeautifulSoup
import argparse

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}
gitlab_domain = 'http://172.16.1.8'
gitlab_login_url = gitlab_domain + '/users/sign_in'
gitlab_issue_url = gitlab_domain + '/fanvil_x6/test_prj/issues'
gitlab_comment_post_url = gitlab_domain + '/fanvil_x6/test_prj/notes'

#gitlab data
gitlab_close_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
}

gitlab_login_data = {
    'user[login]':'********',
    'user[password]':'********',
    'user[remember_me]':0
}

gitlab_open_new_issue_data = {
    'issue[assignee_id]':'',
    'issue[milestone_id]':''
}

gitlab_new_issue_data = { 
        'issue[title]':'',
        'issue[description]':'',
        'issue[assignee_id]':'',
        'issue[milestone_id]':'',
        'issue[label_ids][]':''
        }
gitlab_issue_comment_data = {
        'note[note]':'',
        'commit':'Add Comment'
        }

gitlab_close_issue_data = {
    'issue[state_event]':'close',
    'status_only':'true'
}

def args_handler(argv):
    p = argparse.ArgumentParser(description='download from github.com')
    p.add_argument('-u','--user',action='store',default=None,type = str,help = 'Input user name')
    p.add_argument('-p','--password',action='store',default=None,type = str,help = 'Input password')
#    p.add_argument('-f','--fullmode',action='store',default=0,type = int,help = '1 == Down the whole issue html, 0 == down the title and comment only')
    p.add_argument('-l','--url',action='store',default='http://172.16.1.8/',type = str,help = 'Input src issue url')
    args = p.parse_args(argv[1:])
    return args

def gitlsb_issue_import(session,file_name):
    soup = BeautifulSoup(open(file_name),'html.parser')
    issue_title_val = soup.find_all('span',attrs={'class':'js-issue-title'})[0].text
    issue_close_state = soup.find_all('div',attrs={'class':'state state-closed'})
    if len(issue_close_state) > 0 :
        issue_close_val = True
    else:
        issue_close_val = False
    issue_comment = soup.find_all('div',attrs={'class':'edit-comment-hide'})
    
    r = BeautifulSoup(session.get(gitlab_issue_url,data=gitlab_open_new_issue_data).text,'html.parser')
    gitlab_new_issue_data['utf8'] = r.findAll('input',attrs={'name':'utf8'})[0].get('value')
    gitlab_new_issue_data['authenticity_token'] = r.findAll('meta',attrs={'name':'csrf-token'})[0].get('content')
    gitlab_new_issue_data['issue[title]'] = issue_title_val
    gitlab_new_issue_data['issue[description]'] = issue_comment[0].text

    gitlab_new_issue_response = session.post(gitlab_issue_url,data=gitlab_new_issue_data,headers=header)
    r = BeautifulSoup(gitlab_new_issue_response.text,'html.parser')
    url = r.findAll('meta',attrs={'property':'og:url'})[0].get('content')
    for x in range(1,len(issue_comment)):
        tmp_soup = BeautifulSoup(session.get(url).text,'html.parser')
        gitlab_issue_comment_data['utf8'] = tmp_soup.findAll('input',attrs={'name':'utf8'})[0].get('value')
        gitlab_issue_comment_data['authenticity_token'] = tmp_soup.findAll('meta',attrs={'name':'csrf-token'})[0].get('content')
        gitlab_issue_comment_data['line_type'] = tmp_soup.findAll('input',attrs={'name':'line_type'})[0].get('value')
        gitlab_issue_comment_data['view'] = tmp_soup.findAll('input',attrs={'name':'view'})[0].get('value')
        gitlab_issue_comment_data['target_type'] = tmp_soup.findAll('input',attrs={'name':'target_type'})[0].get('value')
        gitlab_issue_comment_data['target_id'] = tmp_soup.findAll('input',attrs={'name':'target_id'})[0].get('value')
        gitlab_issue_comment_data['note[commit_id]'] = tmp_soup.findAll('input',attrs={'name':'note[commit_id]'})[0].get('value')
        gitlab_issue_comment_data['note[noteable_id]'] = tmp_soup.findAll('input',attrs={'name':'note[noteable_id]'})[0].get('value')
        gitlab_issue_comment_data['note[noteable_type]'] = tmp_soup.findAll('input',attrs={'name':'note[noteable_type]'})[0].get('value')
        gitlab_issue_comment_data['note[note]'] = issue_comment[x].text 
        gitlab_comment_response = session.post(gitlab_comment_post_url,data=gitlab_issue_comment_data,headers=header)
        
    if issue_close_val == True:
        tmp_soup = BeautifulSoup(session.get(url).text,'html.parser')
        gitlab_close_header['X-CSRF-Token'] = tmp_soup.findAll('meta',attrs={'name':'csrf-token'})[0].get('content')
        r = session.put(url,data = gitlab_close_issue_data,headers = gitlab_close_header)
    print 'close state : {0},title:{1} '.format(issue_close_val,issue_title_val)

def gitlab_login(session,user,password):
    log_soup = BeautifulSoup(session.get(gitlab_login_url).text,'html.parser')
    gitlab_login_data['utf8'] = log_soup.findAll('input',attrs={'name':'utf8'})[0].get('value')
    gitlab_login_data['authenticity_token'] = log_soup.findAll('input',attrs={'name':'authenticity_token'})[0].get('value')
    gitlab_login_data['user[login]'] = user
    gitlab_login_data['user[password]'] = password
    response = session.post(gitlab_login_url,data=gitlab_login_data,headers=header)
    print response

def find_src_file(tag):
    src_file_list = []
    file_list = os.listdir(os.getcwd())
    for x in xrange(len(file_list)):
        if (file_list[x].find(tag) >= 0):
            src_file_list.append(file_list[x])
    return src_file_list

def main(argv):
    args = args_handler(argv)
    print args
    import_file_list = find_src_file('issue.html')
    if not len(import_file_list):
        print 'No file found, please check it ...'
        return
    gitlab_session = requests.session()
    gitlab_login(gitlab_session,args.user,args.password)
    time.sleep(1)
#    for x in xrange(len(import_file_list)):
    for x in xrange(1):
        gitlsb_issue_import(gitlab_session,import_file_list[x])
if __name__ == '__main__':
    argv = sys.argv
    main(argv)

