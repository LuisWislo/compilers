samples = [
    # Four data types. Declare and assign on the same line. Print results and on-the-fly expressions.
    '''int x = 5;
    float y = 3.5;
    string cool = "art exhibit";
    boolean flag = true;

    print(x);
    print(y);
    print(cool);
    print(flag);
    print(x + y);
    
    int w = (2^2)^3;
    print(w);
    int wow =  2 ^ 2 ^ 3;
    print(wow);
    print("this is my number " + 1 + " its cool " + 3.0);
    string what = "a beautiful number " + (1 + 3.0) + " is also weird";
    print(what);
    '''
    ,
    # Loops!
    '''
    int i = 5;

    while(i < 10) {
        print(i);
        i = i + 1;
    }

    for(int j=0;j<=3;j=j+1) {
        string msg = "I like the number " + j;
        print(msg);
    }
    '''
    ,
    # If-statements. Notice how 'w' can be declared twice in different scopes!
    '''
    int x = 45;

    if(x == 45) {
        print("it is equal");
        string w = "from this statement i was declared";
        print(w);
    }

    int y = 20;

    if(y > 30) {
        print("greater than 30");
    } else {
        print("it is a smaller number");
        string w = "from this one as well";
        print(w);
    }

    if(false) {
        print("not here");
    } elif(true) {
        print("here");
    } else {
        print("magic");
    }

    if(false) {
        print("not here");
    } elif(false) {
        print("here");
    } else {
        print("magic");
    }

    '''
]