from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Parameters, Base
import datetime
import models
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import math

import plotly




def listToString(results):
    str1 = ""
    for ele in results:
        str1 += str(ele)+","
    return str1


def get_parameters(session):
    parameters_list = session.query(Parameters).all()
    return parameters_list



def add_parameter(session, freq, pwr,sample_size,g_ref,distance,antenna_type,mode):
    parameter_to_add = Parameters(input_frequency=freq, input_Power=pwr, sample_size=sample_size, date=datetime.datetime.now().strftime("%Y-%m-%d-%X"), g_ref=g_ref, distance=distance, antenna_type=antenna_type,mode=mode)
    session.add(parameter_to_add)
    session.commit()
    # session.query(Parameters).first()

def add_results(session,id_number,raw_measured_power,beamwidth,bandwidth,antenna_gain,directivity_tai,directivity_kraus):
    edited_parameter = session.query(Parameters).filter_by(id=id_number).one()
    edited_parameter.raw_measured_power = listToString(raw_measured_power)
    edited_parameter.beamwidth=beamwidth
    edited_parameter.bandwidth=bandwidth
    edited_parameter.antenna_gain=antenna_gain
    edited_parameter.directivity_tai=directivity_tai
    edited_parameter.directivity_kraus=directivity_kraus
    session.add(edited_parameter)
    session.commit()


def update_parameter(session, id_number, freq, pwr):
    edited_parameter = session.query(Parameters).filter_by(id=id_number).one()
    edited_parameter.input_frequency = freq
    edited_parameter.input_Power = pwr
    session.add(edited_parameter)
    session.commit()

def delete_parameter(session, parameter_id):
    parameter_to_delete = session.query(Parameters).filter_by(id=parameter_id).one()
    session.delete(parameter_to_delete)
    session.commit()


def get_parameter(session, parameter_id):
    parameter_ = session.query(Parameters).filter_by(id=parameter_id).one()
    return parameter_


def update_date(session, id_number, date):
    edited_parameter = session.query(Parameters).filter_by(id=id_number).one()
    edited_parameter.date = date
    session.add(edited_parameter)
    session.commit()





def find_nearest(array, value):
    # print("array: {}".format(array))

    idx = (np.abs(array + value))
    idx2 = np.sort(idx)
    # print(["{:0.3f}".format(x) for x in array])
    # print(["-{:0.3f}".format(x) for x in idx])
    # print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    # print(["{:0.3f}".format(x) for x in idx2])
    # print("idx : {} idx2:{} ".format(idx,idx2))
    x1 = np.where(idx == idx2[0])
    x2 = np.where(idx == idx2[5])
    # print("idx : {} idx2: {}".format(array[x1],array[x2]))
    # print("idx : {} idx2: {}".format(x1, x2))
    return array[x1], x1, array[x2], x2


def beamwidth(data):
    maximum_db = np.amax(data)
    # print("data: {}".format(data))
    x = np.linspace(0, 361, 361)
    xvals = np.linspace(0, 361, 1000)
    yinterp = np.interp(xvals, x, data)
    half_power1, halfpower_ind1, half_power2, halfpower_ind2 = find_nearest(yinterp, 0.5)
    beamwidth_angle1 = xvals[halfpower_ind1]
    beamwidth_angle2 = xvals[halfpower_ind2]
    if beamwidth_angle1 > beamwidth_angle2:
        beamwidth_value = 361 - beamwidth_angle1 + beamwidth_angle2
    else:
        beamwidth_value = 361 - beamwidth_angle2 + beamwidth_angle1
    print("beamwidth_value :{}, half_power1:{}, beamwidth_angle1: {}, half_power2: {}, beamwidth_angle2:{}".format(beamwidth_value, half_power1, beamwidth_angle1, half_power2, beamwidth_angle2))
    return beamwidth_value, half_power1, beamwidth_angle1, half_power2, beamwidth_angle2


def bandwidth_6dB(data):
    maximum_db = np.amax(data)
    x = np.linspace(0, 361, 361)
    xvals = np.linspace(0, 361, 1000)
    yinterp = np.interp(xvals, x, data)
    bandwidth_power1, bandwidth_ind1, bandwidth_power2, bandwidth_ind2 = find_nearest(yinterp, 0.75)

    bandwidth_angle1 = xvals[bandwidth_ind1]
    bandwidth_angle2 = xvals[bandwidth_ind2]
    if bandwidth_angle1 > bandwidth_angle2:
        bandwidth_6dB_value = 361 - bandwidth_angle1 + bandwidth_angle2
    else:
        bandwidth_6dB_value = 361 - bandwidth_angle2 + bandwidth_angle1
    print("bandwidth_6dB_value {}, bandwidth_power1{}, bandwidth_angle1{}, bandwidth_power2{}, bandwidth_angle2{}".format(bandwidth_6dB_value, bandwidth_power1, bandwidth_angle1, bandwidth_power2, bandwidth_angle2))
    return bandwidth_6dB_value, bandwidth_power1, bandwidth_angle1, bandwidth_power2, bandwidth_angle2

def directivity(beamwidth_angle1, beamwidth_angle2):
    kraus = 32400 / (beamwidth_angle1 * beamwidth_angle2)
    print("Kraus : {}".format(kraus))
    tai_pereira = 72815 / (pow(beamwidth_angle1, 2) * pow(beamwidth_angle2, 2))
    print("tai_pereira : {}".format(tai_pereira))
    return kraus, tai_pereira










if __name__ == "__main__":
    engine = create_engine('sqlite:///parameters_database.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    parameters_list = models.get_parameters(session)
    id_list = []

    for parameter in parameters_list:
        id_list.append(parameter.id)

    parameter_measurement = models.get_parameter(session, id_list[33])
    parameter_input_power = models.get_parameter(session, id_list[31])

    x = parameter_measurement.raw_measured_power
    x = x.replace(',,,', '/')
    x = x.replace(',', '')
    x = x.replace('/', ',')
    # print("P:{}".format(x))

    y = parameter_input_power.raw_measured_power
    y = y.replace(',,,', '')
    y = y.replace(',', '')
    # print("Input Power:{}".format(y))

    raw_data = np.fromstring(x, dtype=float, sep=',')

    P_max = np.amax(raw_data)

    p_mw = 1 * pow(10, (raw_data / 10))
    p_mw_input = 1 * pow(10, (float(y) / 10))
    p_1db_upper = p_mw * pow(10, (1 / 10))
    p_1db_lower = p_mw * pow(10, (-1 / 10))

    # Pr = np.sum(p_mw)
    print("P_max: {}".format(P_max))
    Pr = np.amax(p_mw)
    print("Pr: {}".format(Pr))
    wavelength = 3 * 10 ** 8 / 1800000000
    print(wavelength)
    distance = 0.93
    gain = math.sqrt((Pr * pow(4 * np.pi * distance, 2)) / (p_mw_input * pow(wavelength, 2)))

    print("Gain : {} ".format(gain))

    max_value_index = np.argmax(p_mw)
    max_value = np.amax(p_mw)

    max_value_index_upper = np.argmax(p_1db_upper)
    max_value_upper = np.amax(p_1db_upper)

    max_value_index_lower = np.argmax(p_1db_lower)
    max_value_lower = np.amax(p_1db_lower)

    normalize = p_mw / max_value
    normalize_upper = p_1db_upper / max_value
    normalize_lower = p_1db_lower / max_value

    log_normalize = np.log(normalize)
    log_normalize_upper = np.log(normalize_upper)
    log_normalize_lower = np.log(normalize_lower)

    min_value = np.amin(log_normalize)

    # find_nearest(log_normalize, 0.5)

    beamwidth_value, half_power1, beamwidth_angle1, half_power2, beamwidth_angle2 = beamwidth(log_normalize)
    bandwidth_6dB_value, bandwidth_power1, bandwidth_angle1, bandwidth_power2, bandwidth_angle2 = bandwidth_6dB(log_normalize)
    kraus, tai_pereira = directivity(beamwidth_value, bandwidth_6dB_value)

    #parameter_measurement = models.get_parameter(session, id_list[33])
    #add_parameter(session,"1.8 GHz",-6,128,2,93,"Patch_A_ Pin= -6.29db Gref =2.2","Measurement")
    parameters_list2 = models.get_parameters(session)
    id_list2 = []
    #for parameter2 in parameters_list2:
        #id_list2.append(parameter2.id)

    #d = datetime.datetime(2021,9,10,hour=12, minute=10, second=31)
    #update_date(session,id_list2[-1],d.strftime("%Y-%m-%d-%X"))
    #add_results(session,id_list2[-1],raw_data,beamwidth_value[0],bandwidth_6dB_value[0],gain,tai_pereira[0],kraus[0])
    parameters_list3 = get_parameters(session)
    parameter3 = parameters_list3[-1]
    print("-------------")
    #print("id:{} F:{} P:{} D:{} mode : {} ".format(parameter3.id, parameter3.input_frequency, parameter3.input_Power, parameter3.date, parameter3.mode))
    print("Raw {} ".format(raw_data))


    print("min value {}".format(raw_data.min()))
    print("max value {}".format(raw_data.max()))

    #print("beamwidth:{} bandwidth:{} antenna_gain:{} directivity_tai:{} directivity_kraus : {} ".format(parameter3.beamwidth, parameter3.bandwidth, parameter3.antenna_gain, parameter3.directivity_tai, parameter3.directivity_kraus))
    #print("raw_measured_powersample_size:{} g_ref:{} distance:{} antenna_type : {} ".format(parameter3.sample_size, parameter3.g_ref, parameter3.distance, parameter3.antenna_type))

    """
    for parameter3 in parameters_list3:
        print("id:{} F:{} P:{} D:{} mode : {} ".format(parameter3.id, parameter3.input_frequency, parameter3.input_Power, parameter3.date,parameter3.mode))
    """