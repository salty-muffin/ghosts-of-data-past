<svelte:options immutable />

<script lang="ts">
	// props
	export let id: string;
	export let sender: string;
	export let text: string;
	export let imageURL: string;
	export let alt: string;
	export let timestamp: number;
	export let attributes: any;

	// get date from timestamp
	const date = new Date(timestamp);
</script>

<div class="message__wrapper message--{attributes[sender]['position']} message--breathing" {id}>
	<div class="message__body">
		<!-- <h6 class="message__sender">{sender}</h6> -->
		{#if imageURL}
			<img class="message__image" src={imageURL} {alt} width="1024" height="1024" />
		{/if}
		{#if text}
			<span class="message__text">{text}</span>
		{/if}
		<span class="message__timestamp"
			>{date.getHours()}:{date.getMinutes().toString().padStart(2, '0')}</span
		>
	</div>
	<svg
		class="message__tip"
		width="25"
		height="21"
		viewBox="0 0 25 21"
		xmlns="http://www.w3.org/2000/svg"
	>
		<path d="M9 0C9 16 1 20 1 20C1 20 9 16 25 16" />
	</svg>
</div>

<style global lang="scss">
	@use '../scss/variables' as *;

	.message__wrapper {
		max-width: 60%;

		background-color: map-get($colors, 'background');
		/* border: map-get($border-width, 'sm') solid map-get($colors, 'foreground'); */
		filter: drop-shadow(0 0 map-get($border-blur, 'sm') map-get($colors, 'foreground'));
		border-radius: map-get($margin-primary, 'sm');

		margin: 0 map-get($margin-secondary, 'sm') map-get($margin-primary, 'sm');
		padding: map-get($margin-secondary, 'sm') map-get($margin-primary, 'sm');
	}
	.message--left {
		align-self: flex-start;

		.message__tip {
			left: map-get($margin-secondary, 'sm') * (-1);
		}
	}
	.message--right {
		align-self: flex-end;

		.message__tip {
			right: map-get($margin-secondary, 'sm') * (-1);

			transform: scaleX(-1);
		}
	}

	.message__sender {
		margin: 0 0 0.2em 0;

		// non-breathing setting
		font-variation-settings: 'wght' 550, 'ital' 0;

		font-size: map-get($sender-size, 'sm');
	}

	.message__image {
		max-width: 100%;
		height: auto;
	}

	.message__text {
		margin: 0;

		// non-breathing setting
		font-variation-settings: 'wght' 400, 'ital' 0;

		line-height: $message-line-height;
		font-size: map-get($message-text-size, 'sm');
	}

	.message__timestamp {
		float: right;
		margin: 0.5em 0 0 0.5em;

		// non-breathing setting
		font-variation-settings: 'wght' 325, 'ital' 0;

		font-size: map-get($timestamp-size, 'sm');
	}

	.message__tip {
		position: absolute;
		bottom: -0.25em;
		width: map-get($margin-primary, 'sm') + map-get($margin-secondary, 'sm');
		height: auto;
	}

	.message--breathing {
		.message__sender {
			font-variation-settings: 'wght' var(--h-weight), 'ital' var(--h-italic);
		}
		.message__text {
			font-variation-settings: 'wght' var(--b-weight), 'ital' var(--b-italic);
		}
		.message__timestamp {
			font-variation-settings: 'wght' var(--t-weight), 'ital' var(--t-italic);
		}
	}

	@media only screen and (min-width: $breakpoint) {
		.message__wrapper {
			/* border-width: map-get($border-width, 'lg'); */
			filter: drop-shadow(0 0 map-get($border-blur, 'lg') map-get($colors, 'foreground'));
			border-radius: map-get($margin-primary, 'lg');

			margin: 0 map-get($margin-secondary, 'lg') map-get($margin-primary, 'lg');
			padding: map-get($margin-secondary, 'lg') map-get($margin-primary, 'lg');
		}
		.message--left {
			.message__tip {
				left: map-get($margin-secondary, 'lg') * (-1);
				margin-left: -0.05em;
			}
		}
		.message--right {
			.message__tip {
				right: map-get($margin-secondary, 'lg') * (-1);
				margin-right: -0.05em;
			}
		}

		.message__sender {
			font-size: map-get($sender-size, 'lg');
		}

		.message__text {
			font-size: map-get($message-text-size, 'lg');
		}

		.message__timestamp {
			font-size: map-get($timestamp-size, 'lg');
		}

		.message__tip {
			position: absolute;
			bottom: -0.4em;
			width: (map-get($margin-primary, 'lg') + map-get($margin-secondary, 'lg'));
		}
	}
</style>
