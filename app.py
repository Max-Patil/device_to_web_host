import os
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import serial
import serial.tools.list_ports
from sensor_comm_v3 import SensorComm

app = Flask(__name__)
CORS(app)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Brightness, Contrast, Digital Zoom, AGC, and NUC Control</title>
    <style>
        /* Your CSS styles here */
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            max-width: 800px;
        }
        td {
            padding: 10px;
            border: 1px solid #ccc;
        }
        label, input, button, select {
            margin: 5px;
        }
        textarea {
            width: 100%;
            height: 150px;
            margin-top: 10px;
        }
        .control {
            display: flex;
            align-items: center;
            border: 1px solid #ccc;
            border-radius: 4px;
            overflow: hidden;
        }
        .control input, .control select {
            border: none;
            text-align: center;
            width: 120px;
            margin: 0;
            padding: 5px;
        }
        .control-buttons {
            display: flex;
            flex-direction: column;
        }
        .control-buttons button {
            background: none;
            border: none;
            font-size: 16px;
            cursor: pointer;
            padding: 2px 5px;
            margin: 0;
        }
        .control {
            display: flex;
            align-items: center;
        }
        .control-buttons {
         margin-left: 10px;
        }
        .row {
         margin-top: 10px;
        }
        .direction-btn {
        margin: 5px;
        }
        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }
    </style>
</head>
<body>
    <table>
        <tr>
            <td>
                <label for="com-port">COM Port:</label>
                <input type="text" id="com-port" value="COM3">
            </td>
            <td>
                <button id="get-all-defaults-button">Get All Defaults</button>
                <button type="button" id="load-factory-btn">Load Factory</button>
            </td>
        </tr>
        <tr>
            <td colspan="2">
                <label for="baud-rate">Baud Rate:</label>
                <input type="text" id="baud-rate" value="115200"> <br>
                <input type="text" id="fw-version-input" placeholder="FW Version" readonly>
            </td>
        </tr>
        <tr>
            <td>
                <label for="brightness-input">Brightness</label>
                <div class="control">
                    <input type="number" id="brightness-input" min="0" max="255" value="0">
                    <div class="control-buttons">
                        <button onclick="changeBrightness(1)">+</button>
                        <button onclick="changeBrightness(-1)">-</button>
                    </div>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <label for="contrast-input">Contrast</label>
                <div class="control">
                    <input type="number" id="contrast-input" min="0" max="255" value="0">
                    <div class="control-buttons">
                        <button onclick="changeContrast(1)">+</button>
                        <button onclick="changeContrast(-1)">-</button>
                    </div>
                </div>
            </td>
        </tr>
        <tr>
            <td colspan="2">
                <label for="dzoom-input">Digital Zoom</label>
                <div class="control">
                    <select id="dzoom-input">
                        <option value="0">1x</option>
                        <option value="1">2x</option>
                        <option value="2">4x</option>
                    </select>
                    <div class="control-buttons">
                        <button onclick="changeDZoom(1)">+</button>
                        <button onclick="changeDZoom(-1)">-</button>
                    </div>
                </div>
            </td>
        </tr>
        <tr>
            <td colspan="2">
                <label for="polarity-input">Polarity</label>
                <div class="control">
                    <select id="polarity-input">
                        <option value="0">White Hot</option>
                        <option value="1">Black Hot</option>
                        <option value="2">Thermal Dart</option>
                    </select>
                    <div class="control-buttons">
                        <button onclick="changePolarity(1)">+</button>
                        <button onclick="changePolarity(-1)">-</button>
                    </div>
                </div>
            </td>
        </tr>
        <tr>
            <td colspan="2">
                <label for="agc-input">AGC Mode</label>
                <div class="control">
                    <select id="agc-input">
                        <option value="0">AGC 0</option>
                        <option value="1">AGC 1</option>
                        <option value="2">AGC 2</option>
                    </select>
                    <div class="control-buttons">
                        <button onclick="changeAgc(1)">+</button>
                        <button onclick="changeAgc(-1)">-</button>
                    </div>
                </div>
            </td>
        </tr>
        <tr>
            <td colspan="2">
                <label for="nuc-input">NUC Mode</label>
                <div class="control">
                    <select id="nuc-input">
                        <option value="0">Shutterless</option>
                        <option value="1">Shuttered</option>
                        <option value="2">SemiNUC</option>
                    </select>
                    <div class="control-buttons">
                        <button onclick="changeNuc(1)">+</button>
                        <button onclick="changeNuc(-1)">-</button>
                    </div>
                </div>
            </td>
        </tr>
        <tr>
            <td colspan="2">
                <label for="reticle-input">Reticle</label>
                <div class="control">
                    <select id="reticle-input">
                        <option value="0">Reticle 0</option>
                        <option value="1">Reticle 1</option>
                        <option value="2">Reticle 2</option>
                        <option value="3">Reticle 3</option>
                        <option value="4">Reticle 4</option>
                        <option value="5">Reticle 5</option>
                        <option value="6">Reticle 6</option>
                    </select>
                    <div class="control-buttons">
                        <button onclick="changeReticle(1)">+</button>
                        <button onclick="changeReticle(-1)">-</button>
                    </div>
                </div>
                <label for="reticle-colour-input">Reticle_Colour</label>
                <div class="control">
                    <div class="control">
                        <select id="reticle-colour-input">
                            <option value="0">White</option>
                            <option value="1">Black</option>
                            <option value="2">Gray1</option>
                            <option value="3">Gray2</option>
                            <option value="4">Gray3</option>
                            <option value="5">auto</option>
                        </select>
                        <div class="control-buttons">
                            <button onclick="changeReticle_Colour(1)">+</button>
                            <button onclick="changeReticle_Colour(-1)">-</button>
                        </div>
                    </div>
                </div>
            </td>
        </tr>
       <tr>
        <td colspan="2">
            <label for="details-textarea">Operation Details:</label>
            <textarea id="details-textarea" readonly aria-describedby="textarea-description"></textarea>
            <p id="textarea-description" class="sr-only">This textarea displays the results and responses of the operations performed.</p>
        </td>
    </tr>
</table>
 <script>
        let connectedComPort = null;

        async function fetchComPorts() {
            try {
                const response = await fetch('/get_com_ports');
                const result = await response.json();

                if (result.status === "success") {
                    console.log("Available COM ports:", result.com_ports);
                    const comPortInput = document.getElementById('com-port');
                    connectedComPort = await findConnectedComPort(result.com_ports);
                    comPortInput.value = connectedComPort ? connectedComPort : 'No connected COM port found';
                    console.log("Connected COM port:", connectedComPort);
                } else {
                    throw new Error(result.message || 'Unknown error occurred');
                }
            } catch (error) {
                console.error('Error fetching COM ports:', error);
                alert('Error fetching COM ports: ' + error.message);
            }
        }

        async function findConnectedComPort(availablePorts) {
            console.log("Checking for a single connected COM port");
            if (!Array.isArray(availablePorts) || availablePorts.length === 0) {
                console.warn("No available ports to check");
                return null;
            }
            for (const port of availablePorts) {
                console.log(`Checking port: ${port}`);
                const isConnected = await checkPortConnection(port);
                if (isConnected) {
                    console.log(`${port} is connected and communicating with the device`);
                    return port;
                }
            }
            console.log("No connected COM port found among available ports");
            return null;
        }

        function checkPortConnection(port) {
            return new Promise((resolve) => {
                setTimeout(() => {
                    const isConnected = port === "COM7";  // Replace this with the correct logic to check connection
                    console.log(`Port ${port} connection check result: ${isConnected}`);
                    resolve(isConnected);
                }, 100);
            });
        }

        function updateComPortInput() {
            const comPortInput = document.getElementById('com-port');
            if (!comPortInput) {
                console.error("COM port input element not found");
                return;
            }
            comPortInput.value = connectedComPort ? connectedComPort : 'No connected COM port found';
            console.log("Updated COM port input value:", comPortInput.value);
        }

        function autoDetectComPort() {
            console.log("Auto-detect button clicked");
            fetchComPorts().then(() => {
                updateComPortInput();
            }).catch(error => {
                console.error("Error in auto-detect process:", error);
            });
        }

        // Functions to handle brightness, contrast, DZoom, etc.
        function changeBrightness(delta) {
            changeValue('brightness-input', delta, 0, 255);
        }

        function changeContrast(delta) {
            changeValue('contrast-input', delta, 0, 255);
        }

        function changeDZoom(delta) {
            const dzoomInput = document.getElementById('dzoom-input');
            const currentIndex = dzoomInput.selectedIndex;
            const newIndex = Math.max(0, Math.min(2, currentIndex + delta));
            dzoomInput.selectedIndex = newIndex;
            setDZoom(newIndex);
        }

        function changePolarity(delta) {
            const polarityInput = document.getElementById('polarity-input');
            const currentIndex = polarityInput.selectedIndex;
            const newIndex = Math.max(0, Math.min(2, currentIndex + delta));
            polarityInput.selectedIndex = newIndex;
            setPolarity(newIndex);
        }

        function changeValue(inputId, delta, min, max) {
            let input = document.getElementById(inputId);
            let currentValue = parseInt(input.value);
            let newValue = Math.max(min, Math.min(max, currentValue + delta));
            input.value = newValue;

            if (inputId === 'brightness-input') {
                setBrightness(newValue);
            } else if (inputId === 'contrast-input') {
                setContrast(newValue);
            }
        }

        // API calls for brightness, contrast, etc.
        async function setParameter(paramName, value) {
            const comPort = document.getElementById('com-port').value;
            const baudRate = document.getElementById('baud-rate').value;

            try {
                const response = await fetch(`/set_${paramName}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        [paramName]: value,
                        com_port: comPort,
                        baud_rate: baudRate
                    })
                });

                const result = await response.json();

                if (result.status === 'success') {
                    logResult(result, paramName);
                } else {
                    throw new Error(result.message);
                }
            } catch (error) {
                console.error(`Error setting ${paramName}:`, error);
                logError(`Error setting ${paramName}`, error.message);
            }
        }

        function logResult(result, paramName) {
            document.getElementById('details-textarea').value += `\nStatus: ${result.status}`;
            document.getElementById('details-textarea').value += `\nValue: ${result.value}`;
            document.getElementById('details-textarea').value += `\nCommand: ${result.command_sent}`;
            document.getElementById('details-textarea').value += `\nResponse: ${result.command_response}`;
        }

        function logError(label, message) {
            document.getElementById('details-textarea').value += `\n${label}: ${message}\n`;
        }

        // Add these functions to handle setting parameters
        async function setBrightness(value) {
            await setParameter('brightness', value);
        }

        async function setContrast(value) {
            await setParameter('contrast', value);
        }

async function setDZoom(value) {
            await setParameter('dzoom', value);
        }

        async function setPolarity(value) {
            await setParameter('polarity', value);
        }

        async function setAgc(value) {
            await setParameter('agc', value);
        }

        async function setNuc(value) {
            await setParameter('nuc', value);
        }

        async function setReticle(value) {
            await setParameter('reticle', value);
        }

        async function setReticleColour(value) {
            await setParameter('reticle_colour', value);
        }

        document.addEventListener('DOMContentLoaded', () => {
            const autoDetectButton = document.getElementById('auto-detect-button');
            if (autoDetectButton) {
                autoDetectButton.addEventListener('click', autoDetectComPort);
            }

            fetchComPorts().catch(error => {
                console.error("Error in initial COM port check:", error);
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_com_ports', methods=['GET'])
def get_com_ports():
    try:
        ports = serial.tools.list_ports.comports()
        com_ports = [port.device for port in ports]
        return jsonify({"status": "success", "com_ports": com_ports}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def handle_serial_communication(com_port, baud_rate, address, value=None):
    try:
        ser = serial.Serial(com_port, baud_rate, timeout=5)
        cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
        
        if value is not None:
            command_sent = [0xe0, 0x0, 0x1, 0x3e, 0xff, 0x3, 0x52, 0x50, address, int(value), 0xff, 0xfe]
            cmd_gen.fpga_write(address, int(value))
            response = cmd_gen.fpga_read(address)
        else:
            command_sent = [0xe0, 0x0, 0x1, 0x3e, 0xff, 0x3, 0x52, 0x50, address]
            response = cmd_gen.fpga_read(address)
        
        ser.close()
        
        return format_response(response, command_sent)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def format_response(response, command_sent):
    response_list = [
        response['header'], response['packet_sequence'] >> 8, response['packet_sequence'] & 0xFF,
        response['device_id'], response['device_number'], response['length'],
        response['cmd_type'], response['cmd_status'], response['cmd'] >> 8, response['cmd'] & 0xFF,
        response['data'][0], response['data'][1], response['data'][2], response['data'][3],
        response['chksum'], response['footer1'], response['footer2']
    ]
    command_response = [hex(x) for x in response_list if isinstance(x, int)]
    
    if response['cmd_status'] != 0x00:
        return jsonify({"status": "error", "message": "Communication Failed"}), 500
    
    result = (
        (response['data'][0] << 24) |
        (response['data'][1] << 16) |
        (response['data'][2] << 8) |
        response['data'][3]
    )

    return jsonify({
        "status": "success",
        "value": result,
        "command_sent": ','.join([f'0x{cmd:02x}' for cmd in command_sent]),
        "command_response": ','.join(command_response),
        "register": hex(command_sent[8])
    }), 200

@app.route('/set_brightness', methods=['POST'])
def set_brightness():
    data = request.json
    com_port = data.get('com_port')
    baud_rate = int(data.get('baud_rate'))
    brightness = data.get('brightness')
    return handle_serial_communication(com_port, baud_rate, 0xd0, brightness)

@app.route('/get_default_brightness', methods=['GET'])
def get_default_brightness():
    com_port = request.args.get('com_port')
    baud_rate = int(request.args.get('baud_rate'))
    return handle_serial_communication(com_port, baud_rate, 0xd0)

@app.route('/set_contrast', methods=['POST'])
def set_contrast():
    data = request.json
    com_port = data.get('com_port')
    baud_rate = int(data.get('baud_rate'))
    contrast = data.get('contrast')
    return handle_serial_communication(com_port, baud_rate, 0xd4, contrast)

@app.route('/get_default_contrast', methods=['GET'])
def get_default_contrast():
    com_port = request.args.get('com_port')
    baud_rate = int(request.args.get('baud_rate'))
    return handle_serial_communication(com_port, baud_rate, 0xd4)

@app.route('/set_dzoom', methods=['POST'])
def set_dzoom():
    data = request.json
    com_port = data.get('com_port')
    baud_rate = int(data.get('baud_rate'))
    dzoom = data.get('dzoom')
    
    zoom_setting = {0: 0, 1: 1, 2: 2}.get(int(dzoom), 0)  # Default to 0 (1x) if out of range
    
    result =  handle_serial_communication(com_port, baud_rate, 0x86, zoom_setting)
    render_template_string( HTML_TEMPLATE, com_port=com_port, baud_rate=baud_rate, contrast=contrast, result=result)
    return result
    # return render_template_string( HTML_TEMPLATE, com_port=com_port, baud_rate=baud_rate, contrast=contrast, result=result)

@app.route('/get_default_dzoom', methods=['GET'])
def get_default_dzoom():
    com_port = request.args.get('com_port')
    baud_rate = int(request.args.get('baud_rate'))
    return handle_serial_communication(com_port, baud_rate, 0x86)

@app.route('/set_polarity', methods=['POST'])
def set_polarity():
    data = request.json
    com_port = data.get('com_port')
    baud_rate = int(data.get('baud_rate'))
    polarity = data.get('polarity')

    polarity_setting = {0: 0, 1: 1, 2: 2}.get(int(polarity), 0)  # Default to 0 (White Hot) if out of range
    
    return handle_serial_communication(com_port, baud_rate, 0x52, polarity_setting)

@app.route('/get_default_polarity', methods=['GET'])
def get_default_polarity():
    com_port = request.args.get('com_port')
    baud_rate = int(request.args.get('baud_rate'))
    return handle_serial_communication(com_port, baud_rate, 0x52)

@app.route('/set_agc', methods=['POST'])
def set_agc():
    data = request.json
    com_port = data.get('com_port')
    baud_rate = int(data.get('baud_rate'))
    agc = data.get('agc')
    
    agc_setting = {0: 0, 1: 1, 2: 2}.get(int(agc), 0)  # Default to 0 if out of range
    
    return handle_serial_communication(com_port, baud_rate, 0x51, agc_setting)

@app.route('/get_default_agc', methods=['GET'])
def get_default_agc():
    com_port = request.args.get('com_port')
    baud_rate = int(request.args.get('baud_rate'))
    return handle_serial_communication(com_port, baud_rate, 0x51)

@app.route('/set_nuc', methods=['POST'])
def set_nuc():
    data = request.json
    com_port = data.get('com_port')
    baud_rate = int(data.get('baud_rate'))
    nuc = data.get('nuc')
    
    nuc_setting = {0: 0, 1: 1, 2: 2}.get(int(nuc), 0)  # Default to 0 (Shutterless) if out of range
    
    return handle_serial_communication(com_port, baud_rate, 0x91, nuc_setting)

@app.route('/get_default_nuc', methods=['GET'])
def get_default_nuc():
    com_port = request.args.get('com_port')
    baud_rate = int(request.args.get('baud_rate'))
    return handle_serial_communication(com_port, baud_rate, 0x91)

@app.route('/set_reticle', methods=['POST'])
def set_reticle():
    data = request.json
    com_port = data.get('com_port')
    baud_rate = int(data.get('baud_rate'))
    reticle = data.get('reticle')
    
    reticle_setting = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}.get(int(reticle), 0)  # Default to 0 if out of range
    
    return handle_serial_communication(com_port, baud_rate, 0x66, reticle_setting)

@app.route('/get_default_reticle', methods=['GET'])
def get_default_reticle():
    com_port = request.args.get('com_port')
    baud_rate = int(request.args.get('baud_rate'))
    return handle_serial_communication(com_port, baud_rate, 0x66)

@app.route('/set_reticle_colour', methods=['POST'])
def set_reticle_colour():
    data = request.json
    com_port = data.get('com_port')
    baud_rate = int(data.get('baud_rate'))
    reticle_colour = data.get('reticle_colour')
    
    colour_setting = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5}.get(int(reticle_colour), 0)  # Default to 0 (White) if out of range
    
    return handle_serial_communication(com_port, baud_rate, 0x67, colour_setting)

@app.route('/get_default_reticle_colour', methods=['GET'])
def get_default_reticle_colour():
    com_port = request.args.get('com_port')
    baud_rate = int(request.args.get('baud_rate'))
    return handle_serial_communication(com_port, baud_rate, 0x67)

@app.route('/get_fw_version', methods=['GET'])
def get_fw_version():
    com_port = request.args.get('com_port')
    baud_rate = int(request.args.get('baud_rate'))
    
    try:
        ser = serial.Serial(com_port, baud_rate, timeout=5)
        cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')
        
        # Reading FW version from address 0x10
        fw_version = cmd_gen.fpga_read(0x10)
        
        ser.close()
        
        if fw_version['cmd_status'] != 0x00:
            return jsonify({"status": "error", "message": "Communication Failed"}), 500
        
        fw_ver_out = [fw_version['data'][0], fw_version['data'][1], fw_version['data'][2], fw_version['data'][3]]
        
        return jsonify({
            "status": "success",
            "fw_version": '.'.join(map(str, fw_ver_out)),
            "command_sent": "0xe0,0x00,0x01,0x3e,0xff,0x03,0x52,0x50,0x10",
            "command_response": ','.join([f'0x{x:02x}' for x in fw_version['data']]),
            "register": "0x10"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Use environment variable for port, defaulting to 8000 if not set
    port = int(os.environ.get('PORT', 8000))
    # In production, you typically want to set debug to False
    app.run(host='0.0.0.0', port=port, debug=False)