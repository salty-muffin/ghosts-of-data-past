<script lang="ts">
	let className = '';
	export { className as class };
</script>

<div class="sidenote-column {className}">
	<slot />
</div>

<style global lang="scss">
	@use '../scss/variables' as *;

	.sidenote-column {
		flex-shrink: 2;
		max-width: $container-width;
		margin: auto;

		pointer-events: none;
		position: absolute;
		inset: 0;
	}

	@media only screen and (min-width: $sidenote-breakpoint) {
		.sidenote-column {
			position: relative;

			max-width: $sidenote-width;

			width: 100em;

			&.sidenote__left {
				margin: 0 0 0 map-get($margin-primary, 'lg');
			}
			&.sidenote__right {
				margin: 0 map-get($margin-primary, 'lg') 0 0;
			}
		}
	}
</style>
