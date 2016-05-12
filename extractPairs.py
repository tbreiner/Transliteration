""" code to determine which languages of interest are desired from the wikipedia_names file,
which should be located in the same directory as this file.
A samples.txt file will be produced containing language code and a sample of a name in that language
which should be examined by hand and annotated with a * at the beginning of
every line of interest - in this case, using a script different from English.
Then this code can gather all relevant pairs of foreign-English data from wikipedia_names and save them in
separate files such as ar.ar and ar.en for the arabic names and corresponding English names respectively."""

from subprocess import call

# # directory to store the raw data files such as ar.txt
raw_data_dir = "../original_columns/all_cols/"
# # directory to store the data files that will contain the pairs of langs of interest, such as ar.ar and ar.en
pairs_dir = "../lang_files/"

# # all langs in the wikipedia_names file
langs = "en	ab	ace	af	als	am	an	ang	ar	arc	arz	as	ast	av	ay	az	ba	bar	bat-smg	bcl	be	be-x-old	bg	bh	bi	bjn	bm	bn	bo	br	bs	ca	cbk-zam	cdo	ce	ceb	chr	chy	ckb	co	crh	cs	cv	cy	da	de	diq	dsb	dv	el	eml	eo	es	et	eu	ext	fa	fi	fo	fr	frr	fur	fy	ga	gan	gd	gl	gn	got	gv	ha	hak	haw	he	hi	hr	hsb	ht	hu	hy	ia	id	ie	ig	ilo	io	is	it	iu	ja	jbo	jv	ka	kaa	kab	kk	kl	km	kn	ko	ks	ksh	ku	kw	ky	la	lad	lb	li	lij	lmo	ln	lo	lt	ltg	lv	map-bms	mg	mhr	mi	mk	ml	mn	mr	ms	mt	my	myv	mzn	na	nah	nap	nds	nds-nl	ne	new	nl	nn	no	nrm	nso	nv	oc	or	os	pa	pag	pam	pap	pdc	pih	pl	pms	pnb	ps	pt	qu	rm	ro	roa-tara	ru	rue	rw	sa	sah	sc	scn	sco	se	sh	si	simple	sk	sl	so	sq	sr	srn	su	sv	sw	szl	ta	te	tet	tg	th	tk	tl	tpi	tr	tt	ty	ug	uk	ur	uz	vec	vep	vi	vls	vo	wa	war	wuu	xmf	yi	yo	zea	zh	zh-min-nan	zh-yue	zu"
langs = langs.split("\t")

# # these were the targets that I chose to use - written with foreign scripts. 
# # Method collect_targs below can be used to read in annotated samples file to gather list of langs
targs = ['ab', 'am', 'ar', 'arc', 'arz', 'as', 'av', 'az', 'ba', 'be', 'be-x-old', 'bg', 'bh', 'bn', 'bo', 'ce', 'ckb', 'cv', 'dv', 'el', 'fa', 'gan', 'got', 'he', 'hi', 'hy', 'iu', 'ja', 'ka', 'kk', 'km', 'kn', 'ko', 'ks', 'ky', 'lo', 'mhr', 'mk', 'ml', 'mn', 'mr', 'my', 'myv', 'mzn', 'ne', 'new', 'or', 'os', 'pa', 'pnb', 'ps', 'ru', 'rue', 'sa', 'sah', 'si', 'sr', 'ta', 'te', 'tg', 'th', 'tt', 'ug', 'uk', 'ur', 'wuu', 'xmf', 'yi', 'zh', 'zh-yue']

def get_lang_samples():
	"""searches through full wikipedia_names file
	puts each language's (column's) data into its own txt file
	then goes through files and outputs one sample line containing text to samples.txt 
	This file can then be examined by eye to find languages with scripts of interest"""

	# extract each column into a lang.txt file

	for n in xrange(1,len(langs)+1):
		cmd = "cut -f " + str(n) + " wikipedia_names > " + langs[n - 1] + ".txt"
		call(cmd, shell=True)

	# get sample text from each column
	samp = open("samples.txt", "w")
	for lang in langs:
		f = open(raw_data_dir + lang + ".txt")
		lines = f.readlines()[1:]
		f.close()
		for line in lines:
			if len(line) > 2:
				samp.write(lang + " " + line + "\n")
				break

	samp.close()

def collect_targs():
	"""goes through samples.txt which should have been annotated with a "*"
	at the start of any language's line of interest. Returns this list of languages of interest"""

	# # collect langs of importance
	chosen = []
	# indices = []
	f = open("samples.txt", "r")
	for i, line in enumerate(f.readlines()):
		if line[0] == "*":
			chosen.append(line.split()[0][1:])
			indices.append(i)
	
	print "languages of interest:", chosen
	# print indices

	# # get indices of langs of interest
	# f = open("info.txt", "r")
	# nums = f.readlines()[1][1:-1].split(",")
	# f.close()
	# ans = []
	# for num in nums:
		# ans.append(int(num) / 2 + 1)
	# print ans

	return chosen

def get_comparables(lang):
	"""Takes the language of interest
	and searches for the English transliteration of every available name in that language 
	in the wikipedia_names file. Produces two new files for the language, one containing all the names 
	in the language and the other containing all of the corresponding English transliterations.
	If lang is ar, for example, files will be called ar.ar and ar.en respectively."""
	f = open(raw_data_dir + "en.txt", "r")
	eng = f.readlines()
	f.close()
	f = open(raw_data_dir + lang + ".txt", "r")
	# # ignore first line which says language code
	target = f.readlines()[1:]
	f.close()
	fen = open(pairs_dir + lang + ".en", "w")
	ftar = open(pairs_dir + lang + "." + lang, "w")
	for i, text in enumerate(target):
		if len(text) > 1:
			fen.write(eng[i])
			ftar.write(text)
	fen.close()
	ftar.close()

####################### MAIN CODE ########################

# # produce samples.txt
get_lang_samples()
# # user must hand annotate languages of interest
# # by adding a * to beginning of line in samples.txt file

# # gather annotated languages
targs = collect_targs()

# # produce pairs of data files for each language of interest
for targ in targs:
	get_comparables(targ)
