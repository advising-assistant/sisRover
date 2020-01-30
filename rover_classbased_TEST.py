# Joey Rudek, @jrdek, jer5ae
# October 21, 2019

from courselist import CourseList

# line = '{"index":49,"crse_id":"006897","crse_offer_nbr":1,"strm":"1202","session_code":"SRT","session_descr":"Short Add","class_section":"001","location":"MAIN","location_descr":"On Grounds","start_dt":"01/13/2020","end_dt":"04/28/2020","class_stat":"A","campus":"MAIN","campus_descr":"Main Campus","class_nbr":15073,"acad_career":"UGRD","acad_career_descr":"Undergraduate","component":"LEC","subject":"CS","subject_descr":"Computer Science","catalog_nbr":"3102","class_type":"E","schedule_print":"Y","acad_group":"ENGR","instruction_mode":"P","instruction_mode_descr":"In Person","acad_org":"CS","wait_tot":0,"wait_cap":199,"class_capacity":200,"enrollment_total":0,"enrollment_available":200,"descr":"Theory of Computation","rqmnt_designtn":"","units":"3","combined_section":"N","enrl_stat":"O","enrl_stat_descr":"Open","topic":"","instructors":[{"name":"Nathan Brunelle","email":"njb2b@virginia.edu"}],"section_type":"Lecture","class_meeting_patterns":[{"class_mtg_nbr":1,"meeting_time_start":"15:30","meeting_time_end":"16:45","mon":"N","tues":"Y","wed":"N","thurs":"Y","fri":"N","sat":"N","sun":"N","start_dt":"01/13/2020","end_dt":"04/28/2020","stnd_mtg_pat":"TuTh","facility_id":"WIL 402","bldg_cd":"WIL","bldg_has_coordinates":true,"facility_descr":"Wilson Hall 402","room":"402","room_descr":"Wilson Hall 402"}],"crse_attr":"","crse_attr_value":"","reserve_caps":[]},'

# theoryOfComp = Course(line)

# print(theoryOfComp.subject, theoryOfComp.catalog_nbr+":", theoryOfComp.descr)

computer = CourseList("CS", "1202")
num = len(computer.courses)

print("There are", num, computer.mnemonic, "courses being offered in term", computer.term)

print("courses taught by Aaron Bloomfield:")
for c in computer.courses:
    for instr in c.instructors:
        if instr.name == "Aaron Bloomfield":
            print(c.subject, c.catalog_nbr+":", c.descr)
