import os
from mqtt_ex import mqtt_main
from predict_ex import pre_main

def main() :
    if os.fork() == 0 :
        mqtt_main()
    
    if os.fork() == 0 :
        pre_main()


main()