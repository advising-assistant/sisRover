# Joey Rudek (jer5ae)
# A test harness for rover.py
import rover

def ppl_to_term(text):
	"""
	converts human-readable semesters to SIS-readable ones.
	e.g. s19 -> 1192
	"""
	text = text.lower()
	sems = ['2','8']
	return '1' + text[-2:] + sems[['s', 'f'].index(text[0])]


# first, ask the user for search terms.
search_mnem = input("What mnemonic (e.g., CS, APMA, BME) would you like to search for? ")
term = input("What semester do you want to search in? (e.g., f19, s20) ")

courses = rover.doSearch(search_mnem, ppl_to_term(term))

k = -1
while True:
	k = input("Enter a course to search for (e.g. CS 3102): ")
	if not k:
		break
	if k != "*":
		query = [k]
	else:
		query = [course for course in courses]

	c = 0
	for k in query:
		try:
			dat = courses[k][0]
		except:
			print("Couldn't find that course.")
			continue
		for sess in range(len(dat)):
				sect_type = dat[sess][40]
				class_num = dat[sess][14]
				prof = dat[sess][39]
				print(class_num+":",sect_type,"taught by",prof)
				c += 1
	print("Total of",c,"courses.")