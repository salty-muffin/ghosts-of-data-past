uniform sampler2D uDataTexture;
uniform sampler2D uTexture;

varying vec2 vUv;

void main() {
    vec4 offset = texture(uDataTexture, vUv);
    vec4 mappedOffset = vec4(2) * (offset - 0.5);
    gl_FragColor = texture(uTexture, vUv + mappedOffset.rg);
    // gl_FragColor = offset;
}