from HCS import HCS

def do_test(expression, expected):
    got_it = HCS().eval(expression)
    if got_it != expected:
        print('FAIL: [Expression "%s"] Got it "%s" but "%s" expected' % (expression, repr(got_it), repr(expected)))

def test_numbers():
    do_test('123',  123)
    do_test('123.456', 123.456)    
    do_test('123e2', 123e2)
    do_test('.1', .1)
    do_test('.12', .12)
    do_test('9.1', 9.1)
    do_test('98.1', 98.1)
    do_test('1.', 1.)
    do_test('12.', 12.)
    do_test('1', 1)
    do_test('12', 12)
    do_test('4.5', 4.5)
    do_test('-4.5', -4.5)
    do_test('- 4.5', -4.5)
    do_test('+ .1e10', .1e10)
    do_test(' 1.01e-2', 1.01e-2)

def test_assignments():
    do_test('a=123', 123)    

def test_expressions():
    do_test('1 + 2 + 3', 6)    
    do_test('3 * 3 / (-3 - 4)', -1.2857142857142858)        

def test_statements():
    do_test("a = 3; a; 123; 23423; b = a + 10", 13)

def test_function_definition():
    do_test("""
        def add_nums(a, b) {
            2 + 3 
        }""", None)

if __name__ == '__main__':
    test_numbers()
    test_assignments()    
    test_expressions()
    test_statements()
    test_function_definition()
