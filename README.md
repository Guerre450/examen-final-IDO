# Start the program
python3 app.py

# Close the program
ctrl-c
wait for "program end" message
ctr-c again to end flask




# Behaviors

# sending data events
sends data every 30 seconds
sends data when button is pressed quickly

# close / open data sends
press button for 2-3 seconds to close/open data sending
send http post request to close/open data sending

# leds:

red led opens when pi's temperature is max on the network
blue led opens when pi's humidity is max on the network
white led opens when data sending is opened.

# Odd behaviors:

sensor might print alot of timeout, this is normal.



