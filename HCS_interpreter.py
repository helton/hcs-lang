#!/usr/bin/env python3

import traceback
from HCS import HCS

def interpret_loop():

    def print_welcome():
        size = 50
        print("=" * size)
        print("HCS Programming Language Interpreter")
        print("=" * size)
        print("Author: Helton Carlos de Souza")
        print("Type 'quit' or 'exit' to end.")
        print("=" * size)

    print_welcome()
    hcs = HCS()
    command_count = 1
    while True:
        print("[%03d]>> " % (command_count), end="")
        try:
            command = input()
            command_count += 1
        except EOFError as e:
            print()
            return            
        if command in ['quit', 'exit']:
            return
        try:
            print(hcs.evaluate(command))            
        except Exception as e:
            #print("%s: %s" % (e.__class__.__name__, str(e)))
            traceback.print_exc()

if __name__ == '__main__':
    interpret_loop()
