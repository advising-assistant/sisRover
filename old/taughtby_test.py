# Joey Rudek (jer5ae)
import rover

def ppl_to_term(text):
    """
    converts human-readable semesters to SIS-readable ones.
    e.g. s19 -> 1192
    """
    text = text.lower()
    sems = ['2','8']
    return '1' + text[-2:] + sems[['s', 'f'].index(text[0])]


term = input("What semester do you want to search in? (e.g., f19, s20) ")
search_mnem = input("What mnemonic (e.g., CS, APMA, BME) would you like to search for? ")
courses = rover.doSearch(search_mnem, ppl_to_term(term))

prof = input("Which professor do you want to search for? ")

res = rover.taught_by(courses, prof)
print(prof,"teaches:")
for key in res:
    for sess in res[key]:
        print("\t"+key,"("+sess+")")
