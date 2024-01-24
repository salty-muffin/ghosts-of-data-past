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
	maxRecordingTime: number;
	playing = false;

	plane?: THREE.Mesh;
	geometry?: THREE.PlaneGeometry;

	gridDivider = 16;
	gridX = 0;
	gridY = 0;
	relaxation = 0.995;
	radius = 0.3;
	strength = 0.1;

	mouseDown = false;

	displacementTexture?: THREE.DataTexture;
	displacementData?: Float32Array;
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

	constructor(container: HTMLDivElement, canvas: HTMLCanvasElement, recordingLength = 10) {
		// store bindings
		this.container = container;
		this.canvas = canvas;

		this.maxRecordingTime = recordingLength;

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
			this.mouse.x = e.clientX / this.container.offsetWidth;
			this.mouse.y = e.clientY / this.container.offsetHeight;

			this.mouse.vX = this.mouseDown ? this.mouse.x - this.mouse.prevX : 0;
			this.mouse.vY = this.mouseDown ? this.mouse.y - this.mouse.prevY : 0;

			this.mouse.prevX = this.mouse.x;
			this.mouse.prevY = this.mouse.y;
		});
	}

	setParameters(relaxation: number, radius: number, strength: number) {
		this.relaxation = relaxation;
		this.radius = radius;
		this.strength = strength;
	}

	startRecording() {
		if (!get(timestamp).recording) {
			console.log('starting recording');

			timestamp.start();
			this.elapsedTime.start();
			this.frameIndex = 0;

			this.playing = false;

			if (this.displacementData) {
				this.displacementData.fill(0.0);
			}
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
		this.gridX = Math.floor(this.container.offsetWidth / this.gridDivider);
		this.gridY = Math.floor(this.container.offsetHeight / this.gridDivider);

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
		this.displacementData = data.slice();

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
			2 + this.frameSize * (1 / this.interval) * this.maxRecordingTime
		);

		this.resetRecording();
	}

	resetRecording() {
		console.log('resetting');

		this.stopRecording();
		this.stop();

		this.displacementTextureBuffer.fill(0.0);
		if (this.displacementTexture) {
			this.displacementTexture.image.data.fill(0.0);
		}
		if (this.displacementData) {
			this.displacementData.fill(0.0);
		}

		this.displacementTextureBuffer[0] = this.gridX;
		this.displacementTextureBuffer[1] = this.gridY;
	}

	getDisplacementBuffer() {
		return this.displacementTextureBuffer;
	}

	addObjects() {
		if (this.geometry) {
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
			if (this.displacementTexture && this.displacementData) {
				const data = this.displacementTexture.image.data;

				if (!this.playing) {
					for (let i = 0; i < data.length; i += 2) {
						this.displacementData[i] = this.displacementData[i] * this.relaxation;
						this.displacementData[i + 1] = this.displacementData[i + 1] * this.relaxation;
					}

					const gridMouseX = this.gridX * this.mouse.x;
					const gridMouseY = this.gridY * (1 - this.mouse.y);
					const maxDist = this.gridX * this.radius;

					for (let i = 0; i < this.gridX; i++) {
						for (let j = 0; j < this.gridY; j++) {
							const distanceSq = (gridMouseX - i) ** 2 / 1 + (gridMouseY - j) ** 2;
							const maxDistSq = maxDist ** 2;

							if (distanceSq < maxDistSq) {
								const index = 2 * (i + this.gridX * j);

								let power =
									((maxDistSq - distanceSq) / maxDistSq) * ((maxDistSq - distanceSq) / maxDistSq);
								power = clamp(power, 0, 10);
								// if(distance <this.size/32) power = 1;
								// power = 1;

								this.displacementData[index] -= this.strength * this.mouse.vX * power;
								this.displacementData[index + 1] += this.strength * this.mouse.vY * power;
							}
						}
					}

					this.mouse.vX *= 0.9;
					this.mouse.vY *= 0.9;

					// if recording, save this frame into the buffer
					if (get(timestamp).recording) {
						const elapsedTime = this.elapsedTime.getElapsedTime();
						timestamp.setTime(Math.floor(elapsedTime));

						if (
							(this.frameIndex + 1) * this.frameSize <
							this.displacementTextureBuffer.length - 2
						) {
							for (let i = 0; i < data.length; i++) {
								data[i] =
									this.displacementData[i] +
									this.displacementTextureBuffer[i + 2 + this.frameIndex * this.frameSize];
							}
							this.displacementTextureBuffer.set(data, 2 + this.frameIndex * this.frameSize);

							this.frameIndex++;
						} else {
							this.stopRecording();
						}
					}
				} else {
					// if playing, get frame from the buffer
					timestamp.setTime(Math.floor(this.elapsedTime.getElapsedTime()));

					if ((this.frameIndex + 1) * this.frameSize < this.displacementTextureBuffer.length - 2) {
						this.displacementTexture.image.data.set(
							this.displacementTextureBuffer.subarray(
								2 + this.frameIndex * this.frameSize,
								2 + (this.frameIndex + 1) * this.frameSize
							)
						);
						this.frameIndex++;
					} else {
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

		const width = this.container.offsetWidth;
		const height = this.container.offsetHeight;
		if (this.geometry) {
			this.geometry.dispose();
		}
		this.geometry = new THREE.PlaneGeometry(
			2,
			2,
			Math.floor(width / this.gridDivider),
			Math.floor(height / this.gridDivider)
		);

		this.renderer.setSize(width, height);
	}
}
