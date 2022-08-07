import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()


class Parameters(Base):
    __tablename__ = 'parameters'
    id = Column(Integer, primary_key=True)
    input_frequency = Column(String(), nullable=True)
    input_Power = Column(String(), nullable=True)
    sample_size = Column(Integer, nullable=True)
    date = Column(String(), nullable=True)
    g_ref = Column(Integer, nullable=True)
    distance = Column(Integer, nullable=True)
    raw_measured_power = Column(String(), nullable=True)
    beamwidth = Column(Integer, nullable=True)
    bandwidth = Column(Integer, nullable=True)
    antenna_gain = Column(Integer, nullable=True)
    directivity_tai = Column(Integer, nullable=True)
    directivity_kraus = Column(Integer, nullable=True)
    antenna_type = Column(String(), nullable=True) # dipole, patch
    mode = Column(String(), nullable=True)  #
