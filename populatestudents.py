
'''
from req_lib import getAllUndergrads
import json

JSON list of dictionaries, with each dictionary representing a student.
Dictionary fields: [first_name, last_name, full_name, class_year, net_id, res_college, 
hometown, home_lat, home_lng, dorm_number, dorm_building, dorm_lat, dorm_lng, major_type, 
major_raw, major_code, photo_link, phone_raw, mailbox, organization_raw, athletics_raw, 
athletics_url_raw, gender*, puid*, alias, email]

# populate database
if __name__ == "__main__":
    req = getAllUndergrads()
    if req.ok:
        for student in req.json():
            for subjects, values in student:
                print(subjects)
    else:
        print(req.text)
'''
        '''
        JSONObject root = new JSONObject(yourJsonString);
JSONArray sportsArray = root.getJSONArray("sports");

// now get the first element:
JSONObject firstSport = sportsArray.getJSONObject(0);

// and details of the first element
String name = firstSport.getString("name"); // basketball
int id = firstSport.getInt("id"); // 40
JSONArray leaguesArray = firstSport.getJSONArray("leagues");
'''
    
