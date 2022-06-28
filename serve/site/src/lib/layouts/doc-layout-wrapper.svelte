<script>
	export let title = ''; // @ts-ignore
	export let links = [];

	import Layout from './doc-layout.svelte';
</script>

<Layout {title} {links}><slot /></Layout>
