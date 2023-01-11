<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<div class="qr">
	{@html data.qr}
</div>
<div class="text">
	<p>This links to <a href="localhost:5000/{data.id}">localhost:5000/{data.id}</a></p>
</div>

<svg>
	<filter class="filter" id="turbulence" x="0" y="0" width="105%" height="105%">
		<feTurbulence id="sea-filter" numOctaves="2" seed="100" />
		<feDisplacementMap scale="2" in="SourceGraphic" />
		<animate
			xlink:href="#sea-filter"
			attributeName="baseFrequency"
			dur="50s"
			keyTimes="0;0.5;1"
			values="0.01 0.01;0.02 0.02;0.01 0.01"
			repeatCount="indefinite"
		/>
	</filter>
</svg>

<style global lang="scss">
	@use '../lib/scss/variables' as *;

	.text {
		font-size: 2em;
		line-height: 1.6;
		font-family: $font-family-text;
		color: map-get($colors, 'foreground');

		font-weight: 200;

		filter: url(#turbulence);

		a {
			color: map-get($colors, 'link');
			text-decoration: none;
		}
	}

	.qr {
		max-width: 60vh;

		svg {
			filter: url(#turbulence);

			& > path:first-of-type {
				fill: map-get($colors, 'background');
			}
			& > path:last-of-type {
				stroke: map-get($colors, 'foreground');
			}
		}
	}
</style>
