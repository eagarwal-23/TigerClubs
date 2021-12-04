from app import db
from models import Club, Student, Tag
import pandas as pd

def add_club(name, description, club_type, diversity = 0, 
    inclusivity = 0, time_commitment = 0,
    experience_requirement = 0, workload = 0):
    club = Club(name, description, club_type, diversity, 
                inclusivity, time_commitment, experience_requirement, 
                workload)
    db.session.add(club)
    db.session.commit()

def add_tag(tagname):
    tag = Tag(tagname)
    db.session.add(tag)
    db.session.commit()

EXISTING_CLUBS = [1, 2, 5, 6, 8, 10, 11, 12, 13, 15, 16, 27]

if __name__ == "__main__":
    filename = "club_data.xlsx"
    df = pd.read_excel(filename)
    print(df.head(5))

    for i in range(len(df)):
        clubname = df.loc[i, "name"]
        clubdesc = df.loc[i, "description"]
        clubtype = df.loc[i, "type"]
        add_club(name = clubname,
                description = clubdesc,
                club_type= clubtype, diversity = 0, 
                inclusivity = 0, 
                time_commitment = 0, 
                experience_requirement = 0, 
                workload = 0)
