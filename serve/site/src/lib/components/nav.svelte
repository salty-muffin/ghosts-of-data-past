<div class="bar" />

<style lang="scss">
	@use '../scss/variables' as *;

	.bar {
		height: 3em;
		flex-shrink: 0;

		border-top: 1px solid map-get($colors, 'foreground');
	}
</style>
