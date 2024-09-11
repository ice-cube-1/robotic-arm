import { initBuffers } from "./cube-buffer.js";
import { drawScene } from "./draw-scene.js";

var mousedown = false;
var mousePos = {x:0,y:0}
var prevmouse = {x:0,y:0}
var positions = [[0, 29.75, 1.5707963267948966, 59.5], [6.283683576271408, 92.71077115505295, 2.9545969675064323, 59.5], [43.78368357627141, 112.96077115505295, 1.1772622130201693, 59.5], [87.5, 100.0, 0.0, 59.5]]

main();
function main() {
    const canvas = document.querySelector("#glcanvas")
    const gl = canvas.getContext("webgl");
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
    const programInfo = {
        program: shaderProgram,
        attribLocations: {
          vertexPosition: gl.getAttribLocation(shaderProgram, "aVertexPosition"),
          vertexNormal: gl.getAttribLocation(shaderProgram, "aVertexNormal"),
          textureCoord: gl.getAttribLocation(shaderProgram, "aTextureCoord"),
        },
        uniformLocations: {
          projectionMatrix: gl.getUniformLocation(shaderProgram, "uProjectionMatrix"),
          modelViewMatrix: gl.getUniformLocation(shaderProgram, "uModelViewMatrix"),
          normalMatrix: gl.getUniformLocation(shaderProgram, "uNormalMatrix"),
          uSampler: gl.getUniformLocation(shaderProgram, "uSampler"),
        },
      };            
    const buffers = initBuffers(gl);
    const texture = loadTexture(gl, [255,0,0, 255]);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
    function render() {
        drawScene(gl, programInfo, buffers, mousePos.x, mousePos.y, positions, 200);
        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);
    canvas.addEventListener('mousemove', function(e) {
        getMousePosition(e, canvas);
    });
}


function initShaderProgram(gl, vsSource, fsSource) {
    const vertexShader = loadShader(gl, gl.VERTEX_SHADER, vsSource);
    const fragmentShader = loadShader(gl, gl.FRAGMENT_SHADER, fsSource);
    const shaderProgram = gl.createProgram();
    gl.attachShader(shaderProgram, vertexShader);
    gl.attachShader(shaderProgram, fragmentShader);
    gl.linkProgram(shaderProgram);
    return shaderProgram;
}

function loadShader(gl, type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    return shader;
}

function loadTexture(gl, color) {
    const texture = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, texture);
    const level = 0;
    const internalFormat = gl.RGBA;
    const width = 1;
    const height = 1;
    const border = 0;
    const srcFormat = gl.RGBA;
    const srcType = gl.UNSIGNED_BYTE;
    const pixel = new Uint8Array(color);
    gl.texImage2D(gl.TEXTURE_2D, level, internalFormat, width, height, border, srcFormat, srcType, pixel);
    return texture;
}

addEventListener("mousedown", (event) => {
    mousedown = true;
    const rect = event.target.getBoundingClientRect();
    prevmouse.x = ((event.clientX - rect.left) / rect.width * 2 - 1) * 4;
    prevmouse.y = ((event.clientY - rect.top) / rect.height * 2 - 1) * 2;
});

addEventListener("mouseup", (_) => {
    mousedown = false;
});

 function getMousePosition(event, target) {
    target = target || event.target;
    if (mousedown) {
        const rect = target.getBoundingClientRect();
        const x = ((event.clientX - rect.left) / rect.width * 2 - 1)*4;
        const y = ((event.clientY - rect.top) / rect.height * 2 - 1)*2;
        mousePos = {x: mousePos.x+x-prevmouse.x, y: mousePos.y+y-prevmouse.y}
        prevmouse = {x: x,y: y}
    }
}