################################################################################
# HTTP at Fortebit Cloud IoT
#
# Created at 2019-05-06 08:40:34.990336
#
################################################################################

from fortebit.polaris import polaris
import mcu
import vm
from wireless import gsm
import ssl

sleep(1000)
print("Test Polaris I/O")
polaris.init()

#print("create IO exp...")
#iox = polaris.IO_EXP()


print("MCU UID:", [hex(b) for b in mcu.uid()])
print("VM info:", vm.info())

# let's import the OKDO cloud modules; first the IoT module...
from fortebit.iot import iot
# ...then the http client
from fortebit.iot import http_client

try:
    modem = polaris.GSM()
    
    minfo = gsm.mobile_info()
    print("Modem:", minfo)
    
    device_token = polaris.getAccessToken(minfo[0], mcu.uid())
    print("Access Token:", device_token)
    
    for _ in range(0,5):
        # put your SSID and password here
        try:
            #gsm.attach("wap.vodafone.co.uk","wap","wap")
            gsm.attach("mobile.vodafone.it")
            #gsm.attach("internet.wind")
            #gsm.attach("tre.it")
            break
        except Exception as e:
            print("Retrying...", e)
        try:
            gsm.detach()
            sleep(2000)
        except:
            pass
    else:
        print("oops, can't attach to wifi!")
        raise IOError

    ninfo = gsm.network_info()
    linfo = gsm.link_info()
    print("Attached to network:", ninfo, linfo)

    # retrieve the CA certificate used to sign the howsmyssl.com certificate
    cacert = __lookup(SSL_CACERT_DST_ROOT_CA_X3)

    # create a SSL context to require server certificate verification
    ctx = ssl.create_ssl_context(cacert=cacert, options=ssl.CERT_NONE)#ssl.CERT_REQUIRED | ssl.SERVER_AUTH)
    # NOTE: if the underlying SSL driver does not support certificate validation
    #       uncomment the following line!
    # ctx = None

    print("Connecting to Fortebit IoT Cloud...")

    # let's create a device passing the id, the token and the type of client
    device = iot.Device(device_token,http_client.HttpClient,ctx)

    device.connect()
    print("Device is connected")

    # start the device
    device.run()
    print("Device is up and running")

    x = 0
    while True:
        # sleep as indicated by rate
        polaris.ledRedOn()
        sleep(3000)
        polaris.ledRedOff()
        x = x+1 #random(0,100)
        msg = device.publish_telemetry({"random":x})
        print("Published telemetry",msg)
        # alternatively, you can publish more than one asset state at a time 
        # by providing them as a dictionary to the following function (uncomment to test)
        # msg = device.publish_state({"random":x})
        # print("Published state",msg)
except Exception as e:
    print(e)



