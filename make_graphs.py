"""file used to generate graphs from gathered data"""


import matplotlib.pyplot as plt
from collections import defaultdict

def evaluations_graph_families(filename):
	"""makes separate graphs for each family.
	reads data from a tsv file where each column is a language:
	row1 = language codes of data model was trained on
	row2 = codes of data model was tested on (unneeded here)
	row3 = word accuracies
	row4 = f scores
	row5 = reciprocal ranks
	row6 = mean avg precisions
	row7 = sizes in terms of # testing instances
	row8 = sizes by # training instances (unneeded here)
	rows 9, 10 unused
	row11 = language family
	"""
	f = open(filename, "r")
	data = f.readlines()
	langs = data[0].split("\t")[1:]
	word_acc = [float(i) for i in data[2].split("\t")[1:]]
	f_score = [float(i) for i in data[3].split("\t")[1:]]
	recip_rank = [float(i) for i in data[4].split("\t")[1:]]
	avg_prec = [float(i) for i in data[5].split("\t")[1:]]
	size = [int(i) for i in data[6].split("\t")[1:]]
	fams = [f for f in data[10].split("\t")[1:]]
	fam_map = {}
	# # group families
	for ind, fam in enumerate(fams):
		if fam not in fam_map:
			fam_map[fam] = [ind]
		else:
			fam_map[fam].append(ind)
	for family in fam_map:
		l = [langs[i] for i in fam_map[family]]
		d = [(word_acc[i], f_score[i], recip_rank[i], avg_prec[i], size[i]) for i in fam_map[family]]
		eval_graph_one_fam(l, d, "Accuracy Metrics for " + family + " Script Languages")


def eval_graph_one_fam(langs, data, name):
	"""Makes one graph for this family using list of langs, list of tuples of data, name of family.
	Data tuples are (word_acc, f_score, recip_rank, mean_avg_prec, test_size)"""
	word_acc = []
	f_s = []
	rec_rank = []
	avg_prec = []
	size = []
	for d in data:
		word_acc.append(d[0])
		f_s.append(d[1])
		rec_rank.append(d[2])
		avg_prec.append(d[3])
		size.append(d[4])
	plt.plot(range(len(langs)), word_acc, "ro", label="Word Accuracy")
	plt.plot(range(len(langs)), f_s, "bs", label="Mean F-Score")
	plt.plot(range(len(langs)), rec_rank, "g^", label="Mean Reciprocal Rank")
	plt.plot(range(len(langs)), avg_prec, "cD", label="Mean Average Precision")

	plt.xticks(range(len(langs)), langs, rotation="vertical")

	# plt.plot(range(len(langs)), word_acc, color=fam_list)
	for i in range(len(langs)):
		plt.annotate(size[i], xy=(i - 0.1, 1.0), xytext=(0, 0), textcoords="offset points", rotation="vertical")
	plt.annotate("Test", xy=(len(langs) - .2, 1.0), xytext=(0,0), textcoords="offset points")
	plt.annotate("Instances", xy=(len(langs) - .2, .96), xytext=(0,0), textcoords="offset points")


	plt.legend(loc="best", numpoints=1, fontsize=10)
	plt.axis([-1,len(langs)+5, 0, 1.1])
	ax = plt.axes()
	plt.title(name)

	plt.show()

def evaluations_graph_all(filename, name):
	"""Make one graph plotting all languages with the data points from file.
	File is formatted as tab-separated where first line is all lang codes, second line is data,
	third line is lang families."""
	f = open(filename, "r")
	data = f.readlines()
	langs = data[0].split("\t")[1:]
	word_acc = [float(i) for i in data[1].split("\t")[1:]]
	size_test = [int(i) for i in data[2].split("\t")[1:]]
	training = [int(i) for i in data[3].split("\t")[1:]]
	fams = [f for f in data[4].split("\t")[1:]]
	colors = "bgrcmyk"
	shapes = "oDs^"
	opts = [c + s for s in shapes for c in colors]
	fam_map = {}
	for ind, fam in enumerate(fams):
		if fam not in fam_map:
			fam_map[fam] = [ind]
		else:
			fam_map[fam].append(ind)
	# fam_list = [fam_map[fam] for fam in fams]

	print langs
	print word_acc
	print len(langs)
	print len(word_acc)

	for i, family in enumerate(fam_map.keys()):
		inds = fam_map[family]
		ys = [word_acc[n] for n in inds]
		sz = [training[n] for n in inds]
		plt.plot(sz, ys, opts[i], label=family)


	# plt.xticks(range(len(langs)), langs, rotation="vertical")

	# plt.plot(range(len(langs)), word_acc, color=fam_list)
	for i, lang in enumerate(langs):
		plt.annotate(lang, xy=(training[i], word_acc[i]), xytext=(0, 10), textcoords="offset points")
	plt.legend(loc="best", fontsize=10, numpoints=1)
	plt.axis([0,max(training) + 100, 0, 1.0])
	plt.xlabel("Number Training Instances")
	plt.ylabel("Performance")
	plt.title(name)
	plt.show()

def learning_curve_graph_all(filename):
	"""Makes one graph of learning curve for one language given in file.
	File format is tab-separated where each line contains:
	lang, word_acc, f-score, recip rank, mean avg prec, testing size, n best, percentage trained on"""
	f = open(filename, "r")
	percs = [line.split("\t") for line in f.readlines()]
	f.close()
	datas = {}
	for perc in percs:
		lang = perc[0]
		if lang not in datas:
			datas[lang] = defaultdict(list)
			datas[lang]["size"] = [int(perc[7])]
		datas[lang]["word_acc"].append(float(perc[2]))
		datas[lang]["f_score"].append(float(perc[3]))
		datas[lang]["recip"].append(float(perc[4]))
		datas[lang]["precision"].append(float(perc[5]))
		datas[lang]["xs"].append(int(perc[9]))
	
	for lang in datas.keys():
		d = datas[lang]
		name = lang + " Performance By Training Size" 
		learning_curve_graph_one(name, d["word_acc"], d["f_score"], d["recip"], d["precision"], d["xs"], d["size"][0])

def learning_curve_graph_one(name, word_acc, f_score, recip, precision, xs, size):
	"""plots one learning curve"""
	plt.plot(xs, word_acc, label="Word Accuracy")
	plt.plot(xs, f_score, label="Mean F-Score")
	plt.plot(xs, recip, label="Mean Reciprocal Rank")
	plt.plot(xs, precision, label="Mean Average Precision")
	plt.legend(loc="best", numpoints=1)
	plt.title(name)
	plt.xlabel("percentage of " + str(size) + " instances used in training")
	plt.ylabel("performance")
	plt.axis([10, 100, 0, 1.0])
	# plt.show()
	plt.savefig(name.split()[0] + "learningCurve.png")
	plt.show()


def cross_testing(filename):
	"""graphs all data in file, one graph for each model that was tested on multiple data sets
	file is structured like excel data sheet where lines contain one set of a data for a model/test set pair
	col1 is the lang code the model was trained on
	col2 is the lang code the model was tested on
	col3 unused (word acc)
	col4 is the f score
	col5 unused (recip rank)
	col6 is the mean avg precision
	col7 is the size in terms of # testing instances
	col8, col9 unused
	col10 is the percentage of data trained on (used to make sure we only store the correct
		pairs of data and not the learning curve data)"""
	f = open(filename, "r")
	lines = [l.split("\t") for l in f.readlines()]
	f.close()
	print len(lines)
	# # will store models and the results of testing on different languages
	# # ex [ab model][tested on fa] = (F-score, Avg Prec, Num Test Instances)
	trials = {}
	for line in lines:
		tested_on = line[1]
		model = line[0]
		if len(line) >= 10:
			if line[9].strip() in ["10", "20", "30", "40", "50", "60", "70", "80", "90"]:
				continue
		if model not in trials:
			trials[model] = {tested_on:(float(line[3]), float(line[5]), int(line[6]))}
		else:
			trials[model][tested_on] = (float(line[3]), float(line[5]), int(line[6]))
	for mod in trials:
		if len(trials[mod]) > 1:
			graph_cross_testing(mod, trials)
	# # this sort of code can be used to only graph one specific model's results
	# graph_cross_testing("bigs", trials)
	# graph_cross_testing("ar", trials)


def graph_cross_testing(mod, trials):
	"""makes one graph using the trials dictionary of trials[trained_on][tested_on]
	using the specific lang code for trained_on passed in as mod"""
	tests = trials[mod].keys()
	test_inst = [trials[test][test][2] for test in tests]
	labelling = sorted([(test_inst[i], i) for i in range(len(test_inst))])
	fs_mod = [trials[mod][test][0] for test in tests]
	map_mod = [trials[mod][test][1] for test in tests]
	fs_self = [trials[test][test][0] for test in tests]
	map_self = [trials[test][test][1] for test in tests]

	from_mod_fs = [fs_mod[labelling[i][1]] for i in range(len(fs_mod))]
	from_mod_map = [map_mod[labelling[i][1]] for i in range(len(fs_mod))]
	from_self_fs = [fs_self[labelling[i][1]] for i in range(len(fs_mod))]
	from_self_map = [map_self[labelling[i][1]] for i in range(len(fs_mod))]

	plt.plot(range(len(tests)), from_self_fs, "g^", label="Mean F-Score Trained on Self")
	plt.plot(range(len(tests)), from_mod_fs, "ro", label="Mean F-Score Trained on " + mod)
	plt.plot(range(len(tests)), from_self_map, "cD", label="Mean Average Precision Trained on Self")
	plt.plot(range(len(tests)), from_mod_map, "bs", label="Mean Average Precision Trained on " + mod)

	# # use these instead for graphing models supplemented with Bigs LM vs original training-corpus-only LM
	# plt.plot(range(len(tests)), from_self_fs, "g^", label="Mean F-Score")
	# plt.plot(range(len(tests)), from_mod_fs, "ro", label="Mean F-Score Trained Using Bigs LM")
	# plt.plot(range(len(tests)), from_self_map, "cD", label="Mean Average Precision")
	# plt.plot(range(len(tests)), from_mod_map, "bs", label="Mean Average Precision Trained Using Bigs LM")


	plt.xticks(range(len(test_inst)), [tests[labelling[i][1]] for i in range(len(tests))])
	for i, t in enumerate(labelling):
		plt.annotate(t[0], xy=(i - .1, 1.0), xytext=(0, 0), textcoords="offset points", rotation="vertical")

	plt.annotate("Test", xy=(len(tests) - .2, 1.0), xytext=(0,0), textcoords="offset points")
	plt.annotate("Instances", xy=(len(tests) - .2, .96), xytext=(0,0), textcoords="offset points")

	plt.legend(loc="lower right", numpoints=1, fontsize=10)
	plt.axis([-1,len(tests)+1, 0, 1.1])
	plt.xlabel("Test Language By Data Set Size")
	plt.ylabel("Performance")
	plt.title("Testing " + mod + " Model on Other Languages")

	# # title for Bigs LM graph instead
	# plt.title("Effect of Incorporating Bigger Target Language Model")
	plt.show()


if __name__ == '__main__':
	# evaluations_graph_all("full_models_word_acc.tsv", "Word Accuracy of Fully Trained Models By Script Family")
	# evaluations_graph_all("full_models_f_score.tsv", "Mean F-Score of Fully Trained Models By Script Family")
	# evaluations_graph_all("full_models_recip_rank.tsv", "Mean Reciprocal Rank of Fully Trained Models By Script Family")
	# evaluations_graph_all("full_models_mean_avg_prec.tsv", "Mean Average Precision of Fully Trained Models By Script Family")
	# evaluations_graph_families("full_models_all_evals.tsv")
	# evaluations_graph_families("data_full.tsv")
	# learning_curve_graph("ab_learning.tsv", "Ab Learning Curve")
	# learning_curve_graph_all("all_data_learning_curve.tsv")
	# cross_testing("all_data.tsv")