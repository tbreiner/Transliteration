"""script to combine eval tables containing all languages' performance using a certain
percentage of training data into one table.
Example: there is one file containing all language data trained using only 10 percent of data
It will be called 10_eval_table.csv"""

# # set the root directory for where the files will be
root = "../numbers/tables/"

# # open new file which will hold combined data
fout = open(root + "all_evals.csv", "w")

for perc in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
	fin = root + str(perc/10) + "_eval_table.csv"
	fin2 = root + str(perc) + "_eval_table2.csv"
	fin3 = root + str(perc) + "_eval_table3.csv"
	for fn in [fin, fin2, fin3]:
		f = open(fn, "r")
		lines = f.readlines()
		for line in lines:
			fout.write(line.strip() + "," + str(perc) + "\n")
		f.close()

for perc in [20, 30, 40, 50, 60, 70, 80, 90]:
	f = open(root + str(perc) + "_eval_table_mhrs.csv", "r")
	lines = f.readlines()
	for line in lines:
		fout.write(line.strip() + "," + str(perc) + "\n")
	f.close()

f = open(root + "eval_table.csv", "r")
lines = f.readlines()
for line in lines:
	fout.write(line.strip() + ",100\n")
f.close()
fout.close()


