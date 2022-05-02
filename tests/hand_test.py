import sys
from multisort import msorted, cmp_func, reversor
import test_util as util
pc = util.pc

def main():
    # test_msorted_dict_single()
    # test_msorted_obj_single()
    # test_msorted_tuple_single()

    test_msorted_dict_multi()
    # test_msorted_obj_multi()
    # test_msorted_tuple_multi()


students_dict = [
     {'idx': 0, 'name': 'joh', 'grade': 'C', 'attend': 100}
    ,{'idx': 1, 'name': 'jan', 'grade': 'a', 'attend': 80}
    ,{'idx': 2, 'name': 'dav', 'grade': 'B', 'attend': 85}
    ,{'idx': 3, 'name': 'bob' , 'grade': 'C', 'attend': 85}
    ,{'idx': 4, 'name': 'jim' , 'grade': 'F', 'attend': 55}
    ,{'idx': 5, 'name': 'joe' , 'grade': None, 'attend': 55}
]

class Student():
    def __init__(self, idx, name, grade, attend):
        self.idx = idx
        self.name = name
        self.grade = grade
        self.attend = attend
    def __str__(self): return f"name: {self.name}, grade: {self.grade}, attend: {self.attend}"
    def __repr__(self): return self.__str__()

students_obj = [
     Student(0, 'joh', 'C', 100)
    ,Student(1, 'jan', 'a', 80)
    ,Student(2, 'dav', 'B', 85)
    ,Student(3, 'bob', 'C', 85)
    ,Student(4, 'jim', 'F', 55)
    ,Student(5, 'joe', None, 55)
]

student_tuple = [
     (0, 'joh', 'C', 100)
    ,(1, 'jan', 'a', 80)
    ,(2, 'dav', 'B', 85)
    ,(3, 'bob', 'C', 85)
    ,(4, 'jim', 'F', 55)
    ,(5, 'joe', None, 55)
]
(COL_IDX, COL_NAME, COL_GRADE, COL_ATTEND) = range(0,4)





def test_msorted_dict_single():
    _sorted = msorted(students_dict, 'grade', reverse=False)
    _print_stud(_sorted)


def test_msorted_obj_single():
    _sorted = msorted(students_obj, 'attend', reverse=False)
    _print_stud(_sorted)


def test_msorted_tuple_single():
    _sorted = msorted(student_tuple, COL_ATTEND, reverse=False)
    _print_stud(_sorted)


def test_msorted_dict_multi():
    _sorted = msorted(students_dict, [('grade', {'reverse': False, 'none_first': False}), 'attend'], reverse=False)
    _print_stud(_sorted)


def test_msorted_obj_multi():
    _sorted = msorted(students_obj, [('grade', {'reverse': True}), 'attend'], reverse=False)
    _print_stud(_sorted)


def test_msorted_tuple_multi():
    _sorted = msorted(student_tuple, [(COL_GRADE, {'reverse': True}), COL_ATTEND], reverse=False)
    _print_stud(_sorted)


def _print_stud(rows):
    print(f"\n{util.getFuncName(2)}() Results:")
    for row in rows:
        print(util.pre(str(row)))
    print('\n')




if __name__ == '__main__':
    main()