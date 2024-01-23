uniform sampler2D uDataTexture;

varying vec2 vUv;

void main() {
    vUv = uv;

    vec4 offset = texture(uDataTexture, vUv);

    gl_Position = projectionMatrix * modelViewMatrix * (vec4(position, 1.0) - vec4(offset.xy, 0, 0));
}