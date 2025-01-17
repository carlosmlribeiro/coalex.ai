import streamlit as st
import asyncio
import time
from ably import AblyRealtime

ABLY_KEY = st.secrets["ABLY_KEY"]

async def main():

    if 'i' not in st.session_state:
        st.session_state['i'] = 0
        i = 0
    else:
        i = st.session_state['i']

    # Connect to Ably with your API key
    ably = AblyRealtime(ABLY_KEY)

    def listener(state_change):
        print(state_change.current)

    ably.connection.on(listener)

    # Create a channel called 'get-started' and register a listener to subscribe to all messages with the name 'first'
    channel = ably.channels.get('get-started')

    if st.button('Publish message'):
        print('Here is message number', i)
        message = 'Here is message number' + str(i)
        await channel.publish('first', message)
        i += 1
        st.session_state['i'] = i
    
    await ably.close()
    print('Closed the connection to Ably.')

asyncio.run(main())