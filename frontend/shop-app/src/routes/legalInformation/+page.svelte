<script>
    import "../../input.css";
    import Header from "$lib/components/Header.svelte";
    import Footer from "$lib/components/Footer.svelte";

</script>

<head>
    <title>Legal Information</title>
</head>

<Header title="Legal Information"/>
<div id="content" class="overflow-hidden">    
    
    <nav class="m-5 md:m-10">
        <p class="text-xl font-semibold pb-2">Content (only available in German)</p>
        <ul class="list-disc list-inside pl-5 space-y-2">
            <li><a href="#terms" class="text-blue-600 hover:underline">General Terms and Conditions</a></li>
            <li><a href="#privacy" class="text-blue-600 hover:underline">Privacy Policy</a></li>
            <li><a href="#cancellation" class="text-blue-600 hover:underline">Cancellation Policy</a></li>
        </ul>
    </nav>
    
    <div id="terms" class="m-5 pb-2 md:m-10">
        <h1 class="text-2xl font-bold pb-2">General Terms and Conditions (Allgemeine Geschäftsbedingungen - AGB)</h1>
        <div class="bg-gray-200 rounded-xl shadow-lg flex flex-col space-y-4 md:space-y-0 relative p-4">
            <p class="font-bold text-xl">1. Geltungsbereich</p>
            <p class="pt-2">Diese Allgemeinen Geschäftsbedingungen (AGB) gelten für alle Bestellungen, die über unseren Webshop [Webshop-Name] abgegeben werden. Vertragspartner für alle Bestellungen ist:</p>
            <p class="pt-4 pl-3">Shopcore</p>
            <p class="pt-2 pl-3">Alteburgstraße 150, 72762 Reutlingen</p>
            <p class="pt-2 pl-3">0157 12345</p>
            <p class="pt-2 pl-3">shopcore.info@gmail.com</p>
            <p class="font-bold text-xl pt-2">2. Vertragsschluss</p>
            <p class="pt-2">1. Die Darstellung der Produkte im Webshop stellt kein rechtlich bindendes Angebot, sondern eine Aufforderung zur Bestellung dar.</p>
            <p class="pt-2">2. Durch das Absenden einer Bestellung im Webshop geben Sie ein verbindliches Angebot zum Kauf der im Warenkorb enthaltenen Waren ab. Die Bestätigung des Eingangs der Bestellung erfolgt per E-Mail unmittelbar nach dem Absenden der Bestellung und stellt noch keine Vertragsannahme dar.</p>
            <p class="pt-2">3. Ein Kaufvertrag kommt erst zustande, wenn wir Ihre Bestellung durch eine weitere E-Mail mit einer Auftragsbestätigung oder durch den Versand der Ware annehmen.</p>
            <p class="font-bold text-xl pt-2">3. Preise und Versandkosten</p>
            <p class="pt-2">1. Alle im Webshop angegebenen Preise verstehen sich inklusive der gesetzlichen Mehrwertsteuer und exklusive der Versandkosten.</p>
            <p class="pt-2">2. Die Versandkosten werden vor Abschluss der Bestellung im Webshop deutlich mitgeteilt.</p>
            <p class="pt-2">3. Bei Lieferungen in Länder außerhalb der EU können zusätzliche Zölle und Gebühren anfallen, die vom Kunden zu tragen sind.</p>
            <p class="font-bold text-xl pt-2">4. Lieferung</p>
            <p class="pt-2">1. Die Lieferung erfolgt an die vom Kunden angegebene Lieferadresse.</p>
            <p class="pt-2">2. Angaben zur Lieferzeit sind unverbindlich, es sei denn, ein Liefertermin wurde ausdrücklich verbindlich zugesagt.</p>
            <p class="pt-2">3. Sollte das bestellte Produkt nicht verfügbar sein, werden wir Sie unverzüglich informieren und eventuell bereits erbrachte Gegenleistungen erstatten.</p>
            <p class="font-bold text-xl pt-2">5. Zahlung</p>
            <p class="pt-2">1. Die Zahlung kann per Kreditkarte erfolgen.</p>
            <p class="pt-2">2. Die Zahlung ist unmittelbar mit Vertragsschluss fällig.</p>
            <p class="pt-2">3. Kommt der Kunde in Zahlungsverzug, sind wir berechtigt, Verzugszinsen in gesetzlicher Höhe zu verlangen.</p>
            <p class="font-bold text-xl pt-2">6. Widerrufsrecht</p>
            <p class="pt-2">1. Verbrauchern steht ein gesetzliches Widerrufsrecht zu. Die Widerrufsfrist beträgt 14 Tage ab dem Tag, an dem Sie oder ein von Ihnen benannter Dritter die Ware in Besitz genommen haben.</p>
            <p class="pt-2">2. Um Ihr Widerrufsrecht auszuüben, müssen Sie uns mittels einer eindeutigen Erklärung (z. B. per Post oder E-Mail) über Ihren Entschluss informieren, diesen Vertrag zu widerrufen.</p>
            <p class="pt-2">3. Die Rücksendekosten trägt der Kunde, es sei denn, die gelieferte Ware entspricht nicht der bestellten.</p>
            <p class="font-bold text-xl pt-2">7. Eigentumsvorbehalt</p>
            <p class="pt-2">Die Ware bleibt bis zur vollständigen Bezahlung unser Eigentum.</p>
            <p class="font-bold text-xl pt-2">8. Gewährleistung und Haftung</p>
            <p class="pt-2">1. Für Verbraucher gelten die gesetzlichen Gewährleistungsrechte.</p>
            <p class="pt-2">2. Unsere Haftung für Schäden, die aus der Verletzung des Lebens, des Körpers oder der Gesundheit resultieren, sowie für sonstige Schäden, die auf einer vorsätzlichen oder grob fahrlässigen Pflichtverletzung beruhen, bleibt unberührt.</p>
            <p class="font-bold text-xl pt-2">9. Datenschutz</p>
            <p class="pt-2">Informationen zum Datenschutz finden Sie in unserer <a href="#privacy" class="text-blue-600 hover:underline">Privacy Policy</a>.</p>
            <p class="font-bold text-xl pt-2">10. Schlussbestimmungen</p>
            <p class="pt-2">1. Es gilt das Recht der Bundesrepublik Deutschland unter Ausschluss des UN-Kaufrechts.</p>
            <p class="pt-2">2. Sollten einzelne Bestimmungen dieser AGB unwirksam sein oder werden, bleibt die Gültigkeit der übrigen Bestimmungen unberührt.</p>
        </div>
    </div>
    
    <div id="privacy" class="m-5 pb-2 md:m-10">
        <h1 class="text-2xl font-bold pb-2">Privacy Policy (Datenschutzrichtlinie gemäß DSGVO)</h1>
        <div class="bg-gray-200 rounded-xl shadow-lg flex flex-col space-y-4 md:space-y-0 relative p-4">
            <p class="font-bold text-xl">1. Allgemeine Hinweise und Pflichtinformationen</p>
            <p class="pt-2 font-bold">Verantwortlicher</p>
            <p class="pt-2">Der Verantwortliche für die Datenverarbeitung auf dieser Website ist:</p>
            <p class="pt-4 pl-2">Shopcore</p>
            <p class="pt-2 pl-2">Alteburgstraße 150, 72762 Reutlingen</p>
            <p class="pt-2 pl-2">0157 12345</p>
            <p class="pt-2 pl-2">shopcore.info@gmail.com</p>
            <p class="pt-4">Verantwortlicher ist die natürliche oder juristische Person, die allein oder gemeinsam mit anderen über die Zwecke und Mittel der Verarbeitung von personenbezogenen Daten entscheidet.</p>
            <p class="font-bold text-xl pt-2">2. Erhebung und Speicherung personenbezogener Daten sowie Art und Zweck von deren Verwendung</p>
            <p class="pt-2 font-bold">a) Beim Besuch der Website</p>
            <p class="pt-2">Beim Aufrufen unserer Website [URL der Website] werden durch den auf Ihrem Endgerät zum Einsatz kommenden Browser automatisch Informationen an den Server unserer Website gesendet. Diese Informationen werden temporär in einem sogenannten Logfile gespeichert. Folgende Informationen werden ohne Ihr Zutun erfasst und bis zur automatisierten Löschung gespeichert:</p>
            <li class="pt-2 pl-2">IP-Adresse des anfragenden Rechners</li>
            <li class="pl-2">Datum und Uhrzeit des Zugriffs</li>
            <li class="pl-2">Name und URL der abgerufenen Datei</li>
            <li class="pl-2">Website, von der aus der Zugriff erfolgt (Referrer-URL)</li>
            <li class="pl-2">verwendeter Browser und ggf. das Betriebssystem Ihres Rechners sowie der Name Ihres Access-Providers</li>
            <p class="pt-2">Die genannten Daten werden von uns zu folgenden Zwecken verarbeitet:</p>
            <li class="pt-2 pl-2">Gewährleistung eines reibungslosen Verbindungsaufbaus der Website,</li>
            <li class="pl-2">Gewährleistung einer komfortablen Nutzung unserer Website,</li>
            <li class="pl-2">Auswertung der Systemsicherheit und -stabilität sowie</li>
            <li class="pl-2">zu weiteren administrativen Zwecken.</li>
            <p class="pt-2">Die Rechtsgrundlage für die Datenverarbeitung ist Art. 6 Abs. 1 S. 1 lit. f DSGVO. Unser berechtigtes Interesse folgt aus den oben aufgelisteten Zwecken.</p>
            <p class="pt-2 font-bold">b) Bei Anmeldung für unseren Newsletter</p>
            <p class="pt-2">Sofern Sie nach Art. 6 Abs. 1 S. 1 lit. a DSGVO ausdrücklich eingewilligt haben, verwenden wir Ihre E-Mail-Adresse, um Ihnen regelmäßig unseren Newsletter zu übersenden. Für den Empfang des Newsletters ist die Angabe einer E-Mail-Adresse ausreichend.</p>
            <p class="pt-2">Die Abmeldung ist jederzeit möglich, zum Beispiel über einen Link am Ende eines jeden Newsletters. Alternativ können Sie Ihren Abmeldewunsch auch jederzeit an shopcore.info@gmail.com per E-Mail senden.</p>
            <p class="pt-2 font-bold">c) Bei Nutzung unseres Kontaktformulars</p>
            <p class="pt-2">Bei Fragen jeglicher Art bieten wir Ihnen die Möglichkeit, mit uns über ein auf der Website bereitgestelltes Formular Kontakt aufzunehmen. Dabei ist die Angabe einer gültigen E-Mail-Adresse erforderlich, damit wir wissen, von wem die Anfrage stammt und um diese beantworten zu können. Weitere Angaben können freiwillig getätigt werden.</p>
            <p class="pt-2">Die Datenverarbeitung zum Zwecke der Kontaktaufnahme mit uns erfolgt nach Art. 6 Abs. 1 S. 1 lit. a DSGVO auf Grundlage Ihrer freiwillig erteilten Einwilligung.</p>
            <p class="font-bold text-xl pt-2">3. Weitergabe von Daten</p>
            <p class="pt-2">Eine Übermittlung Ihrer persönlichen Daten an Dritte zu anderen als den im Folgenden aufgeführten Zwecken findet nicht statt. Wir geben Ihre persönlichen Daten nur an Dritte weiter, wenn:</p>
            <li class="pt-2 pl-2">Sie Ihre nach Art. 6 Abs. 1 S. 1 lit. a DSGVO ausdrückliche Einwilligung dazu erteilt haben,</li>
            <li class="pl-2">die Weitergabe nach Art. 6 Abs. 1 S. 1 lit. f DSGVO zur Geltendmachung, Ausübung oder Verteidigung von Rechtsansprüchen erforderlich ist und kein Grund zur Annahme besteht, dass Sie ein überwiegendes schutzwürdiges Interesse an der Nichtweitergabe Ihrer Daten haben,</li>
            <li class="pl-2">für den Fall, dass für die Weitergabe nach Art. 6 Abs. 1 S. 1 lit. c DSGVO eine gesetzliche Verpflichtung besteht, sowie</li>
            <li class="pl-2">dies gesetzlich zulässig und nach Art. 6 Abs. 1 S. 1 lit. b DSGVO für die Abwicklung von Vertragsverhältnissen mit Ihnen erforderlich ist.</li>
            <p class="font-bold text-xl pt-2">4. Cookies</p>
            <p class="pt-2">Wir setzen auf unserer Seite Cookies ein. Hierbei handelt es sich um kleine Dateien, die Ihr Browser automatisch erstellt und die auf Ihrem Endgerät gespeichert werden, wenn Sie unsere Seite besuchen. Cookies richten auf Ihrem Endgerät keinen Schaden an, enthalten keine Viren, Trojaner oder sonstige Schadsoftware.</p>
            <p class="font-bold text-xl pt-2">5. Betroffenenrechte</p>
            <p class="pt-2">Sie haben das Recht:</p>
            <li class="pl-2">gemäß Art. 15 DSGVO Auskunft über Ihre von uns verarbeiteten personenbezogenen Daten zu verlangen,</li>
            <li class="pl-2">gemäß Art. 16 DSGVO unverzüglich die Berichtigung unrichtiger oder Vervollständigung Ihrer bei uns gespeicherten personenbezogenen Daten zu verlangen,</li>
            <li class="pl-2">gemäß Art. 17 DSGVO die Löschung Ihrer bei uns gespeicherten personenbezogenen Daten zu verlangen,</li>
            <li class="pl-2">gemäß Art. 18 DSGVO die Einschränkung der Verarbeitung Ihrer personenbezogenen Daten zu verlangen,</li>
            <li class="pl-2">gemäß Art. 20 DSGVO Ihre personenbezogenen Daten, die Sie uns bereitgestellt haben, in einem strukturierten, gängigen und maschinenlesebaren Format zu erhalten oder die Übermittlung an einen anderen Verantwortlichen zu verlangen,</li>
            <li class="pl-2">gemäß Art. 7 Abs. 3 DSGVO Ihre einmal erteilte Einwilligung jederzeit gegenüber uns zu widerrufen,</li>
            <li class="pl-2">gemäß Art. 77 DSGVO sich bei einer Aufsichtsbehörde zu beschweren.</li>
            <p class="font-bold text-xl pt-2">6. Widerspruchsrecht</p>
            <p class="pt-2">Sofern Ihre personenbezogenen Daten auf Grundlage von berechtigten Interessen gemäß Art. 6 Abs. 1 S. 1 lit. f DSGVO verarbeitet werden, haben Sie das Recht, Widerspruch gegen die Verarbeitung Ihrer personenbezogenen Daten einzulegen, soweit dafür Gründe vorliegen, die sich aus Ihrer besonderen Situation ergeben.</p>
            <p class="font-bold text-xl pt-2">7. Datensicherheit</p>
            <p class="pt-2">Wir verwenden innerhalb des Website-Besuchs das verbreitete SSL-Verfahren (Secure Socket Layer) in Verbindung mit der jeweils höchsten Verschlüsselungsstufe, die von Ihrem Browser unterstützt wird.</p>
            <p class="font-bold text-xl pt-2">8. Aktualität und Änderung dieser Datenschutzerklärung</p>
            <p class="pt-2">Diese Datenschutzerklärung ist aktuell gültig und hat den Stand [Datum]. Durch die Weiterentwicklung unserer Website oder aufgrund geänderter gesetzlicher beziehungsweise behördlicher Vorgaben kann es notwendig werden, diese Datenschutzerklärung zu ändern.</p>
        </div>
    </div>
    
    <div id="cancellation" class="m-5 pb-2 md:m-10">
        <h1 class="text-2xl font-bold pb-2">Cancellation Policy (Stornierungsbedingungen)</h1>
        <div class="bg-gray-200 rounded-xl shadow-lg flex flex-col space-y-4 md:space-y-0 relative p-4">
            <p class="font-bold text-xl pt-2">1. Allgemeine Stornierungsbedingungen</p>
            <p class="pt-2">1.1. Eine Stornierung Ihrer Bestellung ist bis zu 72 Stunden nach Abschluss der Bestellung kostenfrei möglich, sofern die Ware noch nicht versendet wurde.</p>
            <p class="pt-2">1.2. Nach Ablauf dieser Frist behalten wir uns vor, eine Stornierungsgebühr in Höhe von 20 % des Kaufpreises zu erheben, um entstandene Bearbeitungskosten zu decken.</p>
            <p class="font-bold text-xl pt-2">2. Stornierungsbedingungen für spezielle Produkte oder Dienstleistungen</p>
            <p class="pt-2">2.1. Bei speziell für den Kunden angefertigten Produkten oder personalisierten Artikeln ist eine Stornierung nach Produktionsbeginn ausgeschlossen. In diesem Fall wird der gesamte Kaufpreis fällig.</p>
            <p class="pt-2">2.2. Dienstleistungen, die in Absprache mit dem Kunden terminiert sind, können bis z. B. 72 Stunden vor dem Termin kostenfrei storniert werden. Bei einer Stornierung zu einem späteren Zeitpunkt behalten wir uns vor, 50 % des Dienstleistungspreises als Ausfallgebühr in Rechnung zu stellen.</p>
            <p class="font-bold text-xl pt-2">3. Rückerstattung</p>
            <p class="pt-2">3.1. Im Falle einer rechtzeitigen und gültigen Stornierung erstatten wir bereits geleistete Zahlungen innerhalb von [z. B. 14 Tagen] nach Eingang der Stornierungsanfrage auf dasselbe Zahlungsmittel, das Sie für die ursprüngliche Transaktion verwendet haben.</p>
            <p class="pt-2">3.2. Sollte die Ware bereits versandt worden sein, können Stornierungen erst nach Rücksendung und Eingang der Ware bei uns bearbeitet werden. In diesem Fall gelten die Bedingungen unseres Widerrufsrechts.</p>
            <p class="font-bold text-xl pt-2">4. Sonderfälle</p>
            <p class="pt-2">4.1. Für Angebote und reduzierte Ware ist eine Stornierung nach Bestellabschluss nur nach besonderer Absprache möglich, die jedoch nicht garantiert werden kann.</p>
            <p class="pt-2">4.2. In Fällen höherer Gewalt (z. B. Naturkatastrophen, Pandemien) behalten wir uns das Recht vor, gesonderte Stornierungsregelungen zu definieren und bekannt zu geben.</p>
            <p class="font-bold text-xl pt-2">5. Kontakt für Stornierungsanfragen</p>
            <p class="pt-2">Für alle Anfragen zu Stornierungen oder weiteren Informationen zu unseren Stornierungsbedingungen kontaktieren Sie bitte unseren Kundenservice unter:</p>
            <p class="pt-3 pl-2">shopcore.info@gmail.com</p>
            <p class="pt-2 pl-2">0157 1234567</p>
            <p class="pt-2 pl-2">Alteburgstraße 150, 72762 Reutlingen</p>
        </div>
    </div>
</div>

<Footer/>