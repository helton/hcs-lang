from HCS import HCS

def test_numbers():
    assert HCS().eval('123') == 123
    assert HCS().eval('123.456') == 123.456
    assert HCS().eval('123e2') == 123e2
    assert HCS().eval('.1') == .1
    assert HCS().eval('.12') == .12
    assert HCS().eval('9.1') == 9.1
    assert HCS().eval('98.1') == 98.1
    assert HCS().eval('1.') == 1.
    assert HCS().eval('12.') == 12.
    assert HCS().eval('1') == 1
    assert HCS().eval('12') == 12
    assert HCS().eval('4.5') == 4.5
    assert HCS().eval('-4.5') == -4.5
    assert HCS().eval('- 4.5') == -4.5
    assert HCS().eval('+ .1e10') == .1e10
    assert HCS().eval(' 1.01e-2') == 1.01e-2

def test_assignments():
    assert HCS().eval('a=123') == 123
    assert HCS().eval('a = b = c = 987654') == 987654
    assert HCS().eval('abcde      = 123.98765') == 123.98765

def test_expressions():
    assert HCS().eval('1 + 2 + 3') == 6
    assert HCS().eval('3 * 3 / (-3 - 4)') == -1.2857142857142858

def test_statements():
    assert HCS().eval("a = 3; a; 123; 23423; b = a + 10") == 13

def test_functions():
    hcs = HCS()
    assert hcs.eval('add_ten = def(a) { a + 10 }; add_ten(2)') == 12
    assert hcs.eval("add_nums = def(a, b) { a + b } ; add_nums(4, 5)") == 9
    assert hcs.eval("add_two = def(a, b) { a + b } ; add_two(10, 99)") == 109
    source = """add_two = def(a, b) {
                            a + b
                         };
                x = add_two(10, 99);
                x + 1000
                """
    assert hcs.eval(source) == 1109
    source = """add_two = def(a, b) {
                            a + b;
                            c = 8;
                            avg_three = def(x, y, z) { (x + y + z) / 3 };
                            x = avg_three(a, b, c)
                         };
                y = add_two(7, 9);                
                y + 1000
                """
    assert hcs.eval(source) == 1008    

def test_builtin_function_calls():
    assert HCS().eval('sum(1, 2, 3)') == 6
    assert HCS().eval('max(345.234, 1345.232, 55.34, a = 123)') == 1345.232
    assert HCS().eval('a = 12; min(4545, a, 34, a = 1)') == 1
    assert HCS().eval('print(123)') == None #just print 123 in the screen