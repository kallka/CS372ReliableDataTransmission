import random


# #################################################################################################################### #
# UnreliableChannel                                                                                                    #
#                                                                                                                      #
# Description:                                                                                                         #
# This class is meant to be more of a blackbox but you are allowed to see the implementation. You are not allowed to   #
# change anything in this file. There is also no need to base your algorithms on this particular implementation.       #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is not to be changed.                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class UnreliableChannel():
    RATIO_DROPPED_PACKETS = 0.1
    RATIO_DELAYED_PACKETS = 0.1
    RATIO_DATA_ERROR_PACKETS = 0.1
    RATIO_OUT_OF_ORDER_PACKETS = 0.1
    ITERATIONS_TO_DELAY_PACKETS = 5

    def __init__(self, canDeliverOutOfOrder_, canDropPackets_, canDelayPackets_, canHaveChecksumErrors_):
        self.send_queue = []
        self.receive_queue = []
        self.delayed_packets = []
        self.can_deliver_out_of_order = canDeliverOutOfOrder_
        self.can_drop_packets = canDropPackets_
        self.can_delay_packets = canDelayPackets_
        self.can_have_checksum_errors = canHaveChecksumErrors_
        # stats
        self.count_total_data_packets = 0
        self.count_sent_packets = 0
        self.count_checksum_error_packets = 0
        self.count_dropped_packets = 0
        self.count_delayed_packets = 0
        self.count_out_of_order_packets = 0
        self.count_ack_packets = 0
        self.current_iteration = 0

    def send(self,seg):
        self.send_queue.append(seg)

    def receive(self):
        new_list = list(self.receive_queue)
        self.receive_queue.clear()
        #print("UnreliableChannel len receiveQueue: {0}".format(len(self.receiveQueue)))
        return new_list

    def processData(self):
        #print("UnreliableChannel manage - len sendQueue: {0}".format(len(self.sendQueue)))
        self.current_iteration += 1

        if len(self.send_queue) == 0:
            return

        if self.can_deliver_out_of_order:
            val = random.random()
            if val <= UnreliableChannel.RATIO_OUT_OF_ORDER_PACKETS:
                self.count_out_of_order_packets += 1
                self.send_queue.reverse()

        # add in delayed packets
        no_longer_delayed = []
        for seg in self.delayed_packets:
            num_iter_delayed = self.current_iteration - seg.getStartDelayIteration()
            if num_iter_delayed >= UnreliableChannel.ITERATIONS_TO_DELAY_PACKETS:
                no_longer_delayed.append(seg)

        for seg in no_longer_delayed:
            self.count_sent_packets += 1
            self.delayed_packets.remove(seg)
            self.receive_queue.append(seg)

        for seg in self.send_queue:
            #self.receiveQueue.append(seg)

            add_to_receive_queue = False
            if self.can_delay_packets:
                val = random.random()
                if val <= UnreliableChannel.RATIO_DELAYED_PACKETS:
                    self.count_delayed_packets += 1
                    seg.setStartDelayIteration(self.current_iteration)
                    self.delayed_packets.append(seg)
                    continue

            if self.can_drop_packets:
                val = random.random()
                if val <= UnreliableChannel.RATIO_DROPPED_PACKETS:
                    self.count_dropped_packets += 1
                else:
                    add_to_receive_queue = True
            else:
                add_to_receive_queue = True

            if add_to_receive_queue:
                self.receive_queue.append(seg)
                self.count_sent_packets += 1

            if seg.acknum == -1:
                self.count_total_data_packets += 1

                # only data packets can have checksum errors...
                if self.can_have_checksum_errors:
                    val = random.random()
                    if val <= UnreliableChannel.RATIO_DATA_ERROR_PACKETS:
                        seg.createChecksumError()
                        self.count_checksum_error_packets += 1

            else:
                # count ack packets...
                self.count_ack_packets += 1

            #print("UnreliableChannel len receiveQueue: {0}".format(len(self.receiveQueue)))

        self.send_queue.clear()
        #print("UnreliableChannel manage - len receiveQueue: {0}".format(len(self.receiveQueue)))
