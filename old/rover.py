# Joey Rudek (jer5ae)
import requests
import re

"""
TODO 10/14/19: Turn this file into a class definition (or several), probably.
It might be easier to use like that.
In particular, it might be good to make a course class.
"""

# If you don't feel like counting through the parameters, this list might come in handy...
keys = ['index', 'crse_id', 'crse_offer_nbr', 'strm', 'session_code', 'session_descr', 'class_section', 'location', 'location_descr', 'start_dt', 'end_dt', 'class_stat', 'campus', 'campus_descr', 'class_nbr', 'acad_career', 'acad_career_descr', 'component', 'subject', 'subject_descr', 'catalog_nbr', 'class_type', 'schedule_print', 'acad_group', 'instruction_mode', 'instruction_mode_descr', 'acad_org', 'wait_tot', 'wait_cap', 'class_capacity', 'enrollment_total', 'enrollment_available', 'descr', 'rqmnt_designtn', 'units', 'combined_section', 'enrl_stat', 'enrl_stat_descr', 'topic', 'instructors', 'section_type', 'class_meeting_patterns', 'crse_attr', 'crse_attr_value', 'reserve_caps']


def makeRequest(search_mnem, term, page):
    # Returns the JSON of search results for one page of results
    s = requests.Session()
    results_url = s.get("https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term="+term+"&date_from=01%2F01%2F1971&date_thru=12%2F31%2F2200&subject="+search_mnem+"&catalog_nbr=&time_range=0%2C23.5&days=&campus=&location=&acad_career=&acad_group=&rqmnt_designtn=&instruction_mode=&keyword=&class_nbr=&acad_org=&enrl_stat=&crse_attr=&crse_attr_value=&instructor_name=&session_code=&units=&page="+str(page))
    return results_url.text


def doSearch(search_mnem, term):
    page = 1
    results = ''
    nextresults = makeRequest(search_mnem, term, page)
    while nextresults != '[]':
        results += nextresults
        print("Page", page, "parsed...\r", end="")
        page += 1
        nextresults = makeRequest(search_mnem, term,page)
    print("Found",page-1,"pages of results.")


    coursepattern_raw = r'{"index":(.*?),"crse_id":"(.*?)","crse_offer_nbr":(.*?),"strm":"(.*?)","session_code":"(.*?)","session_descr":"(.*?)","class_section":"(.*?)","location":"(.*?)","location_descr":"(.*?)","start_dt":"(.*?)","end_dt":"(.*?)","class_stat":"(.*?)","campus":"(.*?)","campus_descr":"(.*?)","class_nbr":(.*?),"acad_career":"(.*?)","acad_career_descr":"(.*?)","component":"(.*?)","subject":"(.*?)","subject_descr":"(.*?)","catalog_nbr":"(.*?)","class_type":"(.*?)","schedule_print":"(.*?)","acad_group":"(.*?)","instruction_mode":"(.*?)","instruction_mode_descr":"(.*?)","acad_org":"(.*?)","wait_tot":(.*?),"wait_cap":(.*?),"class_capacity":(.*?),"enrollment_total":(.*?),"enrollment_available":(.*?),"descr":"(.*?)","rqmnt_designtn":"(.*?)","units":"(.*?)","combined_section":"(.*?)","enrl_stat":"(.*?)","enrl_stat_descr":"(.*?)","topic":"(.*?)","instructors":(\[.*?\]),"section_type":"(.*?)","class_meeting_patterns":(\[.*?\]),"crse_attr":"(.*?)","crse_attr_value":"(.*?)","reserve_caps":(\[.*?\])}'
    # Since "instructors", "class_meeting_patterns", and "reserve_caps" are all lists, we should parse them as such
    instrpattern_raw = r'{"name":"(.*?)","email":"(.*?)"},?'
    meetpattern_raw = r'{"class_mtg_nbr":(.*?),"meeting_time_start":"(.*?)","meeting_time_end":"(.*?)","mon":"(.)","tues":"(.)","wed":"(.)","thurs":"(.)","fri":"(.)","sat":"(.)","sun":"(.)","start_dt":"(.*?)","end_dt":"(.*?)","stnd_mtg_pat":"(.*?)","facility_id":"(.*?)","bldg_cd":"(.*?)","bldg_has_coordinates":(.*?),"facility_descr":"(.*?)","room":"(.*?)","room_descr":"(.*?)"}'
    rsrvpattern_raw = r''
    # (compile all the regexps we made)
    coursepattern = re.compile(coursepattern_raw)
    instrpattern = re.compile(instrpattern_raw)
    meetpattern = re.compile(meetpattern_raw)
    p_match = coursepattern.findall(results)
    """
    'courses' is a dictionary whose keys are the titles of all offered courses in the search results
    and whose values are lists of distinct sections of each course with that title.

    courses['Course NameNum'][n] is a list containing the attributes of a particular section.
    """
    courses = {}
    for course in p_match:
        namenum = course[18]+" "+course[20]  # e.g. CS 3102
        # make the list of class info
        this_course = list(course)
        this_course[39] = list(instrpattern.findall(course[39]))
        this_course[41] = list(meetpattern.findall(course[41]))
        if namenum not in courses:
            courses[namenum] = []
            courses[namenum].append([])
        courses[namenum][0].append(this_course)

    print("Done fetching courses.")

    for key in courses:
        courses[key].append(set())
        courses[key].append(set())
        #print(key, "-", courses[key][0][0][32])
        for sess in range(len(courses[key][0])):
            line = ''
            for instr_info in range(len(courses[key][0][sess][39])):
                line += courses[key][0][sess][39][instr_info][0]  # the 0th group is the whole thing!
                if instr_info != len(courses[key][0][sess][39])-1:
                    line += " and " 
            courses[key][0][sess][39] = line
            courses[key][1].add(line)  # set of all combinations of profs teaching a class
            courses[key][2].add(tuple(courses[key][0][sess][41]))  # set of all sessions' respective information

    print("Done creating lists of professors and sessions.")
    
    return courses


def taught_by(courses, prof):
    """
    Returns a dictionary whose keys are the courses taught by
    prof and whose values are the course IDs of the sections
    prof teaches.
    """
    out = {}
    for key in courses:
        for grp in courses[key][1]:
            if prof in grp:
                out[key] = []
    for key in out:
        for sess in courses[key][0]:
            if prof in sess[39]:
                out[key].append(sess[14])
    return out


def name_from_namenum(courses, namenum):
    # e.g., "CS 3102" returns "Theory of Computation"
    out = courses[namenum][0][0][32]


def name_from_id(courses, id):
    # This should only really be used for special topics courses... It's gonna be slow.
    for key in courses:
        for sess in courses[key][0]:
            if id == sess[14]:
                out = sess[32]
                if "Special Topics" in out or "New Course" in out:
                    if sess[38]:
                        out += ": "+sess[38]
                return out
    raise exception("ID not found")
