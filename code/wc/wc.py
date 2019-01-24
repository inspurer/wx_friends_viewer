import matplotlib.pyplot as plt
import jieba
from scipy.misc import imread
from wordcloud import WordCloud


def importStopword(filename=''):
	stopwords = {}
	f = open(filename, 'r', encoding='utf-8')
	line = f.readline().rstrip()
	while line:
		stopwords.setdefault(line, 0)
		stopwords[line] = 1
		line = f.readline().rstrip()
	f.close()
	return stopwords


def processChinese(text, stopwords):
	seg_generator = jieba.cut(text)
	seg_list = [i for i in seg_generator if i not in stopwords]
	seg_list = [i for i in seg_list if i != u' ']
	seg_list = r' '.join(seg_list)
	return seg_list

def painter():
	text = open('sign.txt', encoding="utf-8").read()

	stopwords = importStopword(filename='./StopWords.txt')
	text = processChinese(text, stopwords)
	back_colorimg = imread("./image/bc.png")
	WC = WordCloud(
		font_path='./fonts/4.ttf',
		background_color="#ffffff",
		max_words=2000,
		mask=back_colorimg,
		random_state=42
	)
	WC.generate(text)
	plt.figure('Sign')
	plt.imshow(WC)
	plt.axis("off")
	plt.show()
	WC.to_file("sign.png")

if __name__ == '__main__':
	painter()