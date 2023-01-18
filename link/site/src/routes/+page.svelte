<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<div class="link">
	<div class="qr">
		{@html data.qr}
	</div>
	<div class="text">
		<p>
			This links to <a href="{data.domain}{data.gate ? `/?gate=${data.gate}` : ''}"
				>{data.domain.replace('http://', '').replace('https://', '')}{data.gate
					? `/?gate=${data.gate}`
					: ''}</a
			>
		</p>
	</div>
</div>

<svg id="filter">
	<filter class="filter" id="melting">
		<feTurbulence id="turbulence" numOctaves="3" seed="100" result="turbulence">
			<animate
				attributeName="baseFrequency"
				dur="50s"
				keyTimes="0;0.5;1"
				values="0.01 0.01;0.02 0.02;0.01 0.01"
				repeatCount="indefinite"
			/>
		</feTurbulence>
		<feGaussianBlur in="turbulence" stdDeviation="10" result="softened" />
		<feDisplacementMap scale="6" in="SourceGraphic" in2="softened" result="displaced" />
		<!-- <feGaussianBlur in="displaced" stdDeviation="0.2" /> -->
	</filter>
</svg>

<style global lang="scss">
	@use '../lib/scss/variables' as *;

	.link {
		filter: url(#melting);

		width: 100vw;
		height: 100vh;

		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}

	.text {
		font-size: 3em;
		line-height: 1.6;
		font-family: $font-family-text;
		color: map-get($colors, 'foreground');

		font-weight: 200;

		p {
			margin: 0;
		}

		a {
			color: map-get($colors, 'foreground');
			font-family: $font-family-underline;
			text-decoration: none;
		}
	}

	.qr {
		width: 75vh;

		svg {
			& > path:first-of-type {
				fill: map-get($colors, 'background');
			}
			& > path:last-of-type {
				stroke: map-get($colors, 'foreground');
			}
		}
	}

	#filter {
		position: absolute;
		inset: 0;
		z-index: -1;
	}
</style>
