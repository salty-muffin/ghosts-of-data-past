<script lang="ts">
	interface Link {
		href: string;
		text: string;
	}

	// props
	let className = '';
	export { className as class };
	export let links: Link[];
</script>

<div class="nav__wrapper {className}">
	<nav class="nav__links">
		<slot />

		{#each links as { href, text }, index (index)}
			<h4><a {href}>{text}</a></h4>
		{/each}
	</nav>
</div>

<style global lang="scss">
	@use '../scss/variables' as *;

	.nav__wrapper {
		display: flex;
		align-items: center;

		height: map-get($nav-size, 'sm');

		background-color: map-get($colors, 'background');
	}

	.nav__links {
		width: 100%;
		display: flex;
		flex-wrap: wrap;
		flex-direction: row;
		justify-content: space-between;

		margin: 0 map-get($margin-primary, 'sm');

		h4,
		button {
			font-variation-settings: 'wght' 350;
			font-size: map-get($nav-links-size, 'sm');
			margin: 0;
			text-align: left;
		}
		button:hover h4 {
			font-weight: 350;
		}

		a:hover {
			color: map-get($colors, 'foreground');
			// text-decoration: underline;
			/* font-family: $font-family-underline; */
			font-weight: 350;
		}
	}

	@media (hover: none) {
		button h4 {
			font-weight: 350;
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'md')) {
		.nav__wrapper {
			height: map-get($nav-size, 'md');
		}

		.nav__links {
			margin: 0 map-get($margin-primary, 'md');

			h4 button,
			h4 {
				font-size: map-get($nav-links-size, 'md');
			}
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'lg')) {
		.nav__wrapper {
			height: map-get($nav-size, 'lg');
		}

		.nav__links {
			margin: 0 map-get($margin-primary, 'lg');

			h4 button,
			h4 {
				font-size: map-get($nav-links-size, 'lg');
			}
		}
	}
</style>
