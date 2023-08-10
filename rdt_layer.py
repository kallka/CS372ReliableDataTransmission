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
    # TODO: Add items as needed

    # current window size?
    # current sequence num?
    # incoming ack num?
    # do we need to wait for no ack for x amount of time?
    # do we need to store data from server and/or client?

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
        # TODO: New Items
        self.dataTotalLength = 0
        self.currentSeqNum = 0
        self.currentAckNum = 0
        self.dataReceived = ''
        # TODO: Add items as needed
        self.outOfOrderPackets = 0
        self.countChecksumErrorPackets = 0
        # set a segment timeout?
        # set an Ack?
        # set a start size for window?
        # set a top size for window?
        # wait time?


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
        # ############################################################################################################ #
        # Identify the data that has been received...

        print('getDataReceived(): Complete this...')

        # ############################################################################################################ #
        return self.dataReceived

    # ################################################################################################################ #
    # helpReadData()                                                                                                   #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Takes a list that represents message read from unreliable channel and converts into strings associated with ACK  #
    # SEQ or Payload.                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def helpReadData(self, listToProcess):
        expectedAck = self.currentAckNum
        readableList = []

        # READ DATA and BASIC CHECKS
        #       1. Count out of order packets
        #       2. Checksum
        for index in range(0, len(listToProcess)):
            # if expectedAck does not match the index
            if listToProcess[index].payload != '':
                if expectedAck != listToProcess[index].seqnum:
                    self.outOfOrderPackets += 1
                # if there is data and it matches a checksum
                if listToProcess[index].checkChecksum() is True:
                    readableList.append([listToProcess[index].seqnum, listToProcess[index].payload])
                else:
                    self.countChecksumErrorPackets += 1
                    print("\t\t\t TALLY OUT OF ORDER: ", self.countChecksumErrorPackets)
            expectedAck += 1
        # RETURN IF EMPTY
        if len(readableList) == 0:
            return []

        # SORT PACKETS and STORE FIRST SEQNUM
        readableList.sort()
        firstSeqNum = readableList[0][0]

        # CHECKS FOR SEQNUM AND ACKNUM
        #   1. Does firstSeqNum match expected ack:
        if firstSeqNum != self.currentAckNum:
            return []
        #   2. Were any seqnum dropped and do we need a selective retransmit at that point?
        for num in range(0, len(readableList)):
            if readableList[num][0] - num != firstSeqNum:
                readableList = readableList[:num]              # remove remaining from list
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
        # print(f"\tLine 130: Data in rdt_layer.processData: {self.dataToSend}")
        # self.dataTotalLength = len(self.dataToSend)
        # print(f"\tLine 134: Length in rdt_layer.processData: {self.dataTotalLength}")
        # print(f"\tLine 135: Data in rdt_layer.processData: {self.getDataReceived}")
        print(f"\tCurrentAckNum: {self.currentAckNum}")
        print(f"\tCurrentSeqNum: {self.currentSeqNum}")
        self.currentIteration += 1
        self.processSend()
        self.processReceiveAndSendRespond()


    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment sending tasks for CLIENT                                                                         #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processSend(self):
        # ############################################################################################################ #
        print('processSend(): Complete this...')

        # TODO: Confirm ACK NUM
        receivedAck = self.receiveChannel.receiveQueue
        if len(receivedAck) == 1:
            if self.currentSeqNum+1 >= receivedAck[0].acknum:
                self.currentSeqNum = receivedAck[0].acknum
            print(f"\tLENGTH OF ACKS: {len(receivedAck)}")
            print(f"\tSEGS, ACKS: {receivedAck[0].seqnum}, {receivedAck[0].acknum}")

        # Divide data to send into maximum allowed per segment
        # TODO: Make more efficient
        segmentList = [self.dataToSend[i:i+self.DATA_LENGTH] for i in range(0, len(self.dataToSend), self.DATA_LENGTH)]

        # Pipeline segments to fit the flow-control window - RDTLayer.FLOW_CONTROL_WIN_SIZE until all data sent.
        # 3 Segments can be sent in 1 window as 1 (SEQ) + 4 (Payload)
        seqnum = self.currentSeqNum
        windowStart = seqnum
        segSize = int(self.FLOW_CONTROL_WIN_SIZE//self.DATA_LENGTH)     # Round down to fit all data in window size
        windowStop = seqnum + segSize

        if seqnum < len(segmentList):                          # TODO: may have to add check if last window not received
            for item in range(windowStart, windowStop):
                # Do we have data to send?
                if seqnum < len(segmentList):
                    # Set and display sending segment
                    segmentSend = Segment()
                    data = segmentList[seqnum]
                    segmentSend.setData(seqnum, data)
                    print("Sending segment: ", segmentSend.to_string())

                    # Use the unreliable sendChannel to send the segment
                    self.sendChannel.send(segmentSend)
                    seqnum += 1
                    self.currentSeqNum = seqnum



    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processReceiveAndSendRespond(self):
        segmentAck = Segment()                                  # Segment acknowledging packet(s) received

        # ############################################################################################################ #
        # What segments have been received?
        # How will you get them back in order?
        # This is where a majority of your logic will be implemented
        print('processReceive(): Complete this...')

        # This call returns a list of incoming segments (see Segment class)...
        listIncomingSegments = self.receiveChannel.receive()
        readableList = []                                       # Holds seq num and data

        if len(listIncomingSegments) > 0:
            # Extract and order items from segment
            # helpReadData will handle all error checking and return only usable items
            readableList = self.helpReadData(listIncomingSegments)

            for item in range(0, len(readableList)):
                self.dataReceived = self.dataReceived + readableList[item][1]
                self.currentSeqNum = readableList[item][0]

            # Store new AckNum that represents only accepted data
            self.currentAckNum += len(readableList)

        # ############################################################################################################ #
        # How do you respond to what you have received?
        # How can you tell data segments apart from ack segemnts?

        # Somewhere in here you will be setting the contents of the ack segments to send.
        # The goal is to employ cumulative ack, just like TCP does...
        acknum = self.currentAckNum

        # ############################################################################################################ #
        # Display response segment
        segmentAck.setAck(acknum)
        print("Sending ack: ", segmentAck.to_string())

        # Use the unreliable sendChannel to send the ack packet
        self.sendChannel.send(segmentAck)
