# Transliteration
Here you can find all the files relating to my independent study project on machine transliteration advised by Chris Callison-Burch, UPenn Spring 2016.

My final report can be found in PDF form as BreinerTransliterationAsMachineTranslation.pdf, along with BreinerAppendixTransliterationAsMachineTranslation.pdf. My raw data results are gathered as an excel spreadsheet in BreinerTransliterationData.xlsx.

## Contents of this Document

* Section 1: Getting started downloading the data and Joshua
* Section 2: List of Files with Descriptions
* Section 3: How-to for using my scripts
* Section 4: Troubleshooting

### Section 1 - Getting Started

How to download the data and Joshua decoder:

Data: Download [wikipedia_names](http://www.clsp.jhu.edu/˜anni/data/wikipedia_names)

Joshua: 
[Joshua’s web page](http://joshua.incubator.apache.org/)

[Installation guide](http://joshua.incubator.apache.org/6.0/install.html)

You will need to download the full model, not the runtime version, if you want to train your own models.

You can follow step #4 on the installation guide to get Joshua, note that you will need to [install ant](http://ant.apache.org/manual/install.html).

### Section 2 - Files

The following files can be found in this repository:

##### extractPairs.py
*	determines which languages of interest are desired from the wikipedia_names file.
*	First splits up data in wikipedia_names into separate .txt files by language (ex: ar.txt, en.txt) containing every line from that language’s column in the csv file (some will be empty lines)
*	A samples.txt file will be produced containing language code and a sample of a name in that language
*	Samples.txt should be examined by hand and annotated with a * at the beginning of every line of interest - in this case, using a script different from English.
*	Then this code can gather all relevant pairs of foreign-English data from wikipedia_names and save them in separate files such as ar.ar and ar.en for the Arabic names and corresponding English names respectively.

##### preprocess.py
*	preprocesses raw data files organized by non-english language in the language pair and content language (ex: ar.ar is the Arabic content for the Arabic to English transliteration data, while ar.en is the English content for the same data)
*	preprocesses by replacing spaces with underscores and then adding a space between every Unicode character

##### split_data.py
*	takes the file of data for each language, shuffles it, and then splits it up into three different files for training, tuning, and testing. 
*	Training size is roughly 80% of whole set, tuning and testing are roughly 10% of whole set. 
*	If 10% of whole set is more than 2000 instances, only 2000 are included in tuning and testing and the rest are put into training.

##### generate_scripts.py
*	allows runnable bash scripts to be produced in multiple directories
*	scripts can be made for building models, bundling models, and running models on test sets to produce top n outputs
*	there is a separate method for creating scripts that will be running a model on a different test set other than its own data (create_cross_top_n_runner)
*	this way each model is submitted using a different qsub so progress of each model can be tracked separately
*	if you want to change the n in top-n outputs, pass in the argument to the create_top_n_runner or create_cross_top_n_runner methods. Default is 100.

##### run_builds.sh
*	bash script to qsub the build script in the given list of language directories
*	can also be used to qsub the bundler scripts after training is complete (uncomment last line)

##### run_top_n.sh
*	script to qsub all the scripts that run the trained and bundled models on the testing data to produce the top n results for each input name. Can only be run if the top_n_lang.sh scripts have been generated in each language pack directory after models are bundled. Use generate_scripts.py to generate those scripts after bundling.

##### evaluations.py
*	produces eval tables in csv format containing all of the evaluations based on the reference files found in each language’s input folder (ex: ar-en/input/test.ar-en.en) against the system output found in the language’s test directory (ex: ar-en/test/output.top_100)
*	calculates the word accuracy, mean f-score, mean reciprocal rank, mean average precision
*	also includes information about the number of inputs (testing instances) and the target number of outputs per input (the n in n-best, ex top_100)

##### copy_tune_test_inputs.sh
*	bash script to make directories that will hold all models trained on a given percentage of training data in order to produce learning curves
*	for example one directory models_10 will hold all models trained on 10% of the data
*	script also copies tuning and testing data into the language directories within each percentage directory
*	the training data will be copied in using splitting_training.py afterwards

##### splitting_training.py
*	script to split up training data into percentages and copy the correct amounts into the language directories within each percentage directory
*	this script should be run after copy_tun_test_inputs.sh which has created the directories themselves

##### run_learning_builds.sh
*	bash script to qsub the build scripts for all percentages of languages in order to train smaller models to produce learning curves
*	can also be used to qsub the bundler scripts after training is complete (uncomment last line)

##### make_graphs.py
*	provides code for producing scatter and line plots to represent the data using matplotlib
*	plot all languages using one evaluation metric
*	plot languages in one language family using all 4 metrics
*	plot learning curve of one language
*	plot one model tested on multiple languages using 2 metrics (order test languages by size)

##### combine_data.py
*	quick script to combine separate tables for each percentage of training data into one

##### glom_langs.py
*	quick script to merge sets of data into one larger set (training, tuning, and testing data)


### Section 3 - How To Use the Given Scripts

#### Gathering Data

Run extract_pairs.py to decide which data from wikipedia_names is of interest and create separate paired files for each language and its corresponding English data.

Run preprocess.py to set up data files with spaces between Unicode characters to be fed into Joshua to train a transliteration model.

Run split_data.py to generate training, tuning, and testing files for each language set.

#### Producing simple models for languages trained on their own data

Run generate_scripts.py to create runnable bash scripts that can be submitted via qsub to train the models on each language set.

Run run_builds.sh to qsub the scripts that will train all of the models.

Run run_builds.sh after commenting out the build command and uncommenting the bundle command to qsub the scripts that will bundle all of the models into language packs.

Run generate_scripts.py to create the top_n_lang.sh scripts that will produce the output on the test data. You can change the value of n here if you want, it is set to 100 by default.

Run run_top_n.sh to qsub the top_n_lang.sh scripts that produce the test output saved as a file called output.top_100 in the language’s test directory.

#### Producing Learning Curves
Run copy_tune_test_inputs.sh to make new directories by percentage of data and copy the tuning and testing data in.

Run splitting_training.py to copy the appropriate amount of training data into each directory.

Run learning_builds.sh to train and bundle models on all the subsets of training data.

The rest of the steps can be done by editing the files for training simple models to incorporate the 10 sets of percentages like in learning_builds.sh.

#### Other tasks
Testing models on other test files can be done by generating the $model_$testlang_test.sh script using the create_cross_top_n_runner method in the generate_scripts.py file and then using scripts similar to run_top_n.sh to start them.

Training models on multiple languages can be done by first running glom_langs.py and then following the training pipeline using the language code assigned to the new set within glom_langs.py

Producing evaluation tables by comparing the top n output of each model on testing data to the actual corresponding transliterations can be done using evaluations.py

Combining the evaluation tables from the different percentages of training data can be done using combine_data.py

Graphing can be done using make_graphs.py

### Section 4 - Troubleshooting
The following are some tips that may help when using the given data, Joshua, or UPenn's nlpgrid.

#### Data cleaning
There was one name in the Chinese data set (zh) that contained a traditional Chinese character that doesn’t seem to have a Unicode representation. During the preprocess step, it resulted in a processed language file of gibberish instead of spaced out Chinese characters. Finding the line at which the file can’t be successfully read, spaced and rewritten and deleting this name in both the Chinese script file and the corresponding English file will solve this problem. Unfortunately I lost my notes about which name it was and some quick searching has not yielded any results. I tried running the steps again from the beginning to find the error again but the files are being produced correctly without problem. If you see a problem with gibberish in your zh set, though, this may be the cause.

Aramaic (arc), Divehi (dv) and Gothic (got) do not seem to use parseable characters and so I ignored them.


#### Needing more tools installed

At first, the problems may be that more tools need to be installed.

Error:

```
$JOSHUA/bin/pipeline.pl --source bn --target en    
--type hiero     --no-prepare --aligner berkeley     --corpus input/bn-en/tok/training.bn-en     --tune input/bn-en/tok/dev.bn-en     --test input/bn-en/tok/devtest.bn-en --lm-gen berkeleylm
[source-numlines] cached, skipping...
[source-numlines] retrieved cached result =>    20788
[berkeley-aligner-chunk-0] cached, skipping...
[aligner-combine] cached, skipping...
[lm-sort-uniq] cached, skipping...
[berkeleylm] cached, skipping...
[compile-kenlm] rebuilding...
  dep=lm.gz [CHANGED]
  dep=lm.kenlm [NOT FOUND]
  cmd=/Users/theresabreiner/Documents/MCIT/Spring2016/MachineTranslation/joshua-6.0.5/bin/build_binary lm.gz lm.kenlm
  JOB FAILED (return code 127)
/bin/bash: /Users/theresabreiner/Documents/MCIT/Spring2016/MachineTranslation/joshua-6.0.5/bin/build_binary: No such file or directory”
```

Solution:

It looks like KenLM didn't build. What happens when you type "ant kenlm" from $JOSHUA?

In my case, I got:
```
Error: Could not find or load main class org.apache.tools.ant.launch.Launcher
```
despite the fact that my echo $ANT_HOME showed /usr/local/apache-ant.

After downloading cmake and boost, checking the environment variables for $ANT_HOME and $JAVA_HOME and $JOSHUA, and running ant kenlm again, it worked.

#### Setting environment variables properly using the nlpgrid

You can:

* export JOSHUA=<path>      # in your $HOME/.profilerc file
* use qsub -V option (on command line or in your qsub settings at the top of the script)
* use qsub -v JOSHUA=<path> option (on command line or in qsub settings)

#### Running out of memory
This caused the most problems with trying to train many models at once on the nlpgrid.

Error:
```
gzip: stdout: No space left on device
* FATAL: Couldn't sort the grammar (not enough memory? short on tmp space?)
* __init__() takes at least 3 arguments (2 given)
```

This problem also seemed to be the source of other errors such as:

```
[source-numlines] cached, skipping...
[source-numlines] retrieved cached result => 71
[berkeley-aligner-chunk-0] cached, skipping...
[aligner-combine] cached, skipping...
[lm-sort-uniq] cached, skipping...
[kenlm] cached, skipping...
[compile-berkeleylm] rebuilding...
  dep=lm.gz [CHANGED]
  dep=lm.berkeleylm [NOT FOUND]
  cmd=java -cp /nlp/users/tbreiner/joshua-6.0.5/lib/berkeleylm.jar -server -mx2G edu.berkeley.nlp.lm.io.MakeLmBinaryFromArpa lm.gz lm.berkeleylm
  JOB FAILED (return code 1)
```

Solution:
Making sure that qsub chooses machines that are relatively free by passing in the flag ```–l mem=10G``` (as can be seen in run_builds.sh for example) seemed to help. The above error may result if there wasn’t enough memory to finish building the lm.gz language model file last time the pipeline was run, but since it exists at least partially, this time it tries to run it thinks it was successfully built yet still runs into problems. Deleting all generated files and starting over should make it work.

Also, the space issue may be from the tmp folders on the nlpgrid which don’t have that much space allocated. You can change the tmp folder that Joshua will use by editing line 1143 in pipeline.pl.

### Section 5 - Joshua commands
How to use Joshua commands on the command line:

#### Build models
Edit source and target to be the language codes desired. Corpus (training) tune and test files also need to be correct – the given filename stubs will be completed using the source and target codes so that train.ru-en for example will look at train.ru-en.ru and train.ru-en.en during training.

```--lm-gen berkeleylm``` is used here.

The tag ```–lm EXISTING_FILE``` can be passed in to include an existing language model file, as can be seen in the relevant method in generate_scripts.py.

```
$JOSHUA/bin/pipeline.pl --source ru --target en \
    --type hiero \
    --no-prepare --aligner berkeley \
    --corpus input/train.ru-en \
    --tune input/tune.ru-en \
    --test input/test.ru-en --lm-gen berkeleylm
```

#### Bundle models into language packs
The name of the language pack can be changed to be the correct language pair. (see generate_scripts.py for generating bundlers)
```
$JOSHUA/scripts/support/run_bundler.py tune.joshua.config.final language-pack-zh-en --pack-tm grammar.gz
```

#### Run command-line decoder
Make sure that JOSHUA variable is set correctly then cd into the language pack directory and ```./run-joshua.sh```

#### Run decoder on test files and get output
See generating top_n scripts in generate_scripts.py.
From inside ab language pack directory for example, to run decoder on the test file in the input directory and save it in the test directory as output.top_100, run:
```
cat ../input/test.ab-en.ab | run-joshua.sh -m 3100m -threads 1 -top-n 100 -output-format "%i ||| %s ||| %f ||| %c" > ../test/output.top_100
```
