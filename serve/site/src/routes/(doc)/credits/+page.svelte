<script lang="ts">
	import Nav from '$lib/components/nav.svelte';
	import MuteButton from '$lib/components/mute-button.svelte';
	import Sidenote from '$lib/components/sidenote.svelte';
	import Image from '$lib/components/image.svelte';
</script>

<svelte:head>
	<title>credits / ghosts of data past</title>
</svelte:head>

<h1 class="doc__title">credits</h1>
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
<nav class="doc__toc">
	<ol>
		<li>
			<a href="#ghosts-of">the ghosts of</a>
		</li>
		<li>
			<a href="#inspiration">inspiration</a>
		</li>
		<li>
			<a href="#support">support</a>
		</li>
		<li>
			<a href="#funding">funding</a>
		</li>
	</ol>
</nav>
<p>
	Like most (art) projects, <em>ghosts of data past</em> was not the work of a single person but relied
	on the collaboration with and the support of a large number of people. Some of the people receiving
	credit and thanks here actively participated in this project. Others provided knowledge and inspiration,
	knowingly or unknowingly.
</p>
<h1 id="ghosts-of">the Ghosts of</h1>
<p>
	A big part of the basis for this project were the emails Hendrik Kempt<Sidenote id={1}
		>Henrik Kempt has a practice as a philosopher, working in applied ethics, also in the field of
		AI. He writes books, too: You can find out more about him on his <a
			href="https://twitter.com/hkem">Twitter</a
		></Sidenote
	> and I wrote over the winter of 21/22. These emails make up half of the dataset for the text-generating
	AI.
</p>
<p>
	The other half of the dataset was created by Sarah Lucey and Lola Wittstamm, who worked on the
	project as performers, improvising a messenger chat over three days.
</p>
<p>All participants provided their faces for filming and image dataset creation.</p>
<h1>Material and Software</h1>
<p>
	The fonts used in this project are <a href="https://abcdinamo.com/typefaces/favorit"
		>ABC Favorit</a
	>
	by ABC Dynamo and <a href="https://www.dafont.com/pwsmokey.font">PW Smokey</a>.
</p>
<p>
	The AI used in this project are <a href="https://github.com/EleutherAI/gpt-neo/">GPT Neo</a> by
	Eleuther AI for text generation and
	<a href="https://github.com/NVlabs/stylegan3">StyleGAN3</a><Sidenote id={2} left
		>The source code of StyleGAN3 was modified slightly by me, adding features that make dataset
		preparation from videos easier. You can find my fork <a
			href="https://github.com/salty-muffin/stylegan3">here</a
		>.</Sidenote
	> by NVIDIA<Sidenote id={3} right
		>I would have preferred not to have used AIs by large corporations. Unfortunately, it is hard to
		avoid at this time, especially when quality in image generation is required.</Sidenote
	> for selfie generation. Additionally,
	<a href="https://github.com/magenta/magenta/tree/main/magenta/models/nsynth">NSynth</a> was used for
	generating and abstracting the notification sounds. For all AIs pre-trained models were used that were
	provided by the creators of the respective AIs. For GPT Neo and StyleGAN3, these were finetuned with
	my datasets.
</p>
<h1 id="inspiration">Inspiration</h1>
<p>
	The look of these documentation pages, especially the sidenotes, is inspired by
	[gwern.net](https://www.gwern.net/Faces) by Gwern Branwen. Additionally, this site taught me a lot
	about working with styleGAN.
</p>
<p>
	<a href="https://www.instagram.com/jimo955/">Ben Clarke</a> inspired me to use styleGAN in the first
	place, when I saw his experiments.
</p>
<h1 id="support">Support</h1>
<p>
	I would like to thank all participants of the <a href="https://gbb.kunsthochschulekassel.de/"
		>Graduate School for Moving Images</a
	> at the Kunsthochschule Kassel, to whom I presented the current state of this project multiple times
	and who gave feedback and encouragement. These lovely people are: Alicia Carotta, Laura Därr, Katrin
	Esser, Juliane Henrich, Geeske Janßen, Steph Joyce, Young Kyun Kim, Silke Körber, Benedict Reinhold,
	Tobias Sauer, Christoph Schnerr, Andara Shastika and N.B. Spiders. I am also grateful for the work
	of Lisa Dreykluft and Holger Jenss, which creates this wonderful environment, and lets projects like
	this happen.
</p>
<p>
	Additionally, I would like to thank the teachers and professors at the Kunsthochschule Kassel, who
	supported <em>ghosts of data past</em> through help and feedback: Joel Baumann, Björn Melhus, Rosa
	Menkmann, Jan Peters, and Johanna Schaffer.
</p>
<p>
	Before a shared studio with Nikolai Huckle, I knew very little about how AI worked or what it
	might mean to work with it. Thanks to him that changed very quickly.
</p>
<p>
	Conversations with Lukas Fuchs and Rebekka Wiese were instrumental in shaping the outcome of this
	experiment, thank you for that.
</p>
<p>Thank you, Jonas Deuter and Julia Perkuhn for helping me with picking a font.</p>
<p>
	I would like to give special thanks to my parents, Gero Gries and Ivana Jokl, for their support in
	this project, but of course also for all their support in general.
</p>
<p>
	And last but not at all least I would like to thank Res Sigusch, without whose intelligent input,
	emotional support and love this certainly would have been a much less joyful affair.
</p>
<h1 id="funding">Funding</h1>
<p>
	The project was funded by the <a href="https://www.kdfs.de">KdFS</a>, which allowed me to pay the
	performers and license the fonts used. Hendrik Kempt refused to be paid for his collaboration.
</p>
<p>
	During my time working on this project, I was supported by the HAB scholarship from the <a
		href="https://www.hfmakademie.de/">HfMA</a
	>.
</p>
<p>
	<a href="https://kdfs.de">
		<Image
			image="images/kdfs_logo.png"
			width={1552}
			height={639}
			alt="KdFS Logo"
			sizes={[{ width: 396, maxWidth: 428 }, { width: 410 }]}
			formats={['avif', 'webp', 'png']}
			class="doc__logo"
		/>
	</a>
	Gefördert durch die <a href="https://kdfs.de">Kulturstiftung des Freistaates Sachsen</a>. Diese
	Maßnahme wird mitfinanziert durch Steuermittel auf der Grundlage des vom Sächsischen Landtag
	beschlossenen Haushaltes.
</p>
