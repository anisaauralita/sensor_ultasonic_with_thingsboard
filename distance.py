# memasukkan modul RPi.GPIO
import RPi.GPIO as GPIO

# memasukkan modul time
import time

# memasukkan modul mqtt
import paho.mqtt.client as mqtt

# memasukkan modul json 
import json

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'TQAt0wiI2sncE4MwwA08'


# mengambil data dan mengunggah interval dalam hitungan detik.
INTERVAL=2

sensor_data = {'dist' : 0}

next_reading = time.time() 

client = mqtt.Client()

# mengatur token akses
client.username_pw_set(ACCESS_TOKEN)

# menghubungkan ke ThingsBoard menggunakan port MQTT default dan interval 60 detik
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()
# mengatur mode pin pada raspberry menjadi BCM
GPIO.setmode(GPIO.BCM)
 
# mengatur posisi pin trigger
GPIO_TRIGGER = 18 #pin 12

# mengatur posisi pin echo
GPIO_ECHO = 24 #pin 18

# menonaktifkan warning
GPIO.setwarnings(False)
 
# mengatur pin trigger sebagai output/pemancar gelombang ultrasonic
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)

# mengatur pin echo sebagai input/penerima gelombang ultrasonic
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
# membuat fungsi untuk mengukur jarak
def distance():
    
    # memberikan sinyal hight pada pin trigger
    GPIO.output(GPIO_TRIGGER, True)
 
    # mematikan(memberikan sinyal LOW)pada pin trigger setelah 0,01 ms
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
     
    # mendefinikan waktu mulai
    StartTime = time.time()
    
    # mendefinisikan waktu berhenti
    StopTime = time.time()
 
    # mencatat waktu mulai pin echo saat belum menerima pantulan gelombang ultrasonic
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # menyimpan waktu sampainya gelombang ultra sonic pada pin echo
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # mendefinisikan waktu perjalanan gelombang us dengan mengurangi waktu sampai dikurangi waktu mulai
    # dan memasukan ke dalam variabel TimeElapsed
    TimeElapsed = StopTime - StartTime
    
    # mengalikan nilai dari variabel TimeElapsed dengan kecepatan sonic (34300 cm/s)
    # dan di bagi 2 karena ada dua kali perjalanan gelombang us serta dimasukan kedalam variabel distance
    distance = (TimeElapsed * 34300) / 2
    
    # mengembalikan nilai dalam variabel distance
    return distance
    
    # menjalankan scrip jika nama filenya mengandung main 
if __name__ == '__main__':
    try:
        while True:
        # menjalankan fungsi distance dan menampung hasilnya kedalam variabel dist dalam bentuk bilangan bulat
            dist = round(distance(), 1)
            
        # menampilkan pesan dan memasukan nilai dalam variabel dist
            print ("Jarak benda adalah = %.1f cm" % dist)
        
        # mengambil data dari variabel dist dan mengkonversi menjadi string untuk digabungkan dengan string " cm"
            sensor_data['dist'] = str(dist)+" cm"

        # Mengirim data jarak ke ThingsBoard
            client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
        
        # menghentikan proses selama 1 detik
            time.sleep(1)
 
        # menghentikan proses pengukuran jika user menggunakan kombinasi  tombol ctrl + C 
    except KeyboardInterrupt:
        
        # menampilkan pesan saat proses berhenti
        print("   Ups, anda telah menghentikan proses")
        GPIO.cleanup()
        
