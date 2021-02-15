#encoding=utf-8
import jieba

text = '大妈在路边捡了一个桶准备拿回家，防疫人员告诉她那是废弃口罩回收桶，大妈根本不听'

#with open(r'C:\Users\kennedy\Desktop\jresults\meta.txt', encoding='utf-8') as f:
#    text = f.read()

#Accurate Mode
data = jieba.cut(text, cut_all=False, HMM=False)
print(u"[Accurate Mode]: ", "/".join(data))

#Precise mode+HMM
data = jieba.cut(text, cut_all=False, HMM=True)
print(u"[precise mode]: ", "/".join(data))
