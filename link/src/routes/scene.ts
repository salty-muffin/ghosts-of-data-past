import * as THREE from 'three';
import fragment from '$lib/shaders/fragment.glsl?raw';
import vertex from '$lib/shaders/vertex.glsl?raw';

export default class Sketch {
	container: HTMLDivElement;
	canvas: HTMLCanvasElement;
	displacementVideo: HTMLVideoElement;

	frustumSize: number;

	scene: THREE.Scene;
	camera: THREE.OrthographicCamera;
	renderer: THREE.Renderer;

	clock: THREE.Clock;
	delta = 0;
	interval = 1 / 30;

	gridDivider = 8;

	plane?: THREE.Mesh;
	geometry?: THREE.PlaneGeometry;

	displacementTexture?: THREE.VideoTexture;
	texture?: THREE.Texture;
	material?: THREE.ShaderMaterial;

	constructor(
		container: HTMLDivElement,
		canvas: HTMLCanvasElement,
		displacement: HTMLVideoElement
	) {
		// store bindings
		this.container = container;
		this.canvas = canvas;
		this.displacementVideo = displacement;

		// set up camera
		this.frustumSize = 3;

		this.scene = new THREE.Scene();
		this.camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
		this.camera.position.z = 1;

		// set up renderer
		this.renderer = new THREE.WebGLRenderer();
		this.renderer.setSize(container.offsetWidth, container.offsetHeight);
		container.appendChild(this.renderer.domElement);

		this.clock = new THREE.Clock();

		// adjust to viewport size
		this.resize();

		// set up contents
		this.addObjects();

		// set up event listnener for resize
		window.addEventListener('resize', this.resize.bind(this));
	}

	addObjects() {
		if (this.geometry) {
			this.texture = new THREE.Texture(this.canvas);
			this.texture.needsUpdate = true;

			this.displacementTexture = new THREE.VideoTexture(this.displacementVideo);
			this.material = new THREE.ShaderMaterial({
				extensions: { derivatives: true },
				side: THREE.DoubleSide,
				uniforms: {
					uTexture: {
						value: this.texture
					},
					uDataTexture: {
						value: this.displacementTexture
					},
					uScaler: {
						value: 1
					}
				},
				vertexShader: vertex,
				fragmentShader: fragment
			});

			this.plane = new THREE.Mesh(this.geometry, this.material);
			this.scene.add(this.plane);
		}
	}

	updateCanavas() {
		if (this.texture && this.material) {
			this.texture = new THREE.Texture(this.canvas);
			this.material.uniforms.uTexture.value = this.texture;
			this.texture.needsUpdate = true;
		}
	}

	animate() {
		requestAnimationFrame(this.animate.bind(this));

		this.delta += this.clock.getDelta();

		if (this.delta > this.interval) {
			this.renderer.render(this.scene, this.camera);

			this.delta = this.delta % this.interval;
		}
	}

	resize() {
		const width = this.container.offsetWidth;
		const height = this.container.offsetHeight;
		this.geometry = new THREE.PlaneGeometry(
			2,
			2,
			Math.floor(width / this.gridDivider),
			Math.floor(height / this.gridDivider)
		);

		this.renderer.setSize(width, height);
	}
}
