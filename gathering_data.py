
def count_inputs(lang):
	"returns the number of training instances, number of tuning, and number of testing as a tuple"
	f_train = open("models/" + lang + "-en/input/train." + lang + "-en.en", "r")
	training = f_train.readlines()
	f_train.close()
	f_tune = open("models/" + lang + "-en/input/tune." + lang + "-en.en", "r")
	tuning = f_tune.readlines()
	f_tune.close()
	f_test = open("models/" + lang + "-en/input/test." + lang + "-en.en", "r")
	testing = f_test.readlines()
	f_test.close()
	return (len(training), len(tuning), len(testing))


langs = ['ab', 'am', 'ar', 'arz', 'assm', 'av', 'az', 'ba', 'be', 'be-x-old', 'bg', 'bh', 'bn', 'bo', 'ce', 'ckb', 'cv', 'el', 'fa', 'gan', 'he', 'hi', 'hy', 'iu', 'ja', 'ka', 'kk', 'km', 'kn', 'ko', 'ks', 'ky', 'lo', 'mhr', 'mk', 'ml', 'mn', 'mr', 'my', 'myv', 'mzn', 'ne', 'new', 'or', 'os', 'pa', 'pnb', 'ps', 'ru', 'rue', 'sa', 'sah', 'si', 'sr', 'ta', 'te', 'tg', 'th', 'tt', 'ug', 'uk', 'ur', 'wuu', 'xmf', 'yi', 'zh', 'zh-yue']

f_data = open("data_counts.csv", "w")
for lang in langs:
	data = count_inputs(lang)
	f_data.write(lang + "," + str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "\n")
f_data.close()