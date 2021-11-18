
from req_lib import getAllUndergrads
import json
'''
JSON list of dictionaries, with each dictionary representing a student.
Dictionary fields: [first_name, last_name, full_name, class_year, net_id, res_college, 
hometown, home_lat, home_lng, dorm_number, dorm_building, dorm_lat, dorm_lng, major_type, 
major_raw, major_code, photo_link, phone_raw, mailbox, organization_raw, athletics_raw, 
athletics_url_raw, gender*, puid*, alias, email]
'''
# populate database
if __name__ == "__main__":
    req = getAllUndergrads()
    if req.ok:
        json_resp = req.json()
        for student in json_resp:
            print(student['net_id'])
            print(student['first_name'])
            print(student['last_name'])
    else:
        print(req.text)

