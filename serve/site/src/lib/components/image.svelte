<script lang="ts">
	import { onMount } from 'svelte';

	interface Size {
		width: number;
		maxWidth?: number;
	}
	interface Image {
		srcset: string;
		type: string;
		sizes: string;
	}

	export let image: string;
	export let alt: string;
	export let loading: 'eager' | 'lazy' | null | undefined = 'eager';
	export let sizes: Size[]; // smallest size should come first, last size will be without maxWidth
	export let width: number;
	export let height: number;
	export let aspectRatio: number | undefined = undefined;
	export let query: string | undefined = undefined;
	export let formats = ['avif', 'webp', 'jpg']; // fallback should come last
	export let quality = 80;
	let className = '';
	export { className as class };

	let images: Image[] = [];
	// create a srcset, type & sizes for each format
	let sizes_ = '';
	sizes.forEach((size, index) => {
		if (index < sizes.length - 1) sizes_ += `(max-width: ${size.maxWidth}px) ${size.width}px, `;
		else sizes_ += `${size.width}px`;
	});
	formats.forEach((format) => {
		let srcset = '';
		sizes.forEach((size, index) => {
			srcset += `${image}@w=${size.width}+${aspectRatio ? `h=${size.width / aspectRatio}+` : ''}${
				query ? `${query}+` : ''
			}fm=${format}+q=${quality}.${format} ${size.width}w`;
			if (index < sizes.length - 1) srcset += ', ';
		});

		let type = '';
		switch (format) {
			case 'jpg':
				type = 'image/jpeg';
				break;
			case 'png':
				type = 'image/png';
				break;
			case 'webp':
				type = 'image/webp';
				break;
			case 'gif':
				type = 'image/gif';
				break;
			case 'avif':
				type = 'image/avif';
				break;
		}
		images.push({ srcset: srcset, type: type, sizes: sizes_ });
	});

	let element: HTMLImageElement;
	let loaded = false;
	onMount(() => {
		if (element.complete) {
			loaded = true;
		}
	});
</script>

<picture>
	{#each images as image}
		<source srcset={image.srcset} sizes={image.sizes} type={image.type} />
	{/each}
	<img
		class="image-component {className}"
		class:loaded
		{loading}
		src="{image}@w={sizes[sizes.length - 1].width}+{aspectRatio
			? `h=${sizes[sizes.length - 1].width / aspectRatio}+`
			: ''}{query ? `${query}+` : ''}fm={formats[formats.length - 1]}+q={quality}.{formats[
			formats.length - 1
		]}"
		{alt}
		{width}
		height={aspectRatio ? width / aspectRatio : height}
		on:load={() => {
			loaded = true;
		}}
		bind:this={element}
	/>
</picture>

<style global>
	.image-component {
		display: block;
		width: 100%;
		height: auto;
	}
</style>
