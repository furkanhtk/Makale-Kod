from datetime import datetime
from flask import *
import models
from database import Base,Parameters
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import plotly.express as px
import numpy as np
import plotly
import string
import control
import calculation
import plotly.graph_objects as go

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=today)


def Measurement_page():
    engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == "GET":
        return render_template("Measurement.html")
    elif request.form.get('Start') == 'Start':
        form_frequency = request.form["frequency"]
        form_power = request.form["power"]
        form_sample_size = request.form["sample_size"]
        form_g_ref = request.form["g_ref"]
        form_distance = request.form["distance"]
        form_antenna_type = request.form["antenna_type"]
        form_mode = request.form["mode"]
        models.add_parameter(session, form_frequency, form_power,form_sample_size, form_g_ref, form_distance, form_antenna_type,form_mode)
        return redirect(url_for("Process_Measurement_page"))


def Calibration_fs_page():
    engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == "GET":
        return render_template("Calibration_fs.html")
    elif request.form.get('Start') == 'Start':
        form_frequency = request.form["frequency"]
        form_power = request.form["power"]
        form_sample_size = request.form["sample_size"]
        form_g_ref = request.form["g_ref"]
        form_distance = request.form["distance"]
        form_antenna_type = request.form["antenna_type"]
        form_mode = request.form["mode"]
        models.add_parameter(session, form_frequency, form_power,form_sample_size, form_g_ref, form_distance, form_antenna_type,form_mode)
        return redirect(url_for("Process_CalibrationFreeSpace_page"))


def Calibration_cable_page():
    engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == "GET":
        return render_template("Calibration_cable.html")
    elif request.form.get('Start') == 'Start':
        form_frequency = request.form["frequency"]
        form_power = request.form["power"]
        form_sample_size = request.form["sample_size"]
        form_g_ref = request.form["g_ref"]
        form_distance = request.form["distance"]
        form_antenna_type = request.form["antenna_type"]
        form_mode = request.form["mode"]
        models.add_parameter(session, form_frequency, form_power,form_sample_size, form_g_ref, form_distance, form_antenna_type,form_mode)
        return redirect(url_for("Process_CalibrationCable_page"))


def parameters_page():
    engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == "GET":
        parameters_list = models.get_parameters(session)
        return render_template("parameters.html", parameters=parameters_list)
    elif request.form.get('Add') == 'Add':
        form_frequency = request.form["frequency"]
        form_power = request.form["power"]
        form_g_ref = request.form["g_ref"]
        form_distance = request.form["distance"]
        form_antenna_type = request.form["antenna_type"]
        form_sample_size = request.form["sample_size"]
        models.add_parameter(session,form_frequency,form_power,form_sample_size,form_g_ref,form_distance,form_antenna_type)
        return redirect(url_for("parameters_page"))
    elif request.form.get('Delete') == 'Delete':
        form_parameter_ids = request.form.getlist("parameter_ids")
        for form_parameter_id in form_parameter_ids:
            models.delete_parameter(session, form_parameter_id)
        return redirect(url_for("parameters_page"))
    else:
        return redirect(url_for("parameters_page"))


def parameter_page(parameter_id):
    engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    parameters_list = models.get_parameters(session)
    id_list = []
    for parameter in parameters_list:
        id_list.append(parameter.id)
    parameter = models.get_parameter(session, parameter_id)


    parameter_measurement = models.get_parameter(session, id_list[33])

    my_data_numerical = np.genfromtxt('PowerPattern.csv', delimiter=',') #numerical data
    my_data_numerical = my_data_numerical[:,3]
    theta_numerical = np.arange(0, 361, 5) #numerical angle
    if parameter.mode == "Measurement":

        x = parameter.raw_measured_power
        """
        x = x.replace(',,,','/')
        x = x.replace(',','')
        x = x.replace('/',',')
        
        """
        raw_data = np.fromstring(x, dtype=float, sep=',')
        P_max = np.amax(raw_data)


        p_mw = 1 * pow(10, (raw_data / 10))
        p_1db_upper = p_mw * pow(10, (1 / 10))
        p_1db_lower = p_mw * pow(10, (-1 / 10))
        p_mw_numerical = 1 * pow(10, (my_data_numerical / 10))

        max_value_index = np.argmax(p_mw)
        max_value = np.amax(p_mw)
        max_value_numerical = np.amax(p_mw_numerical)

        max_value_index_upper = np.argmax(p_1db_upper)
        max_value_upper = np.amax(p_1db_upper)

        max_value_index_lower = np.argmax(p_1db_lower)
        max_value_lower = np.amax(p_1db_lower)

        normalize = p_mw / max_value
        normalize_upper = p_1db_upper / max_value
        normalize_lower = p_1db_lower / max_value
        normalize_numerical = p_mw_numerical / max_value_numerical

        log_normalize = np.log(normalize)
        log_normalize_upper = np.log(normalize_upper)
        log_normalize_lower = np.log(normalize_lower)

        log_normalize_numerical = np.log(normalize_numerical)

        min_value = np.amin(log_normalize)

        theta = np.arange(0, 361, 1)



        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=log_normalize,
            theta=theta,
            mode='lines',
            name='Measurement',

        ))

        fig.add_trace(go.Scatterpolar(
            r=log_normalize_numerical,
            theta=theta_numerical,
            mode='lines',
            name='Numeric Measurement',

        ))

        fig.add_trace(go.Scatterpolar(
            r=log_normalize_upper,
            theta=theta,
            mode='lines',
            name='Upper Tolerance',

        ))
        fig.add_trace(go.Scatterpolar(
            r=log_normalize_lower,
            theta=theta,
            mode='lines',
            name='Lower Tolerance',

        ))


        fig.add_trace(go.Barpolar(
            r=[min_value],
            theta=[0],
            #width=[(beamwidth_angle1[0] + (361 - beamwidth_angle2[0]))],
            width=[parameter.beamwidth],
            opacity=0.8,
            name='Beamwidth',
            marker_color="lightblue"

        ))

        fig.update_layout(
            title='Radiation Pattern',
            showlegend=True,
            polar=dict(
                radialaxis=dict(range=[-3.5, 0.5], showticklabels=True, ticks='')
            )
            # width=650,
            # height=650,
        )




        print("Here figure!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        fig.write_image("fig1test_makale.svg")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        parameter = models.get_parameter(session, parameter_id)
        if parameter is None:
            abort(404)
        return render_template("parameter.html", parameter=parameter,graphJSON=graphJSON)
    elif parameter.mode == "Calibration Free Space":
        engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        parameter = models.get_parameter(session, parameter_id)
        if parameter is None:
            abort(404)
        return render_template("parameter_calibrate.html", parameter=parameter)
    elif parameter.mode == "Calibration Cable":
        engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        parameter = models.get_parameter(session, parameter_id)
        if parameter is None:
            abort(404)
        return render_template("parameter_calibrate.html", parameter=parameter)

def Process_Measurement_page():
    status = "Measurement started"
    print(status)
    engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    parameters_list = models.get_parameters(session)
    id_list=[]
    for parameter in parameters_list:
        id_list.append(parameter.id)
    parameter=models.get_parameter(session, id_list[-1])
    input_Power=int(parameter.input_Power)
    input_frequency=parse_frequency(parameter.input_Power)
    status = "Parameters received"
    print(status)
    results = control.Measurement_Antenna(input_frequency,input_Power, parameter.sample_size)
    status = "Measurement completed, calculations in progress"
    print(status)
    beamwidth_value, bandwidth_6dB_value, gain, kraus, tai_pereira = calculation.total_calculation(results,input_frequency,input_Power, parameter.g_ref, parameter.distance)
    beamwidth_value = float(beamwidth_value[0])
    bandwidth_6dB_value = float(bandwidth_6dB_value[0])
    kraus = float(kraus[0])
    tai_pereira = float(tai_pereira[0])
    str1 = ""
    for ele in results:
        str1 += str(ele) + ","
    results_str = str1
    models.add_results(session,id_list[-1],results_str,beamwidth_value, bandwidth_6dB_value, gain, tai_pereira, kraus)
    status = "Measurement complete, calculations complete"
    print(status)
    return redirect(url_for("parameters_page"))



def Process_CalibrationCable_page():
    status = "Calibration cable started"
    print(status)
    engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    parameters_list = models.get_parameters(session)
    id_list=[]
    for parameter in parameters_list:
        id_list.append(parameter.id)
    parameter=models.get_parameter(session, id_list[-1])
    input_Power=int(parameter.input_Power)
    input_frequency=parse_frequency(parameter.input_Power)
    status = "Parameters received"
    print(status)
    results = control.Calibration_Cable(input_frequency,input_Power, parameter.sample_size)
    str1 = ""
    for ele in results:
        str1 += str(ele) + ","
    results_str = str1
    models.add_results(session,id_list[-1],results_str,0, 0, 0, 0, 0)
    status = "Calibration completed"
    print(status)
    return redirect(url_for("parameters_page"))


def Process_CalibrationFreeSpace_page():
    status = "Calibration cable started"
    print(status)
    engine = create_engine('sqlite:///parameters_database.db', connect_args={"check_same_thread": False})
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    parameters_list = models.get_parameters(session)
    id_list=[]
    for parameter in parameters_list:
        id_list.append(parameter.id)
    parameter=models.get_parameter(session, id_list[-1])
    input_Power=int(parameter.input_Power)
    input_frequency=parse_frequency(parameter.input_Power)
    status = "Parameters received"
    print(status)
    results = control.Calibration_Free_Space(input_frequency,input_Power, parameter.sample_size)
    str1 = ""
    for ele in results:
        str1 += str(ele) + ","
    results_str = str1
    models.add_results(session,id_list[-1],results_str,0, 0, 0, 0, 0)
    status = "Calibration completed"
    print(status)
    return redirect(url_for("parameters_page"))


def parse_frequency(value):
    value = value.lower()
    if "ghz" in value:
        frequency = (float(value.strip(string.ascii_letters)))
        frequency = int(frequency * (10 ** 9))
    elif "mhz" in value:
        frequency = (float(value.strip(string.ascii_letters)))
        frequency = int(frequency * (10 ** 6))
    else:
        frequency = (int(value.strip(string.ascii_letters)))
    return frequency
