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

		display: none;
		position: absolute;
		inset: 0;
		margin: 0 map-get($margin-primary, 'sm');
	}

	@media only screen and (min-width: $sidenote-breakpoint) {
		.sidenote-column {
			position: relative;
			display: unset;
			max-width: $sidenote-width;
			width: 100em;
			margin: 0 map-get($margin-primary, 'lg');

			&.sidenote__left {
				margin: 0 0 0 map-get($margin-primary, 'sm');
			}
			&.sidenote__right {
				margin: 0 map-get($margin-primary, 'sm') 0 0;
			}
		}
	}
</style>
