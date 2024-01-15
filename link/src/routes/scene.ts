import * as THREE from 'three';

export default class Sketch {
	container: HTMLDivElement;
	image: HTMLImageElement;
	width: number;
	height: number;

	frustumSize: number;

	scene: THREE.Scene;
	camera: THREE.OrthographicCamera;
	renderer: THREE.Renderer;

	plane: THREE.Mesh;

	constructor(container: HTMLDivElement, image: HTMLImageElement) {
		this.container = container;
		this.image = image;

		this.width = container.offsetWidth;
		this.height = container.offsetHeight;

		this.frustumSize = 3;
		const aspectRatio = this.container.offsetHeight / this.container.offsetWidth;

		this.scene = new THREE.Scene();
		this.camera = new THREE.OrthographicCamera(
			this.frustumSize / -2,
			this.frustumSize / 2,
			(this.frustumSize * aspectRatio) / 2,
			(this.frustumSize * aspectRatio) / -2,
			0.1,
			100
		);
		this.camera.position.z = 1;

		this.renderer = new THREE.WebGLRenderer();
		this.renderer.setSize(container.offsetWidth, container.offsetHeight);
		container.appendChild(this.renderer.domElement);

		const geometry = new THREE.PlaneGeometry(1, 1, 1, 1);
		// const geometry = new THREE.BoxGeometry(1, 1, 1);

		const texture = new THREE.Texture(image);
		texture.needsUpdate = true;
		const material = new THREE.MeshBasicMaterial({ map: texture, side: THREE.DoubleSide });
		this.plane = new THREE.Mesh(geometry, material);
		this.scene.add(this.plane);

		this.camera.position.z = 1;
	}

	animate(time = 0) {
		requestAnimationFrame(this.animate.bind(this));

		// this.plane.rotation.x += 0.01;
		this.plane.rotation.y = (0.5 * time) / 1000;

		this.renderer.render(this.scene, this.camera);
	}
}
