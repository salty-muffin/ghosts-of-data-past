<script lang="ts">
	// props
	let className = '';
	export { className as class };
</script>

<div class="nav__wrapper {className}">
	<nav class="nav__links"><h3><a href="/about">about</a></h3></nav>
</div>

<style global lang="scss">
	@use '../scss/variables' as *;

	.nav__wrapper {
		display: flex;
		align-items: center;

		height: map-get($nav-size, 'sm');

		border-top: map-get($border-width, 'sm') solid map-get($colors, 'foreground');
		@media only screen and (min-width: $breakpoint) {
			height: map-get($nav-size, 'lg');

			border-width: map-get($border-width, 'lg');
		}
	}

	.nav__links {
		width: 100%;
		display: flex;
		justify-content: flex-end;

		margin: 0 map-get($margin-primary, 'sm');
		@media only screen and (min-width: $breakpoint) {
			margin: 0 map-get($margin-primary, 'lg');
		}

		h3 {
			font-weight: normal;
			margin: 0;
		}
	}
</style>
