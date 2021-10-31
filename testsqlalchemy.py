from studentmodel import Student

if __name__ == '__main__':
    student = Student.query.filter_by(netid = 'eagarwal').all()
    print(student.res_college)