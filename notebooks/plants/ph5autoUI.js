// ph4auto.js code for Phidgets4.ipynb
// Copyright 2023. Michael Lamoureux with the Callysto project.

// this is the _esm file for an anywidget object to be created in a Python class
// The UI includes a single button to open, and then close the USB connection to the Phidgets device.
// It includes a text box showing the status, and 4 text boxes to display values from the Phidget sensors. 
// We assume 5 devices: temperature, humidity, moisture (voltage ratio), light, and a pump, as in the Phidgets plant kit. 
// The data is updated every second -- this could be changed in the JS code below (see "onAttached()").

// the anywidget model includes fve Python variables "temperature, humidity, moisture, luminance, pump" that will be
// kept updated between the JS front end and the Python kernel.
// A sixth variable "hubPort" allows the user to specify which port the moisture sensor is connected to. 

// The connection logic takes into account that the USB connection must be made before the sensor channels can be connected.
// We keep track of whether the USB connection is open (variable connOpen) and the channels are open (chOpen). 
// We also need to close the connections when the notebook shuts down. The "return" statement handles this. 

// Lots of errors are posted to the console log, for debugging purposes. 

// The ESM method to import the necessary functions from the phidget22 library
import {USBConnection, TemperatureSensor, HumiditySensor, 
        VoltageRatioInput, LightSensor, DigitalOutput} from "https://esm.sh/phidget22@3.17";

export function render({ model, el }) {
    var conn = 0;
    var chTempe = 0;
    var chHumid = 0;
    var chMoist = 0;
    var chLumin = 0;
    var chPump1 = 0;
    var isOpen = false;
    var connOpen = false;
    var chOpen = false;

    async function openUSB() {
        if (conn) {
            try {await chTempe.close();} catch {console.log('chT.close failed');}
            try {await chHumid.close();} catch {console.log('chH.close failed');}
            try {await chMoist.close();} catch {console.log('chM.close failed');}
            try {await chLumin.close();} catch {console.log('chL.close failed');}
            try {await conn.close();} catch {console.log('conn.close failed');}
            try {await conn.delete();} catch {console.log('conn.delete failed');}
        }
        conn = new USBConnection();
        chTempe = new TemperatureSensor();
        chHumid = new HumiditySensor();
        chMoist = new VoltageRatioInput();
        chLumin = new LightSensor();
        chPump1 = new DigitalOutput();
        conn.onError = function(code, msg) {
            console.log('Conn Code: ' + code);
            console.log('Conn error: ' + msg);
        };
        chTempe.onError = (code, msg) => {
        	console.log('Tempe Code: ' + code);
        	console.log('Tempe error: ' + msg);
        };
        chHumid.onError = (code, msg) => {
        	console.log('Humid Code: ' + code);
        	console.log('Humid error: ' + msg);
        };
        chMoist.onError = (code, msg) => {
        	console.log('Moist Code: ' + code);
        	console.log('Moist error: ' + msg);
        };
        chLumin.onError = (code, msg) => {
        	console.log('Lumin Code: ' + code);
        	console.log('Lumin error: ' + msg);
        };
        chPump1.onError = (code, msg) => {
        	console.log('Pump1 Code: ' + code);
        	console.log('Pump1 error: ' + msg);
        };
        chTempe.onTemperatureChange = function(temperature) {
            textTempe.innerHTML = 'Temperature is ' + temperature;
            model.set('temperature', temperature);
            model.save_changes();
       	};
        chHumid.onHumidityChange = function(humidity) {
            textHumid.innerHTML = 'Humidity is ' + humidity;
            model.set('humidity', humidity);
            model.save_changes();
       	};
        chMoist.onVoltageRatioChange = function(ratio) {
            textMoist.innerHTML = 'Moisture is ' + ratio;
            model.set('moisture', ratio);
            model.save_changes();
       	};
        chLumin.onIlluminanceChange = function(luminance) {
            textLumin.innerHTML = 'Luminance is ' + luminance;
            model.set('luminance', luminance);
            model.save_changes();
       	};
        chTempe.onAttach = onAttach;
        chHumid.onAttach = onAttach;
        chMoist.onAttach = onAttach;
        chLumin.onAttach = onAttach;
        chPump1.onAttach = onAttach;
        chTempe.onDetach = () => {
        	console.log('T onDetach called. ');
        }
        chHumid.onDetach = () => {
        	console.log('H onDetach called. ');
        }
        chMoist.onDetach = () => {
        	console.log('M onDetach called. ');
        }
        chLumin.onDetach = () => {
        	console.log('L onDetach called. ');
        }
        chPump1.onDetach = () => {
        	console.log('P onDetach called. ');
        }

        chPump1.setIsHubPortDevice(true);
        chPump1.setHubPort(model.get("hubPort"));

        try {
    		await conn.connect();
            conn.requestWebUSBDeviceAccess();
            console.log('usb connected');
            connOpen = true;
    	} catch(err) {
    		console.log("Conn open error: ", err);
            connOpen = false;
    	}
        if (connOpen) {
            chOpen = false;
            try {
                await chTempe.open(2000);
                console.log('T Channel connected');
                chOpen = true;
            } catch(err) {
        		console.log("T Channel open error: ", err);
                chOpen ||= false;                
            }
            try {
                await chHumid.open(2000);
                console.log('H Channel connected');
                chOpen = true;
            } catch(err) {
        		console.log("H Channel open error: ", err);
                chOpen ||= false;                
            }
            try {
                await chMoist.open(2000);
                console.log('M Channel connected');
                chOpen = true;
            } catch(err) {
        		console.log("M Channel open error: ", err);
                chOpen ||= false;                
            }
            try {
                await chLumin.open(2000);
                console.log('L Channel connected');
                chOpen = true;
            } catch(err) {
        		console.log("L Channel open error: ", err);
                chOpen ||= false;                
            }
            try {
                await chPump1.open(2000);
                console.log('P Channel connected');
                chOpen = true;
            } catch(err) {
        		console.log("P Channel open error: ", err);
                chOpen ||= false;                
            }
        }
         // now get the UI to reflect the status
        if (connOpen && chOpen) {
            isOpen = true;
            textStatus.innerHTML = 'USB connected, channels open.';
            button.innerHTML = `Click to disconnect`;
        }
        if (connOpen && !chOpen) {
            isOpen = false;
            textStatus.innerHTML = 'USB connected, channels not open.';
            button.innerHTML = `Click to connect`;
        }
        if (!connOpen) {
            isOpen = false;
            textStatus.innerHTML = 'USB did not connect.';
            button.innerHTML = `Click to connect`;        
        }
    };
    async function onAttach(ch) {
        console.log('channel is attached' + ch);
        textStatus.innerHTML = 'Attached.  ';
        await ch.setDataInterval(1000);
    }
    async function closeUSB() {
        console.log('closeUSB called');
        try {await chPump1.setState(false);} catch {console.log('P.set_false failed');} // turn off the water!
        try {await chTempe.close();} catch {console.log('T.close failed');}
        try {await chHumid.close();} catch {console.log('H.close failed');}
        try {await chMoist.close();} catch {console.log('M.close failed');}
        try {await chLumin.close();} catch {console.log('L.close failed');}
        try {await chPump1.close();} catch {console.log('L.close failed');}
        try {await conn.close();} catch {console.log('conn.close failed');}
        try {await conn.delete();} catch {console.log('conn.delete failed');}
        isOpen = false; 
        connOpen = false;
        chOpen = false;
        textStatus.innerHTML = 'Disconnected.  ';
        textTempe.innerHTML = 'Temperature is null.';
        textHumid.innerHTML = 'Humidity is null.';
        textMoist.innerHTML = 'Moisture is null.';
        textLumin.innerHTML = 'Luminance is null.';
        textPump1.innerHTML = 'Pump state is null.';
        button.innerHTML = `Click to connect`;
    };
    model.on('msg:custom', msg => {
        console.log(`new message: ${JSON.stringify(msg)}`);
        if (msg == 'open') {
            console.log('open called');
            openUSB();
        }
        if (msg == 'close') {
            console.log('close called');
            closeUSB();
        }
        if (msg == 'read') {
            console.log('read called');
            readDevices();
        }
        if (msg == 'pumpOn') {
            console.log('pumpOn called');
            chPump1.setState(true);
        }
        if (msg == 'pumpOff') {
            console.log('pumpOff called');
            chPump1.setState(false);
        }
    });
    
    // here we define the user interface
    let button = document.createElement("button");
    button.classList.add("ph-button");
    button.innerHTML = `Click to open USB`;
    button.addEventListener("click", async () => {
        if (isOpen) {closeUSB();} else {openUSB();}
    });
    let textStatus = document.createElement("label");
    textStatus.innerHTML = 'Status message here';
    let textTempe = document.createElement("label");
    textTempe.innerHTML = 'Temperature';
    let textHumid = document.createElement("label");
    textHumid.innerHTML = 'Humidity';
    let textMoist = document.createElement("label");
    textMoist.innerHTML = 'Moisture';
    let textLumin = document.createElement("label");
    textLumin.innerHTML = 'Luminance';
    let textPump1 = document.createElement("label");
    textPump1.innerHTML = 'Pump state';

    // here we access the Python variables in the anywidget model, and connect to the UI
    let getTemperature = () => model.get("temperature");
    let getHumidity = () => model.get("humidity");
    let getMoisture = () => model.get("moisture");
    let getLuminance = () => model.get("luminance");
    let getPump = () => model.get("pump");

    model.on("change:temperature", () => {
        textTempe.innerHTML = `Temperature is ${getTemperature()}`;
    });
    model.on("change:humidity", () => {
        textHumid.innerHTML = `Humidity is ${getHumidity()}`;
    });
    model.on("change:moisture", () => {
        textMoist.innerHTML = `Moisture is ${getMoisture()}`;
    });
    model.on("change:luminance", () => {
        textLumin.innerHTML = `Luminance is ${getLuminance()}`;
    });
    model.on("change:pump", () => {
        textPump1.innerHTML = `Pump state is ${getPump()}`;
    });
    
    // Post the UI into the Jupyter notebook cell
    let div0 = document.createElement("div");
    let div1 = document.createElement("div");
    let div2 = document.createElement("div");
    let div3 = document.createElement("div");
    let div4 = document.createElement("div");
    div0.appendChild(textTempe);
    div1.appendChild(textHumid);
    div2.appendChild(textMoist);
    div3.appendChild(textLumin);
    div4.appendChild(textPump1);

    el.appendChild(button);
    el.appendChild(textStatus);
    el.appendChild(div0);
    el.appendChild(div1);
    el.appendChild(div2);
    el.appendChild(div3);
    el.appendChild(div4);
    
    // we include a return function to close the Phidget when the notebook is close
    return async () => {
        try {await chPump1.setState(false);} catch {} // turn off the water!
        try {await chTempe.close();} catch {}
        try {await chHumid.close();} catch {}
        try {await chMoist.close();} catch {}
        try {await chLumin.close();} catch {}
        try {await conn.close();} catch {}
        try {await conn.delete();} catch {}
    };
    }
