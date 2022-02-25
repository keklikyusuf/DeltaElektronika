# !/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Delta Elektronika SM15K Communication Socket Library.
#
# Revision: @keklikyusuf
# 0.0.7: Initial version


import socket
import threading
import time
import csv
import datetime
import sys
import logging

""" Module to handle communication with DELTA POWER SUPPLY  """

__version__ = "0.0.7"  # semVersion (Major.Minor.Revision)

filename = 'systemlog'
finalName = f'{filename} {datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S")}.log'

activateDebugLogger = False
if activateDebugLogger:
    logging.basicConfig(filename=finalName, level=logging.DEBUG,
                        format='%(asctime)s | %(name)s | %(levelname)s:%(message)s'
                               '\n-----------------------------------------------------------------------------------------------')
    logger = logging.getLogger(__name__)
    logger.propagate = activateDebugLogger
else:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(name)s | %(levelname)s:%(message)s'
                                                    '\n'
                                                    '-----------------------------------------------------------------------------------------------')
    logger = logging.getLogger(__name__)
    logger.propagate = False


class ColorPrinter:
    """
        Colorfull Terminal Printing
        -----------------------------------------------------------------------------------------------------------------
        It creates date and time stamp for debugging purpuses.
        -----------------------------------------------------------------------------------------------------------------
        printError: To print error message to terminal. Color is RED
        -----------------------------------------------------------------------------------------------------------------
        printFeedback: To print feedback message to terminal. Color is GREEN
        -----------------------------------------------------------------------------------------------------------------
        printComment: To print comment message to terminal. Color is BLUE
        -----------------------------------------------------------------------------------------------------------------
        printNormal: To print normal message to terminal. Color is GRAY
        -----------------------------------------------------------------------------------------------------------------
        printColorful: To print any message to terminal. Color is variable (purple, blue, cyan, green, yellow, red, normal).
        -----------------------------------------------------------------------------------------------------------------
    """
    purple = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    normal = '\033[0m'

    def __init__(self):
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
        sys.stdout.write(ColorPrinter.normal)
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
        sys.stdout.write(ColorPrinter.normal)
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
        sys.stdout.write(ColorPrinter.normal)
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
        sys.stdout.write(ColorPrinter.normal)
        return text

    def printColorful(self, message, colour='green'):
        """
            :param colour: type available colors as string!
            :param message: Text message that wanted to be printed
            :return: This function returns to printed text message
            Any message is being printed with defined stamp to create functional colorful printing
        """
        if colour == 'purple':
            sys.stdout.write(ColorPrinter.purple)
        elif colour == 'blue':
            sys.stdout.write(ColorPrinter.blue)
        elif colour == 'cyan':
            sys.stdout.write(ColorPrinter.cyan)
        elif colour == 'green':
            sys.stdout.write(ColorPrinter.green)
        elif colour == 'red':
            sys.stdout.write(ColorPrinter.red)
        elif colour == 'yellow':
            sys.stdout.write(ColorPrinter.yellow)
        elif colour == 'normal':
            sys.stdout.write(ColorPrinter.normal)
        else:
            logger.debug("Color is defined wrong! Default color is used!")
            sys.stdout.write(ColorPrinter.green)
        now = datetime.datetime.now()
        text = f'{now.strftime("%d/%m/%Y - %X")}: {message} \n{self.spacer}'
        print(text)
        sys.stdout.write(ColorPrinter.normal)
        return text


cprint = ColorPrinter()


class Communication:
    """
    Class attributers that are set according to device settings.
    """
    port_name = 8462
    buffer_size = 1024
    timeout = 10

    def __str__(self):
        return f'This is created to be able to communicate with Socket!'

    @staticmethod
    def openSocket():
        communication = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        communication.settimeout(Communication.timeout)
        return communication

    @staticmethod
    def sendMessage(IPV4, message):
        """
        :param message: Message that is going to be sent to Delta which works as command lines!
        :return: It returns the message has been sent to Delta!
        """
        send_message = bytes(message, 'utf-8')
        communication = Communication.openSocket()
        communication.connect((IPV4, Communication.port_name))
        communication.send(send_message)
        communication.close()
        logger.debug(f'{send_message} has been sent to Delta!')
        return send_message

    @staticmethod
    def sendReceiveMessage(IPV4, message):
        """
        :param message: Message that is going to be sent to Delta to get back as query!
        :return: It returns the message has been received from Delta!
        """
        send_message = bytes(message, 'utf-8')
        communication = Communication.openSocket()
        communication.connect((IPV4, Communication.port_name))
        communication.send(send_message)
        communication_message = communication.recv(Communication.buffer_size).decode('UTF-8')
        communication.close()
        received_message = communication_message.rstrip('\n')
        logger.debug(f'{received_message} has been received from Delta!')
        return received_message


class SM15K:

    def __init__(self, IPV4):
        self.IPV4 = IPV4
        self.source = SourceSubsystem(self.IPV4)
        self.measure = MeasureSubsystem(self.IPV4)
        self.system = SystemSubsystem(self.IPV4)
        self.output = OutputSubsystem(self.IPV4)
        self.shutdown = ShutdownOperation(self.IPV4)

    def __str__(self):
        return f'Manual: General Instruction - page 8 - Queries and Commands, for details print object.__doc__'

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

    def Identification(self, IDN="*IDN?\n"):
        """
        IDN = "*IDN?<term>" Read the identification string of the Delta Power Supply
        """
        return Communication().sendReceiveMessage(self.IPV4, message=IDN)

    def ProtectedUserData(self, PUD="*PUD?\n"):
        """
        PUD = "*PUD?<term>" Read the protected user data of the Delta Power Supply
        """
        return Communication().sendReceiveMessage(self.IPV4, message=PUD)

    def ClearErrorQueue(self, CLS="*CLS\n"):
        """
        CLS = "*CLS<term>" Clear the error queue of the Delta Power Supply
        """
        return Communication().sendMessage(self.IPV4, message=CLS)

    def ResetDefinedState(self, RST="*RST\n"):
        """
        RST = "*RST<term>" Set the power supply in a save defined state of the Delta Power Supply
        """
        return Communication().sendMessage(self.IPV4, message=RST)

    def TestGeneralInstructions(self):
        logger.debug("Self Identification runs:")
        self.Identification()
        logger.debug("Protected user data runs:")
        self.ProtectedUserData()
        logger.debug("Clear Error Queue runs:")
        self.ClearErrorQueue()
        logger.debug("Reset Defined State runs:")
        self.ResetDefinedState()
        return None


class SourceSubsystem:
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
        self.IPV4 = IPV4

    def __str__(self):
        return f'Manual: Source Subsystem - page 9 and 10 - Queries and Commands, for details print object.__doc__'

    def MaximumVoltage(self, MaximumVoltage="SOURce:VOLtage:MAXimum?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MaximumVoltage)

    def MaximumCurrent(self, MaximumCurrent="SOURce:CURrent:MAXimum?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MaximumCurrent)

    def MaximumNegativeCurrent(self, MaximumNegativeCurrent="SOURce:CURrent:NEGative:MAXimum?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MaximumNegativeCurrent)

    def MaximumPower(self, MaximumPower="SOURce:POWer:MAXimum?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MaximumPower)

    def MaximumNegativePower(self, MaximumNegativePower="SOURce:POWer:NEGative:MAXimum?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MaximumNegativePower)

    def SetVoltage(self, voltage):
        message = f'SOURce:VOLtage {voltage}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadVoltageSet(self, ReadVoltageSet="SOURce:VOLtage?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadVoltageSet)

    def SetCurrent(self, current):
        message = f'SOURce:CURrent {current}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadCurrentSet(self, ReadCurrentSet="SOURce:CURrent?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadCurrentSet)

    def SetNegativeCurrent(self, negativecurrent):
        message = f'SOURce:CURrent:NEGative {negativecurrent}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadNegativeCurrentSet(self, ReadNegativeCurrentSet="SOURce:CURrent:NEGative?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadNegativeCurrentSet)

    def SetPower(self, power):
        message = f"SOURce:POWer {power}\n"
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadPowerSet(self, ReadPowerSet="SOURce:POWer?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadPowerSet)

    def SetNegativePower(self, negativepower):
        message = f'SOURce:POWer:NEGative {negativepower}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadNegativePowerSet(self, ReadNegativePowerSet="SOURce:POWer:NEGative?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadNegativePowerSet)

    def ReadVoltageStepSize(self, ReadVoltageStepSize="SOURce:VOLtage:STEpsize?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadVoltageStepSize)

    def ReadCurrentStepSize(self, ReadCurrentStepSize="SOURce:CURrent:STEpsize?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadCurrentStepSize)

    def ReadPowerStepSize(self, ReadPowerStepSize="SOURce:POWer:STEpsize?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadPowerStepSize)

    def TestSourceSubsystem(self):
        logger.debug("Maximum Voltage runs:")
        self.MaximumVoltage()
        logger.debug("Maximum Current runs:")
        self.MaximumCurrent()
        logger.debug("Maximum Negative Current runs:")
        self.MaximumNegativeCurrent()
        logger.debug("Maximum Power runs:")
        self.MaximumPower()
        logger.debug("Maximum Negative Power runs:")
        self.MaximumNegativePower()
        logger.debug("Set Voltage runs:")
        self.SetVoltage(5)
        logger.debug("Read Last Voltage Set runs:")
        self.ReadVoltageSet()
        logger.debug("Set Current runs:")
        self.SetCurrent(5)
        logger.debug("Read Last Current Set runs:")
        self.ReadCurrentSet()
        logger.debug("Set Negative Current Set runs:")
        self.SetNegativeCurrent(-5)
        logger.debug("Read Last Negative Current Set runs:")
        self.ReadNegativeCurrentSet()
        logger.debug("Set Power Set runs:")
        self.SetPower(100)
        logger.debug("Read Last Power Set runs:")
        self.ReadPowerSet()
        logger.debug("Set Negative Power Set runs:")
        self.SetNegativePower(-100)
        logger.debug("Read Last Negative Power Set runs:")
        self.ReadNegativePowerSet()
        logger.debug("Read Voltage Stepsize runs:")
        self.ReadVoltageStepSize()
        logger.debug("Read Current Stepsize runs:")
        self.ReadCurrentStepSize()
        logger.debug("Read Power Stepsize runs:")
        self.ReadPowerStepSize()


class MeasureSubsystem:
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
        self.IPV4 = IPV4

    def __str__(self):
        return f'Manual: Measure Subsystem - page 10, 11 and 12 - Queries and Commands, for details print object.__doc__'

    def MeasureVoltage(self, MeasureVoltage="MEASure:VOLtage?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MeasureVoltage)

    def MeasureCurrent(self, MeasureCurrent="MEASure:CURrent?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MeasureCurrent)

    def MeasurePower(self, MeasurePower="MEASure:POWer?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MeasurePower)

    def SetAhMeasurementState(self, setting):
        message = f'MEASure:INStrument AH,STATE,{setting}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadAhMeasurementSetState(self, ReadAhMeasurementSetState="MEASure:INStrument AH,STATE?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadAhMeasurementSetState)

    def ReadAhMeasurementTimeHours(self, ReadAhMeasurementTimeHours="MEASure:INStrument AH,TIMEHR?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadAhMeasurementTimeHours)

    def ReadAhMeasurementTimeSeconds(self, ReadAhMeasurementTimeSeconds="MEASure:INStrument AH,TIMESEC?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadAhMeasurementTimeSeconds)

    def MeasureAhPositiveTotal(self, MeasureAhPositiveTotal="MEASure:INStrument AH,POS,TOTAL?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MeasureAhPositiveTotal)

    def MeasureAhNegativeTotal(self, MeasureAhNegativeTotal="MEASure:INStrument AH,NEG,TOTAL?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MeasureAhNegativeTotal)

    def MeasureAhMinimumCurrent(self, MeasureAhMinimumCurrent="MEASure:INStrument AH,POS,IMIN?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MeasureAhMinimumCurrent)

    def MeasureAhMaximumCurrent(self, MeasureAhMaximumCurrent="MEASure:INStrument AH,POS,IMAX?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MeasureAhMaximumCurrent)

    def MeasureAhMinimumNegativeCurrent(self, MeasureAhMinimumNegativeCurrent="MEASure:INStrument AH,NEG,IMIN?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MeasureAhMinimumNegativeCurrent)

    def MeasureAhMaximumNegativeCurrent(self, MeasureAhMaximumNegativeCurrent="MEASure:INStrument AH,NEG,IMAX?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MeasureAhMaximumNegativeCurrent)

    def SetWhMeasurementState(self, setting):
        message = f'MEASure:INStrument WH,STATE,{setting}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadWhMeasurementSetState(self, ReadWhMeasurementSetState="MEASure:INStrument WH,STATE?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadWhMeasurementSetState)

    def ReadWhMeasurementTimeHours(self, ReadWhMeasurementTimeHours="MEASure:INStrument WH,TIMEHR?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadWhMeasurementTimeHours)

    def ReadWhMeasurementTimeSeconds(self, ReadWhMeasurementTimeSeconds="MEASure:INStrument WH,TIMESEC?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadWhMeasurementTimeSeconds)

    def MeasureWhPositiveTotal(self, MeasureWhPositiveTotal="MEASure:INStrument WH,POS,TOTAL?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MeasureWhPositiveTotal)

    def MeasureWhNegativeTotal(self, MeasureWhNegativeTotal="MEASure:INStrument WH,NEG,TOTAL?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MeasureWhNegativeTotal)

    def MeasureWhMinimumCurrent(self, MeasureWhMinimumCurrent="MEASure:INStrument WH,POS,PMIN?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MeasureWhMinimumCurrent)

    def MeasureWhMaximumCurrent(self, MeasureWhMaximumCurrent="MEASure:INStrument WH,POS,PMAX?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MeasureWhMaximumCurrent)

    def MeasureWhMinimumNegativeCurrent(self, MeasureWhMinimumNegativeCurrent="MEASure:INStrument WH,NEG,PMIN?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MeasureWhMinimumNegativeCurrent)

    def MeasureWhMaximumNegativeCurrent(self, MeasureWhMaximumNegativeCurrent="MEASure:INStrument WH,NEG,PMAX?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MeasureWhMaximumNegativeCurrent)

    def MeasureTemperature(self, MeasureTemperature="MEASure:TEMperature?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=MeasureTemperature)

    def TestMeasureSubsystem(self):
        logger.debug("Measure voltage runs:")
        self.MeasureVoltage()
        logger.debug("Measure current runs:")
        self.MeasureCurrent()
        logger.debug("Measure power runs:")
        self.MeasurePower()
        logger.debug("Set Ah Measurement State runs:")
        self.SetAhMeasurementState('ON')
        logger.debug("Read Ah Measurement State runs:")
        self.ReadAhMeasurementSetState()
        logger.debug("Read Ah Time Hours runs:")
        self.ReadAhMeasurementTimeHours()
        logger.debug("Read Ah Time Seconds runs:")
        self.ReadAhMeasurementTimeSeconds()
        logger.debug("Measure Ah Positive runs:")
        self.MeasureAhPositiveTotal()
        logger.debug("Measure Ah Negative runs:")
        self.MeasureAhNegativeTotal()
        logger.debug("Measure Ah Minimum Current runs:")
        self.MeasureAhMinimumCurrent()
        logger.debug("Measure Ah Maximum Current runs:")
        self.MeasureAhMaximumCurrent()
        logger.debug("Measure Ah Minimum Negative Current runs:")
        self.MeasureAhMinimumNegativeCurrent()
        logger.debug("Measure Ah Maximum Negarive Current runs:")
        self.MeasureAhMinimumNegativeCurrent()
        logger.debug("Set Wh Measurement State runs:")
        self.SetWhMeasurementState('ON')
        logger.debug("Read Wh Measurement State runs:")
        self.ReadWhMeasurementSetState()
        logger.debug("Read Wh Time Hours runs:")
        self.ReadAhMeasurementTimeHours()
        logger.debug("Read Wh Time Seconds runs:")
        self.ReadWhMeasurementTimeSeconds()
        logger.debug("Measure Wh Positive runs:")
        self.MeasureWhPositiveTotal()
        logger.debug("Measure Wh Negative runs:")
        self.MeasureWhNegativeTotal()
        logger.debug("Measure Wh Minimum Current runs:")
        self.MeasureWhMinimumCurrent()
        logger.debug("Measure Wh Maximum Current runs:")
        self.MeasureWhMaximumCurrent()
        logger.debug("Measure Wh Minimum Negative Current runs:")
        self.MeasureWhMinimumNegativeCurrent()
        logger.debug("Measure Wh Maximum Negarive Current runs:")
        self.MeasureWhMaximumNegativeCurrent()
        logger.debug("Measure Temperature runs:")
        self.MeasureTemperature()


class SystemSubsystem:
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
        self.IPV4 = IPV4

    def __str__(self):
        return f'Manual: Measure Subsystem - page 13 and 14 - Queries and Commands, for details print object.__doc__'

    def SetRemoteShutDown(self, setting):
        message = f'SYSTem:RSD[:STAtus] {setting}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadRemoteShutDownSet(self, ReadRemoteShutDownSet="SYSTem:RSD[:STAtus]?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadRemoteShutDownSet)

    def SetVoltageLimit(self, voltagelimit, setting):
        message = f'SYSTem:LIMits:VOLtage {voltagelimit},{setting}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadVoltageLimitSet(self, ReadVoltageLimitSet="SYSTem:LIMits:VOLtage?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadVoltageLimitSet)

    def SetCurrentLimit(self, currentlimit, setting):
        message = f'SYSTem:LIMits:CURrent {currentlimit},{setting}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadCurrentLimitSet(self, ReadCurrentLimitSet="SYSTem:LIMits:CURrent?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadCurrentLimitSet)

    def SetNegativeCurrentLimit(self, negativecurrentlimit, setting):
        message = f'SYSTem:LIMits:CURrent:NEGative {negativecurrentlimit},{setting}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadNegativeCurrentLimitSet(self, ReadNegativeCurrentLimitSet="SYSTem:LIMits:CURrent:NEGative?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadNegativeCurrentLimitSet)

    def SetPowerLimit(self, powerlimit, setting):
        message = f'SYSTem:LIMits:POWer {powerlimit},{setting}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadPowerLimitSet(self, ReadPowerLimitSet="SYSTem:LIMits:POWer?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadPowerLimitSet)

    def SetNegativePowerLimit(self, negativepowerlimit, setting):
        message = f'SYSTem:LIMits:POWer:NEGative {negativepowerlimit},{setting}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadNegativePowerLimitSet(self, ReadNegativePowerLimitSet="SYSTem:LIMits:POWer:NEGative?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadNegativePowerLimitSet)

    def HighlightFrontpanel(self, message="SYSTem:FROntpanel:HIGhlight\n"):
        return Communication().sendMessage(self.IPV4, message=message)

    def LockFrontPanel(self, setting):
        message = f'SYSTem:FROntpanel[:STAtus] {setting}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadLockFrontpanelSet(self, ReadLockFrontpanelSet="SYSTem:FROntpanel[:STAtus]?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadLockFrontpanelSet)

    def LockControlFrontpanel(self, setting):
        message = f'SYSTem:FROntpanel:CONtrols {setting}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadLockControlFrontpanelSet(self, ReadLockControlFrontpanelSet="SYSTem:FROntpanel:CONtrols?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadLockControlFrontpanelSet)

    def SetTime(self, hour, minute, second):
        message = f'SYSTem:TIMe {hour},{minute},{second}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadTimeSet(self, ReadTimeSet="SYSTem:TIMe?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadTimeSet)

    def SetDate(self, year, month, day):
        message = f'SYSTem:DATe {year},{month},{day}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadDateSet(self, ReadDateSet="SYSTem:DATe?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadDateSet)

    def ReadErrors(self, ReadErrors="SYSTem:ERRor?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadErrors)

    def ReadWarnings(self, ReadWarnings="SYSTem:WARning?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadWarnings)

    def SetWatchdog(self, timer):
        message = f'SYSTem:COMmunicate:WATchdog SET,{timer}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadWatchdogSet(self, ReadWatchdogSet="SYSTem:COMmunicate:WATchdog SET?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadWatchdogSet)

    def ReadCurrentWatchdogState(self, ReadCurrentWatchdogState="SYSTem:COMmunicate:WATchdog?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadCurrentWatchdogState)

    def DisableWatchdog(self, message="SYSTem:COMmunicate:WATchdog STOP\n"):
        return Communication().sendMessage(self.IPV4, message=message)

    def TestWatchdog(self, message="SYSTem:COMmunicate:WATchdog TEST\n"):
        return Communication().sendMessage(self.IPV4, message=message)

    def TestSystemSubsystem(self):
        logger.debug("Remote Shut Down Set runs:")
        self.SetRemoteShutDown('OFF')
        logger.debug("Read Remote Shut Down Set runs:")
        self.ReadRemoteShutDownSet()
        logger.debug("Set Voltage Limit runs:")
        self.SetVoltageLimit(50, 'ON')
        logger.debug("Read Voltage Limit Set runs:")
        self.ReadVoltageLimitSet()
        logger.debug("Set Current Limit runs:")
        self.SetCurrentLimit(100, 'ON')
        logger.debug("Read Current Limit Set runs:")
        self.ReadCurrentLimitSet()
        logger.debug("Set Negative Current Limit runs:")
        self.SetNegativeCurrentLimit(-100, 'ON')
        logger.debug("Read Negative Current Limit Set runs:")
        self.ReadNegativeCurrentLimitSet()
        logger.debug("Set Power Limit runs:")
        self.SetPowerLimit(4000, 'ON')
        logger.debug("Read Power Limit Set runs:")
        self.ReadPowerLimitSet()
        logger.debug("Set Negative Power Limit runs:")
        self.SetNegativePowerLimit(-4000, 'ON')
        logger.debug("Read Negative Power Limit Set runs:")
        self.ReadNegativePowerLimitSet()
        logger.debug("Highlight Frontpanel Set runs:")
        self.HighlightFrontpanel()
        logger.debug("Set Lock Frontpanel runs:")
        self.LockFrontPanel('ON')
        logger.debug("Read Lock Frontpanel Set runs:")
        self.ReadLockFrontpanelSet()
        logger.debug("Set Lock Control Frontpanel runs:")
        self.LockControlFrontpanel('ON')
        logger.debug("Read Lock Control Frontpanel Set runs:")
        self.ReadLockControlFrontpanelSet()
        logger.debug("Time Set runs:")
        self.SetTime(9, 10, 0)
        logger.debug("Read Time Set runs:")
        self.ReadTimeSet()
        logger.debug("Date Set runs:")
        self.SetDate(2021, 9, 8)
        logger.debug("Read Date Set runs:")
        self.ReadDateSet()
        logger.debug("Read Errors runs:")
        self.ReadErrors()
        logger.debug("Read Warnings runs:")
        self.ReadWarnings()
        logger.debug("Set Watchdog runs:")
        self.SetWatchdog(500)
        logger.debug("Read Watchdog Set runs:")
        self.ReadWatchdogSet()
        logger.debug("Read Current Watchdog State runs:")
        self.ReadCurrentWatchdogState()
        logger.debug("Disable Watchdog runs:")
        self.DisableWatchdog()
        logger.debug("Test Watchdog runs:")
        self.TestWatchdog()


class OutputSubsystem:
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
        self.IPV4 = IPV4

    def __str__(self):
        return f'Output Subsystem - page 17 - Queries and Commands, for details print object.__doc__'

    def SetOutput(self, setting):
        message = f'OUTPut {setting}\n'
        return Communication().sendMessage(self.IPV4, message=message)

    def ReadOutputSet(self, ReadOutputSet="OUTPut?\n"):
        return Communication().sendReceiveMessage(self.IPV4, message=ReadOutputSet)

    def TestOutputSubsystem(self):
        logger.debug("Output State Set runs:")
        self.SetOutput(1)
        logger.debug("Read Output State runs: ")
        self.ReadOutputSet()
        logger.debug("Output State Set runs:")
        self.SetOutput(0)
        logger.debug("Read Output State runs: ")
        self.ReadOutputSet()


class ShutdownOperation:
    """
        Shutdown Functional Operation
        -----------------------------------------------------------------------------------------------------------------
        IPV4: Address of the desired device to start shutdown operation
        -----------------------------------------------------------------------------------------------------------------
        ShutdownOperation(IPV4).limitShutdownValues() -> limits all limit set points (voltage, current and power) to zero.
        -----------------------------------------------------------------------------------------------------------------
        ShutdownOperation(IPV4).setShutdownValues() -> Sets all set points (voltage, current and power) to zero.
        -----------------------------------------------------------------------------------------------------------------
        ShutdownOperation(IPV4).setShutdownOutput() -> Sets the output to zero.
        -----------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, IPV4):
        self.IPV4 = IPV4

    def __str__(self):
        return f'Shutdown Operation, for details print object.__doc__'

    def limitShutdownValues(self):
        SystemSubsystem(self.IPV4).SetVoltageLimit(0, 'ON')
        SystemSubsystem(self.IPV4).ReadVoltageLimitSet()
        SystemSubsystem(self.IPV4).SetCurrentLimit(0, 'ON')
        SystemSubsystem(self.IPV4).ReadVoltageLimitSet()
        SystemSubsystem(self.IPV4).SetNegativeCurrentLimit(0, 'ON')
        SystemSubsystem(self.IPV4).ReadNegativeCurrentLimitSet()
        SystemSubsystem(self.IPV4).SetPowerLimit(0, 'ON')
        SystemSubsystem(self.IPV4).ReadPowerLimitSet()
        SystemSubsystem(self.IPV4).SetNegativePowerLimit(0, 'ON')
        SystemSubsystem(self.IPV4).ReadNegativePowerLimitSet()

    def setShutdownValues(self):
        SourceSubsystem(self.IPV4).SetVoltage(0)
        SourceSubsystem(self.IPV4).ReadVoltageSet()
        SourceSubsystem(self.IPV4).SetCurrent(0)
        SourceSubsystem(self.IPV4).ReadCurrentSet()
        SourceSubsystem(self.IPV4).SetNegativeCurrent(0)
        SourceSubsystem(self.IPV4).ReadNegativeCurrentSet()
        SourceSubsystem(self.IPV4).SetPower(0)
        SourceSubsystem(self.IPV4).ReadPowerSet()
        SourceSubsystem(self.IPV4).SetNegativePower(0)
        SourceSubsystem(self.IPV4).ReadNegativePowerSet()

    def setShutdownOutput(self):
        OutputSubsystem(self.IPV4).SetOutput(0)
        OutputSubsystem(self.IPV4).ReadOutputSet()
        SystemSubsystem(self.IPV4).HighlightFrontpanel()

    def removeLimitShutdownValues(self):
        SystemSubsystem(self.IPV4).SetVoltageLimit(0, 'OFF')
        SystemSubsystem(self.IPV4).ReadVoltageLimitSet()
        SystemSubsystem(self.IPV4).SetCurrentLimit(0, 'OFF')
        SystemSubsystem(self.IPV4).ReadVoltageLimitSet()
        SystemSubsystem(self.IPV4).SetNegativeCurrentLimit(0, 'OFF')
        SystemSubsystem(self.IPV4).ReadNegativeCurrentLimitSet()
        SystemSubsystem(self.IPV4).SetPowerLimit(0, 'OFF')
        SystemSubsystem(self.IPV4).ReadPowerLimitSet()
        SystemSubsystem(self.IPV4).SetNegativePowerLimit(0, 'OFF')
        SystemSubsystem(self.IPV4).ReadNegativePowerLimitSet()


class WatchdogOperation(threading.Thread):
    """
        Watchdog Functional Operation
        -----------------------------------------------------------------------------------------------------------------
        IPV4: Address of the desired device to start shutdown operation
        -----------------------------------------------------------------------------------------------------------------
        Timer: It is the set point for the watchdog operation, if watchdog time cannot be triggered withing this time
        period, it will switch of the output of the delta for safety.
        -----------------------------------------------------------------------------------------------------------------
        Sleeptime: This thread operates at given time period and sleeps at that timeline for the rest of the main operation.
        -----------------------------------------------------------------------------------------------------------------
        Be careful while setting it that timer is higher than sleep time for proper operation.
        -----------------------------------------------------------------------------------------------------------------
        If device fails with watch operation, it must be resetted manualy for safety reasons.
        -----------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, IPV4, timer, sleeptime, deamonState=True):
        super().__init__()
        self.IPV4 = IPV4
        self.timer = timer * 1000
        self.sleeptime = sleeptime
        self.deamonState = deamonState
        self._stop_event = threading.Event()
        self.setDaemon(self.deamonState)

    def __str__(self):
        return f'Watchdog Operation, for details print object.__doc__'

    def stop(self):
        logger.debug("Stop watchdog thread has been called!")
        return self._stop_event.set()

    def disableWatchdog(self):
        return SystemSubsystem(self.IPV4).DisableWatchdog()

    def run(self):
        logger.debug("Watchdog thread has been started!")
        SystemSubsystem(self.IPV4).SetWatchdog(self.timer)
        while not self._stop_event.is_set():
            logger.debug("Watchdog thread is running!")
            time.sleep(self.sleeptime)
            if float(SystemSubsystem(self.IPV4).ReadWatchdogSet()) != 0:
                logger.debug('Watchdog is still active!')
            else:
                logger.debug('Watchdog has been failed!')
                self.stop()
        logger.debug("Watchdog thread has been stopped!")


class BasicDataloggerOperation(threading.Thread):
    """
        Basic Datalogger Functional Operation
        -----------------------------------------------------------------------------------------------------------------
        Its own class attribute dataframe is; dataFrameBasic = ['Voltage', 'Current', 'Power']
        -----------------------------------------------------------------------------------------------------------------
        IPV4: Address of the desired device to start shutdown operation
        -----------------------------------------------------------------------------------------------------------------
        loggingTime: It is also same with sleep time of the thread. Function will work at every logging time
        -----------------------------------------------------------------------------------------------------------------
        printColor: It is used for optional color printing for the logged data at terminal. Default color is green.
        Note: Available colors are, purple, blue, cyan, green, yellow, red and normal
        -----------------------------------------------------------------------------------------------------------------
        There are three main logger types, be sure that one of them is being used only!
        -----------------------------------------------------------------------------------------------------------------
    """
    dataFrameBasic = ['Voltage', 'Current', 'Power']
    fileName = 'BasicDatalogger'

    def __init__(self, IPV4, loggingTime, printColor='green', deamonState=True):
        super().__init__()
        self.IPV4 = IPV4
        self.printColor = printColor
        self.loggingTime = loggingTime
        self.deamonState = deamonState
        self.setDaemon(self.deamonState)
        self._stop_event = threading.Event()
        self.finalName = f'{BasicDataloggerOperation.fileName} {datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S")}.txt'
        open(f'{self.finalName}', "w+").close()
        BasicDataloggerOperation.dataFrameBasic.insert(0, 'Timestamp')

    def __str__(self):
        return f'Basic Datalogger Operation, for details print object.__doc__'

    def csvLogger(self):
        csvFile = open(self.finalName, 'a', newline='')
        write = csv.writer(csvFile)
        write.writerow(BasicDataloggerOperation.dataFrameBasic)
        csvFile.close()
        BasicDataloggerOperation.dataFrameBasic[0] = time.strftime('%d-%m-%Y %H:%M:%S')
        return BasicDataloggerOperation.dataFrameBasic

    def updateBasicDataFrame(self):
        BasicDataloggerOperation.dataFrameBasic[1] = MeasureSubsystem(self.IPV4).MeasureVoltage()
        BasicDataloggerOperation.dataFrameBasic[2] = MeasureSubsystem(self.IPV4).MeasureCurrent()
        BasicDataloggerOperation.dataFrameBasic[3] = MeasureSubsystem(self.IPV4).MeasurePower()
        logger.debug(
            f'Voltage: {BasicDataloggerOperation.dataFrameBasic[1]}V, Current: {BasicDataloggerOperation.dataFrameBasic[2]}A, '
            f'Power: {BasicDataloggerOperation.dataFrameBasic[3]}W')
        cprint.printColorful(
            f'Voltage: {BasicDataloggerOperation.dataFrameBasic[1]}V, Current: {BasicDataloggerOperation.dataFrameBasic[2]}A, '
            f'Power: {BasicDataloggerOperation.dataFrameBasic[3]}W', self.printColor)
        return BasicDataloggerOperation.dataFrameBasic

    def stop(self):
        logger.debug('Datalogger stop event has been started!')
        self._stop_event.set()

    def run(self):
        logger.debug('Datalogger thread class has been started!')
        while not self._stop_event.is_set():
            logger.debug('Datalogger thread class for basic dataframe is running!')
            self.csvLogger()
            self.updateBasicDataFrame()
            time.sleep(self.loggingTime)
        logger.debug('Datalogger thread class has been stopped!')


class AhDataloggerOperation(threading.Thread):
    """
        Ah Datalogger Functional Operation
        -----------------------------------------------------------------------------------------------------------------
        Its own class attribute dataframe is; dataFrameAh = ['Voltage', 'Current', 'Power', 'PositiveAh', 'NegativeAh', 'AhSeconds', 'AhHours']
        -----------------------------------------------------------------------------------------------------------------
        IPV4: Address of the desired device to start shutdown operation
        -----------------------------------------------------------------------------------------------------------------
        loggingTime: It is also same with sleep time of the thread. Function will work at every logging time
        -----------------------------------------------------------------------------------------------------------------
        printColor: It is used for optional color printing for the logged data at terminal. Default color is green.
        Note: Available colors are, purple, blue, cyan, green, yellow, red and normal
        -----------------------------------------------------------------------------------------------------------------
        There are three main logger types, be sure that one of them is being used only especially Ah vs Wh!
        -----------------------------------------------------------------------------------------------------------------
    """
    dataFrameAh = ['Voltage', 'Current', 'Power', 'PositiveAh', 'NegativeAh', 'AhSeconds', 'AhHours']
    fileName = 'AhDatalogger'

    def __init__(self, IPV4, loggingTime, printColor='green', deamonState=True):
        super().__init__()
        self.IPV4 = IPV4
        self.loggingTime = loggingTime
        self.printColor = printColor
        self.deamonState = deamonState
        self.setDaemon(self.deamonState)
        self._stop_event = threading.Event()
        self.finalName = f'{AhDataloggerOperation.fileName} {datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S")}.txt'
        open(f'{self.finalName}', "w+").close()
        AhDataloggerOperation.dataFrameAh.insert(0, 'Timestamp')

    def __str__(self):
        return f'Ah Datalogger Operation, for details print object.__doc__'

    def csvLogger(self):
        csvFile = open(self.finalName, 'a', newline='')
        write = csv.writer(csvFile)
        write.writerow(AhDataloggerOperation.dataFrameAh)
        csvFile.close()
        AhDataloggerOperation.dataFrameAh[0] = time.strftime('%d-%m-%Y %H:%M:%S')
        return AhDataloggerOperation.dataFrameAh

    def updateAhDataFrame(self):
        AhDataloggerOperation.dataFrameAh[1] = MeasureSubsystem(self.IPV4).MeasureVoltage()
        AhDataloggerOperation.dataFrameAh[2] = MeasureSubsystem(self.IPV4).MeasureCurrent()
        AhDataloggerOperation.dataFrameAh[3] = MeasureSubsystem(self.IPV4).MeasurePower()
        AhDataloggerOperation.dataFrameAh[4] = MeasureSubsystem(self.IPV4).MeasureAhPositiveTotal()
        AhDataloggerOperation.dataFrameAh[5] = MeasureSubsystem(self.IPV4).MeasureAhNegativeTotal()
        AhDataloggerOperation.dataFrameAh[6] = MeasureSubsystem(self.IPV4).ReadAhMeasurementTimeSeconds()
        AhDataloggerOperation.dataFrameAh[7] = MeasureSubsystem(self.IPV4).ReadAhMeasurementTimeHours()
        logger.debug(
            f'Voltage: {AhDataloggerOperation.dataFrameAh[1]}V, Current: {AhDataloggerOperation.dataFrameAh[2]}A, '
            f'Power: {AhDataloggerOperation.dataFrameAh[3]}W, PositiveAh: {AhDataloggerOperation.dataFrameAh[4]}, '
            f'NegativeAh: {AhDataloggerOperation.dataFrameAh[5]}, AhSeconds: {AhDataloggerOperation.dataFrameAh[6]} '
            f'AhHours: {AhDataloggerOperation.dataFrameAh[7]}')
        cprint.printColorful(
            f'Voltage: {AhDataloggerOperation.dataFrameAh[1]}V, Current: {AhDataloggerOperation.dataFrameAh[2]}A, '
            f'Power: {AhDataloggerOperation.dataFrameAh[3]}W, PositiveAh: {AhDataloggerOperation.dataFrameAh[4]}, '
            f'NegativeAh: {AhDataloggerOperation.dataFrameAh[5]}, AhSeconds: {AhDataloggerOperation.dataFrameAh[6]} '
            f'AhHours: {AhDataloggerOperation.dataFrameAh[7]}', self.printColor)
        return AhDataloggerOperation.dataFrameAh

    def stop(self):
        logger.debug('Datalogger stop event has been started!')
        self._stop_event.set()

    def run(self):
        logger.debug('Datalogger thread class has been started!')
        MeasureSubsystem(self.IPV4).SetAhMeasurementState('ON')
        while not self._stop_event.is_set():
            logger.debug('Datalogger thread class for Ah dataframe is running!')
            self.csvLogger()
            self.updateAhDataFrame()
            time.sleep(self.loggingTime)
        logger.debug('Datalogger thread class has been stopped!')


class WhDataloggerOperation(threading.Thread):
    """
        Ah Datalogger Functional Operation
        -----------------------------------------------------------------------------------------------------------------
        Its own class attribute dataframe is; dataFrameWh = ['Voltage', 'Current', 'Power', 'PositiveWh', 'NegativeWh', 'WhSeconds', 'WhHours']
        -----------------------------------------------------------------------------------------------------------------
        IPV4: Address of the desired device to start shutdown operation
        -----------------------------------------------------------------------------------------------------------------
        loggingTime: It is also same with sleep time of the thread. Function will work at every logging time
        -----------------------------------------------------------------------------------------------------------------
        printColor: It is used for optional color printing for the logged data at terminal. Default color is green.
        Note: Available colors are, purple, blue, cyan, green, yellow, red and normal
        -----------------------------------------------------------------------------------------------------------------
        There are three main logger types, be sure that one of them is being used only especially Ah vs Wh!
        -----------------------------------------------------------------------------------------------------------------
    """
    dataFrameWh = ['Voltage', 'Current', 'Power', 'PositiveWh', 'NegativeWh', 'WhSeconds', 'WhHours']
    fileName = 'WhDatalogger'

    def __init__(self, IPV4, loggingTime, printColor='green', deamonState=True):
        super().__init__()
        self.IPV4 = IPV4
        self.loggingTime = loggingTime
        self.printColor = printColor
        self.deamonState = deamonState
        self.setDaemon(self.deamonState)
        self._stop_event = threading.Event()
        self.finalName = f'{WhDataloggerOperation.fileName} {datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S")}.txt'
        open(f'{self.finalName}', "w+").close()
        WhDataloggerOperation.dataFrameWh.insert(0, 'Timestamp')

    def __str__(self):
        return f'Wh Datalogger Operation, for details print object.__doc__'

    def csvLogger(self):
        csvFile = open(self.finalName, 'a', newline='')
        write = csv.writer(csvFile)
        write.writerow(WhDataloggerOperation.dataFrameWh)
        csvFile.close()
        WhDataloggerOperation.dataFrameWh[0] = time.strftime('%d-%m-%Y %H:%M:%S')
        return WhDataloggerOperation.dataFrameWh

    def updateWhDataFrame(self):
        WhDataloggerOperation.dataFrameWh[1] = MeasureSubsystem(self.IPV4).MeasureVoltage()
        WhDataloggerOperation.dataFrameWh[2] = MeasureSubsystem(self.IPV4).MeasureCurrent()
        WhDataloggerOperation.dataFrameWh[3] = MeasureSubsystem(self.IPV4).MeasurePower()
        WhDataloggerOperation.dataFrameWh[4] = MeasureSubsystem(self.IPV4).MeasureWhPositiveTotal()
        WhDataloggerOperation.dataFrameWh[5] = MeasureSubsystem(self.IPV4).MeasureWhNegativeTotal()
        WhDataloggerOperation.dataFrameWh[6] = MeasureSubsystem(self.IPV4).ReadWhMeasurementTimeSeconds()
        WhDataloggerOperation.dataFrameWh[7] = MeasureSubsystem(self.IPV4).ReadWhMeasurementTimeHours()
        logger.debug(
            f'Voltage: {WhDataloggerOperation.dataFrameWh[1]}V, Current: {WhDataloggerOperation.dataFrameWh[2]}A, '
            f'Power: {WhDataloggerOperation.dataFrameWh[3]}W, PositiveWh: {WhDataloggerOperation.dataFrameWh[4]}, '
            f'NegativeWh: {WhDataloggerOperation.dataFrameWh[5]}, WhHours: {WhDataloggerOperation.dataFrameWh[6]}, '
            f'WhSeconds: {WhDataloggerOperation.dataFrameWh[7]}, WhHours: {WhDataloggerOperation.dataFrameWh[6]}')
        cprint.printColorful(
            f'Voltage: {WhDataloggerOperation.dataFrameWh[1]}V, Current: {WhDataloggerOperation.dataFrameWh[2]}A, '
            f'Power: {WhDataloggerOperation.dataFrameWh[3]}W, PositiveWh: {WhDataloggerOperation.dataFrameWh[4]}, '
            f'NegativeWh: {WhDataloggerOperation.dataFrameWh[5]}, WhHours: {WhDataloggerOperation.dataFrameWh[6]}, '
            f'WhSeconds: {WhDataloggerOperation.dataFrameWh[7]}, WhHours: {WhDataloggerOperation.dataFrameWh[6]}',
            self.printColor)
        return WhDataloggerOperation.dataFrameWh

    def stop(self):
        logger.debug('Datalogger stop event has been started!')
        self._stop_event.set()

    def run(self):
        logger.debug('Datalogger thread class has been started!')
        MeasureSubsystem(self.IPV4).SetWhMeasurementState('ON')
        while not self._stop_event.is_set():
            logger.debug('Datalogger thread class for Wh dataframe is running!')
            self.csvLogger()
            self.updateWhDataFrame()
            time.sleep(self.loggingTime)
        logger.debug('Datalogger thread class has been stopped!')


class ChargingOperation(threading.Thread):
    """
        Charging Functional Operation
        -----------------------------------------------------------------------------------------------------------------
        IPV4: Address of the desired device to start shutdown operation
        -----------------------------------------------------------------------------------------------------------------
        sleepTime: Sleep time of the thread, every sleep time, charging state is being checked.
        -----------------------------------------------------------------------------------------------------------------
        bulkCurrent: Current setting for the bulk stage
        -----------------------------------------------------------------------------------------------------------------
        bulkVoltage: Voltage setting for the bulk stage
        -----------------------------------------------------------------------------------------------------------------
        absorptionCurrent: Current setting for the absorption stage, absorptionCurrent = 0.8 * bulkCurrent
        -----------------------------------------------------------------------------------------------------------------
        absorptionVoltage: Voltage setting for the absorption stage, absorptionVoltage = bulkVoltage
        -----------------------------------------------------------------------------------------------------------------
        floatCurrent: Current setting for the floating stage, floatCurrent =  0.02 * bulkCurrent
        -----------------------------------------------------------------------------------------------------------------
        floatVoltage: Voltage setting for the floating stage
        -----------------------------------------------------------------------------------------------------------------
        floatTime: Time setting for the floating stage timer, when it is done charging operion stops!
        -----------------------------------------------------------------------------------------------------------------
        There are three main logger types, be sure that one of them is being used only especially Ah vs Wh!
        -----------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, IPV4='0.0.0.0', sleepTime=10, bulkCurrent=0.0, bulkVoltage=0.0, floatVoltage=0.0, floatTime=0.0,
                 deamonState=True):
        super().__init__()
        self.IPV4 = IPV4
        self.sleepTime = sleepTime
        self.bulkCurrent = bulkCurrent
        self.bulkVoltage = bulkVoltage
        self.absorptionCurrent = self.bulkCurrent * 0.8
        self.absorptionVoltage = self.bulkVoltage
        self.floatCurrent = self.bulkCurrent * 0.02
        self.floatVoltage = floatVoltage
        self.floatTime = floatTime
        self.bulkMode = True
        self.absorptionMode = False
        self.floatingMode = False
        self.deamonState = deamonState
        self.setDaemon(self.deamonState)
        self._stop_event = threading.Event()
        self.bulkInfo = 0
        self.absorptionInfo = 0

    def __str__(self):
        return f'Charging Operation, for details print object.__doc__'

    def chargingInitialize(self):
        logger.debug('Charging is being initialized!')
        cprint.printFeedback('Charging is being initialized!')
        SystemSubsystem(self.IPV4).HighlightFrontpanel()
        SystemSubsystem(self.IPV4).SetVoltageLimit(self.bulkVoltage, 'ON')
        SystemSubsystem(self.IPV4).ReadVoltageLimitSet()
        SystemSubsystem(self.IPV4).SetCurrentLimit(self.bulkCurrent + 10, 'ON')
        SystemSubsystem(self.IPV4).ReadCurrentLimitSet()
        SystemSubsystem(self.IPV4).SetPowerLimit(self.bulkVoltage * self.bulkCurrent + 500, 'ON')
        SystemSubsystem(self.IPV4).ReadPowerLimitSet()
        time.sleep(1)

    def chargingFinalize(self):
        logger.debug(f'Charging is being finalized!')
        cprint.printFeedback(f'Charging is being finalized!')
        ShutdownOperation(self.IPV4).setShutdownOutput()
        ShutdownOperation(self.IPV4).setShutdownValues()
        ShutdownOperation(self.IPV4).limitShutdownValues()
        time.sleep(1)

    def outputInitialize(self):
        logger.debug('Output is Initialized!')
        cprint.printFeedback('Output is Initialized!')
        OutputSubsystem(self.IPV4).SetOutput(1)
        OutputSubsystem(self.IPV4).ReadOutputSet()
        time.sleep(1)

    def bulkStage(self):
        logger.debug('Bulk Stage is Initialized!')
        cprint.printFeedback('Bulk Stage is Initialized!')
        SourceSubsystem(self.IPV4).SetVoltage(self.bulkVoltage)
        SourceSubsystem(self.IPV4).ReadVoltageSet()
        SourceSubsystem(self.IPV4).SetCurrent(self.bulkCurrent)
        SourceSubsystem(self.IPV4).SetPower(self.bulkCurrent * self.bulkVoltage + 50)
        SourceSubsystem(self.IPV4).ReadPowerSet()
        time.sleep(1)

    def absorptionStage(self):
        logger.debug('Absorption Stage is Initialized!')
        cprint.printFeedback('Absorption Stage is Initialized!')
        SourceSubsystem(self.IPV4).SetVoltage(self.absorptionVoltage)
        SourceSubsystem(self.IPV4).ReadVoltageSet()
        SourceSubsystem(self.IPV4).SetCurrent(self.absorptionCurrent)
        SourceSubsystem(self.IPV4).SetPower(self.absorptionVoltage * self.absorptionCurrent + 50)
        SourceSubsystem(self.IPV4).ReadPowerSet()
        time.sleep(1)

    def floatingStage(self):
        logger.debug('Floating Stage is Initialized!')
        cprint.printFeedback('Floating Stage is Initialized!')
        SourceSubsystem(self.IPV4).SetVoltage(self.floatVoltage)
        SourceSubsystem(self.IPV4).ReadVoltageSet()
        SourceSubsystem(self.IPV4).SetCurrent(self.floatCurrent)
        SourceSubsystem(self.IPV4).ReadCurrentSet()
        SourceSubsystem(self.IPV4).SetPower(self.floatCurrent * self.floatVoltage + 500)
        SourceSubsystem(self.IPV4).ReadPowerSet()
        time.sleep(1)

    def checkChargingStage(self):
        if (float(MeasureSubsystem(self.IPV4).MeasureCurrent()) < self.absorptionCurrent) and self.bulkMode:
            self.absorptionStage()
            self.bulkMode = False
            self.absorptionMode = True
        elif (float(MeasureSubsystem(self.IPV4).MeasureCurrent()) < self.floatCurrent) and self.absorptionMode:
            self.floatingStage()
            self.absorptionMode = False
            self.floatingMode = True

        if self.bulkMode:
            logger.debug('Bulk Mode is active!')
            if self.bulkInfo < 1:
                cprint.printFeedback('Bulk Mode is active!')
                self.bulkInfo += 1
        elif self.absorptionMode:
            logger.debug('Absorption mode is active!')
            if self.absorptionInfo < 1:
                cprint.printFeedback('Absorption mode is active!')
                self.absorptionInfo += 1
        elif self.floatingMode:
            logger.debug('Floating mode is active!')
            cprint.printFeedback('Floating mode is active!')
            logger.debug(f'Float time is: {self.floatTime}')
            time.sleep(self.floatTime)
            self.stop()

    def stop(self):
        logger.debug('Charging stop event has been started!')
        cprint.printFeedback('Charging stop event has been started!')
        self._stop_event.set()

    def run(self):
        logger.debug('Charging thread class has been started!')
        self.chargingInitialize()
        self.bulkStage()
        self.outputInitialize()
        while not self._stop_event.is_set():
            logger.debug('Charging thread class is running!')
            time.sleep(self.sleepTime)
            self.checkChargingStage()
        self.chargingFinalize()
        logger.debug('Charging thread class has been stopped!')


class DischargingOperation(threading.Thread):
    """
        Discharging Functional Operation
        -----------------------------------------------------------------------------------------------------------------
        IPV4: Address of the desired device to start shutdown operation
        -----------------------------------------------------------------------------------------------------------------
        sleeptime: Sleep time of the thread, every sleep time, charging state is being checked.
        -----------------------------------------------------------------------------------------------------------------
        dischargeCurrent: Maximum discharging current set
        -----------------------------------------------------------------------------------------------------------------
        dischargeVoltage: Minimum voltage that battery can be discharged
        -----------------------------------------------------------------------------------------------------------------
        cutoffCurrent: Minimum current to decide stop discharging operation
        -----------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, IPV4='0.0.0.0', sleepTime=10, dischargeCurrent=0.0, dischargeVoltage=0.0, cutoffCurrent=0.0,
                 deamonState=True):
        super().__init__()
        self.IPV4 = IPV4
        self.sleepTime = sleepTime
        self.dischargeCurrent = dischargeCurrent
        self.dischargeVoltage = dischargeVoltage
        self.cutoffCurrent = cutoffCurrent
        self.deamonState = deamonState
        self.setDaemon(self.deamonState)
        self._stop_event = threading.Event()

    def __str__(self):
        return f'Discharging Operation, for details print object.__doc__'

    def dischargingInitialize(self):
        logger.debug('Discharging is being initialized!')
        SystemSubsystem(self.IPV4).HighlightFrontpanel()
        SystemSubsystem(self.IPV4).SetVoltageLimit(self.dischargeVoltage, 'ON')
        SystemSubsystem(self.IPV4).ReadVoltageLimitSet()
        SystemSubsystem(self.IPV4).SetNegativeCurrentLimit(self.dischargeCurrent - 10, 'ON')
        SystemSubsystem(self.IPV4).ReadNegativeCurrentLimitSet()
        SystemSubsystem(self.IPV4).SetNegativePowerLimit(self.dischargeVoltage * self.dischargeCurrent - 500, 'ON')
        SystemSubsystem(self.IPV4).ReadNegativePowerLimitSet()
        time.sleep(1)

    def dischargingFinalize(self):
        logger.debug(f'Discharging is being finalized!')
        ShutdownOperation(self.IPV4).setShutdownOutput()
        ShutdownOperation(self.IPV4).setShutdownValues()
        ShutdownOperation(self.IPV4).limitShutdownValues()
        time.sleep(1)

    def outputInitialize(self):
        OutputSubsystem(self.IPV4).SetOutput(1)
        OutputSubsystem(self.IPV4).ReadOutputSet()
        time.sleep(1)

    def dischargingStage(self):
        logger.debug('Discharging stage is started!')
        SourceSubsystem(self.IPV4).SetVoltage(self.dischargeVoltage)
        SourceSubsystem(self.IPV4).ReadVoltageSet()
        SourceSubsystem(self.IPV4).SetNegativeCurrent(self.dischargeCurrent)
        SourceSubsystem(self.IPV4).ReadNegativeCurrentSet()
        SourceSubsystem(self.IPV4).SetNegativePower(self.dischargeCurrent * self.dischargeVoltage - 50)
        SourceSubsystem(self.IPV4).ReadNegativePowerSet()
        time.sleep(1)

    def checkDischargingStage(self):
        if float(MeasureSubsystem(self.IPV4).MeasureCurrent()) > self.cutoffCurrent:
            self.stop()
        else:
            logger.debug('Discharging is still running!')

    def stop(self):
        logger.debug('Discharging stop event has been started!')
        self._stop_event.set()

    def run(self):
        logger.debug('Discharging thread class has been started!')
        self.dischargingInitialize()
        self.dischargingStage()
        self.outputInitialize()
        while not self._stop_event.is_set():
            logger.debug('Discharging thread class is running!')
            time.sleep(self.sleepTime)
            self.checkDischargingStage()
        self.dischargingFinalize()
        logger.debug('Discharging thread class has been stopped!')


class CyclingOperation(threading.Thread):
    """
        Charging Functional Operation
        -----------------------------------------------------------------------------------------------------------------
        IPV4: Address of the desired device to start shutdown operation
        -----------------------------------------------------------------------------------------------------------------
        sleepTime: Sleep time of the thread, every sleep time, charging state is being checked.
        -----------------------------------------------------------------------------------------------------------------
        cycleTime: Total number of cycling the battery, charging and discharging (discharging and charging), it counts as one cycling!
        -----------------------------------------------------------------------------------------------------------------
        bulkCurrent: Current setting for the bulk stage
        -----------------------------------------------------------------------------------------------------------------
        bulkVoltage: Voltage setting for the bulk stage
        -----------------------------------------------------------------------------------------------------------------
        absorptionCurrent: Current setting for the absorption stage, absorptionCurrent = 0.8 * bulkCurrent
        -----------------------------------------------------------------------------------------------------------------
        absorptionVoltage: Voltage setting for the absorption stage, absorptionVoltage = bulkVoltage
        -----------------------------------------------------------------------------------------------------------------
        floatCurrent: Current setting for the floating stage, floatCurrent =  0.02 * bulkCurrent
        -----------------------------------------------------------------------------------------------------------------
        floatVoltage: Voltage setting for the floating stage
        -----------------------------------------------------------------------------------------------------------------
        floatTime: Time setting for the floating stage timer, when it is done charging operation stops!
        -----------------------------------------------------------------------------------------------------------------
        dischargeCurrent: Maximum discharging current set
        -----------------------------------------------------------------------------------------------------------------
        dischargeVoltage: Minimum voltage that battery can be discharged
        -----------------------------------------------------------------------------------------------------------------
        cutoffCurrent: Minimum current to decide stop discharging operation
        -----------------------------------------------------------------------------------------------------------------
        afterChargingRestTime: Timer to decide rest time after charging part is done!
        -----------------------------------------------------------------------------------------------------------------
        afterDischargingRestTime: Timer to decide rest time after discharging part is done!
        -----------------------------------------------------------------------------------------------------------------
        startCharging: Flag to decide starting stage (if True -> Charging starts , if False -> Discharging starts!)
        -----------------------------------------------------------------------------------------------------------------
        There are three main logger types, be sure that one of them is being used especially Ah or Wh!
        -----------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, IPV4='0.0.0.0', sleepTime=10, cycleTime=0, bulkCurrent=0.0, bulkVoltage=0.0, floatVoltage=0.0,
                 floatTime=0.0, dischargeCurrent=0.0, dischargeVoltage=0.0, cutoffCurrent=0.0,
                 afterChargingRestTime=30.0, afterDischargingRestTime=30.0, startCharging=True, deamonState=True):
        super().__init__()
        self.IPV4 = IPV4
        self.sleepTime = sleepTime
        self.cycleTime = cycleTime
        self.bulkCurrent = bulkCurrent
        self.bulkVoltage = bulkVoltage
        self.absorptionCurrent = self.bulkCurrent * 0.8
        self.absorptionVoltage = self.bulkVoltage
        self.floatCurrent = self.bulkCurrent * 0.01
        self.floatVoltage = floatVoltage
        self.floatTime = floatTime
        self.bulkMode = True
        self.absorptionMode = False
        self.floatingMode = False
        self.chargingMode = False
        self.dischargingMode = False
        self.chargingInitializeMode = False
        self.dischargingInitializeMode = False
        self.dischargeCurrent = dischargeCurrent
        self.dischargeVoltage = dischargeVoltage
        self.cutoffCurrent = cutoffCurrent
        self.afterChargingRestTime = afterChargingRestTime
        self.afterDischargingRestTime = afterDischargingRestTime
        self.startCharging = startCharging
        self.deamonState = deamonState
        self.counter = 0
        self.bulkInfo = 0
        self.absorptionInfo = 0
        self.setDaemon(self.deamonState)
        self._stop_event = threading.Event()

    def __str__(self):
        return f'Cycling Operation, for details print object.__doc__'

    def cyclingFinalize(self):
        logger.debug(f'Cycling is being finalized!')
        cprint.printFeedback(f'Cycling is being finalized!')
        ShutdownOperation(self.IPV4).setShutdownOutput()
        ShutdownOperation(self.IPV4).setShutdownValues()
        ShutdownOperation(self.IPV4).limitShutdownValues()
        time.sleep(1)

    def outputInitialize(self):
        logger.debug(f'Output is being initialized!')
        cprint.printFeedback(f'Output is being initialized!')
        OutputSubsystem(self.IPV4).SetOutput(1)
        OutputSubsystem(self.IPV4).ReadOutputSet()
        time.sleep(1)

    def chargingInitialize(self):
        logger.debug('Charging is being initialized!')
        cprint.printFeedback('Charging is being initialized!')
        SystemSubsystem(self.IPV4).HighlightFrontpanel()
        SystemSubsystem(self.IPV4).SetVoltageLimit(self.bulkVoltage, 'ON')
        SystemSubsystem(self.IPV4).ReadVoltageLimitSet()
        SystemSubsystem(self.IPV4).SetCurrentLimit(self.bulkCurrent + 10, 'ON')
        SystemSubsystem(self.IPV4).ReadCurrentLimitSet()
        SystemSubsystem(self.IPV4).SetPowerLimit(self.bulkVoltage * self.bulkCurrent + 500, 'ON')
        SystemSubsystem(self.IPV4).ReadPowerLimitSet()
        time.sleep(1)

    def chargingFinalize(self):
        logger.debug('Charging is being finalized!')
        cprint.printFeedback('Charging is being finalized!')
        SystemSubsystem(self.IPV4).HighlightFrontpanel()
        ShutdownOperation(self.IPV4).setShutdownOutput()
        ShutdownOperation(self.IPV4).setShutdownValues()

    def bulkStage(self):
        logger.debug('Bulk Stage is Initialized!')
        cprint.printFeedback('Bulk Stage is Initialized!')
        SourceSubsystem(self.IPV4).SetVoltage(self.bulkVoltage)
        SourceSubsystem(self.IPV4).ReadVoltageSet()
        SourceSubsystem(self.IPV4).SetCurrent(self.bulkCurrent)
        SourceSubsystem(self.IPV4).SetPower(self.bulkCurrent * self.bulkVoltage + 50)
        SourceSubsystem(self.IPV4).ReadPowerSet()
        time.sleep(1)

    def absorptionStage(self):
        logger.debug('Absorption Stage is Initialized!')
        cprint.printFeedback('Absorption Stage is Initialized!')
        SourceSubsystem(self.IPV4).SetVoltage(self.absorptionVoltage)
        SourceSubsystem(self.IPV4).ReadVoltageSet()
        SourceSubsystem(self.IPV4).SetCurrent(self.absorptionCurrent)
        SourceSubsystem(self.IPV4).SetPower(self.absorptionVoltage * self.absorptionCurrent + 50)
        SourceSubsystem(self.IPV4).ReadPowerSet()
        time.sleep(1)

    def floatingStage(self):
        logger.debug('Floating Stage is Initialized!')
        cprint.printFeedback('Floating Stage is Initialized!')
        SourceSubsystem(self.IPV4).SetVoltage(self.floatVoltage)
        SourceSubsystem(self.IPV4).ReadVoltageSet()
        SourceSubsystem(self.IPV4).SetCurrent(self.floatCurrent)
        SourceSubsystem(self.IPV4).ReadCurrentSet()
        SourceSubsystem(self.IPV4).SetPower(self.floatCurrent * self.floatVoltage + 50)
        SourceSubsystem(self.IPV4).ReadPowerSet()
        time.sleep(1)

    def checkChargingStage(self):
        if (float(MeasureSubsystem(self.IPV4).MeasureCurrent()) < self.absorptionCurrent) and self.bulkMode:
            self.absorptionStage()
            self.bulkMode = False
            self.absorptionMode = True
        elif (float(MeasureSubsystem(self.IPV4).MeasureCurrent()) < self.floatCurrent) and self.absorptionMode:
            self.floatingStage()
            self.absorptionMode = False
            self.floatingMode = True

        if self.bulkMode:
            logger.debug('Bulk Mode is active!')
            if self.bulkInfo < 1:
                cprint.printFeedback('Bulk Mode is active!')
                self.bulkInfo += 1
        elif self.absorptionMode:
            logger.debug('Absorption Mode is active!')
            if self.absorptionInfo < 1:
                cprint.printFeedback('Absorption Mode is active!')
        elif self.floatingMode:
            logger.debug('Floating mode is active!')
            cprint.printFeedback('Floating mode is active!')
            logger.debug(f'Float time is: {self.floatTime}')
            time.sleep(self.floatTime)
            self.chargingFinalize()
            time.sleep(self.afterChargingRestTime)
            self.bulkMode = True
            self.absorptionMode = False
            self.floatingMode = False
            self.chargingMode = False
            if not self.startCharging:
                self.counter += 1
            self.dischargingInitializeMode = True

    def dischargingInitialize(self):
        logger.debug('Discharging is being initialized!')
        cprint.printFeedback('Discharging is being initialized!')
        SystemSubsystem(self.IPV4).HighlightFrontpanel()
        SystemSubsystem(self.IPV4).SetVoltageLimit(self.dischargeVoltage, 'ON')
        SystemSubsystem(self.IPV4).ReadVoltageLimitSet()
        SystemSubsystem(self.IPV4).SetNegativeCurrentLimit(self.dischargeCurrent - 10, 'ON')
        SystemSubsystem(self.IPV4).ReadNegativeCurrentLimitSet()
        SystemSubsystem(self.IPV4).SetNegativePowerLimit(self.dischargeVoltage * self.dischargeCurrent - 100, 'ON')
        SystemSubsystem(self.IPV4).ReadNegativePowerLimitSet()
        time.sleep(1)

    def dischargingStage(self):
        logger.debug('Discharging stage is started!')
        cprint.printFeedback('Discharging stage is started!')
        SourceSubsystem(self.IPV4).SetVoltage(self.dischargeVoltage)
        SourceSubsystem(self.IPV4).ReadVoltageSet()
        SourceSubsystem(self.IPV4).SetNegativeCurrent(self.dischargeCurrent)
        SourceSubsystem(self.IPV4).ReadNegativeCurrentSet()
        SourceSubsystem(self.IPV4).SetNegativePower(self.dischargeCurrent * self.dischargeVoltage - 50)
        SourceSubsystem(self.IPV4).ReadNegativePowerSet()
        time.sleep(1)

    def dischargingFinalize(self):
        logger.debug('Charging is being finalized!')
        cprint.printFeedback('Charging is being finalized!')
        SystemSubsystem(self.IPV4).HighlightFrontpanel()
        ShutdownOperation(self.IPV4).setShutdownOutput()
        ShutdownOperation(self.IPV4).setShutdownValues()

    def checkDischargingStage(self):
        if float(MeasureSubsystem(self.IPV4).MeasureCurrent()) > self.cutoffCurrent:
            self.dischargingFinalize()
            time.sleep(self.afterDischargingRestTime)
            if self.startCharging:
                self.counter += 1
            self.dischargingMode = False
            self.chargingInitializeMode = True
        else:
            logger.debug('Discharging is still running!')

    def stop(self):
        logger.debug('Cycling thread class stop event has been started!')
        cprint.printFeedback('Cycling thread class stop event has been started!')
        self._stop_event.set()

    def run(self):
        logger.debug('Cycling thread class has been started!')
        if self.startCharging:
            self.chargingInitializeMode = True
            self.dischargingInitializeMode = False
            while not self._stop_event.is_set():
                if self.counter < self.cycleTime:
                    if self.chargingInitializeMode:
                        cprint.printFeedback('Charging mode initialized!')
                        self.chargingInitialize()
                        self.bulkStage()
                        self.outputInitialize()
                        self.chargingInitializeMode = False
                        self.chargingMode = True
                    elif self.chargingMode:
                        cprint.printFeedback('Charging mode is running!')
                        time.sleep(self.sleepTime)
                        self.checkChargingStage()
                    elif self.dischargingInitializeMode:
                        cprint.printFeedback('Discharging mode initialized!')
                        self.dischargingInitialize()
                        self.dischargingStage()
                        self.outputInitialize()
                        self.dischargingInitializeMode = False
                        self.dischargingMode = True
                    elif self.dischargingMode:
                        cprint.printFeedback('Discharging mode is running!')
                        time.sleep(self.sleepTime)
                        self.checkDischargingStage()
                else:
                    self.stop()
        else:
            self.chargingInitializeMode = False
            self.dischargingInitializeMode = True
            while not self._stop_event.is_set():
                if self.counter < self.cycleTime:
                    if self.chargingInitializeMode:
                        cprint.printFeedback('Charging mode initialized!')
                        self.chargingInitialize()
                        self.bulkStage()
                        self.outputInitialize()
                        self.chargingInitializeMode = False
                        self.chargingMode = True
                    elif self.chargingMode:
                        cprint.printFeedback('Charging mode is running!')
                        time.sleep(self.sleepTime)
                        self.checkChargingStage()
                    elif self.dischargingInitializeMode:
                        cprint.printFeedback('Discharging mode is initialized!')
                        self.dischargingInitialize()
                        self.dischargingStage()
                        self.outputInitialize()
                        self.dischargingInitializeMode = False
                        self.dischargingMode = True
                    elif self.dischargingMode:
                        cprint.printFeedback('Discharging mode is running!')
                        time.sleep(self.sleepTime)
                        self.checkDischargingStage()
                else:
                    self.stop()
        self.cyclingFinalize()
        cprint.printFeedback('Cycling thread class has been stopped!')


class TestOperations:
    """
        Charging Functional Operation
        -----------------------------------------------------------------------------------------------------------------
        IPV4: Address of the desired device to start shutdown operation
        -----------------------------------------------------------------------------------------------------------------
        testGeneralInstructions: General Instructions class tester.
        -----------------------------------------------------------------------------------------------------------------
        testSourceSubsystem: Source Subsystem class tester.
        -----------------------------------------------------------------------------------------------------------------
        testMeasureSubsystem: Measure Subsystem class tester.
        -----------------------------------------------------------------------------------------------------------------
        testSystemSubsystem: System Subsystem class tester.
        -----------------------------------------------------------------------------------------------------------------
        testOutputSubsystem: Output Subsystem class tester.
        -----------------------------------------------------------------------------------------------------------------
        testWatchdogOperation: Watchdog Operation class tester.
        -----------------------------------------------------------------------------------------------------------------
        testShutdownOperation: Shutdown Operation class tester.
        -----------------------------------------------------------------------------------------------------------------
        testBasicDataloggerOperation: Basic Datalogger Operation class tester.
        -----------------------------------------------------------------------------------------------------------------
        testAhDataloggerOperation: Ah Datalogger Operation class tester.
        -----------------------------------------------------------------------------------------------------------------
        testWhDataloggerOperation: Wh Datalogger Operation class tester.
        -----------------------------------------------------------------------------------------------------------------
        testChargerOperation: Charging Operation class tester.
        -----------------------------------------------------------------------------------------------------------------
        testDischargerOperation: Discharging Operation class tester.
        -----------------------------------------------------------------------------------------------------------------
        testCyclingOperation: Cycling Operation class tester.
        -----------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, IPV4):
        self.IPV4 = IPV4
        logger.debug("Test operations has been created!")
        self.Delta = SM15K(self.IPV4)

    def __str__(self):
        return f'Testing Operations, for details print object.__doc__'

    def testGeneralInstructions(self):
        logger.debug("General Instructions test runs!")
        logger.debug(self.Delta.__doc__)
        self.Delta.TestGeneralInstructions()
        logger.debug("General Instructions test finished!")

    def testSourceSubsystem(self):
        logger.debug("Source Subsystem test runs!")
        logger.debug(self.Delta.source.__doc__)
        self.Delta.source.TestSourceSubsystem()
        logger.debug("Source Subsystem test finished!")

    def testMeasureSubsystem(self):
        logger.debug("Measurement Subsystem test runs!")
        logger.debug(self.Delta.measure.__doc__)
        self.Delta.measure.TestMeasureSubsystem()
        logger.debug("Measurement Subsystem test finished!")

    def testSystemSubsystem(self):
        logger.debug("System Subsystem test runs!")
        logger.debug(self.Delta.measure.__doc__)
        self.Delta.system.TestSystemSubsystem()
        logger.debug("System Subsystem test finished!")

    def testOutputSubsystem(self):
        logger.debug("Output Subsystem test runs!")
        logger.debug(self.Delta.output.__doc__)
        self.Delta.output.TestOutputSubsystem()
        logger.debug("Output Subsystem test finished!")

    def testWatchdogOperation(self, timer, sleepTime):
        logger.debug("Watchdog operation test runs!")
        Watchdog = WatchdogOperation(self.IPV4, timer, sleepTime)
        Watchdog.start()

    def testShutdownOperation(self):
        logger.debug("Shutdown operation test runs!")
        self.Delta.shutdown.limitShutdownValues()
        self.Delta.shutdown.setShutdownValues()
        self.Delta.shutdown.setShutdownOutput()
        self.Delta.shutdown.removeLimitShutdownValues()

    def testBasicDataloggerOperation(self, loggingTime):
        logger.debug("Basic Datalogger operation test runs!")
        BasicDatalogger = BasicDataloggerOperation(self.IPV4, loggingTime)
        BasicDatalogger.start()

    def testAhDataloggerOperation(self, loggingTime):
        logger.debug("Ah Datalogger operation test runs!")
        AhDatalogger = AhDataloggerOperation(self.IPV4, loggingTime)
        AhDatalogger.start()

    def testWhDataloggerOperation(self, loggingTime):
        logger.debug("Wh Datalogger operation test runs!")
        WhDatalogger = WhDataloggerOperation(self.IPV4, loggingTime)
        WhDatalogger.start()

    def testChargingOperation(self, sleepTime, bulkCurrent, bulkVoltage, floatVoltage):
        logger.debug("Charging operation test runs!")
        Charging = ChargingOperation(self.IPV4, sleepTime, bulkCurrent, bulkVoltage, floatVoltage)
        Charging.start()

    def testDischargingOperation(self, sleepTime, voltageSet, currentSet, cutoffCurrent):
        logger.debug("Discharging operation test runs!")
        Discharging = DischargingOperation(self.IPV4, sleepTime, voltageSet, currentSet, cutoffCurrent)
        Discharging.start()

    def testCyclingOperation(self, sleepTime, cycleTime, bulkCurrent, bulkVoltage, floatVoltage,
                             floatTime, dischargeCurrent, dischargeVoltage, cutoffCurrent,
                             afterChargingRestTime, afterDischargingRestTime, startCharging=True):
        logger.debug("Discharging operation test runs!")
        Cycling = CyclingOperation(self.IPV4, sleepTime, cycleTime, bulkCurrent, bulkVoltage, floatVoltage, floatTime,
                                   dischargeCurrent, dischargeVoltage, cutoffCurrent, afterChargingRestTime,
                                   afterDischargingRestTime, startCharging)
        Cycling.start()


if __name__ == '__main__':
    pass
