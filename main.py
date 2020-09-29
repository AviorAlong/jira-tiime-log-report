#!/usr/bin/python
#-*- coding: utf-8 -*-
from atlassian import Jira
import sys
import json
import logging
import config

jira = Jira(
        url=config.Config.URL,
        username = config.Config.USERNSME,
        password=config.Config.PASSWORD
    )

def get_users():
    """
    获取用户信息
    """
    try:
        # 由于账号权限不够 暂未调试该结果
        u = jira.get_all_users_from_group(config.Config.GROUP)
        if u:
            users = json.load(u)
            users_strs = [ i['name'] for i in users ] 
            workers = ','.join(users_strs)
        else:
            raise '获取jira用户组信息失败'
    except Exception as e:
        print(e)
        with open('users.json', 'r',encoding='utf-8') as f:
            users = json.load(f)
            users_strs = [ i['name'] for i in users ] 
            workers = ','.join(users_strs)
    return workers

def getMD(issues,d):
    """
    处理成markdown 格式
    """
    tableHead = '| 姓名 | 任务 | 工作日志 | \n'
    tableMode = '| ---  | --- | ----| \n'
    fileContent = tableHead + tableMode
    for w in  issues['issues']:
        if w['fields'] and  w['fields']['worklog'] and w['fields']['worklog']['worklogs']:
            workerlogs = w['fields']['worklog']['worklogs']
            for i in workerlogs:
                startTime = i['started'].split('T')

                if startTime[0] == d:
                    name = i['author']['displayName']
                    # 替换换行和制表符
                    log = i['comment'].replace('\r\n',' ')
                    task = w['key']
                    tableContent = '| {} | http://jira.zmops.cc/browse/{} | {} | \n'.format(name,task,log)
                    fileContent = fileContent + tableContent
    return fileContent

def get_day_report(d):
    """
    获取某一天的工作日志
    """
  
    # 读取组员信息
    workers = get_users()

    jql_request =  "worklogAuthor in ({}) AND worklogDate = {}".format(workers, d)
    issues = jira.jql(jql_request)
    
    if issues and issues['total'] > 0:
        fileContent = getMD(issues,d) 
        with open('report.md','w', encoding='utf-8') as f:
            f.write(fileContent)
    else:
        print('未查询到有效数据，请检查查询条件')


if __name__ == "__main__":
    args = sys.argv[1]
    get_day_report(args)