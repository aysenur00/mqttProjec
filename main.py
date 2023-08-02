import paho.mqtt.client as mqtt
def on_connect(client, userdata, flags, rc):
    print(f"Connack received with code {rc}")
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

def print_menu():
    print("\nChoose an option")
    for i in options.keys():
        print(i," ", options[i])

def subscribe():
    topic_to_sub = input("Enter the topic to subscribe: ")
    qos_to_sub  = int(input("Enter qos: (default 0)") or "0")
    client.subscribe(f'{topic_to_sub}/#', qos=qos_to_sub)


def publish():
    topic_to_pub = input("Enter the topic to publish: ")
    qos_to_pub = int(input("Enter qos: (default 0)") or "0")
    msg = input("Enter the message: ")
    (rc, mid) = client.publish(f'{topic_to_pub}', str(msg), qos=qos_to_pub)  # rc: return code mid: message id

options = {
    1: "Add subscription",
    2: "Publish",
    3: "Exit"
}

host_name = input("Enter the host name: ") or "broker.mqtt-dashboard.com"
port_number = input("Enter the port number: ") or "1883"

client = mqtt.Client()
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect(host_name, int(port_number))

while True:
    print_menu()
    option = input("Enter the option: ")
    if(option == "1"):
        subscribe()
    elif(option == "2"):
        publish()
        continue
    elif (option == "3"):
        exit()
    else:
        print("Enter a valid option")
        continue

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        continue



