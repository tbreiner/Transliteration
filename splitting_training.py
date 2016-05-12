"""code to split up training data for training smaller models on each set to produce learning curves
should be run after already running copy_tune_test_inputs.sh"""

root = "/nlp/users/tbreiner/models/"

def create_train_split_files(source, target):
	"""takes the full training data from the given language and creates new training files 
	based on the first 10%, first 20% ... first 90% of the training data. Places these new files
	in the correct directory, ie models_40/ar-en/input/train.ar-en.ar
	This script should be run after copy_tune_test_inputs.sh which will have created the percentage directories."""
	f = open(root + source + "-" + target + "/input/train." + source + "-" + target + "." + source, "r")
	source_data = f.readlines()
	f.close()
	f = open(root + source + "-" + target + "/input/train." + source + "-" + target + "." + target, "r")
	target_data = f.readlines()
	f.close()
	total = len(target_data)
	# for cutoff in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
	for cutoff in [10]:
		f_perc_source = open(root + "models_" + str(cutoff) + "/" + source + "-" + target + "/input/train." + source + "-" + target + "." + source, "w")
		f_perc_target = open(root + "models_" + str(cutoff) + "/" + source + "-" + target + "/input/train." + source + "-" + target + "." + target, "w")
		for line in xrange(int(total * cutoff / 100.0)):
			f_perc_source.write(source_data[line])
			f_perc_target.write(target_data[line])
		f_perc_source.close()
		f_perc_target.close()


# langs = ['ab', 'am', 'ar', 'arz', 'assm', 'av', 'az', 'ba', 'be', 'be-x-old', 'bg', 'bh', 'bn', 'bo', 'ce', 'ckb', 'cv', 'el', 'fa', 'gan', 'he', 'hi', 'hy', 'iu', 'ja', 'ka', 'kk', 'km', 'kn', 'ko', 'ks', 'ky', 'lo', 'mhr', 'mk', 'ml', 'mn', 'mr', 'my', 'myv', 'mzn', 'ne', 'new', 'or', 'os', 'pa', 'pnb', 'ps', 'ru', 'rue', 'sa', 'sah', 'si', 'sr', 'ta', 'te', 'tg', 'th', 'tt', 'ug', 'uk', 'ur', 'wuu', 'xmf', 'yi', 'zh', 'zh-yue']
langs = ["ab"]
for lang in langs:
	create_train_split_files(lang, "en")