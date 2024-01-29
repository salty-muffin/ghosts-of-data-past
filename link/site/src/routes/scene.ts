import * as THREE from 'three';
import fragment from '$lib/shaders/fragment.glsl?raw';
import vertex from '$lib/shaders/vertex.glsl?raw';

export default class Sketch {
	container: HTMLDivElement;
	canvas: HTMLCanvasElement;

	dataURL: string;

	scene: THREE.Scene;
	camera: THREE.OrthographicCamera;
	renderer: THREE.Renderer;

	interval: number;
	clock: THREE.Clock;
	delta = 0;

	plane?: THREE.Mesh;
	geometry?: THREE.PlaneGeometry;

	gridX = 0;
	gridY = 0;

	mouseDown = false;

	displacementTexture?: THREE.DataTexture;
	displacementData?: Float32Array;
	texture?: THREE.Texture;
	material?: THREE.ShaderMaterial;

	displacementTextureBuffer = new Float32Array([]);
	frameSize = 0;
	frameIndex = 0;
	frameCount = 0;

	constructor(
		container: HTMLDivElement,
		canvas: HTMLCanvasElement,
		dataURL: string,
		framerate = 60
	) {
		// store bindings
		this.container = container;
		this.canvas = canvas;
		this.dataURL = dataURL;
		this.interval = 1 / framerate;

		// set up camera
		this.scene = new THREE.Scene();
		this.camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
		this.camera.position.z = 1;

		// set up renderer
		this.renderer = new THREE.WebGLRenderer();
		this.renderer.setSize(container.offsetWidth, container.offsetHeight);
		container.appendChild(this.renderer.domElement);

		// set up time keeping
		this.clock = new THREE.Clock();

		// load the displacemt data
		fetch(this.dataURL).then((response) => {
			response.arrayBuffer().then((data) => {
				// buffer for the dispacement data
				this.displacementTextureBuffer = new Float32Array(data);

				this.gridX = this.displacementTextureBuffer[0];
				this.gridY = this.displacementTextureBuffer[1];

				this.frameSize = this.gridX * this.gridY * 2;

				this.frameCount = (this.displacementTextureBuffer.length - 2) / this.frameSize;

				const frame = this.displacementTextureBuffer.subarray(2, 2 + this.frameSize);
				// use the buffer to create a DataTexture
				this.displacementTexture = new THREE.DataTexture(
					frame,
					this.gridX,
					this.gridY,
					THREE.RGFormat,
					THREE.FloatType
				);
				this.displacementTexture.magFilter = THREE.NearestFilter;
				this.displacementTexture.needsUpdate = true;

				// adjust to viewport size
				this.resize();

				// set up contents
				this.addObjects();

				// set up event listnener for resize
				window.addEventListener('resize', this.resize.bind(this));
			});
		});
	}

	addObjects() {
		const geometry = new THREE.PlaneGeometry(2, 2, this.gridX, this.gridY);

		this.texture = new THREE.Texture(this.canvas);
		this.texture.needsUpdate = true;
		this.material = new THREE.ShaderMaterial({
			extensions: { derivatives: true },
			side: THREE.DoubleSide,
			uniforms: {
				uTexture: {
					value: this.texture
				},
				uDataTexture: {
					value: this.displacementTexture
				}
			},
			vertexShader: vertex,
			fragmentShader: fragment
		});
		this.plane = new THREE.Mesh(geometry, this.material);
		this.scene.add(this.plane);
	}

	updateCanvas() {
		if (this.texture && this.material) {
			this.texture = new THREE.Texture(this.canvas);
			this.material.uniforms.uTexture.value = this.texture;
			this.texture.needsUpdate = true;

			this.frameIndex = 0;
		}
	}

	animate() {
		requestAnimationFrame(this.animate.bind(this));

		this.delta += this.clock.getDelta();

		if (this.delta > this.interval) {
			if (this.displacementTexture && this.frameCount) {
				// if playing, get frame from the buffer
				this.displacementTexture.image.data.set(
					this.displacementTextureBuffer.subarray(
						2 + this.frameIndex * this.frameSize,
						2 + (this.frameIndex + 1) * this.frameSize
					)
				);
				this.displacementTexture.needsUpdate = true;

				this.frameIndex++;
				if (this.frameIndex >= this.frameCount) {
					this.frameIndex = 0;
					this.updateCanvas();
				}
			}

			this.renderer.render(this.scene, this.camera);

			this.delta = this.delta % this.interval;
		}
	}

	resize() {
		this.updateCanvas();

		this.renderer.setSize(this.container.offsetWidth, this.container.offsetHeight);
	}
}
