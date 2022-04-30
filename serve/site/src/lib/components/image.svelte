<script lang="ts">
	export let src: string;
	export let alt: string;
	let className: string = '';
	export { className as class };
</script>

<div class="image-wrapper {className}">
	<img {src} {alt} width="1024" height="1024" />
</div>

<style lang="scss">
	img {
		width: 100%;
		height: auto;
	}
</style>
