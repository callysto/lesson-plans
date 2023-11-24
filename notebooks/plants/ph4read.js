// ph4read.js code for PhidgetFour_read.ipynb
// Copyright 2023. Michael Lamoureux with the Callysto project.

// this is the _esm file for an anywidget object to be created in a Python class
// The UI includes a two buttons: one to open and close the USB connection, and one to read the Phidget devices.
// It includes a text box showing the status, and 4 text boxes to display values from the Phidget sensors. 
// We assume 4 devices: temperature, humidity, moisture (voltage ratio), and light, as in the Phidgets plant kit. 
// The data is updated only on button click. It can also be updated using a function call in Python.

// the anywidget model includes four Python variables "temperature, humidity, moisture, luminance" that will be
// kept updated between the JS front end and the Python kernel.
// A fifth variable "hubPort" allows the user to specify which port the moisture sensor is connected to. 

// The connection logic takes into account that the USB connection must be made before the sensor channels can be connected.
// We keep track of whether the USB connection is open (variable connOpen) and the channels are open (chOpen). 
// We also need to close the connections when the notebook shuts down. The "return" statement handles this. 

// Lots of errors are posted to the console log, for debugging purposes. 

// The ESM method to import the necessary functions from the phidget22 library
import {USBConnection, TemperatureSensor, HumiditySensor, 
        VoltageRatioInput, LightSensor} from "https://esm.sh/phidget22@3.17";

export function render({ model, el }) {
    var conn = 0;
    var chTempe = 0;
    var chHumid = 0;
    var chMoist = 0;
    var chLumin = 0;
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
        chTempe.onAttach = onAttach;
        chHumid.onAttach = onAttach;
        chMoist.onAttach = onAttach;
        chLumin.onAttach = onAttach;
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

        chMoist.setIsHubPortDevice(true);
        chMoist.setHubPort(model.get("hubPort"));
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
                await chTempe.open(1000);
                console.log('T Channel connected');
                chOpen = true;
            } catch(err) {
        		console.log("T Channel open error: ", err);
                chOpen ||= false;                
            }
            try {
                await chHumid.open(1000);
                console.log('H Channel connected');
                chOpen = true;
            } catch(err) {
        		console.log("H Channel open error: ", err);
                chOpen ||= false;                
            }
            try {
                await chMoist.open(1000);
                console.log('M Channel connected');
                chOpen = true;
            } catch(err) {
        		console.log("M Channel open error: ", err);
                chOpen ||= false;                
            }
            try {
                await chLumin.open(1000);
                console.log('L Channel connected');
                chOpen = true;
            } catch(err) {
        		console.log("L Channel open error: ", err);
                chOpen ||= false;                
            }
        }
        // now get the UI to reflect the status
        if (connOpen && chOpen) {
            isOpen = true;
            textStatus.innerHTML = 'USB connected, channels open.';
            buttonOpen.innerHTML = 'Click to disconnect';
        }
        if (connOpen && !chOpen) {
            isOpen = false;
            textStatus.innerHTML = 'USB connected, channels not open.';
            buttonOpen.innerHTML = 'Click to connect';
        }
        if (!connOpen) {
            isOpen = false;
            textStatus.innerHTML = 'USB did not connect.';
            buttonOpen.innerHTML = 'Click to connect';        
        }
    };
    function onAttach(ch) {
        console.log('channel is attached' + ch);
        textStatus.innerHTML = 'Attached.  ';
    }
    async function closeUSB() {
        console.log('closeUSB called');
        try {await chTempe.close();} catch {console.log('T.close failed');}
        try {await chHumid.close();} catch {console.log('H.close failed');}
        try {await chMoist.close();} catch {console.log('M.close failed');}
        try {await chLumin.close();} catch {console.log('L.close failed');}
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
        buttonOpen.innerHTML = 'Click to connect';
    };
    function readDevices() {
        let t0 = 0;
        let h0 = 0;
        let m0 = 0;
        let l0 = 0;
        if (chTempe.attached) {t0 = chTempe.temperature; }       
        if (chHumid.attached) {h0 = chHumid.humidity; }       
        if (chMoist.attached) {m0 = chMoist.voltageRatio; }       
        if (chLumin.attached) {l0 = chLumin.illuminance; }       
        model.set('temperature', t0 );
        model.set('humidity', h0);
        model.set('moisture', m0);
        model.set('luminance', l0);
        model.save_changes();
    };

    model.on('msg:custom', msg => {
        console.log('new message: ${JSON.stringify(msg)}');
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
    });
    
    // here we define the user interface
    let buttonOpen = document.createElement("button");
    buttonOpen.classList.add("ph-button");
    buttonOpen.innerHTML = 'Click to open USB';
    buttonOpen.addEventListener("click", async () => {
        if (isOpen) {closeUSB();} else {openUSB();}
    });
    let buttonRead = document.createElement("button");
    buttonRead.classList.add("ph-button");
    buttonRead.innerHTML = 'Click to read data';
    buttonRead.addEventListener("click", async () => {
        if (isOpen) {readDevices();}
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

    // here we access the Python variables in the anywidget model, and connect to the UI
    let getTemperature = () => model.get("temperature");
    let getHumidity = () => model.get("humidity");
    let getMoisture = () => model.get("moisture");
    let getLuminance = () => model.get("luminance");

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
    
    // Post the UI into the Jupyter notebook cell
    let div0 = document.createElement("div");
    let div1 = document.createElement("div");
    let div2 = document.createElement("div");
    let div3 = document.createElement("div");
    div0.appendChild(textTempe);
    div1.appendChild(textHumid);
    div2.appendChild(textMoist);
    div3.appendChild(textLumin);

    el.appendChild(buttonOpen);
    el.appendChild(buttonRead);
    el.appendChild(textStatus);
    el.appendChild(div0);
    el.appendChild(div1);
    el.appendChild(div2);
    el.appendChild(div3);
    
    // we include a return function to close the Phidget when the notebook is close
    return async () => {
        try {await chTempe.close();} catch {}
        try {await chHumid.close();} catch {}
        try {await chMoist.close();} catch {}
        try {await chLumin.close();} catch {}
        try {await conn.close();} catch {}
        try {await conn.delete();} catch {}
    };
}