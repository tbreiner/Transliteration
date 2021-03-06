#!/bin/bash
#$ -v JOSHUA=/nlp/users/tbreiner/joshua-6.0.5
#$ -v JAVA_HOME=/usr/lib64/jvm/java
# This script makes a new directory called models_perc for each ten percent 10-90% and copies each language's
# tuning and testing data into correct subdirectories. Copying the subset of the training data will be 
# done separately

root=/nlp/users/tbreiner/

for perc in 10 20 30 40 50 60 70 80 90
do

	mkdir ${root}models_$perc
	for lang in ab am ar arz assm av az ba be be-x-old bg bh bn bo ce ckb cv el fa gan he hi hy iu ja ka kk km kn ko ks ky lo mhr mk ml mn mr my myv mzn ne new or os pa pnb ps ru rue sa sah si sr ta te tg th tt ug uk ur wuu xmf yi zh zh-yue
	do
		cd ${root}models_$perc
		mkdir $lang-en
		cd $lang-en
		mkdir input
		cd input
		cp ${root}models/$lang-en/input/tune.$lang-en.en .
		cp ${root}models/$lang-en/input/tune.$lang-en.$lang .
		cp ${root}models/$lang-en/input/test.$lang-en.en .
		cp ${root}models/$lang-en/input/test.$lang-en.$lang .
	done
done