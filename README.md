## `multisort` - NoneType Safe Multi Column Sorting

Simplified multi-column sorting of lists of tuples, dicts, lists or objects that are NoneType safe.

### Installation

```
python3 -m pip install multisort
```

### Dependencies
None

### Performance
Average over 10 iterations with 500 rows.
Test | Secs
---|---
cmp_func|0.0054
pandas|0.0061
reversor|0.0149
msorted|0.0179

As you can see, if the `cmp_func` is by far the fastest methodology as long as the number of cells in the table are 500 rows for 5 columns. However for larger data sets, `pandas` is the performance winner and scales extremely well. In such large dataset cases, where performance is key, `pandas` should be the first choice.

The surprising thing from testing is that `cmp_func` far outperforms `reversor` which which is the only other methodology for multi-columnar sorting that can handle `NoneType` values.

### Note on `NoneType` and sorting
If your data may contain None, it would be wise to ensure your sort algorithm is tuned to handle them. This is because sorted uses `<` comparisons; which is not supported by `NoneType`. For example, the following error will result: `TypeError: '>' not supported between instances of 'NoneType' and 'str'`.

### Methodologies
Method|Descr|Notes
---|---|---
cmp_func|Multi column sorting in the model `java.util.Comparator`|Fastest for small to medium size data
reversor|Enable multi column sorting with column specific reverse sorting|Medium speed. [Source](https://stackoverflow.com/a/56842689/286807)
msorted|Simple one-liner designed after `multisort` [example from python docs](https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts)|Slowest of the bunch but not by much



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

### `msorted`
Sort rows_dict by _grade_, descending, then _attend_, ascending and put None first in results:
```
from multisort import msorted
rows_sorted = msorted(rows_dict, [
         ('grade', {'reverse': False, 'none_first': True})
        ,'attend'
])

```

Sort rows_dict by _grade_, descending, then _attend_ and call upper() for _grade_:
```
from multisort import msorted
rows_sorted = msorted(rows_dict, [
         ('grade', {'reverse': False, 'clean': lambda s:None if s is None else s.upper()})
        ,'attend'
])

```

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

### `msorted`
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

### `msorted`
Sort rows_tuple by _grade_, descending, then _attend_, ascending and put None first in results:
```
from multisort import msorted
rows_sorted = msorted(rows_tuple, [
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
tests/test_msorted.py|msorted unit tests|- 
tests/performance_tests.py|Tunable performance tests using asyncio | requires pandas
tests/hand_test.py|Hand testing|-
