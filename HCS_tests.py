from HCS import HCS

def test_numbers():
    assert HCS().evaluate('123') == 123
    assert HCS().evaluate('123.456') == 123.456
    assert HCS().evaluate('123e2') == 123e2
    assert HCS().evaluate('.1') == .1
    assert HCS().evaluate('.12') == .12
    assert HCS().evaluate('9.1') == 9.1
    assert HCS().evaluate('98.1') == 98.1
    assert HCS().evaluate('1.') == 1.
    assert HCS().evaluate('12.') == 12.
    assert HCS().evaluate('1') == 1
    assert HCS().evaluate('12') == 12
    assert HCS().evaluate('4.5') == 4.5
    assert HCS().evaluate('-4.5') == -4.5
    assert HCS().evaluate('- 4.5') == -4.5
    assert HCS().evaluate('+ .1e10') == .1e10
    assert HCS().evaluate(' 1.01e-2') == 1.01e-2

def test_assignments():
    assert HCS().evaluate('a=123') == 123
    assert HCS().evaluate('a = b = c = 987654') == 987654
    assert HCS().evaluate('abcde      = 123.98765') == 123.98765

def test_expressions():
    assert HCS().evaluate('1 + 2 + 3') == 6
    assert HCS().evaluate('3 * 3 / (-3 - 4)') == -1.2857142857142858

def test_statements():
    hcs = HCS()
    assert hcs.evaluate("a = 3; a; 123; 23423; b = a + 10") == 13
    source = """add_two = def(a, b) {
                            a + b
                         };
                x = add_two(10, 99);
                x + 1000
                """
    assert hcs.evaluate(source) == 1109
    
    source = """
       add_two = def(a, b) {
                    a + b;
                    c = 8;
                    avg_three = def(x, y, z) { (x + y + z) / 3 };
                    x = avg_three(a, b, c)
                 };
        y = add_two(7, 9);                
        y + 1000
    """
    assert hcs.evaluate(source) == 1008
    
    source = """
        add_two = def(a, b) {
                     a + b;
                     c = 8;
                     avg_three = def(x, y, z) { (x + y + z) / 3 };
                     x = avg_three(a, b, c);
                  };
        y = add_two(7, 9);                
        y = y + 1000;
        (def(r) { 
            r + 2000
        })(y);
    """ 
    assert hcs.evaluate(source) == 3008

    #without semicolons
    source = """
        add_two = def(a, b) {
                     a + b
                     c = 8
                     avg_three = def(x, y, z) { (x + y + z) / 3 }
                     x = avg_three(a, b, c)
                  };
        y = add_two(7, 9)
        y = y + 1000
        (def(r) { 
            r + 2000
        })(y)
    """ 
    assert hcs.evaluate(source) == 3008    

def test_function_calls():
    hcs = HCS()
    assert hcs.evaluate('add_ten = def(a) { a + 10 }; add_ten(2)') == 12
    assert hcs.evaluate("add_nums = def(a, b) { a + b } ; add_nums(4, 5)") == 9
    assert hcs.evaluate("add_two = def(a, b) { a + b } ; add_two(10, 99)") == 109

def test_builtin_function_calls():
    assert HCS().evaluate('sum(1, 2, 3)') == 6
    assert HCS().evaluate('max(345.234, 1345.232, 55.34, a = 123)') == 1345.232
    assert HCS().evaluate('a = 12; min(4545, a, 34, a = 1)') == 1
    assert HCS().evaluate('print(123)') == None #just print 123 in the screen

def test_anonymous_functions():
    hcs = HCS()
    assert(hcs.evaluate("""
        (def(a, b, c) { 
            sum(a, b, c)
        })(123, 456, 789)
    """)) == 1368

def test_named_functions():
    hcs = HCS()
    assert(hcs.evaluate("""
        def sum_this(a, b, c) { 
            sum(a, b, c);
        };
        x = sum_this(123, 456, 789);
    """)) == 1368


def test_prefix_posfix_operators():
    hcs = HCS()
    hcs.evaluate("a = 1; b = 1") # preparing variables to test
    assert hcs.evaluate("c = ++a") == 2
    assert hcs.evaluate("a") == 2
    assert hcs.evaluate("d = b++") == 1
    assert hcs.evaluate("b") == 2

# def test_ifelse():
#     hcs = HCS()
#     source = """
#         def test_bool (b) {
#             if (b) {
#                 1
#             }
#             else {
#                 0
#             }
#         };
#     """  
#     hcs.evaluate(source)
#     assert hcs.evaluate("test_bool(0)") == 0
#     assert hcs.evaluate("test_bool(1)") == 1
