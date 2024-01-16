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

	size?: number;
	displacementTexture?: THREE.DataTexture;
	texture?: THREE.Texture;
	material?: THREE.ShaderMaterial;

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

		// set up contents
		this.addObjects();

		// adjust to viewport size
		this.resize();

		// set up event listnener for resize
		window.addEventListener('resize', this.resize.bind(this));
	}

	regenerateGrid() {
		this.size = 300;

		const width = this.size;
		const height = this.size;

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
		this.displacementTexture.needsUpdate = true;

		this.displacementTexture.magFilter = this.displacementTexture.minFilter = THREE.NearestFilter;

		if (this.material) {
			this.material.uniforms.uDataTexture.value = this.displacementTexture;
			this.material.uniforms.uDataTexture.value.needsUpdate = true;
		}
	}

	addObjects() {
		this.regenerateGrid();

		const geometry = new THREE.PlaneGeometry(2, 2);

		this.texture = new THREE.Texture(this.canvas);
		this.texture.needsUpdate = true;
		// this.material = new THREE.MeshBasicMaterial({
		// 	map: texture,
		// 	side: THREE.DoubleSide
		// });
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

	animate(time = 0) {
		requestAnimationFrame(this.animate.bind(this));

		// this.plane.rotation.x += 0.01;
		// this.plane.rotation.y = (0.5 * time) / 1000;

		if (this.displacementTexture) {
			const data = this.displacementTexture.image.data;
			for (let i = 0; i < data.length; i += 4) {
				data[i] *= 0.99;
				data[i + 1] *= 0.99;
			}
			this.displacementTexture.needsUpdate = true;
		}

		this.renderer.render(this.scene, this.camera);
	}

	resize() {
		// const width = this.container.offsetHeight;
		// const height = this.container.offsetWidth;
		// const aspectRatio = width / height;

		// this.camera.left = this.frustumSize / -2;
		// this.camera.right = this.frustumSize / 2;
		// this.camera.top = (this.frustumSize * aspectRatio) / 2;
		// this.camera.bottom = (this.frustumSize * aspectRatio) / -2;

		// this.camera.updateProjectionMatrix();

		this.updateCanavas();

		this.renderer.setSize(this.container.offsetWidth, this.container.offsetHeight);
	}
}
