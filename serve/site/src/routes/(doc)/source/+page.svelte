<script lang="ts">
	import Nav from '$lib/components/nav.svelte';
	import MuteButton from '$lib/components/mute-button.svelte';
</script>

<svelte:head>
	<title>source / ghosts of data past</title>
</svelte:head>

<h1 class="doc__title">source</h1>
<Nav
	class="doc__nav"
	links={[
		{ href: '/', text: 'back to work' },
		{ href: '/background', text: 'background' },
		{ href: '/credits', text: 'credits' },
		{ href: '/source', text: 'source' }
	]}
>
	<MuteButton>
		<h4 slot="muted">unmute</h4>
		<h4 slot="unmuted">mute</h4>
	</MuteButton>
</Nav>
<p>
	In case you want to know how all this was implemented exactly or even recreate it with your own
	datasets, you can the source code for this project and further documentation through the following
	links. All source code used for research and production of this work is publicly available and may
	be used, adapted and redistributed for non-commercial projects.
</p>

<ul>
	<li>
		<a href="https://github.com/salty-muffin/ghosts-of-data-past">ghosts-of-data-past</a> – this is the
		code running inside the server object, generating the messages and hosting this work online.
	</li>
	<li>
		<a href="https://github.com/salty-muffin/gpt-2-training">gpt-2-training</a> – for training the text
		generating algorithm.
	</li>
	<li>
		<a href="https://github.com/salty-muffin/stylegan3">stylegan3</a> – for training the image generating
		algorithm.
	</li>
	<li>
		<a href="https://github.com/salty-muffin/nsynth-notification-sound-generation"
			>nsynth-notification-sound-generation</a
		> – for generating the notification sounds.
	</li>
</ul>
