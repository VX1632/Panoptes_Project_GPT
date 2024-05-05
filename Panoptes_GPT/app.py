# Import necessary modules
import os
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import pandas as pd
import logging
import re
from datetime import datetime

# Setup SQLAlchemy
DATABASE_URL = "mysql+pymysql://teamAdmin:NookBrosGotchu@mysql-db/panoptesdb"
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
Base = declarative_base()

# Define the Event model
class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True)
    subject = Column(String(255), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    all_day_event = Column(Boolean, default=True)
    description = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)

# Create database tables
Base.metadata.create_all(engine)

# Session factory setup
Session = scoped_session(sessionmaker(bind=engine))

# Streamlit UI
st.title('🧬 Panoptes Event Logger 🧬')
prompt = st.text_area("Enter event details here:", height=150)

if st.button('Log Events'):
    session = Session()  # Create a session
    try:
        # Parsing input text to extract event details
        date_pattern = re.compile(r'(\w+[\s\w]*?) (\d{1,2}/\d{1,2}/\d{4})')
        matches = date_pattern.findall(prompt)

        for match in matches:
            event_description, date_str = match
            date = datetime.strptime(date_str, '%m/%d/%Y')
            
            new_event = Event(
                subject=event_description.strip(),
                start_date=date,
                end_date=date,
                description=event_description.strip()
            )
            session.add(new_event)

        session.commit()  # Commit the transaction
        st.success('Events logged successfully!')
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        session.rollback()  # Rollback in case of error
    finally:
        session.close()  # Close the session

# Display existing events
with Session() as session:
    existing_events = pd.read_sql(session.query(Event).statement, session.bind)
    st.write(existing_events)

    # Add button to download CSV
    if st.button('Download CSV'):
        csv = existing_events.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='events.csv',
            mime='text/csv',
        )