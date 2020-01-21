# Joey Rudek, @jrdek, jer5ae
# October 21, 2019

import requests
import json
from course import Course

def makeRequest(search_mnem, term, page):
    # Returns the JSON of search results for one page of results
    s = requests.Session()
    results_url = s.get("https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term="+term+"&date_from=01%2F01%2F1971&date_thru=12%2F31%2F2200&subject="+search_mnem+"&catalog_nbr=&time_range=0%2C23.5&days=&campus=&location=&acad_career=&acad_group=&rqmnt_designtn=&instruction_mode=&keyword=&class_nbr=&acad_org=&enrl_stat=&crse_attr=&crse_attr_value=&instructor_name=&session_code=&units=&page="+str(page))
    # results_url = s.get("https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term="+term+"&subject="+search_mnem+"&catalog_nbr=&time_range=0%2C23.5&days=&campus=&location=&acad_career=&acad_group=&rqmnt_designtn=&instruction_mode=&keyword=&class_nbr=&acad_org=&enrl_stat=&crse_attr=&crse_attr_value=&instructor_name=&session_code=&units=&page="+str(page))
    return results_url.text


class CourseList:
    def __init__(self, search_mnem, term):
        self.mnemonic = search_mnem
        self.term = term
        self.courses = self._doSearch(search_mnem, term)
        print("Done!")


    def _doSearch(self, search_mnem, term):
        page = 1
        nextresults = makeRequest(search_mnem, term, page)

        jresults = []

        while nextresults != '[]':
            print("Page", page, "parsed...\r", end="")
            page += 1

            jresults += json.loads(nextresults)

            nextresults = makeRequest(search_mnem,term,page)

        print("Found",page-1,"pages of results.")

        return [Course(c) for c in jresults]
