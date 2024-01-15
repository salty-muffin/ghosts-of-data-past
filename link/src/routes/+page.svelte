<script lang="ts">
	import '$lib/scss/fonts.scss';
	import '$lib/scss/global.scss';

	import type { PageData } from './$types';

	export let data: PageData;
</script>

<div class="link">
	<div class="link__canvas">
		<img class="qr" src={data.qr} alt="qr-code" />
	</div>
	<!-- <div class="text">
		<p>
			this links to <a href="{data.domain}{data.gate ? `/?gate=${data.gate}` : ''}"
				>{data.domain.replace('http://', '').replace('https://', '')}{data.gate
					? `/?gate=${data.gate}`
					: ''}</a
			>
		</p>
	</div> -->
</div>

<style global lang="scss">
	@use '../lib/scss/variables' as *;

	.link {
		width: 100vw;
		height: 100vh;
	}

	.link__canvas {
		position: absolute;
		inset: 0;

		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}

	.qr {
		max-width: 70vh;
		height: auto;
	}

	// .text {
	// 	font-size: 2.5em;
	// 	line-height: 1.6;
	// 	font-family: $font-family-text;
	// 	font-feature-settings: 'calt' 1, 'liga' 1, 'rlig' 1, 'rvrn' 1, 'kern' 1, 'rclt' 1, 'ss04' 1,
	// 		'ss05' 1;
	// 	color: map-get($colors, 'foreground');

	// 	font-weight: 200;

	// 	p {
	// 		margin: 0;
	// 	}

	// 	a {
	// 		color: map-get($colors, 'foreground');
	// 		font-family: $font-family-underline;
	// 		font-feature-settings: 'calt' 1, 'liga' 1, 'rlig' 1, 'rvrn' 1, 'kern' 1, 'rclt' 1, 'ss04' 1,
	// 			'ss05' 1, 'ss09' 1;
	// 		text-decoration: none;
	// 	}
	// }
</style>
