import * as THREE from 'three';
import fragment from '$lib/shaders/fragment.glsl?raw';
import vertex from '$lib/shaders/vertex.glsl?raw';

const clamp = (n: number, min: number, max: number) => {
	return Math.max(min, Math.min(n, max));
};

export default class Sketch {
	container: HTMLDivElement;
	canvas: HTMLCanvasElement;

	frustumSize: number;

	scene: THREE.Scene;
	camera: THREE.OrthographicCamera;
	renderer: THREE.Renderer;

	plane?: THREE.Mesh;

	resolution = { x: 0, y: 0 };

	gridX = 320;
	gridY = 0;
	relaxation = 0.985;
	// MOUSE STUFF ---
	radius = 0.2;
	strength = 0.1;

	mouseDown = false;
	// MOUSE STUFF ---

	displacementTexture?: THREE.DataTexture;
	texture?: THREE.Texture;
	material?: THREE.ShaderMaterial;

	// MOUSE STUFF ---
	mouse = {
		x: 0,
		y: 0,
		vX: 0,
		vY: 0,
		prevX: 0,
		prevY: 0
	};
	// MOUSE STUFF ---

	constructor(container: HTMLDivElement, canvas: HTMLCanvasElement) {
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

		// adjust to viewport size
		this.resize();

		// set up contents
		this.regenerateGrid();
		this.addObjects();

		// set up event listnener for resize
		window.addEventListener('resize', this.resize.bind(this));

		// MOUSE STUFF ---
		window.addEventListener('mousedown', (e) => {
			if (e.button == 0) {
				this.mouseDown = true;
			}
		});
		window.addEventListener('mouseup', (e) => {
			if (e.button == 0) {
				this.mouseDown = false;
			}
		});
		window.addEventListener('mousemove', (e) => {
			this.mouse.x = e.clientX / this.resolution.x;
			this.mouse.y = e.clientY / this.resolution.y;

			// console.log(this.mouse.x,this.mouse.y)

			this.mouse.vX = this.mouseDown ? this.mouse.x - this.mouse.prevX : 0;
			this.mouse.vY = this.mouseDown ? this.mouse.y - this.mouse.prevY : 0;

			this.mouse.prevX = this.mouse.x;
			this.mouse.prevY = this.mouse.y;
		});
		// MOUSE STUFF ---
	}

	regenerateGrid() {
		this.gridY = this.gridX * (this.resolution.y / this.resolution.x);

		// buffer for the dispacement texture
		const size = this.gridX * this.gridY;
		const data = new Float32Array(4 * size);

		for (let i = 0; i < size; i++) {
			// const r = Math.random();
			// const g = Math.random();
			const r = 0.5;
			const g = 0.5;

			const stride = i * 4;

			data[stride] = r;
			data[stride + 1] = g;
			data[stride + 2] = 0.5;
			data[stride + 3] = 1;
		}

		// use the buffer to create a DataTexture
		this.displacementTexture = new THREE.DataTexture(
			data,
			this.gridX,
			this.gridY,
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
				data[i] = (data[i] - 0.5) * this.relaxation + 0.5;
				data[i + 1] = (data[i + 1] - 0.5) * this.relaxation + 0.5;
			}

			// MOUSE STUFF ---
			const gridMouseX = this.gridX * this.mouse.x;
			const gridMouseY = this.gridY * (1 - this.mouse.y);
			const maxDist = this.gridX * this.radius;

			for (let i = 0; i < this.gridX; i++) {
				for (let j = 0; j < this.gridY; j++) {
					const distance = (gridMouseX - i) ** 2 / 1 + (gridMouseY - j) ** 2;
					const maxDistSq = maxDist ** 2;

					if (distance < maxDistSq) {
						const index = 4 * (i + this.gridX * j);

						let power = maxDist / Math.sqrt(distance) - 1;
						power = clamp(power, 0, 10);
						// if(distance <this.size/32) power = 1;
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

		this.resolution = { x: this.container.offsetWidth, y: this.container.offsetHeight };

		this.renderer.setSize(this.resolution.x, this.resolution.y);
	}
}
