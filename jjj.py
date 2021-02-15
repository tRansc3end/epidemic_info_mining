#encoding=utf-8
import jieba

# opening target file for segmentation
with open(r'C:\Users\kennedy\Desktop\jresults\meta.txt', encoding='utf-8') as f:
    text = f.read()
#Jieba at work
data = jieba.cut(text, cut_all=False, HMM=True)
print(u" ", "/".join(data))
