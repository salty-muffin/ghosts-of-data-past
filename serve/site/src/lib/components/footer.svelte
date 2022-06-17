<footer class="footer">
	<p>&copy; zeno gries</p>
	<p><a href="/about">data privacy statement</a></p>
	<p><a href="/about">imprint</a></p>
</footer>

<style global lang="scss">
	@use '../scss/variables' as *;

	.footer {
		max-width: $container-width;
		display: flex;

		margin: map-get($margin-primary, 'sm') 0 map-get($margin-secondary, 'sm');

		justify-content: space-between;

		p {
			font-size: map-get($footer-size, 'sm');
		}

		* {
			margin: 0;
			flex-grow: 1;
			flex-basis: 1;

			text-align: center;
		}

		*:first-child {
			text-align: left;
		}

		*:last-child {
			text-align: right;
		}
	}

	@media only screen and (min-width: $breakpoint) {
		.footer {
			p {
				font-size: map-get($footer-size, 'lg');
			}
		}
	}
</style>
