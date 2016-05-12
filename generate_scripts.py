#!/usr/bin/python
#$ -S /usr/bin/python
# other OGS/SGE options go here, each line beginning with #$
#$ -v JOSHUA=/nlp/users/tbreiner/joshua-6.0.5
#$ -v JAVA_HOME=/usr/lib64/jvm/java

"""file for producing runnable bash scripts in multiple directories at once
can produce scripts that will build models, bundle models, and get n best outputs of models on testing data"""

# # set the path to the supplementary language model that can be used when running joshua
# # for example this one is the one trained on the top 7 languages when training the bigs model
# # used in lm-lang-en models to see if low resource languages can get a boost from a larger LM during training
lm_path = "/nlp/users/tbreiner/models/bigs-en/lm.gz"

def generate_builder(source_lang, target_lang):
	"""joshua command for building model including a language model from training data"""
	return "/nlp/users/tbreiner/joshua-6.0.5/bin/pipeline.pl --source " + source_lang + " \
	--target " + target_lang + " \
	--type hiero \
	--no-prepare --aligner berkeley \
	--corpus input/train." + source_lang + "-" + target_lang + " \
	--tune input/tune." + source_lang + "-" + target_lang + " \
	--test input/test." + source_lang + "-" + target_lang + " \
	--lm-gen berkeleylm"

def gen_with_LM(source_lang, target_lang, lm_path):
	"""joshua command for building model using an existing language model at lm_path"""
	return "/nlp/users/tbreiner/joshua-6.0.5/bin/pipeline.pl --source " + source_lang + " \
	--target " + target_lang + " \
	--type hiero \
	--no-prepare --aligner berkeley \
	--corpus input/train." + source_lang + "-" + target_lang + " \
	--tune input/tune." + source_lang + "-" + target_lang + " \
	--test input/test." + source_lang + "-" + target_lang + " \
	--lmfile " + lm_path


def create_indiv_build_script(models_dir, source_lang, target_lang, use_big_LM=False):
	"""In given models dir, creates build script within correct language directory to run builder.
	If use_big_LM is True then then the model will be trained using the LM provided at the path saved at top of this file"""
	f = open(models_dir + "/" + source_lang + "-" + target_lang + "/" + source_lang + "_build_script.sh", "w")
	if use_big_LM:
		builder = gen_with_LM(source_lang, target_lang, lm_path)
	else:
		builder = generate_builder(source_lang, target_lang)
	f.write("#!/bin/bash\n")
	f.write("#$ -v JOSHUA=/nlp/users/tbreiner/joshua-6.0.5\n")
	f.write("#$ -v JAVA_HOME=/usr/lib64/jvm/java\n")
	f.write(builder + "\n")
	f.close()

def generate_bundler(source, targ):
	"""fills in correct options to bundler"""
	bundler = "$JOSHUA/scripts/support/run_bundler.py \
		tune/joshua.config.final \
		language-pack-" + source + "-" + targ + " \
		--pack-tm grammar.gz"
	return bundler

def create_indiv_bundler(models_dir, source_lang, target_lang):
	"""In given models dir, creates bundler script within correct language directory to run bundler"""
	bundler = generate_bundler(source_lang, target_lang)
	f = open(models_dir + "/" + source_lang + "-" + target_lang + "/" + source_lang + "_bundler_script.sh", "w")
	f.write("#!/bin/bash\n")
	f.write("#$ -v JOSHUA=/nlp/users/tbreiner/joshua-6.0.5\n")
	f.write("#$ -v JAVA_HOME=/usr/lib64/jvm/java\n")
	f.write(bundler + "\n")
	f.close()


def create_top_n_runner(models_dir, source_lang, target_lang, top_n=100):
	"""creates script to run test input through joshua decoder producing top_n output
	in a file named output.top_100 for example, within the test directory. The script will be saved
	within the language pack directory."""
	f = open(models_dir + "/" + source_lang + "-" + target_lang + "/language-pack-" + source_lang + "-" + target_lang + "/top_n_" + source_lang + ".sh", "w")
	f.write("#!/bin/bash\n")
	f.write("#$ -v JOSHUA=/nlp/users/tbreiner/joshua-6.0.5\n")
	f.write("#$ -v JAVA_HOME=/usr/lib64/jvm/java\n")
	f.write("cat ../input/test." + source_lang + "-" + target_lang + "." + source_lang + " | run-joshua.sh -m 3100m -threads 1 -top-n " + str(top_n) + " -output-format \"%i ||| %s ||| %f ||| %c\" > ../test/output.top_" + str(top_n))
	f.close()

def create_cross_top_n_runner(models_dir, source_lang, test_lang, top_n=100):
	"""creates script to run test input through joshua decoder producing top_n output
	in a file named output.top_100 for example, within the test directory. The script will be saved
	within the language pack directory."""
	f = open(models_dir + "/" + source_lang + "-en/language-pack-" + source_lang + "-en/" + source_lang + "_" + test_lang + "_test.sh", "w")
	f.write("#!/bin/bash\n")
	f.write("#$ -v JOSHUA=/nlp/users/tbreiner/joshua-6.0.5\n")
	f.write("#$ -v JAVA_HOME=/usr/lib64/jvm/java\n")
	f.write("cat " + models_dir + "/" + test_lang + "-en/input/test." + test_lang + "-en." + test_lang + " | run-joshua.sh -m 3100m -threads 1 -top-n " + str(top_n) + " -output-format \"%i ||| %s ||| %f ||| %c\" > ../test/on-all/" + test_lang + "_output.top_" + str(top_n))
	f.close()


############# MAIN CODE #############

# # all langs
langs = ['ab', 'am', 'ar', 'arz', 'assm', 'av', 'az', 'ba', 'be', 'be-x-old', 'bg', 'bh', 'bn', 'bo', 'ce', 'ckb', 'cv', 'el', 'fa', 'gan', 'he', 'hi', 'hy', 'iu', 'ja', 'ka', 'kk', 'km', 'kn', 'ko', 'ks', 'ky', 'lo', 'mhr', 'mk', 'ml', 'mn', 'mr', 'my', 'myv', 'mzn', 'ne', 'new', 'or', 'os', 'pa', 'pnb', 'ps', 'ru', 'rue', 'sa', 'sah', 'si', 'sr', 'ta', 'te', 'tg', 'th', 'tt', 'ug', 'uk', 'ur', 'wuu', 'xmf', 'yi', 'zh', 'zh-yue']

# langs = ['av', 'az', 'ba', 'be', 'be-x-old', 'bg', 'bh', 'bn', 'bo', 'ce', 'ckb', 'cv', 'el', 'fa', 'gan', 'he', 'hi', 'hy', 'iu', 'ja', 'ka', 'kk', 'km', 'kn', 'ko', 'ks', 'ky', 'lo', 'mhr', 'mk', 'ml', 'mn', 'mr', 'my', 'myv', 'mzn', 'ne', 'new', 'or', 'os', 'pa', 'pnb', 'ps', 'ru', 'rue', 'sa', 'sah', 'si', 'sr', 'ta', 'te', 'tg', 'th', 'tt', 'ug', 'uk', 'ur', 'wuu', 'xmf', 'yi', 'zh', 'zh-yue']

# langs = ['ab', 'am', 'arz']

# # low resource languages to try training using bigs-en language model
# langs = ["iu", "myv", "lo", "av", "ks", "bh", "ug", "km", "bo", "gan", "or", "assm", "am", "xmf", "si"]

for lang in langs:
	#
	# create_indiv_build_script("/nlp/users/tbreiner/models", "lm-" + lang, "en", True)
	# create_build_runner(lang, "en")
	# create_indiv_bundler("/nlp/users/tbreiner/models", "lm-" + lang, "en")
	# create_bundler_runner(lang, "en")
	# create_top_n_runner("/nlp/users/tbreiner/models", "lm-" + lang, "en", 100)
	create_cross_top_n_runner("/nlp/users/tbreiner/models", "bigs", lang, 100)


# for getting learning curve models
# for lang in langs:
	# for perc in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
		# create_indiv_build_script("/nlp/users/tbreiner/models_" + str(perc), lang, "en")
		# create_build_runner(lang, "en")
		# create_indiv_bundler("/nlp/users/tbreiner/models_" + str(perc), lang, "en")
		# create_bundler_runner(lang, "en")
		# create_top_n_runner("/nlp/users/tbreiner/models_" + str(perc), lang, "en", 100)



########### UNUSED FUNCTIONS ###############

# def create_build_runner(source_lang, target_lang):
# 	"""creates script to change to correct directory and then run build_script using qsub"""
# 	f = open("/nlp/users/tbreiner/script_runners/run_" + source_lang + ".sh", "w")
# 	f.write("#!/bin/bash\n")
# 	f.write("#$ -v JOSHUA=/nlp/users/tbreiner/joshua-6.0.5\n")
# 	f.write("#$ -v JAVA_HOME=/usr/lib64/jvm/java\n")
# 	f.write("cd /nlp/users/tbreiner/models/" + source_lang + "-" + target_lang + "/\n")
# 	f.write("mkdir temp\n")
# 	f.write("qsub -cwd -l mem=10G " + source_lang + "_build_script.sh\n")
# 	f.close()


# def create_bundler_runner(source_lang, target_lang):
# 	"""creates script to change to correct directory and then run bundler_script using qsub"""
# 	f = open("/nlp/users/tbreiner/script_runners/bundle_" + source_lang + ".sh", "w")
# 	f.write("#!/bin/bash\n")
# 	f.write("#$ -v JOSHUA=/nlp/users/tbreiner/joshua-6.0.5\n")
# 	f.write("#$ -v JAVA_HOME=/usr/lib64/jvm/java\n")
# 	f.write("cd /nlp/users/tbreiner/models/" + source_lang + "-" + target_lang + "/\n")
# 	f.write("qsub -cwd " + source_lang + "_bundler_script.sh\n")
# 	f.close()
