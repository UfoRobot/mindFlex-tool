#!/usr/bin/env python

from __future__ import division             # For float precision division. 
import serial
import time
import os


def read():

    # Choose a name for log file
    name = raw_input("Enter name for the session ")
    
    # This script doesn't know (yet) his current directory. This is where the logfiles are gonna be saved.
    # TODO: automatic set current working directory
    if os.path.exists('/Users/Ascanio/Documents/PPrograms/mindFlex/'+name+'.txt'):
        print "File exists"
        return
    else:
        f = open("/Users/Ascanio/Documents/PPrograms/mindFlex/"+name+".txt", 'w')

    # Select minimum signal strength 
    # All packets are going to be logged but only the filtered ones are gonna be used for stat-values
    dropLower = int(raw_input("Set mininum signal strength: (200 to accept them all) "))

    # Set the port your arduino is on. You can find it in the arduino IDE, right bottom corner.
    mindFlex = serial.Serial('/dev/tty.usbmodem1411', 9600)

    # Init sampleSum where to store sum of all accepted values
    sampleSum = dict.fromkeys(['signal', 'attention', 'meditation', 'delta', 'theta', 'lowAlpha', 'highAlpha', 'lowGamma', 'highGamma'], 0)
    sampleMax = dict.fromkeys(['signal', 'attention', 'meditation', 'delta', 'theta', 'lowAlpha', 'highAlpha', 'lowGamma', 'highGamma'], 0)
    # Manual max
    sampleMax['attention'] = 100
    sampleMax['meditation']=100
    sampleMean = {}
    sampleMeanN = {}
    count = 0

    
    try:
        while True:
            # packet is a string, ending with '/r/n'
            packet = mindFlex.readline()
            # Save on logfile
            f.writelines(packet)

            # Dropping '/r/n'
            packet = packet[:-4]
            print packet
            
            # Parsing using comas and inserting values (converted to numbers) into 'data' dictionary
            parsed = packet.split(',')
            data = {}
            data['signal'] = int(parsed[0])
            data['attention'] = int(parsed[1])
            data['meditation'] = int(parsed[2])
            data['delta'] = int(parsed[3])
            data['theta'] = int(parsed[4])
            data['lowAlpha'] = int(parsed[5])
            data['highAlpha'] = int(parsed[6])
            data['lowGamma'] = int(parsed[7])
            data['highGamma'] = int(parsed[8])

            if (data['signal'] > dropLower):
                print "Dropped"
                continue

            # +1 if packet's been accepted
            count += 1

            # Update sampleSum
            for key in data.keys():
                sampleSum[key] += data[key]
                if (data[key] > sampleMax[key]):
                    sampleMax[key] = data[key]
            





            print "Added"
    except KeyboardInterrupt:
        
        sampleMean = {key : (value/count) for (key,value) in sampleSum.items()}
        sampleMeanN = {key : (value/sampleMax[key]) for (key,value) in sampleMean.items()}
          
        print "Interrupted!"
        print "Sample sum"
        print sampleSum
        print "Sample mean"
        print sampleMean
        print "Max values"
        print sampleMax
        print "Normalized mean"
        print sampleMeanN
        
        # TODO: close serial comunication



        
        

        

if __name__ == "__main__":
    read()

