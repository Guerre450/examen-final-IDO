from flask import Flask, request, jsonify                                                         
import threading
import paho.mqtt.client as pmc
import paho.mqtt.subscribe as subscribe
import time
from countdown import Timer 
from button import Button
from sensor import TempSensor
import pigpio


isRunning = True


HOTE = "rapper"
BROKER = "mqttbroker.lan"
PORT = 1883
TOPIC_SEND_T = "final/%s/T" % HOTE
TOPIC_SEND_H = "final/%s/H" % HOTE
TOPIC_RECEIVE_T = "final/+/T"
TOPIC_HUMIDITY_RECEIVE_H = "final/+/H"
etat = True #can send or not data
mqtt_temparatures = {} #collected temperatures
mqtt_humidities = {}  #collected humidites
last_t_max_topic = "" #latest collected max temp topic
last_h_max_topic = "" # latest collected max humidity topic
# ----------------mqtt callbacks -----------------
def connexion(client, userdata, flags, code, properties):
    print(client)
    if code == 0:
        print("Connecté")
    else:
        print("Erreur code %d\n", code)

def reception_msg(cl,userdata,msg):
    global last_h_max_topic, last_t_max_topic
    message_content = msg.payload.decode()
    print("Recu", message_content, "de", msg.topic)
    if message_content.isnumeric():
        if msg.topic[-1] == "T":
            mqtt_temparatures[msg.topic] = message_content
            print(mqtt_temparatures)
            last_t_max_topic = temparature_max_topic()  
        if msg.topic[-1] == "H":
            mqtt_humidities[msg.topic] = message_content
            print(mqtt_humidities)
            last_h_max_topic = humidity_max_topic()


def send_sensor_data():
    global client
    global temp_sensor
    global etat
    if etat:
        last_result = temp_sensor.result
        client.publish(TOPIC_SEND_T,last_result["temp_c"])
        client.publish(TOPIC_SEND_H,last_result["humidity"])
    else:
        print("Cannot send data, state is close!")

#------------max functions ------------------
def temparature_max_topic() -> str:
    maxtopic = None
    for i in mqtt_temparatures:
        try:
            if not maxtopic or int(mqtt_temparatures[i]) > int(mqtt_temparatures[maxtopic]):
                maxtopic = i
        except Exception:
            pass
    return maxtopic
def humidity_max_topic() -> str:
    maxtopic = None
    for i in mqtt_humidities:
        try:
            if not maxtopic or int(mqtt_humidities[i]) > int(mqtt_humidities[maxtopic]):
                maxtopic = i
        except Exception:
            pass
    return maxtopic







#------------ flask configuration ----------------------
# starting source :https://stackoverflow.com/questions/31264826/start-a-flask-application-in-separate-thread

host_name = "0.0.0.0"
port = 23336
app = Flask(__name__)

#--------- flask routes ------------------------
# test : curl -X POST http://<domain>:23336/etat -H "Content-type:application/json" -d "{\"etat\":\"1\"}"
@app.route("/etat", methods=["POST"])
def return_etat():
    data : dict = request.get_json()
    if "etat" in data:
        global etat
        etat = True if "1" in data["etat"] else False
        print(etat)
    return data
#curl -X GET http://<domain>:23336/donnees -H "Content-type:application/json"
@app.route("/donnees", methods=["GET"])
def donnees():
    if mqtt_humidities.get(TOPIC_SEND_H,"unknown") != "unknown" and mqtt_temparatures.get(TOPIC_SEND_T,"unknown") != "unknown":
        return_dict = {"H" : mqtt_humidities[TOPIC_SEND_H],
        "T" : mqtt_temparatures[TOPIC_SEND_T]}
        return return_dict


    response = {"message" : "data unknown"}
    return response

# -------------pins functions -------------------
def activate_pins(list_of_pins : list):
    global pi
    for i in list_of_pins:
        pi.set_mode(i, pigpio.OUTPUT)

def deactivate_pins(list_of_pins : list):
    global pi
    for i in list_of_pins:
        pi.write(i,0)


if __name__ == "__main__":
    # Objects
    pi = pigpio.pi()
    button = Button(26,pi=pi)
    #threads objects
    temp_sensor = TempSensor()
    timer = Timer()
    # leds 
    temp_max_pin = 6
    humidity_max_pin = 13
    activation_state_pin = 19
    all_pins = [temp_max_pin,humidity_max_pin,activation_state_pin]
    activate_pins(all_pins)
    #flask
    flask_thread = threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=True, use_reloader=False))
    flask_thread.start()
    
    # mqtt
    #source : https://pypi.org/project/paho-mqtt/#callbacks
    client = pmc.Client(pmc.CallbackAPIVersion.VERSION2)
    client.on_connect = connexion
    client.connect(BROKER,PORT)
    client.on_message = reception_msg
    client.subscribe(TOPIC_RECEIVE_T)
    client.subscribe(TOPIC_HUMIDITY_RECEIVE_H)
    #

    #starting all custom threads
    threads = [timer, temp_sensor]
    for i in threads: #starts the threads
        i.start()
    print("threads started")
    
    
    client.loop_start()
    try :
        while isRunning and flask_thread.is_alive():
            #reseting timer
            if timer.get_state() == "timeout":
                send_sensor_data()
                timer.update_time()
            #button logic
            button_result = button.isReleased()
            if button_result != -1.0:
                if button_result < 2.0:
                    send_sensor_data()
                elif button_result >= 2.0:
                    etat = not etat
                    print("closed data" if etat == False else "opened data")
            button.detectPress()
            # led logic
            pi.write(activation_state_pin, int(etat))
            pi.write(temp_max_pin, int(last_t_max_topic == TOPIC_SEND_T))
            pi.write(humidity_max_pin, int(last_h_max_topic == TOPIC_SEND_H))

    except KeyboardInterrupt:
        #close program ctrl-c
        pass
    #stopping all threads, pins and ects
    deactivate_pins(all_pins)
    client.loop_stop()
    threads_amount = len(threads)
    all_threads_ended_number = threading.active_count() - threads_amount
    for i in threads:
        i.kill = True
    while threading.active_count() > all_threads_ended_number:
        print("waiting for {0} threads".format(str(threading.active_count() - all_threads_ended_number)))
        time.sleep(1)
    print("Program end")
 
 

