<script lang="ts">
	import IframePanel from '$lib/components/iframe-panel.svelte';
	import Nav from '$lib/components/nav.svelte';
	import MuteVideoButton from '$lib/components/mute-video-button.svelte';

	import { muted } from '$lib/stores/muted';

	import type Player from '@vimeo/player';

	let player: Player;

	const videoIds = ['753293224?h=780f35ea9e', '753293778'];
	let videoSelector = Math.floor(Math.random() * videoIds.length);
</script>

<svelte:head>
	<title>ghosts of data past</title>
</svelte:head>

<div class="video">
	<IframePanel
		bind:player
		class="video__panel"
		url="https://player.vimeo.com/video/{videoIds[videoSelector]}"
	/>
	<Nav class="video__nav" links={[{ href: '/background', text: 'background' }]}>
		<MuteVideoButton
			on:click={() => {
				$muted = !$muted;

				if (player) {
					player.setMuted($muted);
				}
			}}
		>
			<h4 slot="muted">unmute</h4>
			<h4 slot="unmuted">mute</h4>
		</MuteVideoButton>
	</Nav>
</div>
<a href="#text">
	<div class="video__arrow">
		<svg width="30" height="37" viewBox="0 0 30 37" fill="none" xmlns="http://www.w3.org/2000/svg">
			<path
				d="M15 2V34M15 34L27 22.0784M15 34L3 22.0784"
				stroke-width="3"
				stroke-linecap="square"
			/>
		</svg>
	</div>
</a>
<div class="video__text" id="text">
	<p>
		This is the video documentation of <em>ghosts of data past</em>.
	</p>
	<p>
		All other parts of this website are exactly like they are in artwork itself. On this page
		however, you can find the documentation instead of the actual live-generated chat.
	</p>
	<p>
		<em>ghosts of data past</em> is a project by <a href="https://zenogries.com">zeno gries</a>. For
		more information, please see the <a href="/background">background</a>.
	</p>
	<p>The software documented here is complimented by an installation when exhibited.</p>
</div>

<style global lang="scss">
	@use '../../lib/scss/variables' as *;

	.video {
		position: relative;
		width: 100vw;
		height: 100vh;
		max-height: -webkit-fill-available;
	}

	.video__arrow {
		position: absolute;
		bottom: map-get($nav-size, 'sm');
		left: 0;

		padding: 0.5em 0.5em 0.2em;
		margin: 1em;

		background-color: map-get($colors, 'background');

		z-index: 1;

		svg {
			path {
				stroke: map-get($colors, 'foreground');
			}
		}
	}

	.video__panel {
		width: 100%;
		height: calc(100% - map-get($nav-size, 'sm'));

		z-index: -1;

		.iframe-panel__iframe {
			transform: scale(1.3);
		}
	}

	.video__nav {
		position: absolute;
		left: 0;
		bottom: 0;
		right: 0;
	}

	.video__text {
		padding: map-get($margin-primary, 'sm');
		border-top: map-get($border-width, 'sm') solid map-get($colors, 'foreground');

		& > *:first-of-type {
			margin-top: 0;
		}
		& > *:last-of-type {
			margin-bottom: 0;
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'md')) {
		.video__arrow {
			bottom: map-get($nav-size, 'lg');

			svg {
				width: 3em;
				height: auto;
			}

			padding: 0.7em 0.7em 0.3em;
			margin: 1.5em;
		}

		.video__panel {
			height: calc(100% - map-get($nav-size, 'md'));

			.iframe-panel__iframe {
				transform: none;
			}
		}

		.video__text {
			padding: map-get($margin-primary, 'md');
			border-top: map-get($border-width, 'md') solid map-get($colors, 'foreground');
		}
	}

	@media only screen and (min-width: 80em) {
		.video__arrow {
			display: none;
		}

		.video__elements {
			position: absolute;
			bottom: 0;
			left: 0;
			right: 0;
		}

		.video__text {
			position: absolute;
			bottom: map-get($nav-size, 'md');
			left: 0;

			margin: 2em;
			padding: 2em;

			width: 21em;

			border-top: none;

			background-color: map-get($colors, 'background');
		}
	}

	@media only screen and (min-width: map-get($breakpoint, 'lg')) {
		.video__panel {
			height: calc(100% - map-get($nav-size, 'lg'));
		}

		.video__text {
			bottom: map-get($nav-size, 'lg');

			width: 24em;
		}
	}
</style>
