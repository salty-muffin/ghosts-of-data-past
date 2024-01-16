import * as THREE from 'three';
import fragment from '$lib/shaders/fragment.glsl?raw';
import vertex from '$lib/shaders/vertex.glsl?raw';

export default class Sketch {
	container: HTMLDivElement;
	canvas: HTMLCanvasElement;

	frustumSize: number;

	scene: THREE.Scene;
	camera: THREE.OrthographicCamera;
	renderer: THREE.Renderer;

	plane?: THREE.Mesh;

	grid: number;
	relaxation: number;
	// MOUSE STUFF ---
	radius: number;
	strength: number;
	// MOUSE STUFF ---

	displacementTexture?: THREE.DataTexture;
	texture?: THREE.Texture;
	material?: THREE.ShaderMaterial;

	// MOUSE STUFF ---
	mouse: { x: number; y: number; vX: number; vY: number; prevX: number; prevY: number } = {
		x: 0,
		y: 0,
		vX: 0,
		vY: 0,
		prevX: 0,
		prevY: 0
	};
	// MOUSE STUFF ---

	constructor(container: HTMLDivElement, canvas: HTMLCanvasElement) {
		// settings
		this.grid = 300;
		this.relaxation = 0.98;
		// MOUSE STUFF ---
		this.radius = 0.11;
		this.strength = 0.2;
		// MOUSE STUFF ---

		// store bindings
		this.container = container;
		this.canvas = canvas;

		// set up camera
		this.frustumSize = 3;

		this.scene = new THREE.Scene();
		this.camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
		this.camera.position.z = 1;

		// set up renderer
		this.renderer = new THREE.WebGLRenderer();
		this.renderer.setSize(container.offsetWidth, container.offsetHeight);
		container.appendChild(this.renderer.domElement);

		// set up contents
		this.regenerateGrid();
		this.addObjects();

		// adjust to viewport size
		this.resize();

		// set up event listnener for resize
		window.addEventListener('resize', this.resize.bind(this));

		// MOUSE STUFF ---
		window.addEventListener('mousemove', (e) => {
			this.mouse.x = e.clientX / this.container.offsetWidth;
			this.mouse.y = e.clientY / this.container.offsetHeight;

			// console.log(this.mouse.x,this.mouse.y)

			this.mouse.vX = this.mouse.x - this.mouse.prevX;
			this.mouse.vY = this.mouse.y - this.mouse.prevY;

			this.mouse.prevX = this.mouse.x;
			this.mouse.prevY = this.mouse.y;
		});
		// MOUSE STUFF ---
	}

	regenerateGrid() {
		const width = this.grid;
		const height = this.grid;

		const size = width * height;
		const data = new Float32Array(4 * size);

		for (let i = 0; i < size; i++) {
			const r = Math.random() * 2 - 1;
			const g = Math.random() * 2 - 1;

			const stride = i * 4;

			data[stride] = r;
			data[stride + 1] = g;
			data[stride + 2] = 0;
			data[stride + 3] = 1;
		}

		// used the buffer to create a DataTexture

		this.displacementTexture = new THREE.DataTexture(
			data,
			width,
			height,
			THREE.RGBAFormat,
			THREE.FloatType
		);
		this.displacementTexture.magFilter = THREE.NearestFilter;
		this.displacementTexture.needsUpdate = true;

		this.displacementTexture.magFilter = this.displacementTexture.minFilter = THREE.NearestFilter;

		if (this.material) {
			this.material.uniforms.uDataTexture.value = this.displacementTexture;
			this.material.uniforms.uDataTexture.value.needsUpdate = true;
		}
	}

	addObjects() {
		const geometry = new THREE.PlaneGeometry(2, 2);

		this.texture = new THREE.Texture(this.canvas);
		this.texture.needsUpdate = true;
		this.material = new THREE.ShaderMaterial({
			extensions: { derivatives: true },
			side: THREE.DoubleSide,
			uniforms: {
				time: {
					value: 0
				},
				resolution: {
					value: new THREE.Vector4()
				},
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

	updateCanavas() {
		if (this.texture && this.material) {
			this.texture = new THREE.Texture(this.canvas);
			this.material.uniforms.uTexture.value = this.texture;
			this.texture.needsUpdate = true;
		}
	}

	animate() {
		requestAnimationFrame(this.animate.bind(this));

		if (this.displacementTexture) {
			const data = this.displacementTexture.image.data;
			for (let i = 0; i < data.length; i += 4) {
				data[i] *= this.relaxation;
				data[i + 1] *= this.relaxation;
			}

			// MOUSE STUFF ---
			const gridMouseX = this.grid * this.mouse.x;
			const gridMouseY = this.grid * (1 - this.mouse.y);
			const maxDist = this.grid * this.radius;
			const aspect = this.container.offsetHeight / this.container.offsetWidth;

			for (let i = 0; i < this.grid; i++) {
				for (let j = 0; j < this.grid; j++) {
					const distance = (gridMouseX - i) ** 2 / aspect + (gridMouseY - j) ** 2;
					const maxDistSq = maxDist ** 2;

					if (distance < maxDistSq) {
						const index = 4 * (i + this.grid * j);

						let power = maxDist / Math.sqrt(distance);
						power = Math.max(0, Math.min(power, 10));
						// if(distance <this.grid/32) power = 1;
						// power = 1;

						data[index] -= this.strength * this.mouse.vX * power;
						data[index + 1] += this.strength * this.mouse.vY * power;
					}
				}
			}

			this.mouse.vX *= 0.9;
			this.mouse.vY *= 0.9;
			// MOUSE STUFF ---

			this.displacementTexture.needsUpdate = true;
		}

		this.renderer.render(this.scene, this.camera);
	}

	resize() {
		this.updateCanavas();
		this.regenerateGrid();

		this.renderer.setSize(this.container.offsetWidth, this.container.offsetHeight);
	}
}
