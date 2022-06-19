<script lang="ts">
	let className = '';
	export { className as class };
	export let id: string;
	export let offset = 0;

	import { onMount } from 'svelte';

	let markerPos: number;
	onMount(() => {
		const marker = document.getElementById(`marker_${id}`);
		if (marker) markerPos = marker.offsetTop;
	});
</script>

<div
	id="sidenote_{id}"
	class="sidenote {className}"
	style="top: calc({markerPos}px + {offset}rem);"
	on:mouseenter={() => {
		const marker = document.getElementById(`marker_${id}`);
		if (marker) marker.classList.add('marker--selected');
	}}
	on:mouseleave={() => {
		const marker = document.getElementById(`marker_${id}`);
		if (marker) marker.classList.remove('marker--selected');
	}}
>
	<slot />
</div>

<style global lang="scss">
	@use '../scss/variables' as *;

	.sidenote {
		position: absolute;
		* {
			font-size: map-get($sidenote-size, 'sm');
		}
	}

	@media only screen and (min-width: $breakpoint) {
		.sidenote {
			* {
				font-size: map-get($sidenote-size, 'lg');
			}

			*:first-child {
				margin-top: 0;
			}
			*:last-child {
				margin-bottom: 0;
			}
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
	}
</style>
