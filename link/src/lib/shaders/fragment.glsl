uniform sampler2D uTexture;

varying vec2 vUv;

void main() {
    gl_FragColor = texture(uTexture, vUv);
    // gl_FragColor = offset;
}