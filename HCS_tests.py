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

def test_expressions():
    assert HCS().eval('1 + 2 + 3') == 6
    assert HCS().eval('3 * 3 / (-3 - 4)') == -1.2857142857142858

def test_statements():
    assert HCS().eval("a = 3; a; 123; 23423; b = a + 10") == 13

def test_functions():
    assert HCS().eval('addten = function(a) { a + 10 }; addten(2)') == 12
    hcs = HCS()
    hcs.eval("add_nums = function(a, b) { a + b }")
    hcs.eval("add_nums(4, 5)")
    #assert HCS().eval("""add_nums = function(a, b) {
    #                        a + b;
    #                    };
    #                    add_nums(10, 99);
    #                    """) == 109

def test_builtin_function_calls():
    assert HCS().eval('sum(1, 2, 3)') == 6
    assert HCS().eval('max(345.234, 1345.232, 55.34, a = 123)') == 1345.232
    assert HCS().eval('a = 12; min(4545, a, 34, a = 1)') == 1
    assert HCS().eval('print(123)') == None #just print 123 in the screen

if __name__ == '__main__':
    test_numbers()
    test_assignments()    
    test_expressions()
    test_statements()
    test_functions()
    test_builtin_function_calls()