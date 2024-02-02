# jop
This is repository for json operations

## Note : This is abandoned project. 
There are multiple better alternatives. You may want to look at jsonAta , jsonpatch etc.

## Syntax

```
A = {"name" : "Mahesh" , "age" : 30};
ret = A.name;
```
```
.           It is a seperator. Used to get child.
A.b         Get child of A where key == value of b.
A."name"    Get key "name" from A's children
A.*         Get all children of A. 
A.+B        Elementwise Addition of all members of A and B recursively. 
A.*B        Elementwise multiplication of all members of A and B recursively. 
A.\/B        Elementwise division of all members of A and B recursively. Note the difference.  
A.-B        Elementwise subtraction of all members of A and B recursively. 
A+B         Union of A and B 
A./B.C      Get A -> B -> C and treat B as root of new dictionary. (Not to be confused with elementwise division.)
A."class"."subject"[10] = 30        Set "class" as child of A , set "subject" array as child of "class",
            Extend "subject" array to length 11 (0 through 10) and set subject[10] = 30 
```

### How to use the script

#### Running from command line

```
python3 jop_main.py -s <string> [OR] -f <input file>
```

#### Using in python 
```
import test_1_visitor
output = test_1_visitor.run_1(ip_string = string , ip_file=file)
```