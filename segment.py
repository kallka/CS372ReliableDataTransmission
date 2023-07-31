import random
from functools import reduce


# #################################################################################################################### #
# Segment                                                                                                              #
#                                                                                                                      #
# Description:                                                                                                         #
# The segment is a segment of data to be transferred on a communication channel.                                       #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is not to be changed.                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class Segment():

    def __init__(self):
        self.seqnum = -1
        self.acknum = -1
        self.payload = ''
        self.checksum = 0
        self.start_iteration = 0
        self.start_delay_iteration = 0

    def setData(self,seq,data):
        self.seqnum = seq
        self.acknum = -1
        self.payload = data
        self.checksum = 0
        str = self.toString()
        self.checksum = self.calcChecksum(str)

    def setAck(self,ack):
        self.seqnum = -1
        self.acknum = ack
        self.payload = ''
        self.checksum = 0
        str = self.toString()
        self.checksum = self.calcChecksum(str)

    def setStartIteration(self,iteration):
        self.start_iteration = iteration

    def getStartIteration(self):
        return self.start_iteration

    def setStartDelayIteration(self,iteration):
        self.start_delay_iteration = iteration

    def getStartDelayIteration(self):
        return self.start_delay_iteration

    def toString(self):
        return "seq: {0}, ack: {1}, data: {2}"\
        .format(self.seqnum, self.acknum, self.payload)         # TODO: check this ".format"

    def checkChecksum(self):
        cs = self.calcChecksum(self.toString())
        return cs == self.checksum

    def calcChecksum(self, str):
        return reduce(lambda x, y: x+y, map(ord, str))

    def printToConsole(self):
        print(self.toString())

    # Function to cause an error - Do not modify
    def createChecksumError(self):
        if not self.payload:
            return
        char = random.choice(self.payload)
        self.payload = self.payload.replace(char, 'X', 1)