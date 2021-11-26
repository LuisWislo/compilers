# compilers

Luis Wilson A00226649

### November 26, 2021

#### WCompiler, the final project of the course.

Write your code in a .txt file and run as follows:

```
python3 wcompiler.py -f file_with_code.txt
```

A three-address-code table will be printed and then a "virtual" STDOUT for the actual execution of the code:

```
// code.txt
int x = 0;

while(x < 5) {
    print(x);
    x = x+1;
}
```
```
$ python3 wcompiler.py -f code.txt

Label Result Operation   Arg1 Arg2 
l0    -      INT         S0-x -    
l1    -      ASSIGN      S0-x 0    
l2    -      COND_MARKER -    -    
l3    v0     LTHAN       S0-x 5    
l4    -      IFNOTGOTO   v0   l5   
l6    0      PRINT       S0-x -    
l7    v1     PLUS        S0-x 1    
l8    -      ASSIGN      S0-x v1   
l9    -      GOTO        l2   -    
l5    -      CHECKPOINT  -    -    

>> STDOUT BEGIN >>
0
1
2
3
4
>> STDOUT END >>
```

Please check out samples.py for some examples on core functionalities of wcompiler.

Run a specific sample with the -s flag following its index:

```
$ python3 wcompiler.py -s 0 // will run the first sample
```

**Notes:**
- String values can only be alpha-numeric characters.