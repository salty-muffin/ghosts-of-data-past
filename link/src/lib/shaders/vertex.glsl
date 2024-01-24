uniform sampler2D uDataTexture;
uniform float uScaler;

varying vec2 vUv;

void main() {
    vUv = uv;

    vec4 offset = texture(uDataTexture, vUv);
    vec4 mappedOffset = vec4(2) * vec4(uScaler) * (offset - 0.5);

    gl_Position = projectionMatrix * modelViewMatrix * (vec4(position, 1.0) - vec4(mappedOffset.xy, 0, 0));
}