// We use the WebAudio API in Javascript in order to access the user's microphone. It asks for permission first. 

// Some variable to keep track of the audio context, source, and stream

var audioCtx = new (window.AudioContext || window.webkitAudioContext)({sampleRate: 10000,});
var source;
var stream;

//set up the analyser node that grabs the sound samples

var analyser = audioCtx.createAnalyser();
    analyser.minDecibels = -90;
    analyser.maxDecibels = -10;
    analyser.smoothingTimeConstant = 0.85;

// a variable to keep track of animation frames

var drawVisual;

// start up the microphone (media) and then connect it to the visualizer

if (navigator.mediaDevices.getUserMedia) {
    console.log("mediaDevices.getUserMedia supported.");
    async function getMedia(constraints) {
        try {
            stream = await navigator.mediaDevices.getUserMedia(constraints);
            source = audioCtx.createMediaStreamSource(stream);
            source.connect(analyser);
            visualize();
        } 
        catch (err) {
            console.log("The following gUM error occured: " + err);
        }
    }
    getMedia({audio: true,})
} else {
          console.log("mediaDevices.getUserMedia not supported on your browser!");
};

// This visualize function catches the sound samples then passes it to the Plotly device in Python
// We also check one global variable "killDraw" to see when we should stop the drawing. 
function visualize() {
    analyser.fftSize = 256;
    var dataArray = new Float32Array(analyser.frequencyBinCount);
    var fps = 4;
    window.killDraw = false;
    function draw(timestamp){
        if (window.killDraw) {return;}
        setTimeout(function(){ //throttle requestAnimationFrame to 4 fps
            analyser.getFloatFrequencyData(dataArray);
            IPython.notebook.kernel.execute(
                "f.data[0]['y'] = "+ dataArray + ";"
            ); 
            drawVisual = requestAnimationFrame(draw)
        }, 1000/fps)
    }
    draw();
}

// finally, we save the "visualize" function in a variable we can call from a Jupyter cell later. 
window.myVis = visualize;