#
#导入词云库
from wordcloud import WordCloud
 #导入图像处理库
import PIL.Image as image
 #导入数据处理库
import numpy as np
 #导入结巴分词库
import jieba

 # 分词模块
def cut(text):
   # 选择分词模式
   word_list = jieba.cut(text,cut_all= True)
   # 分词后在单独个体之间加上空格
   result = " ".join(word_list)
   return result

 #导入文本文件,进行分词,制作词云
fp =r'C:\Users\kennedy\Desktop\jresults\meta1.txt'
text = open(fp).read()
   # 将读取的中文文档进行分词
#text = cut(text)
   #设置词云形状
mask = np.array(image.open(r'C:\Users\kennedy\Desktop\jresults\img.jpg'))
   #自定义词云
wordcloud = WordCloud(
     # 遮罩层,除白色背景外,其余图层全部绘制（之前设置的宽高无效）
     mask=mask,
     #默认黑色背景,更改为白色
     background_color='#FFFFFF',
     #按照比例扩大或缩小画布
     #scale=,
     # 若想生成中文字体,需添加中文字体路径
     font_path= r'C:\Users\kennedy\Desktop\jresults\Zenzai Itacha.ttf'
).generate(text)
   #返回对象
image_produce = wordcloud.to_image()
   #保存图片
wordcloud.to_file("new_wordcloud.jpg")
   #显示图像
image_produce.show()
