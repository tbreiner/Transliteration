"""file to preprocess the language data by first changing spaces to underscores
then adding a space between every unicode character
input filename is of the format ar.ar or ar.en
writes output to a new file with name format ar-en.ar or ar-en.en"""

import codecs

# # set directories for where raw data is and where new files should be saved
raw_data_dir = "lang_files/unprocessed/"
processed_data_dir = "lang_files/"

# # list of language codes
langs = ['ab', 'am', 'ar', 'arc', 'arz', 'assm', 'av', 'az', 'ba', 'be', 'be-x-old', 'bg', 'bh', 'bn', 'bo', 'ce', 'ckb', 'cv', 'dv', 'el', 'fa', 'gan', 'got', 'he', 'hi', 'hy', 'iu', 'ja', 'ka', 'kk', 'km', 'kn', 'ko', 'ks', 'ky', 'lo', 'mhr', 'mk', 'ml', 'mn', 'mr', 'my', 'myv', 'mzn', 'ne', 'new', 'or', 'os', 'pa', 'pnb', 'ps', 'ru', 'rue', 'sa', 'sah', 'si', 'sr', 'ta', 'te', 'tg', 'th', 'tt', 'ug', 'uk', 'ur', 'wuu', 'xmf', 'yi', 'zh', 'zh-yue']

targs = langs

def preprocess(lang, ext):
	"""takes the (nonenglish) source language of the pair
	and the ext representing the language of the document
	ex: ar, ar will be for the arabic set, arabic data
	ar, en will be for the arabic set, english data.
	Writes preprocessed data to a new file with name ex: ar-en.en or ar-en.ar
	Preprocesses data by changing spaces to underscores and then inserting space
	between every unicode character"""

	filename = raw_data_dir + lang + "." + ext
	new_filename = processed_data_dir + lang + "-en." + ext
	f = open(filename, "r")
	lines = f.readlines()[1:]
	f.close()
	# can i specify file encoding during opening?
	f = open(new_filename, "w")
	for line in lines:
		line = line.decode("utf-8")
		line = line.replace(u" ", u"_")
		chars = [(ch + u" ").encode("utf-8") for ch in line[:-1]]
		for ch in chars:
			f.write(ch)
		f.write("\n")
	f.close()

################## MAIN CODE ##################

# # preprocess every language's data
for targ in targs:
	preprocess(targ, targ)
 	preprocess(targ, "en")

# preprocess("ar", "en")
# preprocess("ar", "ar")
# preprocess("zh-yue", "zh-yue")

# data = [line.decode("utf-16", "replace") for line in file]