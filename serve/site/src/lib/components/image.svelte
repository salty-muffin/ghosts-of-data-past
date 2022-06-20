<script lang="ts">
	interface Image {
		width: number;
		height: number;
		src: string;
	}

	export let webpSrcset = '';
	export let jpgSrcset: string;
	export let placeholder: Image;
	export let alt: string;
</script>

<picture>
	{#if webpSrcset}
		<source srcset={webpSrcset} type="image/webp" />
	{/if}
	<source srcset={jpgSrcset} type="image/jpeg" />
	<img src={placeholder.src} width={placeholder.width} height={placeholder.height} {alt} />
</picture>
