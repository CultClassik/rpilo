import os, subprocess
from subprocess import Popen
from flask import Flask, url_for, request, render_template, json, send_from_directory, jsonify

app = Flask(__name__)

############
# Internal Functions
############
def get_conf(file_name):
    i = "test"
    return "blah"


def check_online(device):
    p1 = Popen(["fping", '-r', '1', '-t', '100', device], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p1.communicate()

    if (str(output).find('alive') != -1):
        return True
    elif (str(output).find('alive') == -1):
        return False


def get_stats():
    import psutil
    stats = {}
    temp = str(os.system("/opt/vc/bin/vcgencmd measure_temp"))
    stats['temp'] = temp.replace("temp=", "")
    stats['cpu'] = str(psutil.cpu_percent())
    stats['mem'] = str(psutil.virtual_memory())

    return stats


def read_conf():
    conf_file = os.path.normpath(os.path.join(os.path.normpath(os.path.dirname(__file__)), 'templates/private/conf', 'private.json'))
    conf_data = json.load(open(conf_file))
    return conf_data


def gpio_read(p):
    gpio_status = False

    try:
        p = int(p)

        import RPi.GPIO as GPIO
        import time, traceback, sys

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(p, GPIO.IN)
        gpio_status = GPIO.input(p)
        GPIO.cleanup()

        del p

    except:
        traceback.print_exc(file=sys.stdout)

    finally:
        return gpio_status


def gpio_ctl(p, t):
    try:
        p = int(p)
        t = int(t)

        import RPi.GPIO as GPIO
        import time, traceback, sys

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, True)
        time.sleep(t)
        GPIO.output(p, False)
        GPIO.cleanup()

        del p, t

    except:
        traceback.print_exc(file=sys.stdout)


############
# MVC Routes
############
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', stats=get_stats())

@app.route('/services', methods=['GET'])
def services():
    conf_file = os.path.normpath(os.path.join(os.path.normpath(os.path.dirname(__file__)), 'templates/private/conf', 'private.json'))
    conf_data = json.load(open(conf_file))
    return render_template('private/services.html', services = conf_data['services'], stats=get_stats())

@app.route('/devices/power/<device>', methods=['GET'])
def power(device):
    t = int(2)
    conf_data = read_conf()
    gpio = conf_data['devices'][device]['gpio-power']
    gpio_ctl(gpio, t)

    # get the power status from the corresponding gpio input pin or refresh page - currently refreshing page from javascript

    del conf_data

    if (request.args.get('json')):
        result = {'gpio': gpio}
        return jsonify(result)
    else:
        return request.referrer

@app.route('/devices/reset/<device>', methods=['GET'])
def reset(device):
    t = int(2)
    conf_data = read_conf()
    gpio = conf_data['devices'][device]['gpio-reset']
    gpio_ctl(gpio, t)

    del conf_data

    if (request.args.get('json')):
        result = {'gpio': gpio}
        return jsonify(result)
    else:
        return request.referrer

@app.route('/devices', methods=['GET'])
def devices():
    conf_data = read_conf()

    # Read device status by pinging it
    for device in conf_data['devices']:
        is_online = check_online(conf_data['devices'][device]['host'])
        conf_data['devices'][device]['pingable'] = is_online

    ### update this once opto couplers are in place to read power LED
    # Read device status by checking gpio input defined for this device
    for device in conf_data['devices']:
        gpio_pin = conf_data['devices'][device]['gpio-status']
        conf_data['devices'][device]['is_online'] = True #gpio_read(gpio_pin)

    return render_template('private/devices.html', devices=conf_data['devices'], stats=get_stats())

@app.route('/test', methods=['GET'])
def test():
    # Since this is using Travis for integration we need to omit Raspberry Pi specific stuff like getting system stats because the build will fail otherwise
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
