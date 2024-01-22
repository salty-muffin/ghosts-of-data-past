import * as THREE from 'three';
import fragment from '$lib/shaders/fragment.glsl?raw';
import vertex from '$lib/shaders/vertex.glsl?raw';

import { timestamp } from '$lib/stores/timestamp';
import { get } from 'svelte/store';

const clamp = (n: number, min: number, max: number) => {
	return Math.max(min, Math.min(n, max));
};

export default class Sketch {
	container: HTMLDivElement;
	canvas: HTMLCanvasElement;

	scene: THREE.Scene;
	camera: THREE.OrthographicCamera;
	renderer: THREE.Renderer;

	clock: THREE.Clock;
	delta = 0;
	interval = 1 / 60;

	elapsedTime: THREE.Clock;
	maxRecordingTime = 5;
	playing = false;

	plane?: THREE.Mesh;

	resolution = { x: 0, y: 0 };

	gridX = 320;
	gridY = 0;
	relaxation = 0.985;
	radius = 0.3;
	strength = 0.1;

	mouseDown = false;

	displacementTexture?: THREE.DataTexture;
	texture?: THREE.Texture;
	material?: THREE.ShaderMaterial;

	displacementTextureBuffer = new Float32Array([]);
	frameSize = 0;
	frameIndex = 0;

	mouse = {
		x: 0,
		y: 0,
		vX: 0,
		vY: 0,
		prevX: 0,
		prevY: 0
	};

	constructor(container: HTMLDivElement, canvas: HTMLCanvasElement) {
		// store bindings
		this.container = container;
		this.canvas = canvas;

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

		this.elapsedTime = new THREE.Clock(false);

		// adjust to viewport size
		this.resize();

		// set up contents
		this.regenerateGrid();
		this.addObjects();

		// set up event listnener for resize
		window.addEventListener('resize', this.resize.bind(this));

		// set up mouse event listeners
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

			this.mouse.vX = this.mouseDown ? this.mouse.x - this.mouse.prevX : 0;
			this.mouse.vY = this.mouseDown ? this.mouse.y - this.mouse.prevY : 0;

			this.mouse.prevX = this.mouse.x;
			this.mouse.prevY = this.mouse.y;
		});
	}

	startRecording() {
		if (!get(timestamp).recording) {
			console.log('starting recording');

			timestamp.start();
			this.elapsedTime.start();
			this.frameIndex = 0;

			this.playing = false;
		}
	}

	stopRecording() {
		if (get(timestamp).recording) {
			console.log('stopping recording');

			timestamp.stop();
			this.elapsedTime.stop();
		}
	}

	play() {
		if (!get(timestamp).recording && !this.playing) {
			console.log('playing');

			this.elapsedTime.start();

			this.playing = true;
			this.frameIndex = 0;
		}
	}

	stop() {
		if (this.playing) {
			console.log('stopping');

			this.elapsedTime.stop();

			this.playing = false;
		}
	}

	regenerateGrid() {
		this.gridX = Math.floor(this.gridX);
		this.gridY = Math.ceil(this.gridX * (this.resolution.y / this.resolution.x));

		// buffer for the dispacement texture
		const size = this.gridX * this.gridY;
		const data = new Float32Array(2 * size);

		for (let i = 0; i < size; i++) {
			// const r = Math.random();
			// const g = Math.random();
			const r = 0;
			const g = 0;

			const stride = i * 2;

			data[stride] = r;
			data[stride + 1] = g;
		}

		// use the buffer to create a DataTexture
		this.displacementTexture = new THREE.DataTexture(
			data,
			this.gridX,
			this.gridY,
			THREE.RGFormat,
			THREE.FloatType
		);
		this.displacementTexture.magFilter = THREE.NearestFilter;
		this.displacementTexture.needsUpdate = true;

		this.displacementTexture.magFilter = this.displacementTexture.minFilter = THREE.NearestFilter;

		if (this.material) {
			this.material.uniforms.uDataTexture.value = this.displacementTexture;
			this.material.uniforms.uDataTexture.value.needsUpdate = true;
		}

		// set up buffer for recording
		timestamp.stop();

		this.frameSize = this.displacementTexture.image.data.length;
		this.displacementTextureBuffer = new Float32Array(
			this.frameSize * (1 / this.interval) * this.maxRecordingTime
		);
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
				},
				uResolution: {
					value: [this.resolution.x, this.resolution.y]
				},
				uBlur: {
					value: true
				},
				uBlurRadius: {
					value: 10
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

		this.delta += this.clock.getDelta();

		if (this.delta > this.interval) {
			if (this.displacementTexture) {
				const data = this.displacementTexture.image.data;

				if (!this.playing) {
					for (let i = 0; i < data.length; i += 2) {
						data[i] = data[i] * this.relaxation;
						data[i + 1] = data[i + 1] * this.relaxation;
					}

					const gridMouseX = this.gridX * this.mouse.x;
					const gridMouseY = this.gridY * (1 - this.mouse.y);
					const maxDist = this.gridX * this.radius;

					for (let i = 0; i < this.gridX; i++) {
						for (let j = 0; j < this.gridY; j++) {
							const distance = (gridMouseX - i) ** 2 / 1 + (gridMouseY - j) ** 2;
							const maxDistSq = maxDist ** 2;

							if (distance < maxDistSq) {
								const index = 2 * (i + this.gridX * j);

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

					// if recording, save this frame into the buffer
					if (get(timestamp).recording) {
						const elapsedTime = this.elapsedTime.getElapsedTime();
						timestamp.setTime(Math.floor(elapsedTime));
						if ((this.frameIndex + 1) * this.frameSize < this.displacementTextureBuffer.length) {
							this.displacementTextureBuffer.set(data, this.frameIndex * this.frameSize);
							this.frameIndex++;
						} else {
							this.stopRecording();
						}
					}
				} else {
					timestamp.setTime(Math.floor(this.elapsedTime.getElapsedTime()));

					// if playing, get frame from the buffer
					this.displacementTexture.image.data.set(
						this.displacementTextureBuffer.subarray(
							this.frameIndex * this.frameSize,
							(this.frameIndex + 1) * this.frameSize
						)
					);

					// console.log(
					// 	this.displacementTexture.image.data.length,
					// 	this.displacementTextureBuffer.subarray(
					// 		this.frameIndex * this.frameSize,
					// 		(this.frameIndex + 1) * this.frameSize
					// 	).length
					// );

					this.frameIndex++;

					if ((this.frameIndex + 1) * this.frameSize >= this.displacementTextureBuffer.length) {
						this.stop();
					}
				}

				this.displacementTexture.needsUpdate = true;
			}

			this.renderer.render(this.scene, this.camera);

			this.delta = this.delta % this.interval;
		}
	}

	resize() {
		this.updateCanavas();
		this.regenerateGrid();

		this.resolution = { x: this.container.offsetWidth, y: this.container.offsetHeight };

		this.renderer.setSize(this.resolution.x, this.resolution.y);
	}
}
