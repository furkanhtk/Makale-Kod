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
    beamwidth_value = beamwidth_angle1 + (361 - beamwidth_angle2)
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
    bandwidth_6dB_value = (361 - bandwidth_angle1) + bandwidth_angle2
    print("bandwidth_6dB_value {}, bandwidth_power1{}, bandwidth_angle1{}, bandwidth_power2{}, bandwidth_angle2{}".format(bandwidth_6dB_value, bandwidth_power1, bandwidth_angle1, bandwidth_power2, bandwidth_angle2))
    return bandwidth_6dB_value, bandwidth_power1, bandwidth_angle1, bandwidth_power2, bandwidth_angle2

def directivity(beamwidth_angle1, beamwidth_angle2):
    kraus = 32400 / (beamwidth_angle1 * beamwidth_angle2)
    print("Kraus : {}".format(kraus))
    tai_pereira = 72815 / (pow(beamwidth_angle1, 2) * pow(beamwidth_angle2, 2))
    print("tai_pereira : {}".format(tai_pereira))
    return kraus, tai_pereira



engine = create_engine('sqlite:///parameters_database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
parameters_list = models.get_parameters(session)
id_list=[]

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
wavelength = 3*10**8 / 1800000000
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

beamwidth(log_normalize)

# print("Log : {}".format(log_normalize))


beamwidth_value, half_power1, beamwidth_angle1, half_power2, beamwidth_angle2 = beamwidth(log_normalize)
bandwidth_6dB_value, bandwidth_power1, bandwidth_angle1, bandwidth_power2, bandwidth_angle2 = bandwidth_6dB(log_normalize)
kraus, tai_pereira = directivity(beamwidth_value,bandwidth_6dB_value)



aaaa = np.append(beamwidth_angle2,beamwidth_angle1)
theta = np.arange(0, 361, 1)
fig = go.Figure()
fig.add_trace(go.Scatterpolar(
        r = log_normalize,
        theta = theta,
        mode = 'lines',
        name = 'Measurement',

    ))
fig.add_trace(go.Scatterpolar(
        r = log_normalize_upper,
        theta = theta,
        mode = 'lines',
        name = 'Upper Tolerance',

    ))
fig.add_trace(go.Scatterpolar(
        r = log_normalize_lower,
        theta = theta,
        mode = 'lines',
        name = 'Lower Tolerance',

    ))

fig.add_trace(go.Barpolar(
        r = [min_value],
        theta = [0],
        width=[(beamwidth_angle1[0] + (361 - beamwidth_angle2[0]))],
        opacity=0.8,
        name = 'Beamwidth',
    ))


fig.add_trace(go.Barpolar(
        r = [abs(min_value)],
        theta = [0],
        width=[(bandwidth_angle2[0] + (361 - bandwidth_angle1[0]))],
        opacity=0.6,
        name = 'Bandwidth',
    ))




fig.update_layout(
    title = 'Radiation Pattern',
    showlegend = True,
    width=650,
    height=650,
)

fig.show()

# theta = np.arange(0, 361, 1)
# fig = px.line_polar(log_normalize,r=log_normalize, theta=theta, start_angle=0,labels={'log_normalize': "hello"})
# fig.add_scatterpolar(r=log_normalize_upper, theta=theta, name= "Upper")
# fig.add_scatterpolar(r=log_normalize_lower, theta=theta, name="Lower")
#
# fig.add_barpolar(r=np.array([min_value]),width=np.array([360-beamwidth_value]),theta= np.array([0]))
#
#
#
# fig.show()

# print(raw_data)
