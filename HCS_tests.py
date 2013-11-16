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

def test_function_definition():
    assert HCS().eval("""
        def add_nums(a, b) {
            2 + 3 
        }""") is None

if __name__ == '__main__':
    test_numbers()
    test_assignments()    
    test_expressions()
    test_statements()
    test_function_definition()