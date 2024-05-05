import os
import sys
import streamlit as st
from langchain_openai.llms.base import OpenAI
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import pandas as pd
import logging

# Logging configuration
logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s, %(name)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
)

# Set up environment variable for API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY is not set. Please set it in your environment variables.")
    raise ValueError("OPENAI_API_KEY is not set. Please set it in your environment variables.")
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.9)

# SQLAlchemy setup for MySQL
DATABASE_URL = "mysql+pymysql://teamAdmin:NookBrosGotchu@mysql-db/panoptesdb"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# Define models
class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True)
    event_name = Column(String(255), nullable=False)  # String type defaults to VARCHAR
    description = Column(String(255), nullable=True)  # Specify a length such as 255


class Location(Base):
    __tablename__ = 'locations'
    location_id = Column(Integer, primary_key=True)
    city = Column(String(100), nullable=False)   # Ensure a length is specified
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=False)

Base.metadata.create_all(engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Streamlit UI
st.title('🧬 Panoptes 🧬')
prompt = st.text_input("Submit Prompt Here!")

if st.button('Generate'):
    response = llm.generate(prompts=[prompt])
    full_text = " ".join([gen.text for gen in response.generations[0]])
    st.write(full_text)
    logging.debug(f"Generated response: {full_text}")

    session = Session()
    # Here, you would parse the `full_text` to extract data and add it to your database
    # Example:
    new_event = Event(event_name="Sample Event", description="Sample description")
    session.add(new_event)
    session.commit()

    Session.remove()
    st.success('Data processed and saved to database successfully!')
