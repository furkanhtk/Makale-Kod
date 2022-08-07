from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Parameters, Base
import datetime


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


