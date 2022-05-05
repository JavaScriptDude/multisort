## `multisort` - NoneType Safe Multi Column Sorting For Python

Simplified multi-column sorting of lists of tuples, dicts, lists or objects that are NoneType safe.

### Installation

```
python3 -m pip install multisort
```

### Dependencies
None

### Performance
Average over 10 iterations with 1000 rows.
Test | Secs
---|---
superfast|0.0005
multisort|0.0035
pandas|0.0079
cmp_func|0.0138
reversor|0.037

Hands down the fastest is the `superfast` methdology shown below. You do not need this library to accomplish this as its just core python.

`multisort` from this library gives reasonable performance for large data sets; eg. its better than pandas up to about 5,500 records. It is also much simpler to read and write, and it has error handling that does its best to give useful error messages.

### Note on `NoneType` and sorting
If your data may contain None, it would be wise to ensure your sort algorithm is tuned to handle them. This is because sorted uses `<` comparisons; which is not supported by `NoneType`. For example, the following error will result: `TypeError: '>' not supported between instances of 'NoneType' and 'str'`. All examples given on this page are tuned to handle `None` values.

### Methodologies
Method|Descr|Notes
---|---|---
multisort|Simple one-liner designed after `multisort` [example from python docs](https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts)|Second fastest of the bunch but most configurable and easy to read.
cmp_func|Multi column sorting in the model `java.util.Comparator`|Reasonable speed|Enable multi column sorting with column specific reverse sorting|Medium speed. [Source](https://stackoverflow.com/a/56842689/286807)
superfast|NoneType safe sample implementation of multi column sorting as mentioned in [example from python docs](https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts)|Fastest by orders of magnitude but a bit more complex to write.




### Dictionary Examples
For data:
```
rows_dict = [
     {'idx': 0, 'name': 'joh', 'grade': 'C', 'attend': 100}
    ,{'idx': 1, 'name': 'jan', 'grade': 'a', 'attend': 80}
    ,{'idx': 2, 'name': 'dav', 'grade': 'B', 'attend': 85}
    ,{'idx': 3, 'name': 'bob' , 'grade': 'C', 'attend': 85}
    ,{'idx': 4, 'name': 'jim' , 'grade': 'F', 'attend': 55}
    ,{'idx': 5, 'name': 'joe' , 'grade': None, 'attend': 55}
]
```

### `multisort`
Sort rows_dict by _grade_, descending, then _attend_, ascending and put None first in results:
```
from multisort import multisort
rows_sorted = multisort(rows_dict, [
         ('grade', {'reverse': False})
        ,'attend'
])

```
Sort rows_dict by _grade_, descending, then _attend_ and call upper() for _grade_:
```
from multisort import multisort
rows_sorted = multisort(rows_dict, [
         ('grade', {'reverse': False, 'clean': lambda s: None if s is None else s.upper()})
        ,'attend'
])

```
`multisort` parameters:
option|dtype|description
---|---|---
`key`|int or str|Key to access data. int for tuple or list
`spec`|str, int, list|Sort specification. Can be as simple as a column key / index
`reverse`|bool|Reverse order of final sort (defalt = False)

`multisort` `spec` options:
option|dtype|description
---|---|---
reverse|bool|Reverse sort of column
clean|func|Function / lambda to clean the value. These calls can cause a significant slowdown.
required|bool|Default True. If false, will substitute None or default if key not found (not applicable for list or tuple rows)
default|any|Value to substitute if required==False and key does not exist or None is found. Can be used to achive similar functionality to pandas `na_position`



### `sorted` with `reversor`
Sort rows_dict by _grade_, descending, then _attend_ and call upper() for _grade_:
```
rows_sorted = sorted(rows_dict, key=lambda o: (
             reversor(None if o['grade'] is None else o['grade'].upper())
            ,o['attend'])
))
```


### `sorted` with `cmp_func`
Sort rows_dict by _grade_, descending, then _attend_ and call upper() for _grade_:
```
def cmp_student(a,b):
    k='grade'; va=a[k]; vb=b[k]
    if va != vb: 
        if va is None: return -1
        if vb is None: return 1
        return -1 if va > vb else 1
    k='attend'; va=a[k]; vb=b[k]; 
    if va != vb: return -1 if va < vb else 1
    return 0
rows_sorted = sorted(rows_dict, key=cmp_func(cmp_student), reverse=True)
```



### Object Examples
For data:
```
class Student():
    def __init__(self, idx, name, grade, attend):
        self.idx = idx
        self.name = name
        self.grade = grade
        self.attend = attend
    def __str__(self): return f"name: {self.name}, grade: {self.grade}, attend: {self.attend}"
    def __repr__(self): return self.__str__()

rows_obj = [
     Student(0, 'joh', 'C', 100)
    ,Student(1, 'jan', 'a', 80)
    ,Student(2, 'dav', 'B', 85)
    ,Student(3, 'bob', 'C', 85)
    ,Student(4, 'jim', 'F', 55)
    ,Student(5, 'joe', None, 55)
]
```

### `multisort`
(Same syntax as with 'dict' example)


### `sorted` with `reversor`
Sort rows_obj by _grade_, descending, then _attend_ and call upper() for _grade_:
```
rows_sorted = sorted(rows_obj, key=lambda o: (
             reversor(None if o.grade is None else o.grade.upper())
            ,o.attend)
))
```


### `sorted` with `cmp_func`
Sort rows_obj by _grade_, descending, then _attend_ and call upper() for _grade_:
```
def cmp_student(a,b):
    if a.grade != b.grade: 
        if a.grade is None: return -1
        if b.grade is None: return 1
        return -1 if a.grade > b.grade else 1
    if a.attend != b.attend: 
        return -1 if a.attend < b.attend else 1
    return 0
rows_sorted = sorted(rows_obj, key=cmp_func(cmp_student), reverse=True)
```


### List / Tuple Examples
For data:
```
rows_tuple = [
     (0, 'joh', 'a'  , 100)
    ,(1, 'joe', 'B'  , 80)
    ,(2, 'dav', 'A'  , 85)
    ,(3, 'bob', 'C'  , 85)
    ,(4, 'jim', None , 55)
    ,(5, 'jan', 'B'  , 70)
]
(COL_IDX, COL_NAME, COL_GRADE, COL_ATTEND) = range(0,4)
```

### `multisort`
Sort rows_tuple by _grade_, descending, then _attend_, ascending and put None first in results:
```
from multisort import multisort
rows_sorted = multisort(rows_tuple, [
         (COL_GRADE, {'reverse': False, 'none_first': True})
        ,COL_ATTEND
])

```


### `sorted` with `reversor`
Sort rows_tuple by _grade_, descending, then _attend_ and call upper() for _grade_:
```
rows_sorted = sorted(rows_tuple, key=lambda o: (
             reversor(None if o[COL_GRADE] is None else o[COL_GRADE].upper())
            ,o[COL_ATTEND])
))
```


### `sorted` with `cmp_func`
Sort rows_tuple by _grade_, descending, then _attend_ and call upper() for _grade_:
```
def cmp_student(a,b):
    k=COL_GRADE; va=a[k]; vb=b[k]
    if va != vb: 
        if va is None: return -1
        if vb is None: return 1
        return -1 if va > vb else 1
    k=COL_ATTEND; va=a[k]; vb=b[k]; 
    if va != vb: 
        return -1 if va < vb else 1
    return 0
rows_sorted = sorted(rows_tuple, key=cmp_func(cmp_student), reverse=True)
```

### Tests / Samples
Name|Descr|Other
---|---|---
tests/test_multisort.py|multisort unit tests|- 
tests/performance_tests.py|Tunable performance tests using asyncio | requires pandas
tests/hand_test.py|Hand testing|-
