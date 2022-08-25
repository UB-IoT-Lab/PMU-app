import datetime
import socket
import sys
import statistics
# import pandas as pd
# import ntplib
import time
import re

import sqlite3

conn = sqlite3.connect('db/pmu_database')
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS data2
          ( count [INTEGER],
            time_stamp [INTEGER],
            arduino_min [INTEGER],
            arduino_sec [FLOAT],
            server_min [INTEGER],
            server_sec [FLOAT],
            diff [FLOAT],
            roll_mean [FLOAT],
            pha_mag [INTEGER],
            pha_ang [FLOAT],
            pha_freq [INTEGER],
            pps [INTEGER],
            pac_seq[INTEGER],
	    ident[INTEGER],
		pmu_ident[INTEGER]);
          ''')

conn.commit()
# from matplotlib import pyplot as plt

# Function to convert signed values to unsigned


def s16(value):
    return -(value & 0x8000) | (value & 0x7fff)

# Function to return current milliseconds


def milli():
    return round(time.time() * 1000)


def create_socket():
    try:
        global host
        global port
        global s
        host = "0.0.0.0"
        port = 7777
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    except socket.error as msg:
        print("Socket creation error" + str(msg))


def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the port " + str(port))
        s.bind((host, port))
        # s.listen(5)

    except socket.error as msg:
        print("Socket binding error"+str(msg)+"\n"+"Retrying...")
        bind_socket()


def socket_accept():
    packets = 7500

    Packet_Data, Magnitude, Phase, Minutes, Seconds, Phasor, Comp_Min,  Comp_Sec, Difference, Packets_gen = [
    ], [], [], [], [], [], [], [], [], []

    Packets_sen, Packet_size, Frequency, ROCOF, Phasor_id = [], [], [], [], []

    Delay_cal = [0] * 100
    time_stamp = 0
    diff = 0
    count = 0
    a = 20
    m = 0
    phasor_id_old = 100
    packets_lost = 0
    flag = False
    Delay_diff = 0
    Delay_diff_old = 0
    jitter = 0
    search = ['!', '#', 'x', 'X', '&']
    Rolling_Mean = 0
    Mean_Flag = False
    sent_milli = 0
    message = '1'
    Packets_rec = 0
    skip = 20
    print("Listening")
    # data,address = s.recvfrom(1024)
    # print("Connection has been established " + " IP : " + str(address[0])+ " Port : " + str(address[1]))
    # send_command(address)

    try:

        while True:

            data, addr = s.recvfrom(1024)
            Packet_Data = (data.decode())
            curr_time = datetime.datetime.now()

            check = True
            # Function to skip packets which do not conform to the standard set
            # for i in range(len(data)):
            #     if (not (bool(re.match("(?:([a-f]|[0-9]))", data[i])))):
            #         check = False
            #         print("************  skipped  **************")
            if check:
                count += 1
                Packets_rec += 1
                print(sys.getsizeof(data))

                print("{} : {} , {} , {} , {}, {}, {}, {}, {}".format(count, int(Packet_Data[0:8], 16),
                                                                      int(Packet_Data[8:16], 16), int(
                                                                          Packet_Data[16:20], 16),
                                                                      (s16(
                                                                          int(Packet_Data[20:24], 16)) * 180 / 31400),
                                                                      int(Packet_Data[24:28], 16), int(
                                                                          Packet_Data[30:32], 16),
                                                                      int(Packet_Data[32:34], 16), Packet_Data[34:39]))

                # Get UDP_Server (current) Time in seconds
                sys_timestamp = float(curr_time.strftime(
                    '%S')) + (float(curr_time.strftime('%f')) / 1000000)
                arduino_unix = datetime.datetime.utcfromtimestamp(
                    (int(Packet_Data[0:8], 16)))
                Mag = int(Packet_Data[16:20], 16) * 2 / 10000
                Pha = (s16(int(Packet_Data[20:24], 16)) * 180 / 31400)
                Fre = (int(Packet_Data[24:28], 16)) / 100
                identifier = int(Packet_Data[34:39])
                pmu_identifier = int(Packet_Data[39:46])
                # RCF = (int(Packet_Data[34:38], 16)) / 100
                Min = arduino_unix.strftime('%M')
                Sec = int(arduino_unix.strftime('%S')) + \
                    int(Packet_Data[8:16], 16) / 1000000
                Rate = int(Packet_Data[30:32], 16)  # Phasor reporting rate
                P_ID = int(Packet_Data[32:34], 16)  # Phasor ID
                Server_min = float(curr_time.strftime('%M'))
                diff = (Server_min * 60 - float(Min) * 60) + \
                    (sys_timestamp - Sec)  # Delay
                print(diff)
                print("Test identifier {}".format(identifier))
                print("PMU identifier {}".format(pmu_identifier))
                # Rolling mean Calculation to send feedback ######################################

                Delay_cal[m] = diff
                m += 1

                if m == 100:
                    m = 0
                    Mean_Flag = True

                if Mean_Flag:
                    Rolling_Mean = statistics.mean(Delay_cal)
                    print(Rolling_Mean)

                c.execute("insert into data2 (count,time_stamp,arduino_min,arduino_sec,server_min,server_sec,diff,roll_mean,pha_mag,\
                    pha_ang,pha_freq,pps,pac_seq,ident,pmu_ident) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                          (count, curr_time, Min, Sec, Server_min, sys_timestamp, diff, Rolling_Mean, Mag, Pha, Fre, Rate, P_ID, identifier, pmu_identifier))

                conn.commit()
                # try:
                #     outFile = open('P4Output.txt','a')
                #     #outFile.write("{} {}\n".format(diff,Rolling_Mean))
                #     outFile.write("{} : {} , {} , {} , {}, {}, {}, {}\n".format(count, int(Packet_Data[0:8], 16),
                #                                                   int(Packet_Data[8:16], 16), int(Packet_Data[16:20], 16),
                #                                                   (s16(int(Packet_Data[20:24], 16)) * 180 / 31400),
                #                                                   int(Packet_Data[24:28], 16), int(Packet_Data[30:32], 16),
                #                                                   int(Packet_Data[32:34], 16)))
                #     outFile.close()
                # except IOError as errno:
                #     print("I/O error({0})".format(errno))
                # Jitter Calculation ######################################

                # if count > 1:
                #     Delay_diff = diff
                #     jitter = jitter + abs(Delay_diff - Delay_diff_old)
                #     # if (count > 10):
                #         # print(jitter / (count - 2))

                # Delay_diff_old = diff

                # Packet Loss Calculation ################################

                # if count > 5:
                #     if ((P_ID - phasor_id_old) > 1 and (P_ID - phasor_id_old) < 99 and (flag == False)):
                #         packets_lost = packets_lost + (P_ID - phasor_id_old - 1)
                #     elif (((P_ID - phasor_id_old) < -2) and ((P_ID - phasor_id_old) > -99)):
                #         packets_lost = packets_lost + (P_ID - (phasor_id_old - 101) - 1)

                # flag = False

                # if diff > 10 or diff < (-10):
                #     diff = 1
                # if (P_ID - phasor_id_old) == -1:
                #     packets_lost = packets_lost - 1
                #     flag = True

                # if packets_lost < 0:
                #     packets_lost = 0

                # phasor_id_old = P_ID
                #########################################################

                # Magnitude.append(Mag)
                # Phase.append(Pha)
                # Frequency.append(Fre)
                # ROCOF.append(RCF)
                # Minutes.append(Min)
                # Seconds.append(Sec)
                # Phasor.append(Rate)

                # Comp_Min.append(float(curr_time.strftime('%M')))
                # Comp_Sec.append(sys_timestamp)
                # Difference.append(diff)

                # Phasor_id.append(P_ID)
                # Packet_size.append(sys.getsizeof(data))

            # if Packets_rec == packets:
            #     Packets_gen = Packets_rec + packets_lost
            #     jitter = jitter / (count - 2)
            #     break

            #     try:
            #         outFile = open('P4Output.txt','a')
            #         outFile.write("{} {}\n".format(diff,Rolling_Mean))
            #         outFile.close()
            #     except IOError as errno:
            #         print("I/O error({0})".format(errno))

            # println(Sec,end=" \n")
            # print(server_time-client_response,end="")
    except socket.error as msg:
        print(msg)
        s.close()
        # outFile.close()

# def send_command(address):
#     while True:
#         cmd = input()
#         if cmd == 'quit' :
#             s.close()
#             sys.exit()
#         if len(str.encode(cmd)) > 0:
#             s.sendto(bytes(cmd,'utf-8'),address)
#             data,addr = s.recvfrom(1024)
#             client_response = data.decode('utf-8')
#             print(client_response,end="")


def main():
    create_socket()
    bind_socket()

    while True:
        # num = input('Accept data ? ')
        # if num=='y':
        socket_accept()
        # else:
        #     s.close()
        #     break


main()
