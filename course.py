# Joey Rudek, @jrdek, jer5ae
# October 21, 2019

import re

class Course:
    def __init__(self, result):
        # result is a tuple of strings representing one course

        # assign all fields as named!
        keys = ['index', 'crse_id', 'crse_offer_nbr', 'strm', 'session_code', 'session_descr', 'class_section', 'location', 'location_descr', 'start_dt', 'end_dt', 'class_stat', 'campus', 'campus_descr', 'class_nbr', 'acad_career', 'acad_career_descr', 'component', 'subject', 'subject_descr', 'catalog_nbr', 'class_type', 'schedule_print', 'acad_group', 'instruction_mode', 'instruction_mode_descr', 'acad_org', 'wait_tot', 'wait_cap', 'class_capacity', 'enrollment_total', 'enrollment_available', 'descr', 'rqmnt_designtn', 'units', 'combined_section', 'enrl_stat', 'enrl_stat_descr', 'topic', 'instructors', 'section_type', 'class_meeting_patterns', 'crse_attr', 'crse_attr_value', 'reserve_caps']
        for key in range(len(keys)):
            exec('self.'+keys[key]+'=\''+result[key]+'\'')  # result[key] was info[key]

        # since "instructors", "class_meeting_patterns", and
        # "reserve_caps" are all lists, we should parse them
        # as such.
        instr_pattern = re.compile(r'{"name":"(.*?)","email":"(.*?)"},?')
        meet_pattern = re.compile(r'{"class_mtg_nbr":(.*?),"meeting_time_start":"(.*?)","meeting_time_end":"(.*?)","mon":"(.)","tues":"(.)","wed":"(.)","thurs":"(.)","fri":"(.)","sat":"(.)","sun":"(.)","start_dt":"(.*?)","end_dt":"(.*?)","stnd_mtg_pat":"(.*?)","facility_id":"(.*?)","bldg_cd":"(.*?)","bldg_has_coordinates":(.*?),"facility_descr":"(.*?)","room":"(.*?)","room_descr":"(.*?)"}')
        # (TODO)
        rsrv_pattern = re.compile(r'')

        self.instructors = list(instr_pattern.findall(self.instructors))
        self.class_meeting_patterns = list(meet_pattern.findall(self.class_meeting_patterns))