<script lang="ts">
	interface Image {
		width: number;
		height: number;
		src: string;
	}

	let className = '';
	export { className as class };
	export let style = '';
	export let webpSrcset = '';
	export let jpgSrcset: string;
	export let placeholder: Image;
	export let alt: string;
</script>

<div class="image {className}" {style}>
	<picture>
		{#if webpSrcset}
			<source srcset={webpSrcset} type="image/webp" />
		{/if}
		<source srcset={jpgSrcset} type="image/jpeg" />
		<img src={placeholder.src} width={placeholder.width} height={placeholder.height} {alt} />
	</picture>
</div>

<style global lang="scss">
	.image img {
		display: block;
		width: 100%;
		height: auto;
	}
</style>
