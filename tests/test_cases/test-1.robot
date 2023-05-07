** Settings ***
Documentation      Here we have documentation for this suite.
...                Documentation is often quite long.
...
...                It can also contain multiple paragraphs.
Default Tags       default tag 1    default tag 2    default tag 3
...                default tag 4    default tag 5
Library            baseLib.py

*** Variables ***
${STRING}          This is a long string.
...                It has multiple sentences.
...                It does not have newlines.
${MULTILINE}       SEPARATOR=\n
...                This is a long multiline string.
...                This is the second line.
...                This is the third and the last line.
@{LIST}            this     list     is      quite    long     and
...                items in it can also be long
&{DICT}            first=This value is pretty long.
...                second=This value is even longer. It has two sentences.

*** Test Cases ***
SimpleTests
    [Tags]    simpleTests
    Test new    Sample input

RunTest
    [Tags]    baseTest
    Run file and check output  ../inputs/test-1.jop   ../inputs/test-1.exp
    Run file and check output  ../inputs/test-2.jop   ../inputs/test-2.exp
    Run file and check output  ../inputs/test-3.jop   ../inputs/test-3.exp
    Run file and check output  ../inputs/test-4.jop   ../inputs/test-4.exp
    Run file and check output  ../inputs/test-5.jop   ../inputs/test-5.exp
    Run file and check output  ../inputs/test-6.jop   ../inputs/test-6.exp
    Run file and check output  ../inputs/test-7-non-string-keys.jop   ../inputs/test-7-non-string-keys.exp
    Run file and check output  ../inputs/member_assignment.jop   ../inputs/member_assignment.exp

NegativeTests
    Run file and check output  ../inputs/test-8-invalid-root-syntax.jop   ../inputs/test-8-invalid-root-syntax.exp

RandomModTest
    [Tags]    Random
    Random op check


ListTest
    Run file and check output  ../inputs/test-list-1.jop   ../inputs/test-list-1.exp
    Run file and check output  ../inputs/test-list-2.jop   ../inputs/test-list-2.exp
    Run file and check output  ../inputs/test-list-3.jop   ../inputs/test-list-3.exp
    Run file and check output  ../inputs/test-list-4.jop   ../inputs/test-list-4.exp
    Run file and check output  ../inputs/test-list-5.jop   ../inputs/test-list-5.exp
    Run file and check output  ../inputs/test-list-6.jop   ../inputs/test-list-6.exp
    Run file and check output  ../inputs/test-list-7.jop   ../inputs/test-list-7.exp
    Run file and check output  ../inputs/test-list-8.jop   ../inputs/test-list-8.exp
    Run file and check output  ../inputs/test-list-9.jop   ../inputs/test-list-9.exp
    

SetTest
    Run file and check output  ../inputs/set-ops/set-1-union.jop   ../inputs/set-ops/set-1-union.exp
    Run file and check output  ../inputs/set-ops/set-2-intersection.jop   ../inputs/set-ops/set-2-intersection.exp
    Run file and check output  ../inputs/set-ops/set-3-diff.jop   ../inputs/set-ops/set-3-diff.exp
    Run file and check output  ../inputs/set-ops/set-4-intersection.jop   ../inputs/set-ops/set-4-intersection.exp


MemberWiseOpTest
    [Tags]    New
    Run file and check output  ../inputs/member-wise-ops/memb-1-add.jop   ../inputs/member-wise-ops/memb-1-add.exp
    Run file and check output  ../inputs/member-wise-ops/memb-2-add.jop   ../inputs/member-wise-ops/memb-2-add.exp
    Run file and check output  ../inputs/member-wise-ops/memb-3-mul.jop   ../inputs/member-wise-ops/memb-3-mul.exp
    Run file and check output  ../inputs/member-wise-ops/memb-4-mul.jop   ../inputs/member-wise-ops/memb-4-mul.exp
    Run file and check output  ../inputs/member-wise-ops/memb-5-div.jop   ../inputs/member-wise-ops/memb-5-div.exp
    Run file and check output  ../inputs/member-wise-ops/memb-6-div.jop   ../inputs/member-wise-ops/memb-6-div.exp
    Run file and check output  ../inputs/member-wise-ops/memb-7-sub.jop   ../inputs/member-wise-ops/memb-7-sub.exp
    Run file and check output  ../inputs/member-wise-ops/memb-8-and.jop   ../inputs/member-wise-ops/memb-8-and.exp
    Run file and check output  ../inputs/member-wise-ops/memb-9-or.jop   ../inputs/member-wise-ops/memb-9-or.exp

