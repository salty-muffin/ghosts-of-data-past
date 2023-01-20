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
		<feTurbulence id="turbulence" numOctaves="1" seed="100" result="turbulence">
			<animate
				attributeName="baseFrequency"
				dur="50s"
				keyTimes="0;0.5;1"
				values="0.01 0.01;0.02 0.02;0.01 0.01"
				repeatCount="indefinite"
			/>
		</feTurbulence>
		<feDisplacementMap scale="5" in="SourceGraphic" in2="turbulence" result="displaced" />
		<!-- <feGaussianBlur in="displaced" stdDeviation="0.2" /> -->
	</filter>
</svg>

<style global lang="scss">
	@use '../lib/scss/variables' as *;

	.link {
		width: 100vw;
		height: 100vh;

		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}

	@keyframes textMove {
		from {
			transform: translateY(-50%);
		}

		to {
			transform: translateY(50%);
		}
	}

	.text {
		filter: url(#melting);
		animation: 30s infinite alternate linear textMove;

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

	@keyframes qrMove {
		from {
			transform: translateX(-20%);
		}

		to {
			transform: translateX(20%);
		}
	}

	.qr {
		filter: url(#melting);
		animation: 30s infinite alternate linear qrMove;

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
