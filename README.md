# Newsfilter
News filtering and Named Entity Recognition
新闻合同签署实体标签和规则识别

项目思路：
为了判断新闻是否为公司之间的合同签署的内容，我们采取了两种方式：一方面通过关键字组合匹配新闻内容；另一方面我们通过foolnlp命名实体识别出关于‘company’的标签，抽取大于等于两个实体标签的新闻内容；
