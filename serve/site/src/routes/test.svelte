<script lang="ts">
	import IframePanel from '$lib/components/iframe-panel.svelte';
</script>

<IframePanel class="video__panel" url="https://player.vimeo.com/video/636103889" />

<style global lang="scss">
	.video__panel {
		position: fixed;
		top: 0;
		left: 0;
		width: 100vw;
		height: 100vh;

		z-index: -1;

		overflow: hidden;
	}
</style>
