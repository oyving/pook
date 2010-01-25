#!/usr/bin/env python
#
# an Ook! interpreter written in python
#
# you can wrap the memory pointer to the end of the the memory cells
# but you cannot do the same trick to get the first cell, since going
# further out would just initiate a new memory cell.
#
# 2001 (C) Øyvind Grønnesby <oyving@pvv.ntnu.no>
#
# 2003-02-06: Thanks to John Farrell for spotting a bug!

import sys, string, types

def massage(text):
    ret = []
    tok = []

    for line in text:
        if line[0] != ";" and line != "\n" and line != "":
            for token in line.split(" "):
                if token != "":
                    ret.append(token.strip())
    return ret

def sane(code):
    if len(code) % 2 == 0:
        return 1
    else:
        return 0

class OokInterpreter:

    memory = [0]
    memptr = 0
    file   = None
    code   = None
    len    = 0
    codei  = 0

    def __langinit(self):
        self.lang   = {'Ook. Ook?' : self.mvptrup,
                       'Ook? Ook.' : self.mvptrdn,
                       'Ook. Ook.' : self.incptr,
                       'Ook! Ook!' : self.decptr,
                       'Ook. Ook!' : self.readc,
                       'Ook! Ook.' : self.prntc,
                       'Ook! Ook?' : self.startp,
                       'Ook? Ook!' : self.endp}

    def mem(self):
        return self.memory[self.memptr]

    def __init__(self, file):
        self.__langinit()
        self.file = open(file)
        self.code = massage(self.file.readlines())
        self.file.close()
        if not sane(self.code):
            print self.code
            raise "OokSyntaxError", "Code not sane."
        else:
            self.cmds()

    def run(self):
        self.codei = 0
        self.len  = len(self.code)
        while self.codei < self.len:
            self.lang[self.code[self.codei]]()
            self.codei += 1

    def cmds(self):
        i = 0
        l = len(self.code)
        new = []
        while i < l:
            new.append(string.join((self.code[i], self.code[i+1]), " "))
            i += 2
        self.code = new

    def startp(self):
        ook = 0
        i   = self.codei
        if self.memory[self.memptr] != 0:
            return None
        while 1:
            i += 1
            if self.code[i] == 'Ook! Ook?':
                ook += 1
            if self.code[i] == 'Ook? Ook!':
                if ook == 0:
                    self.codei = i
                    break
                else:
                    ook -= 1
            if i >= self.len:
                raise 'OokSyntaxError', 'Unmatched "Ook! Ook?".'

    def endp(self):
        ook = 0
        i   = self.codei
        if self.memory[self.memptr] == 0:
            return None
        if i == 0:
            raise 'OokSyntaxError', 'Unmatched "Ook? Ook!".'
        while 1:
            i -= 1
            if self.code[i] == 'Ook? Ook!':
                ook += 1
            if self.code[i] == 'Ook! Ook?':
                if ook == 0:
                    self.codei = i
                    break
                else:
                    ook -= 1
            if i <= 0:
                raise 'OokSyntaxError', 'Unmatched "Ook? Ook!".'

    def incptr(self):
        self.memory[self.memptr] += 1

    def decptr(self):
        self.memory[self.memptr] -= 1

    def mvptrup(self):
        self.memptr += 1
        if len(self.memory) <= self.memptr:
            self.memory.append(0)

    def mvptrdn(self):
        if self.memptr == 0:
            self.memptr = len(self.memory) - 1
        else:
            self.memptr -= 1

    def readc(self):
        self.memory[self.memptr] = ord(sys.stdin.read(1))

    def prntc(self):
        sys.stdout.write(chr(self.mem()))


if __name__ == '__main__':
    o = OokInterpreter(sys.argv[1])
    o.run()
