# -dvwa-sql-
这是基于dvwa靶场的sql注入攻击，是本人为实现安全系统实验而完成的
dvwa选择的难度为low，为get型注入，至于post以后大概会修改上传
其中联合查询注入和报错注入是针对sql injection
时间盲注和布尔盲注是针对sql injection（blind）
输入要求：url，cookie
比如：url=http://192.168.1.13/DVWA/vulnerabilities/sqli_blind/
cookie信息可在浏览器下F12 network中查看http头部信息获得，或者用burpsuite抓包
