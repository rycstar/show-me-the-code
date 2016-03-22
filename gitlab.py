#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
#Filename:gitlab.py

import codecs
import requests  
from bs4 import BeautifulSoup
  
#s = requests.session()

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'}
#gitlab_new_issue_url = 'http://172.16.1.8/fanvil_x6/VGUI/issues/new'
gitlab_new_issue_url = 'http://172.16.1.8/fanvil_x6/test_prj/issues/new?issue%5Bassignee_id%5D=&issue%5Bmilestone_id%5D='

form_data = {
    'utf8':'✓',
    'user[login]':'Terry',
    'user[password]':'12345678',
    'user[remember_me]':0
}

new_issue_data = {
    'issue[title]':'Just for a test',
    'issue[description]':"I'm a joke 2",
    'issue[assignee_id]':'',
    'issue[milestone_id]':'',
    'issue[label_ids][]':''
}

issue_comment_data = {
    'note[note]':"I'm a comment",  
    'commit':'Add Comment'
}

with requests.session() as res:
    log_soup = BeautifulSoup(res.get('http://172.16.1.8/users/sign_in').text,'html.parser')
    form_data['utf8'] = log_soup.findAll('input',attrs={'name':'utf8'})[0].get('value')
    form_data['authenticity_token'] = log_soup.findAll('input',attrs={'name':'authenticity_token'})[0].get('value')
#    print form_data
    response = res.post('http://172.16.1.8/users/sign_in',data=form_data,headers=header)
    print response

    #r = BeautifulSoup(res.get(gitlab_new_issue_url).text,'html.parser')
#    print r
    #new_issue_data['utf8'] = r.findAll('input',attrs={'name':'utf8'})[0].get('value')
    #new_issue_data['authenticity_token'] = r.findAll('meta',attrs={'name':'csrf-token'})[0].get('content')
    #print new_issue_data
    #response = res.post('http://172.16.1.8/fanvil_x6/test_prj/issues',data=new_issue_data,headers=header)
    #res_issue = BeautifulSoup(response.text,'html.parser')

#get the new issue id from response.text. If we open the redirected.
    #issue_url = res_issue.findAll('meta',attrs={'property':'og:url'})[0].get('content')
    issue_url = 'http://172.16.1.8/fanvil_x6/test_prj/issues/15'
    print issue_url
    r = BeautifulSoup(res.get(issue_url).text,'html.parser')
#first, we get the authenticity_token
    issue_comment_data['utf8'] = r.findAll('input',attrs={'name':'utf8'})[0].get('value')
    issue_comment_data['authenticity_token'] = r.findAll('meta',attrs={'name':'csrf-token'})[0].get('content')
    issue_comment_data['line_type'] = r.findAll('input',attrs={'name':'line_type'})[0].get('value')
    issue_comment_data['view'] = r.findAll('input',attrs={'name':'view'})[0].get('value')
    issue_comment_data['target_type'] = r.findAll('input',attrs={'name':'target_type'})[0].get('value')
    issue_comment_data['target_id'] = r.findAll('input',attrs={'name':'target_id'})[0].get('value')
    issue_comment_data['note[commit_id]'] = r.findAll('input',attrs={'name':'note[commit_id]'})[0].get('value')
    issue_comment_data['note[noteable_id]'] = r.findAll('input',attrs={'name':'note[noteable_id]'})[0].get('value')
    issue_comment_data['note[noteable_type]'] = r.findAll('input',attrs={'name':'note[noteable_type]'})[0].get('value')
    comment_response = res.post('http://172.16.1.8/fanvil_x6/test_prj/notes',data=issue_comment_data,headers=header)
    print comment_response
#   print response
#   print res_issue
#with codecs.open('./new_issue_id.txt','wb','utf-8') as f:
#    f.write(res.get(issue_url).text)
#    f.close()
