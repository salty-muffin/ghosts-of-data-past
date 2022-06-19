<script lang="ts">
	export let id: string;
</script>

<span
	class="marker"
	id="marker_{id}"
	on:mouseenter={() => {
		const sidenote = document.getElementById(`sidenote_${id}`);
		if (sidenote) sidenote.classList.add('sidenote--selected');
	}}
	on:mouseleave={() => {
		const sidenote = document.getElementById(`sidenote_${id}`);
		if (sidenote) sidenote.classList.remove('sidenote--selected');
	}}
	on:click={() => {
		const sidenote = document.getElementById(`sidenote_${id}`);
		if (sidenote) sidenote.classList.toggle('sidenote--clicked');
	}}
>
	<slot />
</span>

<style global lang="scss">
	@use '../scss/variables' as *;

	.marker {
		font-feature-settings: 'sups' 1;

		padding: 0 0.4em;
		cursor: pointer;

		&:hover {
			font-family: $font-family-underline;
		}

		&.marker--selected {
			font-family: $font-family-underline;
		}
	}

	@media (hover: none) {
		.marker {
			color: map-get($colors, 'link');
			font-family: $font-family-underline;
		}
	}
</style>
