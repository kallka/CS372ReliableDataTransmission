from rdt_layer import *
from unreliable import UnreliableChannel

# #################################################################################################################### #
# Main                                                                                                                 #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #

# #################################################################################################################### #
# The following are two sets of data input to the communication test. The first is small and the second is longer.     #
# Start by uncomming the shorter until you feel you have a good algorithm. Then confirm it still works on a larger     #
# scale by switching to the larger.                                                                                    #
#                                                                                                                      #
# #################################################################################################################### #

data_to_send = "The quick brown fox jumped over the lazy dog"

# data_to_send = "\r\n\r\n...We choose to go to the moon. We choose to go to the moon in this "\
# "decade and do the other things, not because they are easy, but because they are hard, "\
# "because that goal will serve to organize and measure the best of our energies and skills, "\
# "because that challenge is one that we are willing to accept, one we are unwilling to "\
# "postpone, and one which we intend to win, and the others, too."\
# "\r\n\r\n"\
# "...we shall send to the moon, 240,000 miles away from the control station in Houston, a giant "\
# "rocket more than 300 feet tall, the length of this football field, made of new metal alloys, "\
# "some of which have not yet been invented, capable of standing heat and stresses several times "\
# "more than have ever been experienced, fitted together with a precision better than the finest "\
# "watch, carrying all the equipment needed for propulsion, guidance, control, communications, food "\
# "and survival, on an untried mission, to an unknown celestial body, and then return it safely to "\
# "earth, re-entering the atmosphere at speeds of over 25,000 miles per hour, causing heat about half "\
# "that of the temperature of the sun--almost as hot as it is here today--and do all this, and do it "\
# "right, and do it first before this decade is out.\r\n\r\n"\
# "JFK - September 12, 1962\r\n"

# #################################################################################################################### #

# Create client and server
client = RDTLayer()
server = RDTLayer()

# Start with a reliable channel (all flags false)
# As you create your rdt algorithm for send and receive, turn these on.
out_of_order = False
drop_packets = False
delay_packets = False
data_errors = False

# Create unreliable communication channels
client_to_server_channel = UnreliableChannel(out_of_order, drop_packets, delay_packets, data_errors)
server_to_client_channel = UnreliableChannel(out_of_order, drop_packets, delay_packets, data_errors)

# Creat client and server that connect to unreliable channels
client.setSendChannel(client_to_server_channel)
client.setReceiveChannel(server_to_client_channel)
server.setSendChannel(server_to_client_channel)
server.setReceiveChannel(client_to_server_channel)

# Set initial data that will be sent from client to server
client.setDataToSend(data_to_send)

loop_iter = 0            # Used to track communication timing in iterations
while True:
    print("-----------------------------------------------------------------------------------------------------------")
    loop_iter += 1
    print("Time (iterations) = {0}".format(loop_iter))

    # Sequence to pass segments back and forth between client and server
    print("Client------------------------------------------")
    client.processData()
    client_to_server_channel.processData()
    print("Server------------------------------------------")
    server.processData()
    server_to_client_channel.processData()

    # show the data received so far
    print("Main--------------------------------------------")
    data_received_from_client = server.getDataReceived()
    print("DataReceivedFromClient: {0}".format(data_received_from_client))

    if data_received_from_client == data_to_send:
        print('$$$$$$$$ ALL DATA RECEIVED $$$$$$$$')
        break

    # time.sleep(0.1)
    input("Press enter to continue...")

print("countTotalDataPackets: {0}".format(client_to_server_channel.count_total_data_packets))
print("countSentPackets: {0}".format(client_to_server_channel.count_sent_packets + server_to_client_channel.count_sent_packets))
print("countChecksumErrorPackets: {0}".format(client_to_server_channel.count_checksum_error_packets))
print("countOutOfOrderPackets: {0}".format(client_to_server_channel.count_out_of_order_packets))
print("countDelayedPackets: {0}".format(client_to_server_channel.count_delayed_packets + server_to_client_channel.count_delayed_packets))
print("countDroppedDataPackets: {0}".format(client_to_server_channel.count_dropped_packets))
print("countAckPackets: {0}".format(server_to_client_channel.count_ack_packets))
print("countDroppedAckPackets: {0}".format(server_to_client_channel.count_dropped_packets))

print("# segment timeouts: {0}".format(client.countSegmentTimeouts))

print("TOTAL ITERATIONS: {0}".format(loop_iter))
