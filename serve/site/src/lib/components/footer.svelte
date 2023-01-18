<footer class="footer">
	<p>zeno gries 2023</p>
	<p><a href="/datenschutz">data privacy statement</a></p>
	<p><a href="/impressum">imprint</a></p>
</footer>

<style global lang="scss">
	@use '../scss/variables' as *;

	.footer {
		display: flex;
		align-self: stretch;

		margin: map-get($margin-layout, 'sm') map-get($margin-primary, 'sm')
			map-get($margin-secondary, 'sm');

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

	@media only screen and (min-width: map-get($breakpoint, 'md')) {
		.footer {
			margin: map-get($margin-layout, 'md') map-get($margin-primary, 'md')
				map-get($margin-secondary, 'md');

			p {
				font-size: map-get($footer-size, 'md');
			}
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'lg')) {
		.footer {
			margin: map-get($margin-layout, 'lg') map-get($margin-primary, 'lg')
				map-get($margin-secondary, 'lg');

			p {
				font-size: map-get($footer-size, 'lg');
			}
		}
	}
</style>
