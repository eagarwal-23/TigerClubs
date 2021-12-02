
from req_lib import getAllUndergrads
import json
from db_admin import add_student
'''
JSON list of dictionaries, with each dictionary representing a student.
Dictionary fields: [first_name, last_name, full_name, class_year, net_id, res_college, 
hometown, home_lat, home_lng, dorm_number, dorm_building, dorm_lat, dorm_lng, major_type, 
major_raw, major_code, photo_link, phone_raw, mailbox, organization_raw, athletics_raw, 
athletics_url_raw, gender*, puid*, alias, email]
'''
# MAKE SURE TO NOT CREATE A USER IF THE USER ALREADY EXISTS
# populate database
if __name__ == "__main__":
    req = getAllUndergrads()
    if req.ok:
        json_resp = req.json()
        for student in json_resp:
            net_id = student['net_id'].strip()
            full_name = student['full_name'].strip()
            res_college = student['res_college'].strip()
            class_year = "20" + str(student['class_year'])
            major_code = student['major_code'].strip()
            profile_url = student['photo_link']
            print(net_id)
            # Have to do photos too -- tigerbook down but check if photos are none or just placeholder

            # uncomment line below to add students

            #add_student(net_id, full_name, res_college, class_year, major_code, "", False, profile_url)
    else:
        print(req.text)

