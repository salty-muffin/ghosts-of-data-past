<script lang="ts">
	let className = '';
	export { className as class };
	export let id: string;
	export let offset = 0;

	import { onMount } from 'svelte';

	let markerPos: number;
	let debounceTimer: any;
	onMount(() => {
		// get the corresponding marker element
		const marker = document.getElementById(`marker_${id}`);

		// on resize, get the position of it
		const onResize = () => {
			if (marker) markerPos = marker.offsetTop;
		};
		// debounce the resize event listener
		const debounce = () => {
			clearTimeout(debounceTimer);
			debounceTimer = setTimeout(onResize, 100);
		};
		onResize();

		addEventListener('resize', debounce);

		return () => {
			removeEventListener('resize', debounce);
			console.log('removed');
		};
	});
</script>

<div
	id="sidenote_{id}"
	class="sidenote {className}"
	style="top: {markerPos}px; --offset: {offset}em"
	on:mouseenter={() => {
		const marker = document.getElementById(`marker_${id}`);
		if (marker) marker.classList.add('marker--selected');
	}}
	on:mouseleave={() => {
		const marker = document.getElementById(`marker_${id}`);
		if (marker) marker.classList.remove('marker--selected');
	}}
	on:click={() => {
		const sidenote = document.getElementById(`sidenote_${id}`);
		if (sidenote) {
			sidenote.classList.remove('sidenote--clicked');
			sidenote.classList.remove('sidenote--selected');
		}
	}}
>
	<p class="sidenote__close">close</p>
	<div class="sidenote__content">
		<p class="sidenote__number">{id}</p>
		<slot />
	</div>
</div>

<style global lang="scss">
	@use '../scss/variables' as *;

	.sidenote {
		display: none;
		position: absolute;

		pointer-events: auto;

		background-color: map-get($colors, 'background');
		border-top: solid map-get($border-width, 'sm') map-get($colors, 'foreground');
		border-bottom: solid map-get($border-width, 'sm') map-get($colors, 'foreground');
		margin-top: 1.8em;

		padding: map-get($margin-primary, 'sm');

		* {
			font-size: map-get($sidenote-size, 'sm');
		}

		*:first-child,
		*:nth-child(2) {
			margin-top: 0;
		}
		*:last-child {
			margin-bottom: 0;
		}

		&.sidenote--selected,
		&.sidenote--clicked {
			display: unset;
		}

		&:hover .sidenote__close {
			font-family: $font-family-underline;
			color: map-get($colors, 'foreground');
		}
	}

	.sidenote__close {
		color: map-get($colors, 'link');
		text-align: right;
	}

	.sidenote__content {
		display: flex;
	}

	.sidenote__number {
		margin: 0;
		padding-right: 1em;
	}

	@media (hover: none) {
		.sidenote__close {
			font-family: $font-family-underline;
		}
	}

	@media only screen and (min-width: $breakpoint) {
		.sidenote {
			border-top: solid map-get($border-width, 'lg') map-get($colors, 'foreground');
			border-bottom: solid map-get($border-width, 'lg') map-get($colors, 'foreground');

			* {
				font-size: map-get($sidenote-size, 'lg');
			}
		}
	}

	@media only screen and (min-width: $sidenote-breakpoint) {
		.sidenote {
			display: unset;

			margin-top: var(--offset);

			border-bottom: unset;

			padding: map-get($margin-primary, 'lg') 0 0 map-get($margin-primary, 'lg');
		}

		.sidenote__left {
			.sidenote {
				padding-right: map-get($margin-primary, 'lg');

				border-right: solid map-get($border-width, 'lg') map-get($colors, 'background');

				&.sidenote--selected,
				&:hover {
					border-right: solid map-get($border-width, 'lg') map-get($colors, 'foreground');
				}
			}
		}
		.sidenote__right {
			.sidenote {
				padding-left: map-get($margin-primary, 'lg');
				border-left: solid map-get($border-width, 'lg') map-get($colors, 'background');

				&.sidenote--selected,
				&:hover {
					border-left: solid map-get($border-width, 'lg') map-get($colors, 'foreground');
				}
			}
		}

		.sidenote__close {
			display: none;
		}
	}
</style>
