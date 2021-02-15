# coding=utf-8
import re
import jieba.analyse as analyse
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy

comments = []
cleaned_comments = ''
def filterComments():
    cleaned_comments = ''
    with open(r'C:\Users\kennedy\Desktop\final\march12text.txt', encoding='utf8') as f:
        for line in f:
            comments.append(line)
    for k in range(len(comments)):
        cleaned_comments = cleaned_comments + (str(comments[k])).strip()
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern, cleaned_comments)
    cleaned_comments = ''.join(filterdata)
    return  cleaned_comments
#cut and tag
cleaned_comments = filterComments()
analyse.set_stop_words(r'C:\Users\kennedy\Desktop\jresults\STOPWORDS.txt')
words_df = analyse.extract_tags(cleaned_comments,topK=100,withWeight=True)
# Generate a word cloud image
wordcloud =  WordCloud(font_path=r'C:\Users\kennedy\Desktop\jresults\ZCOOLKuaiLe-Regular.ttf',
                width = 3600, #width of the canvas.
                height = 2800, #height of the canvas.
                max_font_size = 580,
                max_words=1500,
                font_step = 1,
                background_color = "white",
                random_state = 42,
                margin = 2,
                )
wordcloud.fit_words(dict(words_df))
# Display the generated image using matplotlib:
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
