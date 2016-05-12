""" file to do train tune test split, create the three new files in each language directory"""
import random
import subprocess

# # set path to directory containing data files and where new directories, one per language, will be
root = "../original_columns/"

# # list of language codes that will serve as the model names
# # example ab-en directory will contain data sets of ab data and en data
langs = ['ab', 'am', 'ar', 'arc', 'arz', 'assm', 'av', 'az', 'ba', 'be', 'be-x-old', 'bg', 'bh', 'bn', 'bo', 'ce', 'ckb', 'cv', 'dv', 'el', 'fa', 'gan', 'got', 'he', 'hi', 'hy', 'iu', 'ja', 'ka', 'kk', 'km', 'kn', 'ko', 'ks', 'ky', 'lo', 'mhr', 'mk', 'ml', 'mn', 'mr', 'my', 'myv', 'mzn', 'ne', 'new', 'or', 'os', 'pa', 'pnb', 'ps', 'ru', 'rue', 'sa', 'sah', 'si', 'sr', 'ta', 'te', 'tg', 'th', 'tt', 'ug', 'uk', 'ur', 'wuu', 'xmf', 'yi', 'zh', 'zh-yue']

targs = langs

def split_up(source_lang_code, target_lang_code):

	# # ex: ar-en, will be name of directory and files such as train.ar-en.en, tune.ar-en.ar
	together_code = source_lang_code + "-" + target_lang_code

	# # first time run can use this command to make the directory first
	# subprocess.call("mkdir " + together_code, shell=True)

	f = open(root + together_code + "." + target_lang_code, "r")
	target = f.readlines()
	f.close()

	f = open(root + together_code + "." + source_lang_code, "r")
	source = f.readlines()
	if len(source[-1]) ==0:
		source = source[:-1]
	f.close()

	together = list(zip(source, target))

	random.shuffle(together)

	# # check if 10% of data is greater than 2000 examples
	# # limit test to last 2000 and tune to 2000 before that if so
	if .1 * len(together) > 2000:
		cut1 = len(together) - 4000
		cut2 = len(together) - 2000
	else:
		cut1 = int(len(together) * .8)
		cut2 = int(len(together) * .9)
	train = together[:cut1]
	tune = together[cut1:cut2]
	test = together[cut2:]

	# # add input to the path
	full_path = together_code + "/input"

	source_train = open(full_path + "/train." + together_code + "." + source_lang_code, "w")
	target_train = open(full_path + "/train." + together_code + "." + target_lang_code, "w")

	for a, b in train:
		source_train.write(a)
		target_train.write(b)

	source_train.close()
	target_train.close()

	source_tune = open(full_path + "/tune." + together_code + "." + source_lang_code, "w")
	target_tune = open(full_path + "/tune." + together_code + "." + target_lang_code, "w")

	for a, b in tune:
		source_tune.write(a)
		target_tune.write(b)

	source_tune.close()
	target_tune.close()

	source_test = open(full_path + "/test." + together_code + "." + source_lang_code, "w")
	target_test = open(full_path + "/test." + together_code + "." + target_lang_code, "w")

	for a, b in test:
		source_test.write(a)
		target_test.write(b)

	source_test.close()
	target_test.close()

############################# main ###################

# # split up every language's data
for targ in targs:
	split_up(targ, "en")

# for targ in targs:
	# subprocess.call("mkdir " + targ + "-en/input", shell=True)
	# subprocess.call("mv " + targ + "-en/*.* " + targ + "-en/input/", shell=True)

