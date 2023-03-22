import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import numpy as np
from pathlib import Path
from PIL import Image
import pymorphy2
import string
import wordcloud
from wordcloud import WordCloud, ImageColorGenerator

def remove_chars_from_text(text, chars):
    return "".join([ch for ch in text if ch not in chars])
#tokenize  ==  text_tokens = word_tokenize(text)
def lemmatize(text):
    words = text.split() # разбиваем текст на слова
    res = []
    
    for word in words:
        p = morph.parse(word)[0]
        res.append(p.normal_form)       

    return res

morph = pymorphy2.MorphAnalyzer()


text = open('test_text.txt',encoding='utf-8')
text = text.read()
#text.close()

text = text.lower()
spec_chars = string.punctuation + '\n\xa0«»\t—…'
text = remove_chars_from_text(text, spec_chars)
text = remove_chars_from_text(text, string.digits)

russian_stopwords = stopwords.words("russian")
text = lemmatize(text) # list
result = [word for word in text if word not in russian_stopwords]


fdist = FreqDist(result)


common_wrd = fdist.most_common() 

current_directory = Path.cwd()

python_mask = np.array(Image.open(current_directory/"mask.png"))

wordcloud = WordCloud(background_color='white', mask=python_mask, max_words = 500, 
                        width = 600, height = 300)

wordcloud.generate_from_frequencies(dict(common_wrd)) #dict

image_colors = ImageColorGenerator(python_mask)
# show
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig('Python_mask_cloud.png')
plt.show()
 