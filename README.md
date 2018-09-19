# Newsfilter
News filtering and Named Entity Recognition
新闻合同签署实体标签和规则识别

项目思路：
为了判断新闻是否为公司之间的合同签署的内容，我们采取了两种方式：一方面通过关键字组合匹配新闻内容；另一方面我们通过foolnlp命名实体识别出关于‘company’的标签，抽取大于等于两个实体标签的新闻内容；
RULE-KEYS:
(协议&(签约|签订|签署|签定|协定|订交|契约|订定|合同|和议))|((投资|入股|合作|备忘录|协议书|达成|三方|意向性|框架性|商签|合作意向)&协议)
FOOLNLP: 
text='中国移动公司和和中国联通达成了战略合作’
命名实体识别结果:
[(0, 7, ‘company’, ‘中国移动公司’), (8, 13, ‘company’, ‘中国联通’)]
运行环境：
python3.6
INSTALL THE DEPENDENCIES AND DEVDEPENDENCIES AND START THE SERVER.
$ pip install foolnlp
$ pip install pandas
源码
数据加载：
$ df = pd.read_csv('d:/new/20180710173001_webspider.csv', sep='|', encoding='utf-8')
数据指定列去重:
$ df.drop_duplicates(subset='content',keep='first',inplace=True)
对CONTENT列进行规则匹配，返回抓取关键字：
$ df['tages_rule'] = df['content'].apply(rule)
对CONTENT列进行命名实体识别，识别包含‘COMPANY’标签的实体，取出大于且等于2的标签实体:
$ df['tages_rule_1'] = df['content'].apply(tages)
对‘TAGES_RULE’和’TAGES_RULE‘列进行过滤，只取出符合规则的文件:
$ df1=df[(~df['tages_rule'].isin(['0'])) | (~df['tages_rule_1'].isin(['0']))]
处理文件输出:
df1.to_csv('d:/new/new_rule.csv',sep='|',encoding='utf-8')

