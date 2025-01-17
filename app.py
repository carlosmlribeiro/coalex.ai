import streamlit as st
import asyncio
import time
from ably import AblyRealtime
from streamlit_autorefresh import st_autorefresh
import duckdb
import json

ABLY_KEY = "4AP9lw.EkAf5g:qbXWzWLYR7rxSppJKSxS4AnXlWMW104yVQTkSBv96aw"

async def main():

    # Connect to Ably with your API key
    realtime = AblyRealtime(ABLY_KEY)

    await realtime.connection.once_async('connected')

    # Create a channel called 'get-started' and register a listener to subscribe to all messages with the name 'first'
    channel = realtime.channels.get('[?rewind=20s]doctor-ai')
    
    def listener(message):
        print("converting message")
        data_json = json.loads(message.data.replace("'", '"'))
        insert_st = f"INSERT OR IGNORE INTO doctor_ai VALUES ('{message.id}', '{data_json['args']['query']}', FALSE)"
        print(insert_st)
        db.sql(insert_st)
        #db.sql("INSERT OR IGNORE INTO doctor_ai VALUES ('123', 'message data', FALSE)")
        #st.write('Message received: ' + message.data)

    await channel.subscribe('tool-call', listener)

    st.dataframe(db.sql("SELECT * from doctor_ai").df())

    await realtime.close()

st_autorefresh(interval=15000, key="auto_refresh")

if 'db' not in st.session_state:
    db = duckdb.connect()
    st.session_state.db = db
else:
    db = st.session_state.db

db.sql("CREATE TABLE IF NOT EXISTS doctor_ai (id VARCHAR PRIMARY KEY, message VARCHAR, handled BOOLEAN DEFAULT FALSE)")

asyncio.run(main())

