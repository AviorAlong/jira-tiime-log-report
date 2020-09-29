## jira 工时日志导出

## 环境
 - python 3
## 下载
```git clone git@gitlab.zmaxis.com:along.shi/zm-jira-timelog-report.git ```
## 安装依赖

```pip install -r  requirements``` 

## 配置
- 配置 jira 

```sh
URL = ''  # jira 地址
USERNSME = '' # jira 账号
PASSWORD = '' # jira 密码
```
- 配置用户

由于jira账号体系有权限，分组，低权限账号不能访问组信息，所以提供user.json 配置文件，配置需要关注的账户信息
```json
[{
    "displayName": "",
    "emailAddress": "",
    "name": ""
}]
```
## 运行
指定日期，暂时只支持具体某一天，执行完成后会生成report.md文件
``` python main.py "xxxx-xx-xx"```
