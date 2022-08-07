import time
"""
import serial
import spidev
import math
import board
import digitalio
from adafruit_motor import stepper
import Encoder


enc = Encoder.Encoder(17, 27)
coils = (
    digitalio.DigitalInOut(board.D19),  # A1
    digitalio.DigitalInOut(board.D26),  # A2
    digitalio.DigitalInOut(board.D20),  # B1
    digitalio.DigitalInOut(board.D21),  # B2
)

for coil in coils:
    coil.direction = digitalio.Direction.OUTPUT
motor = stepper.StepperMotor(coils[0], coils[1], coils[2], coils[3], microsteps=None)

"""



def Measurement_Antenna(frequency, input_power, sample_size):
    control_degree = 5.5
    frequency=str(frequency)
    if len(frequency) < 10:
        add_zero = 10 - len(frequency)
        zero = ""
        for x in range(add_zero):
            zero = "0" + zero
        frequency = zero + frequency
    p_dbm = []
    voltage_code = attenuator_dac(input_power)
    #stm32_uart(frequency, voltage_code)
    #time.sleep(60)
    angle = 0
    p_dbm.append(cn0150(sample_size=sample_size))
    while angle < 360:
        angle = angle + 1
        motor_rotate(control_degree)
        p_dbm.append(cn0150(sample_size=sample_size))
        control_degree = control_degree + 5.5
    enc.reset()
    return p_dbm


def Calibration_Free_Space(frequency, input_power, sample_size):
    frequency=str(frequency)
    if len(frequency) < 10:
        add_zero = 10 - len(frequency)
        zero = ""
        for x in range(add_zero):
            zero = "0" + zero
        frequency = zero + frequency
    p_dbm_calibration_fs = []
    voltage_code = attenuator_dac(input_power)
    stm32_uart(frequency, voltage_code)
    time.sleep(60)
    p_dbm_calibration_fs.append(cn0150(sample_size=sample_size))
    return p_dbm_calibration_fs


def Calibration_Cable(frequency, input_power, sample_size):
    frequency=str(frequency)
    if len(frequency) < 10:
        add_zero = 10 - len(frequency)
        zero = ""
        for x in range(add_zero):
            zero = "0" + zero
        frequency = zero + frequency
    p_dbm_calibration_cable = []
    voltage_code = attenuator_dac(input_power)
    stm32_uart(frequency, voltage_code)
    time.sleep(60)
    p_dbm_calibration_cable.append(cn0150(sample_size=sample_size))
    return p_dbm_calibration_cable


def stm32_uart(frequency, input_power):
    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1000
    )
    data = str(frequency) + "," + str(input_power)
    ser.write(str(data).encode())


def cn0150(sample_size=100, SLOPE_ADC=-37.494, INTERCEPT=24.662):
    result_list = []
    bus = 0
    device = 0
    spi = spidev.SpiDev()
    spi.open(bus, device)
    spi.max_speed_hz = 500000
    spi.mode = 0
    msg = [0x01]
    for x in range(sample_size):
        time.sleep(0.01)
        spi.writebytes(msg)
        reply = spi.readbytes(2)
        result = reply[0] << 8 | reply[1]
        result_list.append(result)
    CODE_OUT = sum(result_list) / len(result_list)
    PIN = (CODE_OUT / SLOPE_ADC) + INTERCEPT
    return PIN


def cn0150_CODEOUT(sample_size=100):
    result_list = []
    bus = 0
    device = 0
    spi = spidev.SpiDev()
    spi.open(bus, device)
    spi.max_speed_hz = 500000
    spi.mode = 0
    msg = [0x01]
    for x in range(sample_size):
        time.sleep(0.5)
        spi.writebytes(msg)
        reply = spi.readbytes(2)
        result = reply[0] << 8 | reply[1]
        result_list.append(result)
    CODE_OUT = sum(result_list) / len(result_list)
    return CODE_OUT


def calibrate_cn0150(frequency):
    stm32_uart(frequency, attenuator_dac(-10))
    CODE_1 = cn0150_CODEOUT()
    stm32_uart(frequency, attenuator_dac(-50))
    CODE_2 = cn0150_CODEOUT()
    SLOPE_ADC = (CODE_2 - CODE_1) / (-50 - (-10))
    INTERCEPT = -50 - (CODE_2 / SLOPE_ADC)
    return SLOPE_ADC, INTERCEPT


def attenuator_dac(power_dbm, Vref=3.3):
    p_mw = 1 * pow(10, (power_dbm / 10))
    db = 10 * math.log(p_mw)
    SLOPE_DAC = -27.82
    INTERCEPT_DAC = 1.09
    voltage = (db / SLOPE_DAC) + INTERCEPT_DAC
    voltage_code = (voltage * 4096) / Vref
    voltage_code = str(int(voltage_code))
    if len(voltage_code) < 4:
        add_zero = 4 - len(voltage_code)
        zero = ""
        for x in range(add_zero):
            zero = "0" + zero
        voltage_code = zero + voltage_code
    return voltage_code




def motor_rotate(control_degree):
    #encoder_degree = (degree * 2000) / 360
    DELAY = 0.01
    while enc.read() <= control_degree:
        try:
            motor.onestep()
            time.sleep(float(DELAY))
        except KeyboardInterrupt:
            motor.release()
