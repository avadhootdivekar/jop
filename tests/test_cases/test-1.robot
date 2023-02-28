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
    Run file and check output  ../inputs/member_assignment.jop   ../inputs/member_assignment.exp

RandomModTest
    [Tags]    Random
    Run file and check output  ../inputs/random-1.jop   ../inputs/random-1.exp





