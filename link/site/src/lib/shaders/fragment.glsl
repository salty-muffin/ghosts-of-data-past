uniform sampler2D uTexture;
uniform sampler2D uDataTexture;

varying vec2 vUv;

void main() {
    gl_FragColor = texture(uTexture, vUv);
    // vec4 offset = texture(uDataTexture, vUv);
    // gl_FragColor = offset + vec4(0.5);
}