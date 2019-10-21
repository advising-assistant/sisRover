# Joey Rudek, @jrdek, jer5ae
# October 21, 2019

from course import Course
import requests
import re

def makeRequest(search_mnem, term, page):
	# Returns the JSON of search results for one page of results
	s = requests.Session()
	results_url = s.get("https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term="+term+"&date_from=01%2F01%2F1971&date_thru=12%2F31%2F2200&subject="+search_mnem+"&catalog_nbr=&time_range=0%2C23.5&days=&campus=&location=&acad_career=&acad_group=&rqmnt_designtn=&instruction_mode=&keyword=&class_nbr=&acad_org=&enrl_stat=&crse_attr=&crse_attr_value=&instructor_name=&session_code=&units=&page="+str(page))
	return results_url.text


class CourseList:
	def __init__(self, search_mnem, term):
		self.mnemonic = search_mnem
		self.term = term
		self.courses = self._doSearch(search_mnem, term)
		print("Done!")


	def _doSearch(self, search_mnem, term):
		page = 1
		results = ''
		nextresults = makeRequest(search_mnem, term, page)
		while nextresults != '[]':
			results += nextresults
			print("Page", page, "parsed...\r", end="")
			page += 1
			nextresults = makeRequest(search_mnem, term,page)
		print("Found",page-1,"pages of results.")
		found_courses = []
		course_pattern = re.compile(r'{"index":(.*?),"crse_id":"(.*?)","crse_offer_nbr":(.*?),"strm":"(.*?)","session_code":"(.*?)","session_descr":"(.*?)","class_section":"(.*?)","location":"(.*?)","location_descr":"(.*?)","start_dt":"(.*?)","end_dt":"(.*?)","class_stat":"(.*?)","campus":"(.*?)","campus_descr":"(.*?)","class_nbr":(.*?),"acad_career":"(.*?)","acad_career_descr":"(.*?)","component":"(.*?)","subject":"(.*?)","subject_descr":"(.*?)","catalog_nbr":"(.*?)","class_type":"(.*?)","schedule_print":"(.*?)","acad_group":"(.*?)","instruction_mode":"(.*?)","instruction_mode_descr":"(.*?)","acad_org":"(.*?)","wait_tot":(.*?),"wait_cap":(.*?),"class_capacity":(.*?),"enrollment_total":(.*?),"enrollment_available":(.*?),"descr":"(.*?)","rqmnt_designtn":"(.*?)","units":"(.*?)","combined_section":"(.*?)","enrl_stat":"(.*?)","enrl_stat_descr":"(.*?)","topic":"(.*?)","instructors":(\[.*?\]),"section_type":"(.*?)","class_meeting_patterns":(\[.*?\]),"crse_attr":"(.*?)","crse_attr_value":"(.*?)","reserve_caps":(\[.*?\])}')
		for c in course_pattern.findall(results):
			found_courses.append(Course(c))
		return found_courses