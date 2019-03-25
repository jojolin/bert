#!/usr/bin/env python
import sys
import json

'''
POS	Meaning

n	common nouns
f	localizer
s	space
t	time
nr	noun of people
ns	noun of space
nt	noun of time
nw	noun of work
nz	other proper noun
v	verbs
vd	verb of adverbs
vn	verb of noun
a	adjective
ad	adjective of adverb
an	adnoun
d	adverbs
m	numeral
q	quantity
r	pronoun
p	prepositions
c	conjunction
u	auxiliary
xc	other function word
w	punctuations
'''

def check_postag(datafp):
    '''
    {"postag": [{"word": "斑刺莺", "pos": "nz"}, {"word": "是", "pos": "v"}, {"word": "雀形目", "pos": "n"}, {"word": "、", "pos": "w"}, {"word": "剌嘴莺科", "pos": "nz"}, {"word": "的", "pos": "u"}, {"word": "一种", "pos": "m"}, {"word": "动物", "pos": "n"}, {"word": "，", "pos": "w"}, {"word": "分布", "pos": "v"}, {"word": "于", "pos": "p"}, {"word": "澳大利亚", "pos": "ns"}, {"word": "和", "pos": "c"}, {"word": "新西兰", "pos": "ns"}, {"word": "，", "pos": "w"}, {"word": "包括", "pos": "v"}, {"word": "澳大利亚", "pos": "ns"}, {"word": "、", "pos": "w"}, {"word": "新西兰", "pos": "ns"}, {"word": "、", "pos": "w"}, {"word": "塔斯马尼亚", "pos": "ns"}, {"word": "及其", "pos": "c"}, {"word": "附近", "pos": "f"}, {"word": "的", "pos": "u"}, {"word": "岛屿", "pos": "n"}], "text": "斑刺莺是雀形目、剌嘴莺科的一种动物，分布于澳大利亚和新西兰，包括澳大利亚、新西兰、塔斯马尼亚及其附近的岛屿", "spo_list": [{"predicate": "目", "object_type": "目", "subject_type": "生物", "object": "雀形目", "subject": "斑刺莺"}]}
    '''
    postag_set = set()
    with open(datafp, 'r', encoding='utf8') as r:
        for line in r.readlines():
            ljson = json.loads(line)
            spo_list = ljson['spo_list']
            postag = ljson['postag']
            for spo in spo_list:
                obj = spo['object']
                sub = spo['subject']

                for x in postag:
                    if x['word'] == obj or x['word'] == sub:
			#{'nz', 'r', 'n', 'a', 'nw', 't', 'ns', 'vn', 'an', 'xc', 'm', 'ad', 'v', 'd', 'nt', 'nr'}
                        if x['pos'] in ('ad', 'xc', 'vn', 'a', 'r', 'd', 'an', 'ad', 'v'):
                            print(x, '--', ljson, '\n')
                        postag_set.add(x['pos'])
                        break
            #break
    print(postag_set - set(['ad', 'xc', 'vn', 'a', 'r', 'd', 'an', 'ad', 'v']))
    print(postag_set)

#{'n', 'nt', 'nr', 'nz', 'm', 'nw', 't', 'ns'}

def convert_example(datafp, data_tgt_fp):
    '''{"postag": [{"word": "斑刺莺", "pos": "nz"}, {"word": "是", "pos": "v"}, {"word": "雀形目", "pos": "n"}, {"word": "、", "pos": "w"}, {"word": "剌嘴莺科", "pos": "nz"}, {"word": "的", "pos": "u"}, {"word": "一种", "pos": "m"}, {"word": "动物", "pos": "n"}, {"word": "，", "pos": "w"}, {"word": "分布", "pos": "v"}, {"word": "于", "pos": "p"}, {"word": "澳大利亚", "pos": "ns"}, {"word": "和", "pos": "c"}, {"word": "新西兰", "pos": "ns"}, {"word": "，", "pos": "w"}, {"word": "包括", "pos": "v"}, {"word": "澳大利亚", "pos": "ns"}, {"word": "、", "pos": "w"}, {"word": "新西兰", "pos": "ns"}, {"word": "、", "pos": "w"}, {"word": "塔斯马尼亚", "pos": "ns"}, {"word": "及其", "pos": "c"}, {"word": "附近", "pos": "f"}, {"word": "的", "pos": "u"}, {"word": "岛屿", "pos": "n"}], "text": "斑刺莺是雀形目、剌嘴莺科的一种动物，分布于澳大利亚和新西兰，包括澳大利亚、新西兰、塔斯马尼亚及其附近的岛屿", "spo_list": [{"predicate": "目", "object_type": "目", "subject_type": "生物", "object": "雀形目", "subject": "斑刺莺"}]} '''
    pos_name_map = {
            'n': '名词',
            'nt': '机构',
            'nr': '人物',
            'nz': '其他名词',
            'm': '数字',
            'nw': '作品',
            't': '时间',
            'ns': '空间'
            }
    pos_name_map = {
            'n': '名',
            'nt': '机',
            'nr': '人',
            'nz': '名',
            'm': '数',
            'nw': '作',
            't': '时',
            'ns': '空'
            }
    num = 0
    data_tgt_fo = open(data_tgt_fp, 'w', encoding='utf8')
    data_tgt_fo.write('{}\t{}\n'.format('text_a', 'label')) # write header
    line_max_len = 0
    with open(datafp, 'r', encoding='utf8') as r:
        for line in r:
            if line.strip() == '':
                continue

            ljson = json.loads(line)
            postag = ljson['postag']
            tag_text_ls = []
            for x in postag:
                # TODO: modify allow pos set
                if x['pos'] in ('n', 'nt', 'nr', 'nz', 'm', 'nw', 't', 'ns'):
                    #if x['pos'] == 'nt':
                    #    print('---', ljson)
                    name = pos_name_map.get(x['pos'])
                    tag_text_ls.append('<{}>{}<{}>'.format(name, x['word'], name))
                else:
                    tag_text_ls.append(x['word'])
            if len(tag_text_ls) > line_max_len:
                line_max_len = len(tag_text_ls)
            #print(''.join(tag_text_ls), '\n')
            for spo in ljson['spo_list']:
                pre = spo['predicate']
                obj = spo['object']
                sub = spo['subject']
                label_obj = _get_label(obj, 'OBJ')
                label_sub = _get_label(sub, 'SUB')
                tag_text_copy = tag_text_ls.copy()
                tag_text_copy.append('“{}”'.format(pre))
                tag_text = ''.join(tag_text_copy)
                label_text = ['O'] * len(tag_text)
                obj_st = tag_text.find(obj)
                if obj_st > -1:
                    label_text[obj_st: obj_st+len(obj)] = label_obj
                sub_st = tag_text.find(sub)
                if sub_st > -1:
                    label_text[sub_st: sub_st+len(sub)] = label_sub

                #print(len(list(tag_text)), '\x02'.join(list(tag_text)))
                #print(len(label_text), '\x02'.join(label_text))
                data_tgt_fo.write('\x02'.join(list(tag_text)))
                data_tgt_fo.write('\t')
                data_tgt_fo.write('\x02'.join(label_text))
                data_tgt_fo.write('\n')

            #print(ljson)
            num += 1
            #if num > 5:
            #    break

    data_tgt_fo.close()
    print('max len(line)', line_max_len)

def _get_label(o, typ=''):
    labels = ['I-{}'.format(typ)] * len(o)
    labels[0] = 'B-{}'.format(typ)
    return labels

def main():
    #check_postag(sys.argv[1])
    convert_example(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
