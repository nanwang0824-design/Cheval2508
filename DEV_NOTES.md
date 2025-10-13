
https://netkeiba.com/

https://github.com/nanwang0824-design/Cheval2508

Race
https://jra.jp/JRADB/accessS.html?CNAME=pw01sde1005202405050820241116/CC

Horse
https://jra.jp/JRADB/accessU.html?CNAME=pw01dud102019110120/45
https://jra.jp/JRADB/accessU.html?CNAME=pw01dud102021110161/03
https://jra.jp/JRADB/accessU.html?CNAME=pw01dud102019105399/FF

returns from race_parser of old version
{'pw01dud102011105541/19': '/JRADB/accessU.html?CNAME=pw01dud102011105541/19', 'pw01dud102011103649/04': '/JRADB/accessU.html?CNAME=pw01dud102011103649/04', 'pw01dud102009105131/3A': '/JRADB/accessU.html?CNAME=pw01dud102009105131/3A', 'pw01dud102011105995/F9': '/JRADB/accessU.html?CNAME=pw01dud102011105995/F9', 'pw01dud102012101215/F2': '/JRADB/accessU.html?CNAME=pw01dud102012101215/F2', 'pw01dud102009106336/CA': '/JRADB/accessU.html?CNAME=pw01dud102009106336/CA', 'pw01dud102010104176/49': '/JRADB/accessU.html?CNAME=pw01dud102010104176/49', 'pw01dud102012100680/F8': '/JRADB/accessU.html?CNAME=pw01dud102012100680/F8', 'pw01dud102012100255/43': '/JRADB/accessU.html?CNAME=pw01dud102012100255/43', 'pw01dud102010100524/1B': '/JRADB/accessU.html?CNAME=pw01dud102010100524/1B', 'pw01dud102012106003/45': '/JRADB/accessU.html?CNAME=pw01dud102012106003/45', 'pw01dud102012105338/58': '/JRADB/accessU.html?CNAME=pw01dud102012105338/58', 'pw01dud102013100218/E8': '/JRADB/accessU.html?CNAME=pw01dud102013100218/E8', 'pw01dud102010104560/4B': '/JRADB/accessU.html?CNAME=pw01dud102010104560/4B'}
{'pw04kmk001067/84': "doAction('/JRADB/accessK.html', 'pw04kmk001067/84');", 'pw04kmk001123/F2': "doAction('/JRADB/accessK.html', 'pw04kmk001123/F2');", 'pw04kmk001008/8E': "doAction('/JRADB/accessK.html', 'pw04kmk001008/8E');", 'pw04kmk001139/A5': "doAction('/JRADB/accessK.html', 'pw04kmk001139/A5');", 'pw04kmk000691/10': "doAction('/JRADB/accessK.html', 'pw04kmk000691/10');", 'pw04kmk001068/10': "doAction('/JRADB/accessK.html', 'pw04kmk001068/10');", 'pw04kmk001069/9C': "doAction('/JRADB/accessK.html', 'pw04kmk001069/9C');", 'pw04kmk001087/5A': "doAction('/JRADB/accessK.html', 'pw04kmk001087/5A');", 'pw04kmk001113/87': "doAction('/JRADB/accessK.html', 'pw04kmk001113/87');", 'pw04kmk001023/A8': "doAction('/JRADB/accessK.html', 'pw04kmk001023/A8');", 'pw04kmk000727/B5': "doAction('/JRADB/accessK.html', 'pw04kmk000727/B5');", 'pw04kmk001035/2B': "doAction('/JRADB/accessK.html', 'pw04kmk001035/2B');", 'pw04kmk001120/4E': "doAction('/JRADB/accessK.html', 'pw04kmk001120/4E');", 'pw04kmk000695/40': "doAction('/JRADB/accessK.html', 'pw04kmk000695/40');"}
{'pw05cmk001006/B9': "doAction('/JRADB/accessC.html', 'pw05cmk001006/B9');", 'pw05cmk001076/A6': "doAction('/JRADB/accessC.html', 'pw05cmk001076/A6');", 'pw05cmk000353/E1': "doAction('/JRADB/accessC.html', 'pw05cmk000353/E1');", 'pw05cmk001042/35': "doAction('/JRADB/accessC.html', 'pw05cmk001042/35');", 'pw05cmk001032/CA': "doAction('/JRADB/accessC.html', 'pw05cmk001032/CA');", 'pw05cmk000412/F3': "doAction('/JRADB/accessC.html', 'pw05cmk000412/F3');", 'pw05cmk001051/14': "doAction('/JRADB/accessC.html', 'pw05cmk001051/14');", 'pw05cmk001109/A7': "doAction('/JRADB/accessC.html', 'pw05cmk001109/A7');", 'pw05cmk001080/C9': "doAction('/JRADB/accessC.html', 'pw05cmk001080/C9');", 'pw05cmk001029/33': "doAction('/JRADB/accessC.html', 'pw05cmk001029/33');", 'pw05cmk001120/91': "doAction('/JRADB/accessC.html', 'pw05cmk001120/91');", 'pw05cmk000411/67': "doAction('/JRADB/accessC.html', 'pw05cmk000411/67');", 'pw05cmk001012/F4': "doAction('/JRADB/accessC.html', 'pw05cmk001012/F4');", 'pw05cmk001054/B8': "doAction('/JRADB/accessC.html', 'pw05cmk001054/B8');"}

本地安装包改为线上安装，否则requirements难以正确生成

src/cheval/parsers/parsers.py以后不用的话就删掉

GitHub更新：
git add .
git commit -m "更新了XXX"
git push


1, 打开你的 Clash for Windows → 查看「代理端口」。
一般 HTTP 代理端口是 7890（或者 7891）。
你可以在 Clash 主界面右下角或设置页看到。
2, 在 VS Code 的终端中执行以下命令（假设端口是 7890）：
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
如果你不想影响所有 Git 项目，可以只在当前项目生效：
git config http.proxy http://127.0.0.1:7890
git config https.proxy http://127.0.0.1:7890
3, 当你不需要使用 Clash 时，可以取消这些设置：
git config --global --unset http.proxy
git config --global --unset https.proxy
4, 可选：检查当前代理设置
git config --global --get http.proxy
git config --global --get https.proxy


通过 SQLAlchemy / SQLModel 查询得到的对象默认都是 attached / 受 Session 管理 的对象，Session 会自动追踪它们的属性变化，commit() 时会把改动写回数据库。
如果你希望拿到查询结果用于分析、建模或其他操作，而不希望对原对象的修改被写回数据库，有几种常用方法：
1, session.expunge(obj)
2, 使用 session.expunge_all()
3, 使用 session.rollback() + copy
4, 使用 autoflush=False 或 expire_on_commit=False 配合 Session
如果只是分析建模，可以在拿到结果后 deepcopy() 或 expunge()；
如果会有大量对象或关系复杂，可以用独立 Session + expunge_all()。