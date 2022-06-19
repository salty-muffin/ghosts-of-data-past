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
>
	<slot />
</span>

<style global lang="scss">
	.marker {
		font-feature-settings: 'sups' 1;

		padding: 0 0.4em;
		cursor: pointer;

		&:hover {
			text-decoration: underline;
		}

		&.marker--selected {
			text-decoration: underline;
		}
	}
</style>
