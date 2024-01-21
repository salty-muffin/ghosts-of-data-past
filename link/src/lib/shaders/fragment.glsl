uniform sampler2D uDataTexture;
uniform sampler2D uTexture;

uniform vec2 uResolution;
uniform bool uBlur;
uniform int uBlurRadius;

varying vec2 vUv;

void main() {
    vec4 offset;
    if(uBlur) {
        vec2 step = vec2(1) / uResolution;
        offset = vec4(0);
        int min = -(uBlurRadius - 1) / 2;
        int max = (uBlurRadius - uBlurRadius % 2) / 2;
        for(int i = min; i <= max; i++) {
            for(int j = min; j <= max; j++) {
                offset += texture(uDataTexture, vUv + step * vec2(i, j));
            }
        }
        offset /= vec4(uBlurRadius * uBlurRadius);
    } else {
        offset = texture(uDataTexture, vUv);
    }
    gl_FragColor = texture(uTexture, vUv + offset.rg);
    gl_FragColor = offset + vec4(0.5);
}