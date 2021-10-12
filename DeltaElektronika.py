#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Delta Elektronika SM15K Communication Socket Library.
#
# Revision: @keklikyusuf
# 0.0.1: Initial version


import socket
import threading
import time
import csv
import datetime
import sys

""" Module to handle communication with DELTA POWER SUPPLY  """

__version__ = "0.0.1"  # semVersion (Major.Minor.Revision)

IPV4 = "169.254.100.243"


class ColorPrinter:

    purple = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    normal = '\033[0m'

    def __init__(self):
        """
        :param color: Enter desired color that has been alredy defined at BColors class!
        Funtional printing object is being created. For seperation spacer can be changed according to wishes.
        """
        self.spacer = '------------------------------------------------------------------------------------'

    def printError(self, message):
        """
        :param message: Text message that wanted to be printed
        :return: This function returns to printed text message
        Any message is being printed with defined stamp to create functional colorful printing
        """
        sys.stdout.write(ColorPrinter.red)
        now = datetime.datetime.now()
        text = f'{now.strftime("%d/%m/%Y - %X")}: {message} \n{self.spacer}'
        print(text)
        return text

    def printFeedback(self, message):
        """
        :param message: Text message that wanted to be printed
        :return: This function returns to printed text message
        Any message is being printed with defined stamp to create functional colorful printing
        """
        sys.stdout.write(ColorPrinter.green)
        now = datetime.datetime.now()
        text = f'{now.strftime("%d/%m/%Y - %X")}: {message} \n{self.spacer}'
        print(text)
        return text

    def printComment(self, message):
        """
        :param message: Text message that wanted to be printed
        :return: This function returns to printed text message
        Any message is being printed with defined stamp to create functional colorful printing
        """
        sys.stdout.write(ColorPrinter.blue)
        now = datetime.datetime.now()
        text = f'{now.strftime("%d/%m/%Y - %X")}: {message} \n{self.spacer}'
        print(text)
        return text

    def printNormal(self, message):
        """
        :param message: Text message that wanted to be printed
        :return: This function returns to printed text message
        Any message is being printed with defined stamp to create functional colorful printing
        """
        sys.stdout.write(ColorPrinter.normal)
        now = datetime.datetime.now()
        text = f'{now.strftime("%d/%m/%Y - %X")}: {message} \n{self.spacer}'
        print(text)
        return text


class Communication:
    """
    Class attributers that are set according to device settings.
    """
    port_name = 8462
    buffer_size = 1024
    timeout = 10

    def __init__(self, IPV4):
        """
        :param IPV4: Decive IP Address which must be set accordingly!
        """
        self.IPV4 = IPV4
        # self.communication = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.communication.settimeout(Communication.timeout)

    def __str__(self):
        return f'This is created to be able to communicate with Delta! Connect is the father class!'

    @staticmethod
    def openSocket():
        communication = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        communication.settimeout(Communication.timeout)
        return communication

    def sendMessage(self, message):
        """
        :param message: Message that is going to be sent to Delta which works as command lines!
        :return: It returns the message has been sent to Delta!
        """
        send_message = bytes(message, 'utf-8')
        communication = Communication.openSocket()
        communication.connect((self.IPV4, Communication.port_name))
        communication.send(send_message)
        communication.close()
        ColorPrinter.printFeedback(f'{send_message} has been sent to Delta!')
        return send_message

    def sendReceiveMessage(self, message):
        """
        :param message: Message that is going to be sent to Delta to get back as query!
        :return: It returns the message has been received from Delta!
        """
        send_message = bytes(message, 'utf-8')
        communication = Communication.openSocket()
        communication.connect((self.IPV4, Communication.port_name))
        communication.send(send_message)
        communication_message = communication.recv(Communication.buffer_size).decode('UTF-8')
        communication.close()
        received_message = communication_message.rstrip('\n')
        ColorPrinter.printFeedback(f'{received_message} has been received from Delta!')
        return received_message

    def sendMessageWithountPrint(self, message):
        """
        :param message: Message that is going to be sent to Delta which works as command lines!
        :return: It returns the message has been sent to Delta!
        """
        send_message = bytes(message, 'utf-8')
        communication = Communication.openSocket()
        communication.connect((self.IPV4, Communication.port_name))
        communication.send(send_message)
        communication.close()
        return send_message

    def sendReceiveMessageWithoutPrint(self, message):
        """
        :param message: Message that is going to be sent to Delta to get back as query!
        :return: It returns the message has been received from Delta!
        """
        send_message = bytes(message, 'utf-8')
        communication = Communication.openSocket()
        communication.connect((self.IPV4, Communication.port_name))
        communication.send(send_message)
        communication_message = communication.recv(Communication.buffer_size).decode('UTF-8')
        communication.close()
        received_message = communication_message.rstrip('\n')
        return received_message


class GeneralInstructions(Communication):
    """
    Manual: General Instruction - page 8 - Queries and Commands
    -----------------------------------------------------------------------------------------------------------------
    IDN = "*IDN?<term>" Read the identification string of the Delta Power Supply
    -----------------------------------------------------------------------------------------------------------------
    PUD = "*PUD?<term>" Read the protected user data of the Delta Power Supply
    -----------------------------------------------------------------------------------------------------------------
    CLS = "*CLS<term>" Clear the error queue of the Delta Power Supply
    -----------------------------------------------------------------------------------------------------------------
    RST = "*RST<term>" Set the power supply in a save defined state of the Delta Power Supply
    -----------------------------------------------------------------------------------------------------------------
    Note: All commands can be tested with 'TestGeneralInstructions Method'
    :return Queries will return the Received Message!
    :return Commands will return the Command has been sent!
    """

    def __init__(self, IPV4):
        super().__init__(IPV4)

    def __str__(self):
        return f'Manual: General Instruction - page 8 - Queries and Commands, for details print object.__doc__'

    def Identification(self, IDN="*IDN?\n"):
        return self.sendReceiveMessage(IDN)

    def ProtectedUserData(self, PUD="*PUD?\n"):
        return self.sendReceiveMessage(PUD)

    def ClearErrorQueue(self, CLS="*CLS\n"):
        return self.sendMessage(CLS)

    def ResetDefinedState(self, RST="*RST\n"):
        return self.sendMessage(RST)

    def TestGeneralInstructions(self):
        ColorPrinter.printComment("Self Identification runs:")
        self.Identification()
        ColorPrinter.printComment("Protected user data runs:")
        self.ProtectedUserData()
        ColorPrinter.printComment("Clear Error Queue runs:")
        self.ClearErrorQueue()
        ColorPrinter.printComment("Reset Defined State runs:")
        self.ResetDefinedState()
        return None


class SourceSubsystem(Communication):
    """
    Manual: Source Subsystem - page 9 and 10 - Queries and Commands
    -----------------------------------------------------------------------------------------------------------------
    MaximumVoltage = "SOURce:VOLtage:MAXimum?<term>" Read the maximum output voltage
    -----------------------------------------------------------------------------------------------------------------
    MaximumCurrent = "SOURce:CURrent:MAXimum?<term>" Read the maximum output current
    -----------------------------------------------------------------------------------------------------------------
    MaximumNegativeCurrent = "SOURce:CURrent:NEGative:MAXimum?<term>" Read the maximum negative output current
    -----------------------------------------------------------------------------------------------------------------
    MaximumPower = "SOURce:POWer:MAXimum?<term>" Read the maximum output power
    -----------------------------------------------------------------------------------------------------------------
    MaximumNegativePower = "SOURce:POWer:NEGative:MAXimum?<term>" Read the maximum negative output power
    -----------------------------------------------------------------------------------------------------------------
    SetVoltage = "SOURce:VOLtage<sp><NR2><term>" To set the output voltage of the power supply
    -----------------------------------------------------------------------------------------------------------------
    ReadVoltageSet = "SOURce:VOLTage?<term>" To see last voltage set point of the power supply
    -----------------------------------------------------------------------------------------------------------------
    SetCurrent = "SOURce:CURrent<sp><NR2><term>" To set the output current of the power supply
    -----------------------------------------------------------------------------------------------------------------
    ReadCurrentSet = "SOURce:CURrent?<term>" To see last current set point of the power supply
    -----------------------------------------------------------------------------------------------------------------
    SetNegativeCurrent = "SOURce:CURrent:NEGative<sp><NR2><term>" To set the output negative current of the power supply
    -----------------------------------------------------------------------------------------------------------------
    ReadNegativeCurrentSet = "SOURce:CURrent:NEGative?<term>" To see last negative current set point of the power supply
    -----------------------------------------------------------------------------------------------------------------
    SetPower = "SOURce:POWer<sp><NR2><term>" To set the output power of the power supply
    -----------------------------------------------------------------------------------------------------------------
    ReadPowerSet = "SOURce:POWer?<term>" To see last output power set point of the power supply
    -----------------------------------------------------------------------------------------------------------------
    SetNegativePower = "SOURce:POWer:NEGative<sp><NR2><term>" To set the negative output power of the power supply
    -----------------------------------------------------------------------------------------------------------------
    ReadNegativePowerSet = "SOURce:POWer:NEGative?<term>" To see last negative output power set point of the power supply
    -----------------------------------------------------------------------------------------------------------------
    VoltageStepSize = "SOURce:VOLtage:STEpsize?<term>" To read the programming stepsize of the output voltage
    -----------------------------------------------------------------------------------------------------------------
    CurrentStepSize = "SOURce:CURrent:STEpsize?<term>" To read the programming stepsize of the output current
    -----------------------------------------------------------------------------------------------------------------
    PowerStepSize = "SOURce:POWer:STEpsize?<term>" To read the programming stepsize of the output power
    -----------------------------------------------------------------------------------------------------------------
    Note: All commands can be tested with 'TestSourceSubsystem Method'
    :return Queries will return the Received Message!
    :return Commands will return the Command has been sent!
    """

    def __init__(self, IPV4):
        super().__init__(IPV4)

    def __str__(self):
        return f'Manual: Source Subsystem - page 9 and 10 - Queries and Commands, for details print object.__doc__'

    def MaximumVoltage(self, MaximumVoltage="SOURce:VOLtage:MAXimum?\n"):
        return self.sendReceiveMessage(MaximumVoltage)

    def MaximumCurrent(self, MaximumCurrent="SOURce:CURrent:MAXimum?\n"):
        return self.sendReceiveMessage(MaximumCurrent)

    def MaximumNegativeCurrent(self, MaximumNegativeCurrent="SOURce:CURrent:NEGative:MAXimum?\n"):
        return self.sendReceiveMessage(MaximumNegativeCurrent)

    def MaximumPower(self, MaximumPower="SOURce:POWer:MAXimum?\n"):
        return self.sendReceiveMessage(MaximumPower)

    def MaximumNegativePower(self, MaximumNegativePower="SOURce:POWer:NEGative:MAXimum?\n"):
        return self.sendReceiveMessage(MaximumNegativePower)

    def SetVoltage(self, voltage):
        message = f'SOURce:VOLtage {voltage}\n'
        return self.sendMessage(message)

    def ReadVoltageSet(self, ReadVoltageSet="SOURce:VOLtage?\n"):
        return self.sendReceiveMessage(ReadVoltageSet)

    def SetCurrent(self, current):
        message = f'SOURce:CURrent {current}\n'
        return self.sendMessage(message)

    def ReadCurrentSet(self, ReadCurrentSet="SOURce:CURrent?\n"):
        return self.sendReceiveMessage(ReadCurrentSet)

    def SetNegativeCurrent(self, negativecurrent):
        message = f'SOURce:CURrent:NEGative {negativecurrent}\n'
        return self.sendMessage(message)

    def ReadNegativeCurrentSet(self, ReadNegativeCurrentSet="SOURce:CURrent:NEGative?\n"):
        return self.sendReceiveMessage(ReadNegativeCurrentSet)

    def SetPower(self, power):
        message = f"SOURce:POWer {power}\n"
        return self.sendMessage(message)

    def ReadPowerSet(self, ReadPowerSet="SOURce:POWer?\n"):
        return self.sendReceiveMessage(ReadPowerSet)

    def SetNegativePower(self, negativepower):
        message = f'SOURce:POWer:NEGative {negativepower}\n'
        return self.sendMessage(message)

    def ReadNegativePowerSet(self, ReadNegativePowerSet="SOURce:POWer:NEGative?\n"):
        return self.sendReceiveMessage(ReadNegativePowerSet)

    def VoltageStepSize(self, VoltageStepSize="SOURce:VOLtage:STEpsize?\n"):
        return self.sendReceiveMessage(VoltageStepSize)

    def CurrentStepSize(self, CurrentStepSize="SOURce:CURrent:STEpsize?\n"):
        return self.sendReceiveMessage(CurrentStepSize)

    def PowerStepSize(self, PowerStepSize="SOURce:POWer:STEpsize?\n"):
        return self.sendReceiveMessage(PowerStepSize)

    def TestSourceSubsystem(self):
        ColorPrinter.printComment("Maximum Voltage runs:")
        self.MaximumVoltage()
        ColorPrinter.printComment("Maximum Current runs:")
        self.MaximumCurrent()
        ColorPrinter.printComment("Maximum Negative Current runs:")
        self.MaximumNegativeCurrent()
        ColorPrinter.printComment("Maximum Power runs:")
        self.MaximumPower()
        ColorPrinter.printComment("Maximum Negative Power runs:")
        self.MaximumNegativePower()
        ColorPrinter.printComment("Set Voltage runs:")
        self.SetVoltage(5)
        ColorPrinter.printComment("Read Last Voltage Set runs:")
        self.ReadVoltageSet()
        ColorPrinter.printComment("Set Current runs:")
        self.SetCurrent(5)
        ColorPrinter.printComment("Read Last Current Set runs:")
        self.ReadCurrentSet()
        ColorPrinter.printComment("Set Negative Current Set runs:")
        self.SetNegativeCurrent(-5)
        ColorPrinter.printComment("Read Last Negative Current Set runs:")
        self.ReadNegativeCurrentSet()
        ColorPrinter.printComment("Set Power Set runs:")
        self.SetPower(100)
        ColorPrinter.printComment("Read Last Power Set runs:")
        self.ReadPowerSet()
        ColorPrinter.printComment("Set Negative Power Set runs:")
        self.SetNegativePower(-100)
        ColorPrinter.printComment("Read Last Negative Power Set runs:")
        self.ReadNegativePowerSet()
        ColorPrinter.printComment("Read Voltage Stepsize runs:")
        self.VoltageStepSize()
        ColorPrinter.printComment("Read Current Stepsize runs:")
        self.CurrentStepSize()
        ColorPrinter.printComment("Read Power Stepsize runs:")
        self.PowerStepSize()


class MeasureSubsystem(Communication):
    """
    Manual: Measure Subsystem - page 10, 11 and 12 - Queries and Commands
    -----------------------------------------------------------------------------------------------------------------
    MeasureVoltage = "MEASure:VOLtage?<term>" To measure output voltage of the power supply
    -----------------------------------------------------------------------------------------------------------------
    MeasureCurrent = "MEASure:CURrent?<term>" To measure output current of the power supply
    -----------------------------------------------------------------------------------------------------
    MeasurePower = "MEASure:POWer?<term>" To measure output power of the power supply
    -----------------------------------------------------------------------------------------------------------------
    SetAhMeasurementState = "MEASure:INStrument<sp>AH,STATE,<setting><term>" To enable the current measurement
        instrument <setting>: OFF, ON, SUSPEND or RESUME Turning the instrument ON will reset all previous measurements
    -----------------------------------------------------------------------------------------------------------------
    ReadAhMeasurementSetState = "MEASure:INStrument<sp>AH,STATE?<term>" To read enable status (OFF, ON, SUSPEND or RESUME)
    -----------------------------------------------------------------------------------------------------------------
    ReadAhMeasurementTimeHours = "MEASure:INStrument<sp>AH,TIMEHR?<term>" To read the time the instrument is active
        (hours with three decimals) If the instrument is not enabled, the result will be zero
    -----------------------------------------------------------------------------------------------------------------
    ReadAhMeasurementTimeSeconds = "MEASure:INStrument<sp>AH,TIMESEC?<term>" To read the time the instrument is active
        (seconds with one decimal) If the instrument is not enabled, the result will be zero
    -----------------------------------------------------------------------------------------------------------------
    MeasureAhPositiveTotal = "MEASure:INStrument<sp>AH,POS,TOTAL?<term>"  To read the total Ah for positive current - w
        Scientifiec Notation If the instrument is not enabled, the result will be zero.
    -----------------------------------------------------------------------------------------------------------------
    MeasureAhNegativeTotal = "MEASure:INStrument<sp>AH,NEG,TOTAL?<term>"  To read the total Ah for negative current - w
        Scientifiec Notation If the instrument is not enabled, the result will be zero.
    -----------------------------------------------------------------------------------------------------------------
    MeasureAhMinimumCurrent = "MEASure:INStrument<sp>AH,POS,IMIN?<term>" To read minimum positive current during the time
        the instrument is enabled. Result will be in Ampere, if the instrument is not enabled, the result will be zero.
    -----------------------------------------------------------------------------------------------------------------
    MeasureAhMaximumCurrent = "MEASure:INStrument<sp>AH,POS,IMAX?<term>" To read maximum positive current during the time
        the instrument is enabled. Result will be in Ampere, if the instrument is not enabled, the result will be zero.
    -----------------------------------------------------------------------------------------------------------------
    MeasureAhMinimumNegativeCurrent = "MEASure:INStrument<sp>AH,NEG,IMIN?<term>" To read minimum negative current during
        the time the instrument is enabled. Result will be in Ampere, if the instrument is not enabled, the result will be zero.
    -----------------------------------------------------------------------------------------------------------------
    MeasureAhMaximumNegativeCurrent = "MEASure:INStrument<sp>AH,NEG,IMAX?<term>" To read maximum negative current during
        the time the instrument is enabled. Result will be in Ampere, if the instrument is not enabled, the result will be zero.
    -----------------------------------------------------------------------------------------------------------------
    SetWhMeasurementState = "MEASure:INStrument<sp>WH,STATE,<setting><term>" To enable the power measurement
        instrument <setting>: OFF, ON, SUSPEND or RESUME Turning the instrument ON will reset all previous measurements
    -----------------------------------------------------------------------------------------------------------------
    ReadWhMeasurementSetState = "MEASure:INStrument<sp>WH,STATE?<term>" To read enable status (OFF, ON, SUSPEND or RESUME)
    -----------------------------------------------------------------------------------------------------------------
    ReadWhMeasurementTimeHours = "MEASure:INStrument<sp>WH,TIMEHR?<term>" To read the time the instrument is active
        (hours with three decimals) If the instrument is not enabled, the result will be zero
    -----------------------------------------------------------------------------------------------------------------
    ReadWhMeasurementTimeSeconds = "MEASure:INStrument<sp>WH,TIMESEC?<term>" To read the time the instrument is active
        (seconds with one decimal) If the instrument is not enabled, the result will be zero
    -----------------------------------------------------------------------------------------------------------------
    MeasureWhPositiveTotal = "MEASure:INStrument<sp>WH,POS,TOTAL?<term>"  To read the total Wh for positive power - w
        Scientifiec Notation If the instrument is not enabled, the result will be zero.
    -----------------------------------------------------------------------------------------------------------------
    MeasureWhNegativeTotal = "MEASure:INStrument<sp>WH,NEG,TOTAL?<term>"  To read the total Wh for negative power - w
        Scientifiec Notation If the instrument is not enabled, the result will be zero.
    -----------------------------------------------------------------------------------------------------------------
    MeasureWhMinimumCurrent = "MEASure:INStrument<sp>WH,POS,PMIN?<term>" To read minimum positive power during the time
        the instrument is enabled. Result will be in Watts, if the instrument is not enabled, the result will be zero.
    -----------------------------------------------------------------------------------------------------------------
    MeasureWhMaximumCurrent = "MEASure:INStrument<sp>WH,POS,PMAX?<term>" To read maximum positive power during the time
        the instrument is enabled. Result will be in Watts, if the instrument is not enabled, the result will be zero.
    -----------------------------------------------------------------------------------------------------------------
    MeasureWhMinimumNegativeCurrent = "MEASure:INStrument<sp>WH,NEG,PMIN?<term>" To read minimum negative power during
        the time the instrument is enabled. Result will be in Watss, if the instrument is not enabled, the result will be zero.
    -----------------------------------------------------------------------------------------------------------------
    MeasureWhMaximumNegativeCurrent = "MEASure:INStrument<sp>WH,NEG,PMAX?<term>" To read maximum negative power during
        the time the instrument is enabled. Result will be in Watts, if the instrument is not enabled, the result will be zero.
    -----------------------------------------------------------------------------------------------------------------
    MeasureTemperature = "MEASure:TEMperature?<term>" To read highest internal temperature of the power supply
    -----------------------------------------------------------------------------------------------------------------
    Note: All commands can be tested with 'TestMeasureSubsystem Method'
    :return Queries will return the Received Message!
    :return Commands will return the Command has been sent!
    """

    def __init__(self, IPV4):
        super().__init__(IPV4)

    def __str__(self):
        return f'Manual: Measure Subsystem - page 10, 11 and 12 - Queries and Commands, for details print object.__doc__'

    def MeasureVoltage(self, MeasureVoltage="MEASure:VOLtage?\n"):
        return self.sendReceiveMessage(MeasureVoltage)

    def MeasureCurrent(self, MeasureCurrent="MEASure:CURrent?\n"):
        return self.sendReceiveMessage(MeasureCurrent)

    def MeasurePower(self, MeasurePower="MEASure:POWer?\n"):
        return self.sendReceiveMessage(MeasurePower)

    def SetAhMeasurementState(self, setting):
        message = f'MEASure:INStrument AH,STATE,{setting}\n'
        return self.sendMessage(message)

    def ReadAhMeasurementSetState(self, ReadAhMeasurementSetState="MEASure:INStrument AH,STATE?\n"):
        return self.sendReceiveMessage(ReadAhMeasurementSetState)

    def ReadAhMeasurementTimeHours(self, ReadAhMeasurementTimeHours="MEASure:INStrument AH,TIMEHR?\n"):
        return self.sendReceiveMessage(ReadAhMeasurementTimeHours)

    def ReadAhMeasurementTimeSeconds(self, ReadAhMeasurementTimeSeconds="MEASure:INStrument AH,TIMESEC?\n"):
        return self.sendReceiveMessage(ReadAhMeasurementTimeSeconds)

    def MeasureAhPositiveTotal(self, MeasureAhPositiveTotal="MEASure:INStrument AH,POS,TOTAL?\n"):
        return self.sendReceiveMessage(MeasureAhPositiveTotal)

    def MeasureAhNegativeTotal(self, MeasureAhNegativeTotal="MEASure:INStrument AH,NEG,TOTAL?\n"):
        return self.sendReceiveMessage(MeasureAhNegativeTotal)

    def MeasureAhMinimumCurrent(self, MeasureAhMinimumCurrent="MEASure:INStrument AH,POS,IMIN?\n"):
        return self.sendReceiveMessage(MeasureAhMinimumCurrent)

    def MeasureAhMaximumCurrent(self, MeasureAhMaximumCurrent="MEASure:INStrument AH,POS,IMAX?\n"):
        return self.sendReceiveMessage(MeasureAhMaximumCurrent)

    def MeasureAhMinimumNegativeCurrent(self, MeasureAhMinimumNegativeCurrent="MEASure:INStrument AH,NEG,IMIN?\n"):
        return self.sendReceiveMessage(MeasureAhMinimumNegativeCurrent)

    def MeasureAhMaximumNegativeCurrent(self, MeasureAhMaximumNegativeCurrent="MEASure:INStrument AH,NEG,IMAX?\n"):
        return self.sendReceiveMessage(MeasureAhMaximumNegativeCurrent)

    def SetWhMeasurementState(self, setting):
        message = f'MEASure:INStrument WH,STATE,{setting}\n'
        return self.sendMessage(message)

    def ReadWhMeasurementSetState(self, ReadWhMeasurementSetState="MEASure:INStrument WH,STATE?\n"):
        return self.sendReceiveMessage(ReadWhMeasurementSetState)

    def ReadWhMeasurementTimeHours(self, ReadWhMeasurementTimeHours="MEASure:INStrument WH,TIMEHR?\n"):
        return self.sendReceiveMessage(ReadWhMeasurementTimeHours)

    def ReadWhMeasurementTimeSeconds(self, ReadWhMeasurementTimeSeconds="MEASure:INStrument WH,TIMESEC?\n"):
        return self.sendReceiveMessage(ReadWhMeasurementTimeSeconds)

    def MeasureWhPositiveTotal(self, MeasureWhPositiveTotal="MEASure:INStrument WH,POS,TOTAL?\n"):
        return self.sendReceiveMessage(MeasureWhPositiveTotal)

    def MeasureWhNegativeTotal(self, MeasureWhNegativeTotal="MEASure:INStrument WH,NEG,TOTAL?\n"):
        return self.sendReceiveMessage(MeasureWhNegativeTotal)

    def MeasureWhMinimumCurrent(self, MeasureWhMinimumCurrent="MEASure:INStrument WH,POS,PMIN?\n"):
        return self.sendReceiveMessage(MeasureWhMinimumCurrent)

    def MeasureWhMaximumCurrent(self, MeasureWhMaximumCurrent="MEASure:INStrument WH,POS,PMAX?\n"):
        return self.sendReceiveMessage(MeasureWhMaximumCurrent)

    def MeasureWhMinimumNegativeCurrent(self, MeasureWhMinimumNegativeCurrent="MEASure:INStrument WH,NEG,PMIN?\n"):
        return self.sendReceiveMessage(MeasureWhMinimumNegativeCurrent)

    def MeasureWhMaximumNegativeCurrent(self, MeasureWhMaximumNegativeCurrent="MEASure:INStrument WH,NEG,PMAX?\n"):
        return self.sendReceiveMessage(MeasureWhMaximumNegativeCurrent)

    def MeasureTemperature(self, MeasureTemperature="MEASure:TEMperature?\n"):
        return self.sendReceiveMessage(MeasureTemperature)

    def TestMeasureSubsystem(self):
        ColorPrinter.printComment("Measure voltage runs:")
        self.MeasureVoltage()
        ColorPrinter.printComment("Measure current runs:")
        self.MeasureCurrent()
        ColorPrinter.printComment("Measure power runs:")
        self.MeasurePower()
        ColorPrinter.printComment("Set Ah Measurement State runs:")
        self.SetAhMeasurementState('ON')
        ColorPrinter.printComment("Read Ah Measurement State runs:")
        self.ReadAhMeasurementSetState()
        ColorPrinter.printComment("Read Ah Time Hours runs:")
        self.ReadAhMeasurementTimeHours()
        ColorPrinter.printComment("Read Ah Time Seconds runs:")
        self.ReadAhMeasurementTimeSeconds()
        ColorPrinter.printComment("Measure Ah Positive runs:")
        self.MeasureAhPositiveTotal()
        ColorPrinter.printComment("Measure Ah Negative runs:")
        self.MeasureAhNegativeTotal()
        ColorPrinter.printComment("Measure Ah Minimum Current runs:")
        self.MeasureAhMinimumCurrent()
        ColorPrinter.printComment("Measure Ah Maximum Current runs:")
        self.MeasureAhMaximumCurrent()
        ColorPrinter.printComment("Measure Ah Minimum Negative Current runs:")
        self.MeasureAhMinimumNegativeCurrent()
        ColorPrinter.printComment("Measure Ah Maximum Negarive Current runs:")
        self.MeasureAhMinimumNegativeCurrent()
        ColorPrinter.printComment("Set Wh Measurement State runs:")
        self.SetWhMeasurementState('ON')
        ColorPrinter.printComment("Read Wh Measurement State runs:")
        self.ReadWhMeasurementSetState()
        ColorPrinter.printComment("Read Wh Time Hours runs:")
        self.ReadAhMeasurementTimeHours()
        ColorPrinter.printComment("Read Wh Time Seconds runs:")
        self.ReadWhMeasurementTimeSeconds()
        ColorPrinter.printComment("Measure Wh Positive runs:")
        self.MeasureWhPositiveTotal()
        ColorPrinter.printComment("Measure Wh Negative runs:")
        self.MeasureWhNegativeTotal()
        ColorPrinter.printComment("Measure Wh Minimum Current runs:")
        self.MeasureWhMinimumCurrent()
        ColorPrinter.printComment("Measure Wh Maximum Current runs:")
        self.MeasureWhMaximumCurrent()
        ColorPrinter.printComment("Measure Wh Minimum Negative Current runs:")
        self.MeasureWhMinimumNegativeCurrent()
        ColorPrinter.printComment("Measure Wh Maximum Negarive Current runs:")
        self.MeasureWhMaximumNegativeCurrent()
        ColorPrinter.printComment("Measure Temperature runs:")
        self.MeasureTemperature()


class SystemSubsystem(Communication):
    """
    Manual: Measure Subsystem - page 13, 14, 15 and 16 - Queries and Commands
    -----------------------------------------------------------------------------------------------------------------
    SetRemoteShutDown = "SYSTem:RSD[:STAtus]<sp><boolean><term>" To activate and deactivate remote shutdown
        Boolean = 0, 1, OFF (Unlocked), ON (Locked)
    -----------------------------------------------------------------------------------------------------------------
    ReadRemoteShutDownSet = "SYSTem:RSD[:STAtus]?<term>" To read last RSD (remote shut down) settings
    -----------------------------------------------------------------------------------------------------------------
    SetVoltageLimit =  "SYSTem:LIMits:VOLtage<sp><NR2>,<boolean><term>" To set the limits of the voltage
        Off = disabled, On = enabled
    -----------------------------------------------------------------------------------------------------------------
    ReadVoltageLimitSet = "SYSTem:LIMits:VOLtage?<term>" To read last voltage limit setting
    -----------------------------------------------------------------------------------------------------------------
    SetCurrentLimit = "SYSTem:LIMits:CURrent<sp><NR2>,<boolean><term>" To set the limits of the positive current
        Off = disabled, On = enabled
    -----------------------------------------------------------------------------------------------------------------
    ReadCurrentLimitSet = "SYSTem:LIMits:CURrent?" To read last positive current limit setting
    -----------------------------------------------------------------------------------------------------------------
    SetNegativeCurrentLimit = "SYSTem:LIMits:CURrent:NEGative<sp><NR2>,<boolean><term>" To set the limits of the
        negative current Off = disabled, On = enabled
    -----------------------------------------------------------------------------------------------------------------
    ReadNegativeCurrentLimitSet = "SYSTem:LIMits:CURrent:NEGative?<term>" To read last negative current limit setting
    -----------------------------------------------------------------------------------------------------------------
    SetPowerLimit = "SYSTem:LIMits:POWer<sp><NR2>,<boolean><term>" "To set the limits of the positive power
        Off = disabled, On = enabled"
    -----------------------------------------------------------------------------------------------------------------
    ReadPowerLimitSet = "SYSTem:LIMits:POWer?<term>" To read last positive power limit setting
    -----------------------------------------------------------------------------------------------------------------
    SetNegativePowerLimit = "SYSTem:LIMits:POWer:NEGative<sp><NR2>,<boolean><term>" To set the limits of the
        negative power Off = disabled, On = enabled
    -----------------------------------------------------------------------------------------------------------------
    ReadNegativePowerLimitSet = "SYSTem:LIMits:POWer:NEGative?<term>" To read last negative power limit setting
    -----------------------------------------------------------------------------------------------------------------
    HighlightFrontpanel = "SYSTem:FROntpanel:HIGhlight<term>" "To highlight front panel
        - Display on front will blink for about 2 seconds
        - Buzzer on front is on for about 2 seconds."
    -----------------------------------------------------------------------------------------------------------------
    LockFrontPanel = "SYSTem:FROntpanel[:STAtus]<sp><boolean><term>" To lock the front panel
        Boolean = 0, 1, OFF (Unlocked), ON (Locked)
    -----------------------------------------------------------------------------------------------------------------
    ReadLockFrontpanelSet = "SYSTem:FROntpanel[:STAtus]?<term>" To read the last settings about the front lock
    -----------------------------------------------------------------------------------------------------------------
    LockControlFrontpanel = "SYSTem:FROntpanel:CONtrols<sp><boolean><term>" To lock or unluck front panel and/or control
        Boolean = 0 (Menu), 1 (Menu & Controls), OFF (Menu), ON (Menu & Controls)
    -----------------------------------------------------------------------------------------------------------------
    ReadLockControlFrontpanelSet = "SYSTem:FROntpanel:CONtrols?" To read the last settings about the front lock&control
    -----------------------------------------------------------------------------------------------------------------
    SetTime = "SYSTem:TIMe<sp><hour>,<minute>,<second><term>" To set time as hour, minute, second
        Hour = 0-23 - Minute = 0-59 - Second = 0-59
    -----------------------------------------------------------------------------------------------------------------
    ReadTimeSet = "SYSTem:TIMe?<term>" To read the current time, answer  <hour>:<minute>:<second>
        The answer will be “UNKNOWN” in case the time was not set.
    -----------------------------------------------------------------------------------------------------------------
    SetDate = "SYSTem:DATe<sp><year>,<month>,<day><term>" To set the date as year, month, day
        Year = 2019-2099 - Month = 1-12 - Day = 1-31
    -----------------------------------------------------------------------------------------------------------------
    ReadDateSet = "SYSTem:DATe?<term>" To read the current date, answer <year>-<month>-<day>
        The answer will be “UNKNOWN” in case the time was not set.
    -----------------------------------------------------------------------------------------------------------------
    ReadErrors = "SYSTem:ERRor?<term>" To read the error message, If there are no errors (so the queue is empty)
        the result of this query will be : 0,None<term>. So after 10 readings of SYSTem:ERRor? the queue is empty
        for sure, or after using the *CLS command.
    -----------------------------------------------------------------------------------------------------------------
    ReadWarnings = "SYSTem:WARning?<term>" To read the warning message
        If there are no warnings, the result of this query will be: 0,None<term>
    -----------------------------------------------------------------------------------------------------------------
    SetWatchdog = "SYSTem:COMmunicate:WATchdog<sp>SET,<NR1><term>" To set the Watchdog timer (in ms) - <NR1>= 20…10000
    -----------------------------------------------------------------------------------------------------------------
    ReadWatchdogSet = "SYSTem:COMmunicate:WATchdog<sp>SET?<term>" To read the last setting: (valid until Timeout)
    -----------------------------------------------------------------------------------------------------------------
    ReadCurrentWatchdogState = "SYSTem:COMmunicate:WATchdog?<term>" To read the current state of the Watchdog timer with
        three possibilities, 20…10000<term> Current timer value in ms, 0<term> Timeout.
        Clears indicator on Front panel and Web -1<term> Clears Timeout, Watchdog is off.
        Note:  The indicator on the Front panel and Web will be activated. Enable, disable or query
            the state of the Watchdog timer to clear the indicators.
    -----------------------------------------------------------------------------------------------------------------
    DisableWatchdog = "SYSTem:COMmunicate:WATchdog<sp>STOP<term>" To disable the Watchdog timer
    -----------------------------------------------------------------------------------------------------------------
    TestWatchdog = "SYSTem:COMmunicate:WATchdog<sp>TEST<term>" To test the Watchdog timer
    -----------------------------------------------------------------------------------------------------------------
    Note: All commands can be tested with 'TestSystemSubsystem Method'
    :return Queries will return the Received Message!
    :return Commands will return the Command has been sent!
    """

    def __init__(self, IPV4):
        super().__init__(IPV4)

    def __str__(self):
        return f'Manual: Measure Subsystem - page 13 and 14 - Queries and Commands, for details print object.__doc__'

    def SetRemoteShutDown(self, setting):
        message = f'SYSTem:RSD[:STAtus] {setting}\n'
        return self.sendMessage(message)

    def ReadRemoteShutDownSet(self, ReadRemoteShutDownSet="SYSTem:RSD[:STAtus]?\n"):
        return self.sendReceiveMessage(ReadRemoteShutDownSet)

    def SetVoltageLimit(self, voltagelimit, setting):
        message = f'SYSTem:LIMits:VOLtage {voltagelimit},{setting}\n'
        return self.sendMessage(message)

    def ReadVoltageLimitSet(self, ReadVoltageLimitSet="SYSTem:LIMits:VOLtage?\n"):
        return self.sendReceiveMessage(ReadVoltageLimitSet)

    def SetCurrentLimit(self, currentlimit, setting):
        message = f'SYSTem:LIMits:CURrent {currentlimit},{setting}\n'
        return self.sendMessage(message)

    def ReadCurrentLimitSet(self, ReadCurrentLimitSet="SYSTem:LIMits:CURrent?\n"):
        return self.sendReceiveMessage(ReadCurrentLimitSet)

    def SetNegativeCurrentLimit(self, negativecurrentlimit, setting):
        message = f'SYSTem:LIMits:CURrent:NEGative {negativecurrentlimit},{setting}\n'
        return self.sendMessage(message)

    def ReadNegativeCurrentLimitSet(self, ReadNegativeCurrentLimitSet="SYSTem:LIMits:CURrent:NEGative?\n"):
        return self.sendReceiveMessage(ReadNegativeCurrentLimitSet)

    def SetPowerLimit(self, powerlimit, setting):
        message = f'SYSTem:LIMits:POWer {powerlimit},{setting}\n'
        return self.sendMessage(message)

    def ReadPowerLimitSet(self, ReadPowerLimitSet="SYSTem:LIMits:POWer?\n"):
        return self.sendReceiveMessage(ReadPowerLimitSet)

    def SetNegativePowerLimit(self, negativepowerlimit, setting):
        message = f'SYSTem:LIMits:POWer:NEGative {negativepowerlimit},{setting}\n'
        return self.sendMessage(message)

    def ReadNegativePowerLimitSet(self, ReadNegativePowerLimitSet="SYSTem:LIMits:POWer:NEGative?\n"):
        return self.sendReceiveMessage(ReadNegativePowerLimitSet)

    def HighlightFrontpanel(self, HighlightFrontpanel="SYSTem:FROntpanel:HIGhlight\n"):
        return self.sendMessage(HighlightFrontpanel)

    def LockFrontPanel(self, setting):
        message = f'SYSTem:FROntpanel[:STAtus] {setting}\n'
        return self.sendMessage(message)

    def ReadLockFrontpanelSet(self, ReadLockFrontpanelSet="SYSTem:FROntpanel[:STAtus]?\n"):
        return self.sendReceiveMessage(ReadLockFrontpanelSet)

    def LockControlFrontpanel(self, setting):
        message = f'SYSTem:FROntpanel:CONtrols {setting}\n'
        return self.sendMessage(message)

    def ReadLockControlFrontpanelSet(self, ReadLockControlFrontpanelSet="SYSTem:FROntpanel:CONtrols?\n"):
        return self.sendReceiveMessage(ReadLockControlFrontpanelSet)

    def SetTime(self, hour, minute, second):
        message = f'SYSTem:TIMe {hour},{minute},{second}\n'
        return self.sendMessage(message)

    def ReadTimeSet(self, ReadTimeSet="SYSTem:TIMe?\n"):
        return self.sendReceiveMessage(ReadTimeSet)

    def SetDate(self, year, month, day):
        message = f'SYSTem:DATe {year},{month},{day}\n'
        return self.sendMessage(message)

    def ReadDateSet(self, ReadDateSet="SYSTem:DATe?\n"):
        return self.sendReceiveMessage(ReadDateSet)

    def ReadErrors(self, ReadErrors="SYSTem:ERRor?\n"):
        return self.sendReceiveMessage(ReadErrors)

    def ReadWarnings(self, ReadWarnings="SYSTem:WARning?\n"):
        return self.sendReceiveMessage(ReadWarnings)

    def SetWatchdog(self, time):
        message = f'SYSTem:COMmunicate:WATchdog SET,{time}\n'
        self.sendMessage(message)

    def ReadWatchdogSet(self, ReadWatchdogSet="SYSTem:COMmunicate:WATchdog SET?\n"):
        return self.sendReceiveMessage(ReadWatchdogSet)

    def ReadCurrentWatchdogState(self, ReadCurrentWatchdogState="SYSTem:COMmunicate:WATchdog?\n"):
        return self.sendReceiveMessage(ReadCurrentWatchdogState)

    def DisableWatchdog(self, DisableWatchdog="SYSTem:COMmunicate:WATchdog STOP\n"):
        return self.sendMessage(DisableWatchdog)

    def TestWatchdog(self, TestWatchdog="SYSTem:COMmunicate:WATchdog TEST\n"):
        return self.sendMessage(TestWatchdog)

    def TestSystemSubsystem(self):
        ColorPrinter.printComment("Remote Shut Down Set runs:")
        self.SetRemoteShutDown('OFF')
        ColorPrinter.printComment("Read Remote Shut Down Set runs:")
        self.ReadRemoteShutDownSet()
        ColorPrinter.printComment("Set Voltage Limit runs:")
        self.SetVoltageLimit('16.5', 'ON')
        ColorPrinter.printComment("Read Voltage Limit Set runs:")
        self.ReadVoltageLimitSet()
        ColorPrinter.printComment("Set Current Limit runs:")
        self.SetCurrentLimit('50', 'ON')
        ColorPrinter.printComment("Read Current Limit Set runs:")
        self.ReadCurrentLimitSet()
        ColorPrinter.printComment("Set Negative Current Limit runs:")
        self.SetNegativeCurrentLimit('-50', 'ON')
        ColorPrinter.printComment("Read Negative Current Limit Set runs:")
        self.ReadNegativeCurrentLimitSet()
        ColorPrinter.printComment("Set Power Limit runs:")
        self.SetPowerLimit('100', 'ON')
        ColorPrinter.printComment("Read Power Limit Set runs:")
        self.ReadPowerLimitSet()
        ColorPrinter.printComment("Set Negative Power Limit runs:")
        self.SetNegativePowerLimit('-100', 'ON')
        ColorPrinter.printComment("Read Negative Power Limit Set runs:")
        self.ReadNegativePowerLimitSet()
        ColorPrinter.printComment("Highlight Frontpanel Set runs:")
        self.HighlightFrontpanel()
        ColorPrinter.printComment("Set Lock Frontpanel runs:")
        self.LockFrontPanel('ON')
        ColorPrinter.printComment("Read Lock Frontpanel Set runs:")
        self.ReadLockFrontpanelSet()
        ColorPrinter.printComment("Set Lock Control Frontpanel runs:")
        self.LockControlFrontpanel('ON')
        ColorPrinter.printComment("Read Lock Control Frontpanel Set runs:")
        self.ReadLockControlFrontpanelSet()
        ColorPrinter.printComment("Time Set runs:")
        self.SetTime('9', '10', '0')
        ColorPrinter.printComment("Read Time Set runs:")
        self.ReadTimeSet()
        ColorPrinter.printComment("Date Set runs:")
        self.SetDate('2021', '9', '8')
        ColorPrinter.printComment("Read Date Set runs:")
        self.ReadDateSet()
        ColorPrinter.printComment("Read Errors runs:")
        self.ReadErrors()
        ColorPrinter.printComment("Read Warnings runs:")
        self.ReadWarnings()
        ColorPrinter.printComment("Set Watchdog runs:")
        self.SetWatchdog("500")
        ColorPrinter.printComment("Read Watchdog Set runs:")
        self.ReadWatchdogSet()
        ColorPrinter.printComment("Read Current Watchdog State runs:")
        self.ReadCurrentWatchdogState()
        ColorPrinter.printComment("Disable Watchdog runs:")
        self.DisableWatchdog()
        ColorPrinter.printComment("Test Watchdog runs:")
        self.TestWatchdog()


class OutputSubsystem(Communication):
    """
    Manual: Output Subsystem - page 17 - Queries and Commands
    -----------------------------------------------------------------------------------------------------------------
    SetOutput = "OUTPut<sp><boolean><term>" To switch power supply on/off - boolean = 0, 1, OFF, ON
    -----------------------------------------------------------------------------------------------------------------
    ReadOutputSet = "OUTPut?<term> To read the last stage of the output
    -----------------------------------------------------------------------------------------------------------------
    Note: All commands can be tested with 'TestOutputSubsystem Method'
    :return Queries will return the Received Message!
    :return Commands will return the Command has been sent!
    """

    def __init__(self, IPV4):
        super().__init__(IPV4)

    def __str__(self):
        return f'Output Subsystem - page 17 - Queries and Commands, for details print object.__doc__'

    def SetOutput(self, setting):
        message = f'OUTPut {setting}\n'
        return self.sendMessage(message)

    def ReadOutputSet(self, ReadOutputSet="OUTPut?\n"):
        return self.sendReceiveMessage(ReadOutputSet)

    def TestOutputSubsystem(self):
        ColorPrinter.printComment("Output State Set runs:")
        self.SetOutput('1')
        ColorPrinter.printComment("Read output state ")
        self.ReadOutputSet()
        ColorPrinter.printComment("Output State Set runs:")
        self.SetOutput('0')
        ColorPrinter.printComment("Read output state ")
        self.ReadOutputSet()


class WatchdogOperation(threading.Thread):
    """
        This is a created thread for Watchdog Operation
        -----------------------------------------------------------------------------------------------------------------
        Timer: It is the set point for the watchdog operation, if watchdog time cannot be triggered withing this time
        period, it will switch of the output of the delta for safety.
        -----------------------------------------------------------------------------------------------------------------
        Sleeptime: This thread operates at given time period and sleeps at that timeline for the rest of the main operation.
        -----------------------------------------------------------------------------------------------------------------
        Be careful while setting it that timer is higher than sleep time for proper operation.
        -----------------------------------------------------------------------------------------------------------------
        If device fails with watch operation, it must be resetted manualy for safety reasons.
    """

    def __init__(self, timer, sleeptime, deamonState=True):
        super().__init__()
        self.timer = timer
        self.sleeptime = sleeptime
        self.deamonState = deamonState
        self._stop_event = threading.Event()
        self.setDaemon(self.deamonState)

    def __str__(self):
        return f'This is created to have watchdog operation for Delta Power Supply'

    def stop(self):
        ColorPrinter.printFeedback("Stop watchdog thread has been called!")
        return self._stop_event.set()

    def run(self):
        ColorPrinter.printFeedback("Watchdog thread has been started!")
        SystemSubsystem(IPV4).SetWatchdog(self.timer)
        while not self._stop_event.is_set():
            ColorPrinter.printFeedback("Watchdog thread is running!")
            time.sleep(self.sleeptime)
            if float(SystemSubsystem(IPV4).ReadWatchdogSet()) != 0:
                ColorPrinter.printFeedback('Watchdog is still active!')
            else:
                ColorPrinter.printFeedback('Watchdog has been failed!')
                self.stop()
        ColorPrinter.printFeedback("Watchdog thread has been stopped!")


# TODO Add datalogger class as Thread
class DataloggerOperation(threading.Thread):
    """
    It has been created to log CSV data type into TXT. Data can be adjusted according to user desire!
    """
    dataFrame = ['Measured_Voltage', 'Measured_Current', 'Measured_Power', 'Measured_Ah', 'Ah_Time_Seconds',
                 'Ah_Time_Hours']
    fileName = 'Datalogger'

    def __init__(self, loggingTime, deamonState=True):
        """
        :param fileName: Enter desired file name for your log file. -String
        Log file is being created with that time time-stamp and closed as soon as object is being generated!
        """
        super().__init__()
        DataloggerOperation.dataFrame.insert(0, 'TimeStamp')
        self.loggingTime = loggingTime
        self.deamonState = deamonState
        self.setDaemon(self.deamonState)
        self._stop_event = threading.Event()
        self.finalName = f'{DataloggerOperation.fileName} {datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S")}.txt'
        open(f'{self.finalName}', "w+").close()

    def csvLogger(self):
        csvFile = open(self.finalName, 'a', newline='')
        write = csv.writer(csvFile)
        write.writerow(self.dataFrame)
        csvFile.close()
        DataloggerOperation.dataFrame[0] = time.strftime('%d-%m-%Y %H:%M:%S')
        return self.dataFrame

    def updateDataFrame(self):
        DataloggerOperation.dataFrame[1] = MeasureSubsystem(IPV4).MeasureVoltage()
        DataloggerOperation.dataFrame[2] = MeasureSubsystem(IPV4).MeasureCurrent()
        DataloggerOperation.dataFrame[3] = MeasureSubsystem(IPV4).MeasurePower()
        DataloggerOperation.dataFrame[4] = MeasureSubsystem(IPV4).MeasureAhPositiveTotal()
        DataloggerOperation.dataFrame[5] = MeasureSubsystem(IPV4).ReadAhMeasurementTimeSeconds()
        DataloggerOperation.dataFrame[6] = MeasureSubsystem(IPV4).ReadAhMeasurementTimeHours()
        return self.dataFrame

    def stop(self):
        ColorPrinter.printFeedback('Datalogger stop event has been started!')
        self._stop_event.set()

    def run(self):
        ColorPrinter.printFeedback('Datalogger thread class has been started!')
        MeasureSubsystem(IPV4).SetAhMeasurementState('ON')
        while not self._stop_event.is_set():
            ColorPrinter.printFeedback('Datalogger thread class is running!')
            self.csvLogger()
            self.updateDataFrame()
            time.sleep(self.loggingTime)
        ColorPrinter.printFeedback('Datalogger thread class has been stopped!')


# TODO Add shutdown class
# TODO Add battery charging class as Thread

def TestAll(cprint):
    cprint.printComment('Test all function is running!')
    cprint.printComment("System runs to test!")
    cprint.printComment("General Instructions run to test!")
    GeneralComments = GeneralInstructions(IPV4)
    cprint.printComment(GeneralComments.__doc__)
    #GeneralComments.TestGeneralInstructions()
    cprint.printComment("Source Subsystem run to test!")
    SourceComments = SourceSubsystem(IPV4)
    cprint.printComment(SourceComments.__doc__)
    #SourceComments.TestSourceSubsystem()
    cprint.printComment("Source Subsystem run to test!")
    MeasureComments = MeasureSubsystem(IPV4)
    cprint.printComment(MeasureComments.__doc__)
    #MeasureComments.TestMeasureSubsystem()
    cprint.printComment("System Subsystem run to test!")
    SystemComments = SystemSubsystem(IPV4)
    cprint.printComment(SystemComments.__doc__)
    #SystemComments.TestSystemSubsystem()
    cprint.printComment("Output Subsystem run to test!")
    OutputComments = OutputSubsystem(IPV4)
    cprint.printComment(OutputComments.__doc__)
    #OutputComments.TestOutputSubsystem()
    cprint.printComment('Test all function is done!')


if __name__ == '__main__':
    cprint = ColorPrinter()
    TestAll(cprint)
    while True:
        time.sleep(5)
        cprint.printError('This is an Error Message!')
        cprint.printFeedback('Main Operion is running now!')
        cprint.printComment('Watchdog runs every 2 seconds')
        cprint.printNormal('Datalogger runs every 5 seconds')
