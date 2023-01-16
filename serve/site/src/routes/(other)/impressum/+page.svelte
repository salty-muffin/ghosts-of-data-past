<script lang="ts">
	import Nav from '$lib/components/nav.svelte';
	import MuteButton from '$lib/components/mute-button.svelte';
</script>

<svelte:head>
	<title>impressum</title>
</svelte:head>

<h1 class="other__title">Impressum</h1>
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
<p>Zeno Gries</p>
<p>Kontakt:</p>
<p>E-Mail: <a href="mailto:zeno@zenogries.com">zeno@zenogries.com</a></p>
<h1>Haftungsausschluss</h1>
<h2>Haftung für Links</h2>
<p>
	Unser Angebot enthält Links zu externen Webseiten Dritter, auf deren Inhalte wir keinen Einfluss
	haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte
	der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der Seiten verantwortlich.
	Die verlinkten Seiten wurden zum Zeitpunkt der Verlinkung auf mögliche Rechtsverstöße überprüft.
	Rechtswidrige Inhalte waren zum Zeitpunkt der Verlinkung nicht erkennbar. Eine permanente
	inhaltliche Kontrolle der verlinkten Seiten ist jedoch ohne konkrete Anhaltspunkte einer
	Rechtsverletzung nicht zumutbar. Bei Bekanntwerden von Rechtsverletzungen werden wir derartige
	Links umgehend entfernen.
</p>
<h2>Urheberrecht</h2>
<p>
	Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem
	deutschen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung
	außerhalb der Grenzen des Urheberrechtes bedürfen der schriftlichen Zustimmung des jeweiligen
	Autors bzw. Erstellers. Downloads und Kopien dieser Seite sind nur für den privaten, nicht
	kommerziellen Gebrauch gestattet. Soweit die Inhalte auf dieser Seite nicht vom Betreiber erstellt
	wurden, werden die Urheberrechte Dritter beachtet. Insbesondere werden Inhalte Dritter als solche
	gekennzeichnet. Sollten Sie trotzdem auf eine Urheberrechtsverletzung aufmerksam werden, bitten
	wir um einen entsprechenden Hinweis. Bei Bekanntwerden von Rechtsverletzungen werden wir derartige
	Inhalte umgehend entfernen.
</p>
<h2>Datenschutz</h2>
<p>
	Die Nutzung unserer Webseite ist in der Regel ohne Angabe personenbezogener Daten möglich. Soweit
	auf unseren Seiten personenbezogene Daten (beispielsweise Name, Anschrift oder eMail-Adressen)
	erhoben werden, erfolgt dies, soweit möglich, stets auf freiwilliger Basis. Diese Daten werden
	ohne Ihre ausdrückliche Zustimmung nicht an Dritte weitergegeben.
</p>
<p>
	Wir weisen darauf hin, dass die Datenübertragung im Internet (z.B. bei der Kommunikation per
	E-Mail) Sicherheitslücken aufweisen kann. Ein lückenloser Schutz der Daten vor dem Zugriff durch
	Dritte ist nicht möglich.
</p>
<p>
	Der Nutzung von im Rahmen der Impressumspflicht veröffentlichten Kontaktdaten durch Dritte zur
	Übersendung von nicht ausdrücklich angeforderter Werbung und Informationsmaterialien wird hiermit
	ausdrücklich widersprochen. Die Betreiber der Seiten behalten sich ausdrücklich rechtliche
	Schritte im Falle der unverlangten Zusendung von Werbeinformationen, etwa durch Spam-Mails, vor.
</p>
<p>
	Impressum vom <a href="https://www.impressum-generator.de/" rel="nofollow">Impressum Generator</a>
	der
	<a href="https://www.kanzlei-hasselbach.de/standorte/bonn/" rel="nofollow"
		>Kanzlei Hasselbach, Bonn</a
	>.
</p>
