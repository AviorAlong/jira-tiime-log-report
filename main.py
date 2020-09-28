#!/usr/bin/python
from atlassian import Jira
import sys
import json
import logging

def get_day_report(date):
    """
    docstring
    """
    jira = Jira(
            url='',
            username='',
            password=''
        )
    # 读取组员信息
    with open('users.json', 'r',encoding='utf-8') as f:
        users = json.load(f)
        users_strs = [ i['name'] for i in users ] 

        workers = ','.join(users_strs)

    jql_request =  "worklogAuthor in ({}) AND worklogDate = {}".format(workers, date)
    issues = jira.jql(jql_request)
    
    tableHead = '| 姓名 | 任务 | 工作日志 | \n'
    tableMode = '| ---  | --- | ----| \n'
    fileContent = tableHead + tableMode
    if issues and issues['total'] > 0:
        for w in  issues['issues']:
            if w['fields'] and  w['fields']['worklog'] and w['fields']['worklog']['worklogs']:
                workerlogs = w['fields']['worklog']['worklogs']
                for i in workerlogs:
                    updatetime = i['updated'].split('T')

                    if updatetime[0] == date:
                        name = i['author']['displayName']
                        # 替换换行和制表符
                        log = i['comment'].replace('\r\n',' ')
                        task = w['key']
                        tableContent = '| {} | http://jira.zmops.cc/browse/{} | {} | \n'.format(name,task,log)
                        fileContent = fileContent + tableContent
                  
        with open('report.md','w', encoding='utf-8') as f:
            f.write(fileContent)
    else:
        print('未查询到有效数据，请检查查询条件')


if __name__ == "__main__":
    args = sys.argv[1]
    get_day_report(args)