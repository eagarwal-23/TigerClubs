from app import db
from models import Student, Club, Tag

def club_search(name = None, tag = None):
    clubs = None
    if name:
        name_search = '%' + name + '%'
        clubs = Club.query.filter((Club.name.ilike(name_search))).all()
    elif tag:
        tag_search = '%' + tag + '%'
        clubs = Club.query.join(Tag).filter(Tag.name.ilike(tag_search)).all()
    for club in clubs:
        print(club)

if __name__ == "__main__":
    tag = 'c'
    club_search(tag = tag)