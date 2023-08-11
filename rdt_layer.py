from segment import Segment


# #################################################################################################################### #
# RDTLayer                                                                                                             #
#                                                                                                                      #
# Description:                                                                                                         #
# The reliable data transfer (RDT) layer is used as a communication layer to resolve issues over an unreliable         #
# channel.                                                                                                             #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is meant to be changed.                                                                                    #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class RDTLayer(object):
    # ################################################################################################################ #
    # Class Scope Variables                                                                                            #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    DATA_LENGTH = 4 # in characters                     # The length of the string data that will be sent per packet...
    FLOW_CONTROL_WIN_SIZE = 15 # in characters          # Receive window size for flow-control
    sendChannel = None
    receiveChannel = None
    dataToSend = ''
    currentIteration = 0                                # Use this for segment 'timeouts'

    # ################################################################################################################ #
    # __init__()                                                                                                       #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None
        self.dataToSend = ''
        self.currentIteration = 0
        self.countSegmentTimeouts = 0

        # Add segment list so that don't need to recreate each time
        self.segmentlist = ''

        # Added items for window, seq, ack and data received
        self.windowStart = 0
        self.windowStop = 0
        self.currentSeqNum = 0
        self.currentAckNum = 0
        self.dataReceived = ''

        # Added items for wait and counting outOfOrder, checksumError, droppedPackets
        self.wait = 0
        self.outOfOrderPackets = 0
        self.countChecksumErrorPackets = 0
        self.countDroppedAckPackets = 0


    # ################################################################################################################ #
    # setSendChannel()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable sending lower-layer channel                                                 #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # ################################################################################################################ #
    # setReceiveChannel()                                                                                              #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable receiving lower-layer channel                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # ################################################################################################################ #
    # setDataToSend()                                                                                                  #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the string data to send                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setDataToSend(self, data):
        self.dataToSend = data

    # ################################################################################################################ #
    # getDataReceived()                                                                                                #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to get the currently received and buffered string data, in order                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def getDataReceived(self):
        return self.dataReceived

    # ################################################################################################################ #
    # helpReadData()                                                                                                   #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # - Takes a list that represents segments read from unreliable channel and converts into data strings with SeqNum. #
    # - Performs checks on reliability of data: checksum, order of seq, compares to ack num.                           #
    # - Only returns valid data and seq numbers so that processSendAndReceive send back the ACK needed for go-back-n   #
    #                                                                                                                  #
    # ################################################################################################################ #
    def helpReadData(self, listToProcess):
        expectedAck = self.currentAckNum            # create variable for the expected ACK number
        readableList = []

        # READ DATA and BASIC CHECKS - out of order and checksum
        for index in range(0, len(listToProcess)):
            if listToProcess[index].payload != '':
                # is it out of order?
                if expectedAck != listToProcess[index].seqnum:
                    self.outOfOrderPackets += 1
                # is the checksum True?
                if listToProcess[index].checkChecksum() is True:
                    readableList.append([listToProcess[index].seqnum, listToProcess[index].payload])
                else:
                    self.countChecksumErrorPackets += 1
            # increment an expectedAck local variable
            expectedAck += 4

        # RETURN IF EMPTY - no valid packets sent
        if len(readableList) == 0:
            return []

        # SORT PACKETS and STORE FIRST SEQNUM
        readableList.sort()

        # # CHECKS FOR SEQNUM AND ACKNUM
        # #   Does seq match ack? If not go-back-n immediately
        for num in range(0, len(readableList)):
            if readableList[num][0] - num != self.currentAckNum:
                readableList = readableList[:num]              # remove 'n' remaining from list
                break

        # RETURN : only sends back usable elements
        return readableList

    # ################################################################################################################ #
    # processData()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # "timeslice". Called by main once per iteration                                                                   #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processData(self):
        self.currentIteration += 1
        self.processSend()
        self.processReceiveAndSendRespond()


    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Confirms ACK, looks for timeouts, processes data to send.                                                        #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processSend(self):
        receivedAck = self.receiveChannel.receiveQueue

        # CHECK WAIT TIME
        if self.currentIteration > 1 and len(receivedAck) == 0:
            if self.wait == 3:
                self.currentSeqNum = self.windowStart * 4
                self.countSegmentTimeouts += 1
            else:
                self.wait += 1
                return

        # CHECK ACK NUMS
        if len(self.dataToSend) > 0 and len(receivedAck) == 1:
            # expected data in ack
            if self.currentSeqNum + 4 == receivedAck[0].acknum:
                self.currentSeqNum = receivedAck[0].acknum
            # 3 iterations have passed and expected ack not received
            elif self.currentSeqNum + 4 > receivedAck[0].acknum and self.wait >= 3:
                self.countDroppedAckPackets += 1
                self.currentSeqNum = receivedAck[0].acknum
                self.wait = 0
            else:
                self.wait += 1
                return

        # Divide data to send into maximum allowed per segment on first iteration
        if self.currentIteration == 1:
            self.segmentlist = [self.dataToSend[i:i+self.DATA_LENGTH] for i in range(0, len(self.dataToSend), self.DATA_LENGTH)]

        # Pipeline segments to fit the flow-control window - RDTLayer.FLOW_CONTROL_WIN_SIZE until all data sent.
        # 3 Segments can be sent in 1 window as 15// 4 (Payload)
        seqnum = self.currentSeqNum
        self.windowStart = seqnum // 4
        segSize = int(self.FLOW_CONTROL_WIN_SIZE//self.DATA_LENGTH)     # Round down to fit all data in window size
        self.windowStop = self.windowStart + segSize

        if self.windowStart < len(self.segmentlist):
            for index in range(self.windowStart, self.windowStop):
                # Do we have data to send?
                if index < len(self.segmentlist):
                    # Set and display sending segment
                    segmentSend = Segment()
                    data = self.segmentlist[index]
                    seqnum = index*4
                    segmentSend.setData(seqnum, data)
                    print("Sending segment: ", segmentSend.to_string())

                    # Use the unreliable sendChannel to send the segment
                    self.sendChannel.send(segmentSend)
                    self.currentSeqNum = seqnum



    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    # Sends to helpReadData for processing help                                                                        #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processReceiveAndSendRespond(self):
        segmentAck = Segment()                                  # Segment acknowledging packet(s) received

        # ############################################################################################################ #
        # What segments have been received?
        # How will you get them back in order?
        # This is where a majority of your logic will be implemented

        # This call returns a list of incoming segments (see Segment class)...
        listIncomingSegments = self.receiveChannel.receive()
        readableList = []                                           # Will hold seq num and data

        if len(listIncomingSegments) > 0:
            # Extract and order items from segment
            # helpReadData will handle all error checking and return only usable items
            readableList = self.helpReadData(listIncomingSegments)

            for item in range(0, len(readableList)):
                self.dataReceived = self.dataReceived + readableList[item][1]
                self.currentSeqNum = readableList[item][0]

            # Store new AckNum that represents only accepted data
            self.currentAckNum += 4*len(readableList)

        # Display and send response segment (if self.dataToSend checks if server or client)
        acknum = self.currentAckNum

        segmentAck.setAck(acknum)
        if len(self.dataToSend) == 0:
            print("Sending ack: ", segmentAck.to_string())
            # Use the unreliable sendChannel to send the ack packet
            self.sendChannel.send(segmentAck)
