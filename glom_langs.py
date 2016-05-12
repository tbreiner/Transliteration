"""script to merge certain sets of data together to train bigger models"""

# # set the root directory where the language directories will be found
# # include the final / in the path
root_dir = "models/"

# # what the new glommed set should be called
glom_name = "pers"

# # defining certain sets of names to glom together
# # all langs
# langs = ['ab', 'am', 'ar', 'arz', 'assm', 'av', 'az', 'ba', 'be', 'be-x-old', 'bg', 'bh', 'bn', 'bo', 'ce', 'ckb', 'cv', 'el', 'fa', 'gan', 'he', 'hi', 'hy', 'iu', 'ja', 'ka', 'kk', 'km', 'kn', 'ko', 'ks', 'ky', 'lo', 'mhr', 'mk', 'ml', 'mn', 'mr', 'my', 'myv', 'mzn', 'ne', 'new', 'or', 'os', 'pa', 'pnb', 'ps', 'ru', 'rue', 'sa', 'sah', 'si', 'sr', 'ta', 'te', 'tg', 'th', 'tt', 'ug', 'uk', 'ur', 'wuu', 'xmf', 'yi', 'zh', 'zh-yue']

# # big langs
# langs = ["ar", "fa", "ja", "ko", "ru", "uk", "zh"]
# # chinese langs
# langs = ["gan", "wuu", "zh", "zh-yue"]
# # arabic langs
# langs = ["ar", "arz", "ps", "ug"]
# # bengali langs
# langs = ["assm", "bn"]
# # cyrillic langs
# langs = ["ab", "av", "ba", "be", "be-x-old", "bg", "ce", "cv", "kk", "ky", "mhr", "mk", "mn", "myv", "os", "ru", "rue", "sah", "sr", "tg", "tt", "uk"]
# # devanagari langs
# langs = ["bh", "hi", "mr", "ne", "new", "sa"]
# # georgian langs
# langs = ["ka", "xmf"]
# # hebrew langs
# langs = ["he", "yi"]
# # perso-arabic langs
langs = ["ckb", "fa", "ks", "pnb", "ur"]

def move_data(from_filename, to_f):
	"""moves all data from one file to the other"""
	f = open(from_filename, "r")
	lines = f.readlines()
	f.close()
	for line in lines:
		to_f.write(line)


# # training data files
f1_en = open(root_dir + glom_name + "-en/input/train." + glom_name + "-en.en", "w")
f1_all = open(root_dir + glom_name + "-en/input/train." + glom_name + "-en." + glom_name, "w")

# # tuning data files
f2_en = open(root_dir + glom_name + "-en/input/tune." + glom_name + "-en.en", "w")
f2_all = open(root_dir + glom_name + "-en/input/tune." + glom_name + "-en." + glom_name, "w")

# # testing data files
f3_en = open(root_dir + glom_name + "-en/input/test." + glom_name + "-en.en", "w")
f3_all = open(root_dir + glom_name + "-en/input/test." + glom_name + "-en." + glom_name, "w")

# # move everything into new files
for lang in langs:
	move_data(root_dir + lang + "-en/input/train." + lang + "-en.en", f1_en)
	move_data(root_dir + lang + "-en/input/train." + lang + "-en." + lang, f1_all)
	move_data(root_dir + lang + "-en/input/tune." + lang + "-en.en", f2_en)
	move_data(root_dir + lang + "-en/input/tune." + lang + "-en." + lang, f2_all)
	move_data(root_dir + lang + "-en/input/test." + lang + "-en.en", f3_en)
	move_data(root_dir + lang + "-en/input/test." + lang + "-en." + lang, f3_all)

f1_en.close()
f1_all.close()
f2_en.close()
f2_all.close()
f3_en.close()
f3_all.close()