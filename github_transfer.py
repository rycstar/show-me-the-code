#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
#Filename:github_transfer.py
import time
import codecs
import requests
from bs4 import BeautifulSoup

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}
github_login_url = 'https://github.com/login'
github_login_post_url = 'https://github.com/session'
github_issue_list_url = 'https://github.com/noboundary/xGui/issues'
github_close_issue_list_url = 'https://github.com/noboundary/xGui/issues?q=is%3Aissue+is%3Aclosed'
github_domain = 'https://github.com'

gitlab_close_header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
}

gitlab_domain = 'http://172.16.1.8'
gitlab_login_url = 'http://172.16.1.8/users/sign_in'
gitlab_new_issue_url = 'http://172.16.1.8/fanvil_x6/VGUI/issues/new?issue%5Bassignee_id%5D=&issue%5Bmilestone_id%5D='
gitlab_new_issue_post_url = 'http://172.16.1.8/fanvil_x6/VGUI/issues'
gitlab_comment_post_url = 'http://172.16.1.8/fanvil_x6/VGUI/notes'
#gitlab data
gitlab_login_data = {
    'user[login]':'Terry',
    'user[password]':'********',
    'user[remember_me]':0
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

#github data
github_login_data = {
    'commit':'Sign in',
    'login':'rycstar',
    'password':'********',
}

github_issue_query_data = {
    'q':'is:issue is:closed',
    'page':1
}


#function to write the title & comment into gitlab
def gitlab_issue_set(session,title,comment,close):
    r = BeautifulSoup(session.get(gitlab_new_issue_url).text,'html.parser')
    gitlab_new_issue_data['utf8'] = r.findAll('input',attrs={'name':'utf8'})[0].get('value')
    gitlab_new_issue_data['authenticity_token'] = r.findAll('meta',attrs={'name':'csrf-token'})[0].get('content')
    gitlab_new_issue_data['issue[title]'] = title
    gitlab_new_issue_data['issue[description]'] = comment[0].text
    print gitlab_new_issue_data
    gitlab_new_issue_response = session.post(gitlab_new_issue_post_url,data=gitlab_new_issue_data,headers=header)
    gitlab_new_issue = BeautifulSoup(gitlab_new_issue_response.text,'html.parser')
    gitlab_issue_url = gitlab_new_issue.findAll('meta',attrs={'property':'og:url'})[0].get('content')
#begin to write the comment
    for x in range(1,len(comment) - 1):
        print gitlab_issue_url
        tmp_comment_soup = BeautifulSoup(session.get(gitlab_issue_url).text,'html.parser')
        gitlab_issue_comment_data['utf8'] = tmp_comment_soup.findAll('input',attrs={'name':'utf8'})[0].get('value')
        gitlab_issue_comment_data['authenticity_token'] = tmp_comment_soup.findAll('meta',attrs={'name':'csrf-token'})[0].get('content')
        gitlab_issue_comment_data['line_type'] = tmp_comment_soup.findAll('input',attrs={'name':'line_type'})[0].get('value')
        gitlab_issue_comment_data['view'] = tmp_comment_soup.findAll('input',attrs={'name':'view'})[0].get('value')
        gitlab_issue_comment_data['target_type'] = tmp_comment_soup.findAll('input',attrs={'name':'target_type'})[0].get('value')
        gitlab_issue_comment_data['target_id'] = tmp_comment_soup.findAll('input',attrs={'name':'target_id'})[0].get('value')
        gitlab_issue_comment_data['note[commit_id]'] = tmp_comment_soup.findAll('input',attrs={'name':'note[commit_id]'})[0].get('value')
        gitlab_issue_comment_data['note[noteable_id]'] = tmp_comment_soup.findAll('input',attrs={'name':'note[noteable_id]'})[0].get('value')
        gitlab_issue_comment_data['note[noteable_type]'] = tmp_comment_soup.findAll('input',attrs={'name':'note[noteable_type]'})[0].get('value')
        gitlab_issue_comment_data['note[note]'] = comment[x].text 
        gitlab_comment_response = session.post(gitlab_comment_post_url,data=gitlab_issue_comment_data,headers=header)
        print gitlab_comment_response
    if close == True:
        tmp_comment_soup = BeautifulSoup(session.get(gitlab_issue_url).text,'html.parser')
        gitlab_close_header['X-CSRF-Token'] = tmp_comment_soup.findAll('meta',attrs={'name':'csrf-token'})[0].get('content')
        r = session.put(gitlab_issue_url,data = gitlab_close_issue_data,headers = gitlab_close_header)
        print 'close issue : {0}'.format(r.status_code)

#function to read the title & comment from github
def github_issue_val_transfer(href_val,dest_session,close):
    issue_url = github_domain + href_val
    print 'Now we will get the value of issue : {0}'.format(issue_url)
    issues_values_soup = BeautifulSoup(res.get(issue_url).text,'html.parser')
    issue_title = issues_values_soup.find_all('span',attrs={'class':'js-issue-title'})[0].text
    issue_comment = issues_values_soup.body.find_all('textarea',attrs={'aria-label':'Comment body'})
#    for x in xrange(len(issue_comment) - 1):
#        print 'My comment ({0}):{1}'.format(x,issue_comment[x].text)
    gitlab_issue_set(dest_session,issue_title,issue_comment,close)

def github_issue_read(close_state):
    if (close_state == False):
        github_issue_query_data['q'] = 'is:open is:issue'
    else:
        github_issue_query_data['q'] = 'is:issue is:closed'

    length = 1
    i = 1
    while (length > 0):
        github_issue_query_data['page'] = i
        issue_list_soup = BeautifulSoup(res.get(github_issue_list_url,data = github_issue_query_data).text,'html.parser')
        issue_list = issue_list_soup.body.find_all('a',attrs={'class':'issue-title-link js-navigation-open'})
        print 'close state : {0} issue num:{1},next_page{2}'.format(close_state,len(issue_list),len(issue_list_soup.body.find_all(attrs={'class':'next_page'})))
        for x in xrange(len(issue_list)):
            time.sleep(4)
            github_issue_val_transfer(issue_list[x].get('href'),gitlab_session,close_state)
        next_page = issue_list_soup.body.find_all('a',attrs={'class':'next_page'})
        length = len(next_page)
        i = i + 1
        time.sleep(5)


#open the gitlab session
gitlab_session = requests.session()
gitlab_log_soup = BeautifulSoup(gitlab_session.get(gitlab_login_url).text,'html.parser')
gitlab_login_data['utf8'] = gitlab_log_soup.findAll('input',attrs={'name':'utf8'})[0].get('value')
gitlab_login_data['authenticity_token'] = gitlab_log_soup.findAll('input',attrs={'name':'authenticity_token'})[0].get('value')
print gitlab_login_data
gitlab_response = gitlab_session.post(gitlab_login_url,data=gitlab_login_data,headers=header)
print gitlab_response

#open the github session
with requests.session() as res:
    log_soup = BeautifulSoup(res.get(github_login_url).text,'html.parser')
    github_login_data['utf8'] = log_soup.findAll('input',attrs={'name':'utf8'})[0].get('value')
    github_login_data['authenticity_token'] = log_soup.findAll('input',attrs={'name':'authenticity_token'})[0].get('value')
    response = res.post(github_login_post_url,data=github_login_data,headers=header)
    print response

    github_issue_read(True)
    github_issue_read(False)


#   print response
#with codecs.open('./new_issue_id.txt','wb','utf-8') as f:
#    f.write(issue_list_soup.prettify())
#    f.close()

#soup = BeautifulSoup(open('new_issue_id.txt'),'html.parser')
#print soup.prettify()
#print soup.title
#print soup.head
#print soup.input.name
#print soup.input.attrs
#print len(soup.head.find_all('meta',attrs={'name':'csrf-token'}))
#for child in soup.body.children:
#    print child
#print soup.body.find_all('div',attrs={'class':'auth-form-body'})[0].find_all('label')

