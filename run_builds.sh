#!/bin/bash
#$ -v JOSHUA=/nlp/users/tbreiner/joshua-6.0.5
#$ -v JAVA_HOME=/usr/lib64/jvm/java

root=/nlp/users/tbreiner/

for lang in ar arz assm av az ba be be-x-old bg bh bn bo
	# for lang in ab am ar arz assm av az ba be be-x-old bg bh bn bo ce ckb cv el fa gan he hi hy iu ja ka kk km kn ko ks ky lo mhr mk ml mn mr my myv mzn ne new or os pa pnb ps ru rue sa sah si sr ta te tg th tt ug uk ur wuu xmf yi zh zh-yue
do
    cd ${root}models_$perc/$lang-en/
    qsub -cwd -l mem=10G ${lang}_build_script.sh
    # qsub -cwd -l mem=5G ${lang}_bundler_script.sh
done