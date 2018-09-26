# -*- coding:utf-8 -*-
"""
复杂规则下的文本快速匹配
"""
# -*- coding:utf-8 -*-
"""
复杂规则下的文本快速匹配
"""
import re
import json
import fool


# 规则集合类
class RulesSet:
    def __init__(self, rules):
        self.rules = []
        self.labels = []
        self.hit_rate = []
        self.keywords = []
        self.total_words = set()
        self.parse_rules(rules)
        self.lfreq = index_structure(self.total_words)

    def parse_rules(self, rules):
        for rule, rule_label, hit_rate in rules:
            words = re.split('[\&\~\(\)\|]', rule)
            keywords = set(words) - set([''])
            new_rule = transform_rule(rule)
            new_rule = new_rule.replace('&', ' and ').replace('~', ' and not ').replace('|', ' or ')
            new_rule_compile = compile(new_rule, '', 'eval')
            self.rules.append(new_rule_compile)
            self.labels.append(rule_label)
            self.hit_rate.append(hit_rate)
            self.keywords.append(keywords)
            self.total_words |= keywords


# 根据是否符合规则来标记文本
def mark_text(text, rules_set):
    s_r = text_search(text, rules_set.lfreq)
    result = compute_rules(rules_set, s_r)
    return json.dumps(result, ensure_ascii=False)


# 从文本集合中检索关键字
def retrieval_texts(texts, keywords):
    res = []
    lfreq = index_structure(keywords)
    for text in texts:
        r = text_search(text, lfreq)
        res.append(list(r.keys()))
    return res


# 根据关键字检索结果计算规则表达式
def compute_rules(rules_set, s_r):
    result = dict()
    not_key = ['招标', '投标', '采购', '集采', '中标', '应标', '租赁', '升级', '改造', '租用']
    for index, rule in enumerate(rules_set.rules):
        is_conform = eval(rule)
        if is_conform:
            hit_keys = [key for key in rules_set.keywords[index] if key in s_r and key not in not_key]
            if len(hit_keys) > rules_set.hit_rate[index]:
                result[rules_set.labels[index]] = ','.join(hit_keys)
    return result


# 从文本中检索存在的关键字
def text_search(content, lfreq):
    search_result = dict()
    N = len(content)
    k = 0
    while k < N:
        i = k + 1
        while i <= N:
            word = content[k:i]
            tag = lfreq.get(word, -1)
            if tag > 0:
                search_result[word] = True
            if tag < 0 or i == N:
                k += 1
                break
            i += 1
    return search_result


# 解析关键字集合成适合检索的结构  FREQ
def index_structure(keywords):
    lfreq = dict()
    for word in keywords:
        lfreq[word] = 1
        for ch in range(len(word) - 1):
            wfrag = word[:ch + 1]
            if wfrag not in lfreq:
                lfreq[wfrag] = 0
    return lfreq


# 判断检索结果是否含有关键字
def is_exist(word, search_result):
    return search_result.get(word, False)


# 将关键字检索结果函数增加到规则字符串中
def transform_rule(rule):
    new_rule = ''
    N = len(rule)
    k = 0
    op_set = set(['&', '~', '|', '(', ')'])
    if rule[0] not in op_set:
        new_rule += 'is_exist("'
    while k < N:
        before_k = k - 1
        if before_k >= 0 and rule[before_k] in op_set and rule[k] not in op_set:
            new_rule += 'is_exist("'
        if before_k >= 0 and rule[before_k] not in op_set and rule[k] in op_set:
            new_rule += '", s_r)'
        new_rule += rule[k]
        k += 1
    if rule[N-1] not in op_set:
        new_rule += '", s_r)'
    return new_rule


#规则应用
def rule(x):
        #rules1 = [('(协议&(签约|签订|签署备忘录|协定|合作意向|商签|入股))|(((战略合作~战略合作伙伴的引进)|(合同~用工合同~租赁合同)|(投资投资~在线投资~机构投资者~投资人~投资古玩~投资价值机会~投资者关注~投资理财~投资元素~投资咨询~投资组合~投资相匹配~投资创业~投资战略规划~草根投资~收益性投资行业)|(协议~自贸协议~约定的协议~劳动协议~最后协议~协议规定~脱欧协议)|入股|框架性|协定|协议书|合作意向|签约~这笔签约~签约主播|框架性|达成)&协议)', 'rule4', 0)]
        rules1 = [('(签订|入股|框架性|签署备忘录|合作意向|商签|入股|(战略合作~战略合作伙伴的引进)|(合同~用工合同~租赁合同)|(投资投资~在线投资~机构投资者~投资人~投资古玩~投资价值机会~投资者关注~投资理财~投资元素~投资咨询~投资组合~投资相匹配~投资创业~投资战略规划~草根投资~收益性投资行业)|(协议~自贸协议~约定的协议~劳动协议~最后协议~协议规定~脱欧协议)|(签约~这笔签约~签约主播))','rule4', 0)]

        #rules1 = [('(签订|签署|签约|)&(备忘录|达成|合同~用工合同|合作|投资~在线投资~机构投资者~投资人~投资古玩~投资价值机会~投资者关注~投资理财~投资元素~投资咨询~投资组合~投资相匹配~投资创业~投资战略规划~草根投资~收益性投资行业|协议~自贸协议~约定的协议~劳动协议~最后协议~协议规定~脱欧协议|入股|框架性|协定|协议书|合作意向|签约~这笔签约~签约主播)', 'rule4', 0)]
        #rules2 = [('合同|期限|服务年限|服务期|服务期限|服务有效期|付日期|工期要求|工时|供货期|供货期限|合同签订|合同生效|建设工期|交付（服务、完工）时间|交付或实施时间|交付日期|交付时间|交货期|交货时间|期限(交货期)|期限交货期|完成时间要求|完工期|项目服务期限|项目工期|项目实施周期', 'rule4', 0)]

        rules_set1 = RulesSet(rules1)
        p=retrieval_texts([x], rules_set1.total_words)[0]

        if str(p) == '[]':
            return None
        else:
            return p

        return p
#命名实体识别标签规则

def tages(x):
    q = fool.analysis(x)
    s =[i[3] for i in q[1][0] if i[2] == 'company']

    #if re.findall('央|行|证券|德普|吉恩|期货|酒|美联社|路透社|伊朗|普京|律师|基金|白马股|代写投标书|[a-zA-Z]|\*|[\xa0\u3000]',str(s)):
     #   return None
    #elif re.findall('[[\u4e00-\u9fa5]{0,25}公司]',str(s)):
        #return set(s)
    
    for i in range(len(s)):
        s[i] = s[i].replace(' ','').replace('\u3000','')

    com = []
    for i in s:
        if re.findall('[\u4e00-\u9fa5][^0-9a-zA-Z_]{0,25}公司',str(i)):
            com.append(i)
        if len(set(com)) >2 and len(set(com)) <8:
                return set(com)




#分句
def fenju(x):
    global token
    start=0
    i=0#每个字符的位置
    sentences=[]
    punt_list= '!?. 。'
    texts=str(x)
    for text in texts:
        if text in punt_list and token not in punt_list: #检查标点符号下一个字符是否还是标点
            sentences.append(texts[start:i+1])#当前标点符号位置
            start=i+1#start标记到下一句的开头
            i+=1
        else:
            i+=1#若不是标点符号，则字符位置继续前移
            token=list(texts[start:i+2]).pop()#取下一个字符
    if start<len(texts):
        sentences.append(texts[start:])#这是为了处理文本末尾没有标点符号的情况
    return sentences
def keys(x):
    a = []
    keys ='签订|签署|签约|备忘录|达成|合同|合作|投资|协议|入股|框架性|协定|协议书|合作意向|商签'
    for i in fenju(x):
        if re.findall(keys,i):
            a.append(i)
            if a == '[]':
                return None
            else:
                return a
 

#加载词典
def load_dict_from_file(filepath):
    _dict = {}
    try:
        with io.open(filepath, 'r',encoding='utf-8') as dict_file:
            for line in dict_file:
                (key, value) = line.strip().split(' ') #将原本用空格分开的键和值用冒号分开来，存放在字典中
                _dict[key] = value
    except IOError as ioerr:
        print("文件 %s 不存在" % (filepath))
    return _dict









