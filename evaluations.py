"""file to produce tables of evaluation data
calculated using the top n output files in the testing directories
evaluated against the target language testing data in the input directory"""

from Levenshtein import *
from collections import defaultdict

def get_word_accuracy(reference, predictions):
	"""returns whether the first best output is the same as the reference translation"""
	if reference == predictions[0]:
		return True
	return False

def get_f_score(reference, predictions):
	"""returns the f score of the top prediction based on levenshtein edit distance.
	Spaces that were included during training and testing are removed in
	the f-score calculation to reduce padded correct characters"""
	ref = reference.replace(" ", "")
	pred = predictions[0].replace(" ", "")
	# # calculate Longest Common Subsequence
	LCS = .5 * (len(ref) + len(pred) - distance(ref, pred))
	precision = LCS / len(ref)
	recall = LCS / len(pred)
	return 2.0 * precision * recall / (precision + recall)

def get_reciprocal_rank(reference, predictions):
	"""Find the rank of the first accurate prediction, return 1 / rank
	If no prediction matches reference, return 0"""
	for i, pred in enumerate(predictions):
		if pred == reference:
			return 1.0 / (i + 1)
	return 0.0

def get_average_precision(reference, predictions):
	"""returns the average precision which allows higher ranked predictions
	to have more influence on the precision."""
	correct = 0
	to_sum = []
	for i, pred in enumerate(predictions):
		if pred == reference:
			correct += 1
		to_sum.append(correct)
	return sum(to_sum) * 1.0 / len(to_sum)

def get_all_evaluations(reference_file, prediction_file):
	"""takes in the reference file and n-best prediction file in the n-best output format:
	0 ||| O u t p u t...
	where the first element is the corresponding reference number.
	Returns a tuple of evaluation metrics:
	(Word Accuracy, Mean F-score, Mean Reciprocal Rank, Mean Average Precision, Number Inputs, Target Number Outputs per Input)"""
	# # read data from files
	ref_f = open(reference_file, "r")
	references = ref_f.readlines()
	ref_f.close()
	pred_f = open(prediction_file, "r")
	all_predictions = pred_f.readlines()
	pred_f.close()

	preds = defaultdict(list)
	for pred in all_predictions:
		# # put all predictions into dictionary by corresponding reference
		info = pred.split("|||")
		preds[int(info[0])].append(info[1].strip())


	# # loop through all references with the n best predictions and get metrics
	sum_word_acc = 0.0
	sum_f_scores = 0.0
	sum_recip_ranks = 0.0
	sum_avg_precision = 0.0
	for ind, ref in enumerate(references):
		# # get corresponding predictions
		ps = preds[ind]
		r = ref.strip()
		sum_word_acc += get_word_accuracy(r, ps)
		sum_f_scores += get_f_score(r, ps)
		sum_recip_ranks += get_reciprocal_rank(r, ps)
		sum_avg_precision += get_average_precision(r, ps)
	# # calculate averages and return
	n = len(references)
	n_best = max([len(p) for p in preds.values()])
	return (sum_word_acc / n, sum_f_scores / n, sum_recip_ranks / n, sum_avg_precision / n, n, n_best)

def generate_eval_table(models_dir, langs):
	"""for each language code in the given langs, gets all evaluations and outputs to a csv:
	lang, word accuracy, mean F-score, mean reciprocal rank, mean average precision, number inputs, target number outputs per input"""
	out = open(models_dir[-2] + "_eval_table.csv", "w")
	for lang in langs:
		parent_dir = models_dir + "/"
		# parent_dir = "models/"
		ref_f = parent_dir + lang + "-en/input/test." + lang + "-en.en"
		pred_f = parent_dir + lang + "-en/test/output.top_100"
		# pred_f = "output.top_100"
		info = get_all_evaluations(ref_f, pred_f)
		out.write(lang + ",")
		for i, piece in enumerate(info):
			out.write(str(piece))
			if i < len(info) - 1:
				out.write(",")
			else:
				out.write("\n")

	out.close()

def generate_eval_table_all_cross(models_dir, model_tests_dict):
	"""takes the given dictionary of model run to language tested (ex {ar:[arz, ko, iu]}and produces a csv:
	modellang, testang, word accuracy, mean F-score, mean reciprocal rank, mean average precision, number inputs, target number outputs per input"""
	out = open("families_test_evals.csv", "w")
	for lang in model_tests_dict:
		for targ in model_tests_dict[lang]:
			parent_dir = models_dir + "/"
			ref_f = parent_dir + targ + "-en/input/test." + targ + "-en.en"
			pred_f = parent_dir + lang + "-en/test/on-all/" + targ + "_output.top_100"
			info = get_all_evaluations(ref_f, pred_f)
			out.write(lang + "," + targ + ",")
			for i, piece in enumerate(info):
				out.write(str(piece))
				if i < len(info) - 1:
					out.write(",")
				else:
					out.write("\n")
	out.close()

def my_cross_tests():
	"""generates eval table for models that I ran on certain languages
	the dictionary being passed into the method below maps the larger or multi-language model code
	to the list of language codes that should be tested using that model"""
	d = {}
	# # testing top 7 single language models on multiple languages
	# d["ar"] = ['ab', 'am', 'arz', 'assm', 'av', 'az', 'ba', 'be', 'be-x-old', 'bg', 'bh', 'bn', 'bo', 'ce', 'ckb', 'cv', 'el', 'fa', 'gan', 'he', 'hi', 'hy', 'iu', 'ja', 'ka', 'kk', 'km', 'kn', 'ko', 'ks', 'ky', 'lo', 'mhr', 'mk', 'ml', 'mn', 'mr', 'my', 'myv', 'mzn', 'ne', 'new', 'or', 'os', 'pa', 'pnb', 'ps', 'ru', 'rue', 'sa', 'sah', 'si', 'sr', 'ta', 'te', 'tg', 'th', 'tt', 'ug', 'uk', 'ur', 'wuu', 'xmf', 'yi', 'zh', 'zh-yue']
	# d["fa"] = ['ar', 'arz', 'ckb', 'hy', 'he', 'ka', 'kn', 'ks', 'my', 'mzn', 'or', 'pa', 'pnb', 'ps', 'si', 'ta', 'te', 'ug', 'ur', 'xmf', 'yi']
	# d["ja"] = ['bo', 'gan', 'kn', 'ko', 'lo', 'or', 'si', 'ta', 'te', 'th', 'wuu', 'zh', 'zh-yue']
	# d["ko"] = ['bo', 'gan', 'ja', 'kn', 'lo', 'or', 'si', 'ta', 'te', 'th', 'wuu', 'zh', 'zh-yue']
	# d["ru"] = ['ab', 'av', 'ba', 'be', 'be-x-old', 'bg', 'ce', 'cv', 'el', 'hy', 'ka', 'kk', 'kn', 'ky', 'mhr', 'mk', 'mn', 'my', 'myv', 'or', 'os', 'rue', 'sah', 'si', 'sr', 'ta', 'te', 'tg', 'tt', 'uk']
	# d["uk"] = ['ab', 'av', 'ba', 'be', 'be-x-old', 'bg', 'ce', 'cv', 'el', 'hy', 'ka', 'kk', 'kn', 'ky', 'mhr', 'mk', 'mn', 'my', 'myv', 'or', 'os', 'ru', 'rue', 'sah', 'si', 'sr', 'ta', 'te', 'tg', 'tt']
	# d["zh"] = ['bo', 'gan', 'iu', 'km', 'kn', 'lo', 'or', 'si', 'ta', 'te', 'th', 'wuu', 'zh-yue']
	# d["bigs"] = ['ab', 'am', 'ar', 'arz', 'assm', 'av', 'az', 'ba', 'be', 'be-x-old', 'bg', 'bh', 'bn', 'bo', 'ce', 'ckb', 'cv', 'el', 'fa', 'gan', 'he', 'hi', 'hy', 'iu', 'ja', 'ka', 'kk', 'km', 'kn', 'ko', 'ks', 'ky', 'lo', 'mhr', 'mk', 'ml', 'mn', 'mr', 'my', 'myv', 'mzn', 'ne', 'new', 'or', 'os', 'pa', 'pnb', 'ps', 'ru', 'rue', 'sa', 'sah', 'si', 'sr', 'ta', 'te', 'tg', 'th', 'tt', 'ug', 'uk', 'ur', 'wuu', 'xmf', 'yi', 'zh', 'zh-yue']
	
	# # testing models trained on combined language families on languages within that family
	d["arab"] = ["ar", "arz", "ps", "ug"]
	d["beng"] = ["assm", "bn"]
	d["chin"] = ["gan", "wuu", "zh", "zh-yue"]
	d["deva"] = ["bh", "mr", "new", "hi", "ne", "sa"]
	d["georg"] = ["ka", "xmf"]
	d["hebr"] = ["he", "yi"]
	d["pers"] = ["ckb", "fa", "ks", "pnb", "ur"]
	generate_eval_table_all_cross("/nlp/users/tbreiner/models", d)

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

def generate_counts_table(langs):
	"""generates a csv containing each language and the counts of training, tuning, and testing instances"""
	f_data = open("data_counts.csv", "w")
	f_data.write("language,#training,#tuning,#testing\n")
	for lang in langs:
		data = count_inputs(lang)
		f_data.write(lang + "," + str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "\n")
	f_data.close()


# langs = ['ab', 'am', 'ar', 'arz', 'assm', 'av', 'az', 'ba', 'be', 'be-x-old', 'bg', 'bh', 'bn', 'bo', 'ce', 'ckb', 'cv', 'el', 'fa', 'gan', 'he', 'hi', 'hy', 'iu', 'ja', 'ka', 'kk', 'km', 'kn', 'ko', 'ks', 'ky', 'lo', 'mhr', 'mk', 'ml', 'mn', 'mr', 'my', 'myv', 'mzn', 'ne', 'new', 'or', 'os', 'pa', 'pnb', 'ps', 'ru', 'rue', 'sa', 'sah', 'si', 'sr', 'ta', 'te', 'tg', 'th', 'tt', 'ug', 'uk', 'ur', 'wuu', 'xmf', 'yi', 'zh', 'zh-yue']
# generate_counts_table(langs)

# langs = ['ab', 'am', 'ar', 'arz', 'assm', 'av', 'az', 'ba', 'be', 'be-x-old', 'bg', 'bh', 'bn', 'bo']#, 'ce', 'ckb', 'cv', 'el', 'fa', 'gan', 'he', 'hi', 'hy', 'iu', 'ja', 'ka', 'kk', 'km', 'kn', 'ko', 'ks', 'ky', 'lo', 'mhr', 'mk', 'ml', 'mn', 'mr', 'my', 'myv', 'mzn', 'ne', 'new', 'or', 'os', 'pa', 'pnb', 'ps', 'ru', 'rue', 'sa', 'sah', 'si', 'sr', 'ta', 'te', 'tg', 'th', 'tt', 'ug', 'uk', 'ur', 'wuu', 'xmf', 'yi', 'zh', 'zh-yue']
# for mod in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
	# generate_eval_table("/nlp/users/tbreiner/models_" + str(mod), langs)
# print get_all_evaluations("models/ab-en/input/test.ab-en.en", "output.top_100")

# my_cross_tests()