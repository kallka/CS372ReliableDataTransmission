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
        self.currentAckNum = -1
        self.dataReceived = ''
        # TODO: Add items as needed
        # set a segment timeout?
        # set an Ack?
        # set a start size for window?
        # set a top size for window?
        # who am I talking to? server or client
        # wait time?
        self.whoAmI = None                  #'CLIENT' or 'SERVER'


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
        readableList = []
        for index in range(0, len(listToProcess)):
            # if there is data and it matches a checksum
            if listToProcess[index].payload != '':
                readableList.append([listToProcess[index].seqnum, listToProcess[index].payload])
        readableList.sort()
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

        # print(f"\tLine 130: Data in rdt_layer.processData: {self.dataToSend}")
        # self.dataTotalLength = len(self.dataToSend)
        # print(f"\tLine 134: Length in rdt_layer.processData: {self.dataTotalLength}")
        # print(f"\tLine 135: Data in rdt_layer.processData: {self.getDataReceived}")
        # print(self.currentAckNum)

        self.processSend()
        self.processReceiveAndSendRespond()


    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment sending tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processSend(self):
        segmentSend = Segment()

        # ############################################################################################################ #
        print('processSend(): Complete this...')
        # Determine if this is client.RdtLayer() or server.RdtLayer()
        if len(self.dataToSend) > 0:
            self.whoAmI = 'CLIENT'
        else:
            self.whoAmI = 'SERVER'


        # You should pipeline segments to fit the flow-control window
        # The flow-control window is the constant RDTLayer.FLOW_CONTROL_WIN_SIZE
        # The maximum data that you can send in a segment is RDTLayer.DATA_LENGTH
        # These constants are given in # characters


        # Somewhere in here you will be creating data segments to send.
        # The data is just part of the entire string that you are trying to send.
        # The seqnum is the sequence number for the segment (in character number, not bytes)

        seqnum = self.currentSeqNum
        data = self.dataToSend

        # ############################################################################################################ #
        # Display sending segment
        segmentSend.setData(seqnum,data)
        print("Sending segment: ", segmentSend.to_string())

        # Use the unreliable sendChannel to send the segment
        self.sendChannel.send(segmentSend)

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
            # 1. What items are in the list of incoming segments
            readableList = self.helpReadData(listIncomingSegments)
            for item in range(0, len(readableList)):
                self.dataReceived = self.dataReceived + readableList[item][1]

            # 2. Add on to old ack

        # ############################################################################################################ #
        # How do you respond to what you have received?
        # How can you tell data segments apart from ack segemnts?
        print('processReceive(): Complete this...')

        # Somewhere in here you will be setting the contents of the ack segments to send.
        # The goal is to employ cumulative ack, just like TCP does...
        acknum = "0"


        # ############################################################################################################ #
        # Display response segment
        segmentAck.setAck(acknum)
        print("Sending ack: ", segmentAck.to_string())

        # Use the unreliable sendChannel to send the ack packet
        self.sendChannel.send(segmentAck)
