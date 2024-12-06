function drawScene(gl, programInfo, buffers, cameraRotationX, cameraRotationY, positions, zoom, angle, barrels, stepperpos) {
    var xpos = -zoom * Math.sin(cameraRotationX) * Math.cos(cameraRotationY);
    var ypos = zoom * Math.sin(cameraRotationY);
    var zpos = zoom * Math.cos(cameraRotationX) * Math.cos(cameraRotationY);
    gl.clearColor(0.8, 0.9, 1.0, 1.0);
    gl.clearDepth(1.0);
    gl.enable(gl.DEPTH_TEST);
    gl.depthFunc(gl.LEQUAL);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    const fieldOfView = (45 * Math.PI) / 180;
    const canvas = gl.canvas;
    const aspect = canvas.clientWidth / canvas.clientHeight;
    const zNear = 0.1;
    const zFar = 5000.0;
    const projectionMatrix = mat4.create();
    mat4.perspective(projectionMatrix, fieldOfView, aspect, zNear, zFar);
    var modelViewMatrix = mat4.create();
    mat4.lookAt(modelViewMatrix, [xpos, ypos, zpos], [0, 0, 0], [0, 1, 0]);
    const normalMatrix = mat4.create();
    mat4.invert(normalMatrix, modelViewMatrix);
    mat4.transpose(normalMatrix, normalMatrix);
    setPositionAttribute(gl, buffers, programInfo);
    setTextureAttribute(gl, buffers, programInfo);
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buffers.indices);
    setNormalAttribute(gl, buffers, programInfo);
    gl.useProgram(programInfo.program);
    gl.uniformMatrix4fv(programInfo.uniformLocations.projectionMatrix, false, projectionMatrix);
    gl.uniformMatrix4fv(programInfo.uniformLocations.modelViewMatrix, false, modelViewMatrix);
    gl.uniformMatrix4fv(programInfo.uniformLocations.normalMatrix, false, normalMatrix);
    gl.activeTexture(gl.TEXTURE0);
    gl.uniform1i(programInfo.uniformLocations.uSampler, 0);
    const vertexCount = 36;
    const type = gl.UNSIGNED_SHORT;
    const offset = 0;
    const realinitialmatrix = mat4.clone(modelViewMatrix);
    var initialMatrix = mat4.clone(modelViewMatrix);
    loadTexture(gl, new Uint8Array([200, 200, 200, 255]));
    mat4.translate(modelViewMatrix, modelViewMatrix, [0, -50, 0]);
    mat4.scale(modelViewMatrix, modelViewMatrix, [10000, 5, 10000]);
    gl.uniformMatrix4fv(programInfo.uniformLocations.modelViewMatrix, false, modelViewMatrix);
    gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
    mat4.copy(modelViewMatrix, initialMatrix);
    loadTexture(gl, new Uint8Array([50, 50, 50, 255]));
    mat4.translate(modelViewMatrix, modelViewMatrix, [0, -15, 0]);
    mat4.scale(modelViewMatrix, modelViewMatrix, [50, 30, 50]);
    gl.uniformMatrix4fv(programInfo.uniformLocations.modelViewMatrix, false, modelViewMatrix);
    gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
    for (var i = -1; i < 2; i += 2) {
        mat4.copy(modelViewMatrix, initialMatrix);
        mat4.translate(modelViewMatrix, modelViewMatrix, [0, -40, 0]);
        mat4.rotate(modelViewMatrix, modelViewMatrix, Math.PI / 4, [0, i, 0]);
        mat4.scale(modelViewMatrix, modelViewMatrix, [350, 5, 15]);
        gl.uniformMatrix4fv(programInfo.uniformLocations.modelViewMatrix, false, modelViewMatrix);
        gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
        mat4.copy(modelViewMatrix, initialMatrix);
    }
    mat4.rotate(modelViewMatrix, modelViewMatrix, Math.PI * stepperpos / 100, [0, -1, 0]);
    for (let i = 0; i < 4; i++) {
        const initialMatrix = mat4.clone(modelViewMatrix);
        mat4.translate(modelViewMatrix, modelViewMatrix, [positions[i][0] * 2, positions[i][1] * 2, 0]);
        mat4.rotate(modelViewMatrix, modelViewMatrix, positions[i][2], [0, 0, 1]);
        loadTexture(gl, new Uint8Array([50, 50, 50, 255]));
        mat4.scale(modelViewMatrix, modelViewMatrix, [20, positions[i][3], 20]);
        gl.uniformMatrix4fv(programInfo.uniformLocations.modelViewMatrix, false, modelViewMatrix);
        gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
        mat4.copy(modelViewMatrix, initialMatrix);
    }
    loadTexture(gl, new Uint8Array([250, 250, 250, 255]));
    for (let i = -1; i <= 1; i += 2) {
        const initialMatrix = mat4.clone(modelViewMatrix);
        mat4.translate(modelViewMatrix, modelViewMatrix, [positions[4][0] * 2 + (15 * Math.cos(angle)), positions[4][1] * 2 - 20, i * (15 * Math.sin(angle))]);
        mat4.rotate(modelViewMatrix, modelViewMatrix, Math.PI / 2, [0, 0, 1]);
        mat4.rotate(modelViewMatrix, modelViewMatrix, i * -angle, [1, 0, 0]);
        mat4.scale(modelViewMatrix, modelViewMatrix, [5, 15, 5]);
        gl.uniformMatrix4fv(programInfo.uniformLocations.modelViewMatrix, false, modelViewMatrix);
        gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
        mat4.copy(modelViewMatrix, initialMatrix);
        mat4.translate(modelViewMatrix, modelViewMatrix, [positions[4][0] * 2 + (30 * Math.cos(angle) + 15 * Math.cos(angle - Math.PI / 4)), positions[4][1] * 2 - 20, i * (30 * Math.sin(angle) - 15 * Math.cos(angle + Math.PI / 4))]);
        mat4.rotate(modelViewMatrix, modelViewMatrix, Math.PI / 2, [0, 0, 1]);
        mat4.rotate(modelViewMatrix, modelViewMatrix, i * -(angle - Math.PI / 4), [1, 0, 0]);
        mat4.scale(modelViewMatrix, modelViewMatrix, [5, 15, 5]);
        gl.uniformMatrix4fv(programInfo.uniformLocations.modelViewMatrix, false, modelViewMatrix);
        gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
        mat4.copy(modelViewMatrix, initialMatrix);
    }
    loadTexture(gl, new Uint8Array([0, 200, 50, 255]));
    initialMatrix = mat4.clone(modelViewMatrix);
    mat4.translate(modelViewMatrix, modelViewMatrix, [25, 50, 0]);
    mat4.scale(modelViewMatrix, modelViewMatrix, [2, 25, 25]);
    gl.uniformMatrix4fv(programInfo.uniformLocations.modelViewMatrix, false, modelViewMatrix);
    gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
    mat4.copy(modelViewMatrix, initialMatrix);
    loadTexture(gl, new Uint8Array([50, 50, 50, 255]));
    mat4.translate(modelViewMatrix, modelViewMatrix, [28, 50, 0]);
    mat4.scale(modelViewMatrix, modelViewMatrix, [2, 15, 10]);
    gl.uniformMatrix4fv(programInfo.uniformLocations.modelViewMatrix, false, modelViewMatrix);
    gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
    mat4.copy(modelViewMatrix, initialMatrix);
    var colors = {"red":[255,0,0,255], "yellow": [255,200,0,255]}
    for (let i = 0; i < barrels.length; i++) {
        if (barrels[i].attached == "yes") {
            loadTexture(gl, new Uint8Array(colors[barrels[i].color]));
            const initialMatrix = mat4.clone(modelViewMatrix);
            mat4.translate(modelViewMatrix, modelViewMatrix, [positions[4][0] * 2 + 40, positions[4][1] * 2 - 15, 0]);
            mat4.scale(modelViewMatrix, modelViewMatrix, [15, 30, 15]);
            gl.uniformMatrix4fv(programInfo.uniformLocations.modelViewMatrix, false, modelViewMatrix);
            gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
            mat4.copy(modelViewMatrix, initialMatrix);
        }
    }
    mat4.copy(modelViewMatrix, realinitialmatrix);
    for (let i = 0; i < barrels.length; i++) {
        if (barrels[i].attached != "yes") {
            console.log(colors[barrels[i].color])
            loadTexture(gl, new Uint8Array(colors[barrels[i].color]));
            const initialMatrix = mat4.clone(modelViewMatrix);
            mat4.translate(modelViewMatrix, modelViewMatrix, [barrels[i].position[0] * 2, -15, barrels[i].position[1] * 2]);
            mat4.scale(modelViewMatrix, modelViewMatrix, [15, 30, 15]);
            gl.uniformMatrix4fv(programInfo.uniformLocations.modelViewMatrix, false, modelViewMatrix);
            gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
            mat4.copy(modelViewMatrix, initialMatrix);
        }
    }
}
function drawSceneForPicking(gl, programInfo, buffers, cameraRotationX, cameraRotationY, zoom, barrels) {
    gl.clearColor(1.0, 1.0, 1.0, 1.0);
    gl.clearDepth(1.0);
    gl.enable(gl.DEPTH_TEST);
    gl.depthFunc(gl.LEQUAL);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    const fieldOfView = (45 * Math.PI) / 180;
    const canvas = gl.canvas;
    const aspect = canvas.clientWidth / canvas.clientHeight;
    const zNear = 0.1;
    const zFar = 1000.0;
    const projectionMatrix = mat4.create();
    mat4.perspective(projectionMatrix, fieldOfView, aspect, zNear, zFar);
    let modelViewMatrix = mat4.create();
    const xpos = -zoom * Math.sin(cameraRotationX) * Math.cos(cameraRotationY);
    const ypos = zoom * Math.sin(cameraRotationY);
    const zpos = zoom * Math.cos(cameraRotationX) * Math.cos(cameraRotationY);
    mat4.lookAt(modelViewMatrix, [xpos, ypos, zpos], [0, 0, 0], [0, 1, 0]);
    gl.useProgram(programInfo.program);
    gl.uniformMatrix4fv(programInfo.uniformLocations.projectionMatrix, false, projectionMatrix);
    gl.disableVertexAttribArray(programInfo.attribLocations.vertexNormal);
    gl.disableVertexAttribArray(programInfo.attribLocations.textureCoord);
    setPositionAttribute(gl, buffers, programInfo);
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buffers.indices);
    const vertexCount = 36;
    const type = gl.UNSIGNED_SHORT;
    const offset = 0;
    for (let i = 0; i < barrels.length; i++) {
        if (barrels[i].attached != "yes") {
            const initialMatrix = mat4.clone(modelViewMatrix);
            loadTexture(gl, new Uint8Array(barrels[i].colorID));
            mat4.translate(modelViewMatrix, modelViewMatrix, [barrels[i].position[0] * 2, -15, barrels[i].position[1] * 2]);
            mat4.scale(modelViewMatrix, modelViewMatrix, [15, 30, 15]);
            gl.uniformMatrix4fv(programInfo.uniformLocations.modelViewMatrix, false, modelViewMatrix);
            gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
            mat4.copy(modelViewMatrix, initialMatrix);
        }
    }
}
function setPositionAttribute(gl, buffers, programInfo) {
    const numComponents = 3;
    const type = gl.FLOAT;
    const normalize = false;
    const stride = 0;
    const offset = 0;
    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.position);
    gl.vertexAttribPointer(programInfo.attribLocations.vertexPosition, numComponents, type, normalize, stride, offset);
    gl.enableVertexAttribArray(programInfo.attribLocations.vertexPosition);
}
function setTextureAttribute(gl, buffers, programInfo) {
    const num = 2;
    const type = gl.FLOAT;
    const normalize = false;
    const stride = 0;
    const offset = 0;
    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.textureCoord);
    gl.vertexAttribPointer(programInfo.attribLocations.textureCoord, num, type, normalize, stride, offset);
    gl.enableVertexAttribArray(programInfo.attribLocations.textureCoord);
}
function setNormalAttribute(gl, buffers, programInfo) {
    const numComponents = 3;
    const type = gl.FLOAT;
    const normalize = false;
    const stride = 0;
    const offset = 0;
    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.normal);
    gl.vertexAttribPointer(programInfo.attribLocations.vertexNormal, numComponents, type, normalize, stride, offset);
    gl.enableVertexAttribArray(programInfo.attribLocations.vertexNormal);
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
export { drawScene, drawSceneForPicking };
