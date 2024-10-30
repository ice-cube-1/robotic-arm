import { Buffers, initBuffers } from "./cube-buffer.js";
import { drawScene, drawSceneForPicking } from "./draw-scene.js";

var mousedown = false;
var mousePos = {x:0,y:0}
var prevmouse = {x:0,y:0}
var positions = [[0, 29.75, 0.0, 59.5+4], [6.283683576271408, 92.71077115505295, 2.9545969675064323, 67.6+4], [43.78368357627141, 112.96077115505295, 1.1772622130201693, 67.6+4], [87.5, 100.0, 1.5707963267948966, 25],[100,100]]
var angle = Math.PI/4;
var stepperpos = 100
var barrels: Barrel[] = [];
var websocket = new WebSocket("ws://192.168.137.81:8765")

function updateInfo() {
    const x: string = (document.getElementById("xpos") as HTMLInputElement).value;
    const y: string = (document.getElementById("ypos") as HTMLInputElement).value;
    const step: string = (document.getElementById("step") as HTMLInputElement).value;
    websocket.send(`${x} ${y} ${step}`);
}

export type Barrel = {
    position: number[],
    colorID: number[],
    attached: string
}

function takePhoto() {
    websocket.send("photo")
}

function scan() {
    websocket.send("scan")
}

function moveClaw(checkbox: HTMLInputElement) {
    if (checkbox.checked) {
        angle = Math.PI/2
        websocket.send("claw 45")
    } else {
        websocket.send("claw 0")
        angle = Math.PI/4
    }
}

websocket.onmessage = (event) => {
    if (event.data == "image") {
        const img = document.getElementById('camera') as HTMLImageElement;
        img.src = `static/image.jpg?${Math.ceil(Math.random() * 1000)}`;        
    } else if (event.data.startsWith("barrel ")) {
        var info = event.data.split(" ")
        barrels.push({position: [parseFloat(info[1]),parseFloat(info[2])], colorID:[255,barrels.length*10,0,255,0], attached:"no"})
    } else if (event.data.startsWith("stepperpos")) {
        stepperpos=parseInt(event.data.split(" ")[1])
        console.log(stepperpos)
    } else if (event.data.startsWith("claw ")) {
        angle=parseFloat(event.data.split(" ")[1])
    } else if (event.data == "attached") {
        for (var i = 0; i<barrels.length; i++) {
            if (barrels[i].attached == "next") {
                barrels[i].attached = "yes"
            }
        }
    } else if (event.data.startsWith("dropped")) {
        for (var i = 0; i<barrels.length; i++) {
            if (barrels[i].attached == "yes") {
                barrels[i].attached = "no"
                barrels[i].position = event.data.split(" ").slice(1)
            }
        }
    } else {
        var obj  = JSON.parse(event.data);
        positions = obj
    }
};

(window as any).updateInfo = updateInfo;
(window as any).moveClaw = moveClaw;
(window as any).takePhoto = takePhoto;
(window as any).scan = scan;

main();

export type ProgramInfo = {
    program: WebGLProgram;
    attribLocations: {
        vertexPosition: number;
        vertexNormal: number;
        textureCoord: number;
    };
    uniformLocations: {
        projectionMatrix: WebGLUniformLocation;
        modelViewMatrix: WebGLUniformLocation;
        normalMatrix: WebGLUniformLocation;
        uSampler: WebGLUniformLocation;
    };
}

function main() {
    const canvas = document.querySelector("#glcanvas")
    const gl = (canvas as HTMLCanvasElement).getContext("webgl") as WebGLRenderingContext;
    gl.clearColor(0.0, 0.0, 0.0, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT);
    const vsSource = `
        attribute vec4 aVertexPosition;
        attribute vec3 aVertexNormal;
        attribute vec2 aTextureCoord;
        uniform mat4 uNormalMatrix;
        uniform mat4 uModelViewMatrix;
        uniform mat4 uProjectionMatrix;
        varying highp vec2 vTextureCoord;
        varying highp vec3 vLighting;
        void main(void) {
            gl_Position = uProjectionMatrix * uModelViewMatrix * aVertexPosition;
            vTextureCoord = aTextureCoord;
            highp vec3 ambientLight = vec3(0.3, 0.3, 0.3);
            highp vec3 directionalLightColor = vec3(1, 1, 1);
            highp vec3 directionalVector = normalize(vec3(0.85, 0.8, 0.75));
            highp vec4 transformedNormal = uNormalMatrix * vec4(aVertexNormal, 1.0);
            highp float directional = max(dot(transformedNormal.xyz, directionalVector), 0.0);
            vLighting = ambientLight + (directionalLightColor * directional);
        }
    `;
    const fsSource = `
        varying highp vec2 vTextureCoord;
        varying highp vec3 vLighting;
        uniform sampler2D uSampler;
        void main(void) {
        highp vec4 texelColor = texture2D(uSampler, vTextureCoord);
        gl_FragColor = vec4(texelColor.rgb * vLighting, texelColor.a);
        }
    `;
    const shaderProgram = initShaderProgram(gl, vsSource, fsSource);
    const programInfo: ProgramInfo = {
        program: shaderProgram,
        attribLocations: {
          vertexPosition: gl.getAttribLocation(shaderProgram, "aVertexPosition"),
          vertexNormal: gl.getAttribLocation(shaderProgram, "aVertexNormal"),
          textureCoord: gl.getAttribLocation(shaderProgram, "aTextureCoord"),
        },
        uniformLocations: {
          projectionMatrix: gl.getUniformLocation(shaderProgram, "uProjectionMatrix") as WebGLUniformLocation,
          modelViewMatrix: gl.getUniformLocation(shaderProgram, "uModelViewMatrix") as WebGLUniformLocation,
          normalMatrix: gl.getUniformLocation(shaderProgram, "uNormalMatrix") as WebGLUniformLocation,
          uSampler: gl.getUniformLocation(shaderProgram, "uSampler") as WebGLUniformLocation,
        },
      };            
    const buffers = initBuffers(gl) as Buffers;
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
    function render() {
        drawScene(gl, programInfo, buffers, mousePos.x, mousePos.y, positions, 1000, angle, barrels, stepperpos);
        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);
    (canvas as HTMLCanvasElement).addEventListener('mousemove', function(e) {
        getMousePosition(e);
    });
    addEventListener("click", function(e: MouseEvent) {
        const target = e.currentTarget as HTMLButtonElement
        const rect = target.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        drawSceneForPicking(gl, programInfo, buffers, mousePos.x, mousePos.y, 1000, barrels);
        var pixels = new Uint8Array(4);
        gl.readPixels(x, rect.height - y, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, pixels);
        const scale = 255/Math.max(...pixels.subarray(0,3))
        for (let i = 0; i<pixels.length; i++) {
            pixels[i]=pixels[i]*scale
        }
        console.log(pixels)
        if (pixels[0] == 255 && pixels[2] == 0) {
            websocket.send("barrel "+barrels[Math.round(pixels[1]/10)].position[0]+" "+barrels[Math.round(pixels[1]/10)].position[0])
            console.log("barrel")
        }        
    });
}


function initShaderProgram(gl: WebGLRenderingContext, vsSource: string, fsSource: string) {
    const vertexShader = loadShader(gl, gl.VERTEX_SHADER, vsSource) as WebGLShader;
    const fragmentShader = loadShader(gl, gl.FRAGMENT_SHADER, fsSource) as WebGLShader;
    const shaderProgram = gl.createProgram() as WebGLProgram;
    gl.attachShader(shaderProgram, vertexShader);
    gl.attachShader(shaderProgram, fragmentShader);
    gl.linkProgram(shaderProgram);
    return shaderProgram;
}

function loadShader(gl: WebGLRenderingContext, type: GLenum, source: string) {
    const shader = gl.createShader(type) as WebGLShader;
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    return shader;
}

addEventListener("mousedown", (event) => {
    mousedown = true;
    const rect = (event.target as HTMLElement).getBoundingClientRect();
    prevmouse.x = ((event.clientX - rect.left) / rect.width * 2 - 1) * 4;
    prevmouse.y = ((event.clientY - rect.top) / rect.height * 2 - 1) * 2;
});

addEventListener("mouseup", (_) => {
    mousedown = false;
});

 function getMousePosition(event: MouseEvent) {
    const target = event.currentTarget as HTMLButtonElement
    if (mousedown) {
        const rect = target.getBoundingClientRect();
        const x = ((event.clientX - rect.left) / rect.width * 2 - 1)*4;
        const y = ((event.clientY - rect.top) / rect.height * 2 - 1)*2;
        mousePos = {x: mousePos.x+x-prevmouse.x, y: mousePos.y+y-prevmouse.y}
        prevmouse = {x: x,y: y}
    }
}
