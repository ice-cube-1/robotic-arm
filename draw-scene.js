function drawScene(gl, programInfo, buffers, cameraRotationX, cameraRotationY, positions, zoom) {
    var xpos =-zoom * Math.sin(cameraRotationX) * Math.cos(cameraRotationY);
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
    const zFar = 1000.0;
    const projectionMatrix = mat4.create();
    mat4.perspective(projectionMatrix, fieldOfView, aspect, zNear, zFar);
    var modelViewMatrix = mat4.create();
    mat4.lookAt(modelViewMatrix, [xpos,ypos,zpos], [0,positions[0][3]*2,0], [0,1,0]);
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
    const vertexCount = 36
    const type = gl.UNSIGNED_SHORT;
    const offset = 0;
    for (let i = 0; i < positions.length; i++) {
        const initialMatrix = mat4.clone(modelViewMatrix);
        mat4.translate(modelViewMatrix, modelViewMatrix, [positions[i][0]*2,positions[i][1]*2,0]);
        mat4.rotate(modelViewMatrix, modelViewMatrix, ((0 * Math.PI) / 180)+positions[i][2], [0,0,1])
        mat4.scale(modelViewMatrix,modelViewMatrix, [5, positions[i][3], 5])
        gl.uniformMatrix4fv(programInfo.uniformLocations.modelViewMatrix, false, modelViewMatrix);
        gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
        mat4.copy(modelViewMatrix, initialMatrix);
    }
}
function setPositionAttribute(gl, buffers, programInfo) {
    const numComponents = 3;
    const type = gl.FLOAT;
    const normalize = false;
    const stride = 0;
    const offset = 0;
    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.position);
    gl.vertexAttribPointer(
        programInfo.attribLocations.vertexPosition,
        numComponents,
        type,
        normalize,
        stride,
        offset,
      );
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
    gl.enableVertexAttribArray(programInfo.attribLocations.textureCoord)
}

function setNormalAttribute(gl, buffers, programInfo) {
    const numComponents = 3;
    const type = gl.FLOAT;
    const normalize = false;
    const stride = 0;
    const offset = 0;
    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.normal);
    gl.vertexAttribPointer(programInfo.attribLocations.vertexNormal, numComponents, type, normalize, stride, offset,);
    gl.enableVertexAttribArray(programInfo.attribLocations.vertexNormal);
}

export { drawScene };