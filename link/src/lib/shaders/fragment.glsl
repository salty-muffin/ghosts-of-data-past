uniform sampler2D uDataTexture;
uniform sampler2D uTexture;

varying vec2 vUv;

void main() {
    vec4 offset = texture(uDataTexture, vUv);
    gl_FragColor = texture(uTexture, vUv + offset.rg);
    // gl_FragColor = offset;
}