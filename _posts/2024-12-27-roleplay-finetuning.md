---
layout: post
title: LeMoNPC
date: 2024-12-27 18:00:00
description: Un framework per convertire personaggi in Language Models
tags: llm ai roleplay
categories: [llm, roleplay]
featured: true
thumbnail: /assets/img/limone32_bordo_colorato.png
tabs: true
---

## Cos'è LeMoNPC?

LeMoNPC (**L**anguage **M**odel **N**on-**P**layable **C**haracter) è un progetto che si pone come obiettivo la creazione automatica di NPC (Non-Playable Character), personaggi che all'interno di un videogioco comunicano con il giocatore.

Un NPC ha un ruolo più o meno importante all'interno della struttura del gioco, in quanto può:

- spiegare e portare avanti la trama principale del gioco
- spostare l'attenzione del giocatore su una sotto-trama secondaria
- dare missioni al giocatore

L'obiettivo di questo framework è quello di dare a scrittori di storie e personaggi un tool per rendere "vivi" i loro personaggi.
**LeMoNPC** si occuperà di **raccogliere le informazioni** su loro, **finetunare un LLM** (Large Language Model) per imparare a rispondere come loro, **gestire le memorie** del mondo di gioco e così via.

Una volta pronto, questo LLM potrebbe essere usato per avere delle risposte personalizzate in tempo reale in una campagna di Dungeon&Dragons. Oppure essere integrato all'interno di un videogioco, in cui gli utenti possono scrivere quello che vogliono ai personaggi. O ancora semplicemente avere un personaggio con cui chiacchierare e fare delle domande. Tutto questo seguendo la visione originale che il designer aveva per il personaggio.
Questo può permettere di scrivere personaggi che non vivono su binari prefissati, ma che possono reagire a qualsiasi tipo di input.

In questo post presenterò un primo prototipo di **LeMoNPC**, sviluppato in poco tempo come proof-of-concept e sfida personale. Per testare il framework, ho utilizzato dei Large Language Model per generare sia il personaggio (Orlando Marlo, un nobile del Regno di Luminaria) che un dataset di conversazioni che lo riguardano. L'obiettivo finale è quello di distillare queste informazioni, generate con modelli molto espressivi ma pesanti, in un modello molto più leggero e utilizzabile.

In questo post vedremo:

- Le principali difficoltà tecniche
- Il processo di creazione del personaggio e del suo mondo
- La generazione del dataset di conversazioni del personaggio
- L'allenamento di LeMoNPC per replicare il comportamento del personaggio

## Cosa non è LeMoNPC

Questo non è un framework per generare automaticamente personaggi. Non è un'interfaccia che crea un personaggio da un prompt generico.
L'obiettivo è partire da un personaggio già creato. Deve avere una storia, un mondo originale, esempi di conversazioni, opinioni.

Il focus di questo post è sulle tecniche per creare un NPC digitale, quindi ho utilizzato degli LLM per generare il mio personaggio base. Vedremo che in alcuni casi questo ha influito negativamente su alcuni risultati, e la mia supervisione è stata comunque necessaria.

## Perché LeMoNPC?

Nonostante ChatGPT sia stato rilasciato alla fine del 2022, non sono presenti sul mercato videogiochi mainstream che implementano questa tecnologia (se tralasciamo la pila di applicazioni di _fidanzate AI_).
Questo è dovuto al fatto che questa tecnologia utilizza molte risorse computazionali ed economiche.

Nel caso di LLM **closed-source** (gestiti a porte chiuse dalle aziende produttrici), l'utilizzo è pagato con una tariffa proporzionale alla quantità di testo generato. Utilizzare questi modelli obbligherebbe allo sviluppo di giochi live-service, con una monetizzazione molto aggressiva che serve a coprire i costi.

Nel caso di modelli **open-source** (scaricabili e utilizzabili sulla propria macchina locale), il problema principale è legato alle loro dimensioni.
L'hardware che li ospita deve:

- essere abbastanza potente per generare testo ad una velocità ragionevole;
- avere abbastanza memoria per ospitare il modello.

La [Nvidia RTX 1060](https://www.nvidia.com/it-it/geforce/10-series/) è probabilmente una delle schede video più comprate di sempre. Uscita nel 2016, è già un pezzo di hardware abbastanza vecchiotto, e comunque farebbe fatica a ospitare anche i modelli più piccoli: un modello può essere compresso in 4 GB di VRAM con molti sacrifici, e questa scheda è spesso venduta con 6 GB di VRAM.
L'utilizzo di così tante risorse mette anche grandi limiti al tipo di gioco che può essere sviluppato, visto che il Language Model entra in competizione con la logica del gioco, la pipeline di rendering e eventuali intelligenze artificiali.
Inoltre, non tutti i giocatori hanno a disposizione un computer con una scheda grafica.

Un altro problema degli LLM (sia closed che open) è che presentano un **moralismo** corporate abbastanza spiccio, danneggiando la loro capacità di roleplay.
La tragica conseguenza è una generale sensazione di cringe dell'utente (molto frequentemente questi modelli si comportano da bacchettoni) e un alto livello di **refusal**, ovvero la predisposizione a rifiutarsi a parlare di alcuni argomenti. Questo è un problema nel caso un NPC volesse anche banalmente parlare di alcol.

Il mio sogno è quello di riuscire a digitalizzare un NPC **usando tra i 200 MB e i 2GB di RAM**, senza l'utilizzo di hardware specializzato come le schede grafiche. Questo permetterebbe anche a giocatori senza una macchina particolarmente potente di poter interagire con i personaggi.

LeMoNPC deve essere in grado di produrre un LLM che si comporta come un personaggio scritto da un essere umano. L'essere umano può dare informazioni su questo personaggio, come backstory, esempi di conversazione, eventi importanti, valori, etc.
Opzionalmente, si può fornire un dataset di conversazioni del personaggio, che può essere già utilizzato per allenare un piccolo LLM. Altrimenti, LeMoNPC si occuperà di generarlo.

> _"If life gives you LeMoNs, create an NPC from your DnD character"_
>
> **Socrates, probably**

## Creazione del Personaggio

Ovviamente il primo passaggio per utilizzare LeMoNPC è avere un personaggio. In questa sezione spiego come ho generato **Orlando Marlo, Cavaliere di Luminaria**.

### Contesto Storico

La creazione del contesto storico è fondamentale per definire il palcoscenico in cui i personaggi opereranno.
Infatti, un personaggio non vive da solo nel vuoto, ma assume un certo ruolo in una società, ha delle opinioni, delle relazioni, e tanto altro.

In questo prototipo, ho generato il contesto storico utilizzando Claude Sonnet.
La generazione in sé non era male, anche se conteneva alcune frasi o espressioni che trovavo troppo corporate o generiche e che ho pulito. Ogni tanto aggiungevo io personalmente qualche dettaglio per migliorare un po' la qualità della generazione.

Il contesto storico si articola in diverse sezioni chiave:

- **Descrizione:** Una breve introduzione che offre un primo sguardo al mondo, descrivendo le sue caratteristiche principali.
- **Organizzazione Politica:** Definisce come il potere è strutturato e distribuito all'interno del contesto. Questa sezione definisce i meccanismi di governo e le dinamiche di potere che influenzeranno le scelte e le azioni dei personaggi.
- **Entità di Potere:** Le organizzazioni o individui che detengono il controllo politico ed economico, influenzando la vita quotidiana degli abitanti del mondo.
- **Persone Importanti:** Figure chiave della società, individuate per il loro ruolo sociale, culturale o politico. Queste figure possono offrire spunti interessanti per dialoghi e interazioni con il personaggio.
- **Entità Marginalizzate:** Chi vive ai margini del sistema, spesso oppresso o svantaggiato rispetto ai gruppi dominanti. La loro presenza aggiunge profondità al mondo, evidenziando le disuguaglianze e le tensioni sociali e rendendo un po' più tridimensionale l'ambientazione.
- **Persone Importanti Marginalizzate:** Simili alle persone importanti, ma appartengono a gruppi che si oppongono al sistema dominante, in cerca di rivalsa contro un sistema che li ha scartati e li opprime.

Nel mio caso, ho creato il **Sacro Regno di Luminaria**, una monarchia che condivide il potere con la Chiesa. La legittimità del regno dipende dalla percezione che i suoi sovrani siano stati scelti da Solaris, la divinità venerata nel regno. Il governo ha un sistema di doppio potere, dove le decisioni importanti richiedono l'approvazione sia della Corona che del Concilio Solare. Molti gruppi sono marginalizzati o oppressi, tra cui coloro che vengono considerati non favoriti da Solaris e i praticanti delle tradizioni pre-Solaris.

### Personaggio

Una volta creato il contesto, si può procedere con il personaggio, che ha:

- **Backstory:** Una breve panoramica del passato del personaggio, contenente eventi importanti che hanno plasmato la sua personalità e le sue scelte.
- **Allineamento:** [Un sistema semplificato per categorizzare il personaggio](https://dungeonedraghi.it/regole/personaggio/allineamento/) in base alla sua posizione sociale, alle sue convinzioni morali e al suo atteggiamento nei confronti dell'autorità. Questo elemento aiuta a definire i suoi legami con gli altri personaggi e la società nel suo complesso.
- **Valori:** Una lista di principi fondamentali che guidano le azioni e le decisioni del personaggio. Questi valori sono cruciali per creare un personaggio autentico e credibile.
- **Obiettivi:** Cosa spinge il personaggio a agire? Quali sono i suoi desideri, le sue aspirazioni e i suoi sogni? I suoi obiettivi forniscono una direzione alla sua vita e lo spingono ad interagire con gli altri personaggi e con l'ambiente circostante.
- **Opinioni:** Una serie di posizioni assunte dal personaggio su diversi argomenti. Le opinioni riflettono il suo punto di vista sul mondo, le sue convinzioni e i suoi valori, contribuendo a renderlo un individuo complesso e sfaccettato.

In questo modo ho generato **Orlando Marlo, un nobile del regno di Luminaria**. Fervente credente, disprezza la corruzione presente all'interno del regno, in quanto capisce che la religione in cui ha posto la fede è utilizzata dagli altri come leva di potere. Vuole cambiare il sistema dall'interno diventando Ciambellano. E' un uomo onorevole e molto rispettato, che prova attivamente a costruire un mondo migliore. E' convinto che chiunque possa essere salvato, ma questa convinzione lo rende paternalista nei confronti di chi non condivide la sua fede.

Nelle schede qua sotto è riportato l'intero personaggio.

{% tabs orlando-marlo %}

{% tab orlando-marlo Origin Story %}

> Born into the noble house of Marlo, Orlando grew up witnessing both the splendor and corruption within Luminara's halls of power. As a child, he experienced a profound spiritual moment when sunlight streamed through the Great Cathedral's stained glass during his knighting ceremony, filling him with genuine divine purpose. Unlike many nobles who saw faith as a path to power, Orlando's connection to Solaris became deeply personal and sincere. His father's deathbed confession about the corruption he witnessed as a Crown Council member strengthened Orlando's resolve to serve both crown and faith with true righteousness.
> {% endtab %}

{% tab orlando-marlo Values %}

> - Genuine religious devotion and spiritual purity
> - Justice tempered with mercy
> - Protection of the weak, regardless of their social status
> - Honesty and transparency in governance
> - Balance between secular law and divine guidance
> - Personal integrity over political advantage
> - Duty to both crown and faith
>   {% endtab %}

{% tab orlando-marlo Alignment %}

> Lawful Good
> {% endtab %}

{% tab orlando-marlo Objectives %}

> - Ascend to the position of Chancellor to influence royal policy
> - Reform the relationship between church and state to serve the people rather than power
> - Create a more equitable system for the marginalized while working within existing structures
> - Prove that true faith and effective governance can coexist without corruption
> - Build bridges between the privileged and the Unblessed through official channels
> - Establish transparency in both Crown Council and Solar Conclave dealings
>   {% endtab %}

{% tab orlando-marlo Opinions %}

> ### On the Order of Solar Truth
>
> Orlando recognizes the Order's vital role in preserving sacred knowledge and providing education to the populace - something he deeply values as a foundation of a stable society. He admires their dedication to maintaining the ancient texts and their role in bringing literacy to even remote villages. However, he is troubled by how the Order increasingly manipulates religious doctrine for political gain. Their practice of withholding certain teachings from the "Unblessed" particularly disturbs him, as he believes Solaris's light should shine on all equally. While he would never speak openly against them, he silently disapproves of how they've transformed from spiritual guides into power brokers, using their control over education to shape political narratives. He sees their current path as a corruption of their original sacred mission, though he struggles with this critique, knowing the importance of maintaining religious authority in Luminara's governance.
>
> ### On Sol's Universal Message
>
> Orlando finds profound inspiration in Sol's sermon of the Shared Dawn, where the prophet stood on Mount Luminous and proclaimed that just as the morning sun touches both palace and hovel alike, divine grace knows no walls or borders. This message resonates deeply with Orlando, who often meditates on how Sol compared human-made hierarchies to clouds that foolishly believe they can block the sun's light permanently. The knight particularly cherishes the prophet's warning that "those who claim to own the light cast the darkest shadows," seeing it as a perfect metaphor for the current corruption in Luminara's institutions. When alone in the castle gardens at sunrise, Orlando often recreates Sol's famous gesture of open arms toward the sun, reflecting on how this simple yet powerful truth about universal divine love has been twisted by those who claim to be its guardians. The contradiction between Sol's original teachings and the current practice of marking some as "Unblessed" represents, to Orlando, the greatest betrayal of their prophet's vision.

{% endtab %}

{% endtabs %}

## Modellazione

Tutto quello che è stato discusso fino ad adesso riguarda il tipo di dati e informazioni che il designer del personaggio deve fornire.

Una volta raccolte queste informazioni, può iniziare l'allenamento dell'LLM.
La prima cosa da fare è la creazione di un dataset di conversazioni del personaggio.
Idealmente anche queste dovrebbero essere fornite dal designer.

### Generazione delle domande

Per generare delle domande, ho deciso di utilizzare Gemma2 2B, un modello di Google di dimensioni abbastanza ridotte con capacità dignitose.
Non ho scelto un modello più grande poiché dalle prove sembrava funzionare bene.

Per qualsiasi tipo di generazione, bisogna creare un prompt per Gemma, ovvero delle istruzioni che il modello deve seguire.
Un prompt include:

- **Persona**: chi è il modello e che personalità deve avere.
- **Istruzioni**: cosa deve fare il modello.
- **Esempi**: opzionali, sono degli esempi da mostrare al modello per condizionare meglio la generazione.

```python
from dataclasses import dataclass
from typing import List

@dataclass
class GenerativePrompt:
    persona: str
    instruction: str
    examples: List[str]
```

Per generare le domande, ho adottato un approccio che introduce variabilità attraverso personaggi casuali. Ho creato una decina di personaggi con descrizioni abbastanza scarne (ad esempio **"Elena Solwind, royal historian, scholarly and reserved"**).

Per aumentare ulteriormente la variabilità nelle interazioni, ho aggiunto:

- Un'emozione casuale assegnata al personaggio per ogni conversazione
- Un contesto situazionale che include:
  - Il luogo dell'incontro
  - Il motivo dell'interazione
  - Il livello di intimità tra i personaggi

Nelle sezione **instruction** ho inserito:

- La backstory completa di Orlando Marlo
- Opzionalmente, una delle sue opinioni
- I dettagli contestuali generati

Questo approccio permette di ottenere domande che variano naturalmente in base al background del personaggio (uno storico porrà domande diverse da un capo gilda) e al rapporto che il personaggio ha con Orlando.

Ecco un esempio di prompt:

> You are **Elena Solwind, royal historian, scholarly and reserved**. You are feeling **calm**.
>
> You will be given some information about me. I'm a character from a fantasy world.
>
> _..._
>
> _... backstory di Orlando Marlo ..._
>
> _..._
>
> **Meeting location**: The Great Cathedral of Solaris
>
> **Meeting reason**: delivering urgent message
>
> **Knowledge of my background**: high
>
> We are going to have a conversation. You will ask me a question.We are having a direct conversation. Do not use indirect speech.
>
> ...
> _examples of questions_
> ...

Ora che ho completato questo progetto, posso dire che non sono particolarmente soddisfatto delle domande generate. Il modello Gemma2 2B ha mostrato una tendenza a produrre output verbosi e poco naturali, spesso premettendo un riassunto completo della backstory di Orlando prima di formulare la domanda vera e propria.
Questa performance sub-ottimale potrebbe essere attribuita a diverse cause:

- **Un sovraccarico informativo nel prompt**, con la backstory completa che potrebbe aver "distratto" il modello dal suo obiettivo principale
- **Le limitazioni strutturali di Gemma2B**, che non supporta un prompt di sistema separato, costringendo a includere tutte le istruzioni nel messaggio dell'utente
- **Possibili inefficienze nella struttura del prompt stesso** che non ho avuto modo di perfezionare

{% tabs group-name %}

{% tab group-name Elena Solwind %}

> **Elena Solwind, royal historian, scholarly and reserved**, meeting in **Healing Sanctuaries**:
>
> Orlando Marlo... a name well-known even amongst those who reside outside the realm of Luminara's grandeur. Tell me, what is your assessment of Seraphina's vision regarding the kingdom's future? Do you believe her words carry an inherent warning or merely political commentary?

{% endtab %}

{% tab group-name Isabella Stormwind %}

> **Commander Isabella Stormwind, border patrol leader, pragmatic and direct**, meeting in **Marlo Family Estate**:
>
> Orlando Marlo. I hear whispers of your family, their long history intertwined with this land. But what drove them - specifically _you_ - towards a life dedicated to upholding both Solaris and the crown?

{% endtab %}

{% endtabs %}

### Generazione delle risposte

Il processo di generazione delle risposte segue un approccio simile alla generazione delle domande. In questo caso ho usato Llama3.1 8B (quantizzato a 4 bit).

Per la **persona**, ho utilizzato Orlando Marlo includendo:

- La sua backstory completa
- Una serie di motti e frasi ricorrenti tipiche del personaggio (non tanto per caratterizzarlo, quanto per verificare se il modello riesce a imparare questi pattern dopo l'allenamento)

Il processo di generazione è semplice:

- Il messaggio dell'utente è la domanda generata nello step precedente
- Il modello risponde nei panni di Orlando

Gli esempi di risposte in questa fase sono stati cruciali per catturare la personalità di Orlando.
Sono stati selezionati con un processo iterativo:

1. Selezione di una domanda casuale dal dataset.
2. Valutazione della risposta generata da Orlando.
3. Modifica della risposta per ridurre elementi generici e enfatizzare lo stile caratteristico del personaggio
4. Aggiunta della risposta modificata al set di esempi per migliorare le generazioni successive

Ecco un esempio del prompt, prima di essere riempito con le variabili importanti.
{% raw %}

```python
"""
{% persona %}

{% instruction %}

You are talking with: {% character %}

Meeting location: {% location %}

{% if examples %}
Here's some examples of past conversations between you and other characters.
Use this examples as a style guide.
{% for example in examples %}
## Example {loop.index}
{example}
{% endfor %}
{% endif %}

Use only direct speech. No description of tone.
Answer the question referencing the information about you that you know.
Don't introduce yourself.
Don't be cringe, you are having a conversation with a real person.
"""
```

{% endraw %}

## Allenamento

Ho scelto di utilizzare [SmolLM2](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct), uno dei modelli linguistici più compatti disponibili, per questo esperimento. Esiste in tre varianti (135M, 360M e 1.7B parametri) e ho optato per la versione da 135M. Il modello ha un contesto di 2048 token, una limitazione accettabile per questo test, ma che potrebbe diventare problematica per future conversazioni multi-turno.

L'obiettivo era finetunare il modello sul dataset di circa mille esempi generati precedentemente. Durante i primi tentativi ho scoperto un problema interessante specifico di questi modelli: il token di PAD (usato per uniformare la lunghezza delle sequenze) coincide con il token EOS (fine sequenza). Questo causa un comportamento indesiderato, in cui il modello "dimentica" come terminare le risposte e non smette mai di parlare.

Per l'allenamento ho utilizzato [TRL](https://github.com/huggingface/trl) con i seguenti parametri:

- **learning rate**: 5e-5 (volutamente conservativo)
- **epoche**: 5 (il modello migliore è stato quello della quarta epoca)

Un'ottimizzazione importante è stata l'utilizzo dei [Liger Kernel](https://github.com/linkedin/Liger-Kernel), che mi hanno permesso di raddoppiare la batch size da 4 a 8, riducendo significativamente i tempi di training grazie a una gestione più efficiente della memoria.
Ho sperimentato con due approcci diversi:

1. **Includendo la backstory di Orlando nel contesto di training**: l'allenamento è molto più rapido in quanto tutte le informazioni sono già presenti nel prompt
2. **Senza includere informazioni specifiche nel contesto**: la loss del modello è più alta, in quanto il modello ha dovuto imparare implicitamente le informazioni su Orlando. Il vantaggio di questo approccio è che il contesto è molto più compatto e può quindi essere usato per codificare altre conversazioni.

Le prove sul modello allenato hanno mostrato risultati interessanti: riesce a utilizzare correttamente le frasi caratteristiche di Orlando e mantiene una buona coerenza quando risponde a domande simili a quelle del training. Tuttavia, emerge un limite significativo quando il modello si trova di fronte a domande che si discostano troppo dal dataset di allenamento - in questi casi tende a ignorare la domanda e a ripetere informazioni su se stesso in modo poco naturale.

Queste osservazioni suggeriscono due direzioni principali per migliorare il sistema: da un lato, sarà fondamentale espandere la varietà del dataset di training per coprire un range più ampio di possibili interazioni. Dall'altro, sarà cruciale ridurre la dipendenza da conversazioni generate automaticamente e incorporare invece più esempi di dialoghi creati da esseri umani, che tipicamente presentano sfumature e complessità difficili da replicare attraverso la generazione automatica.

## Conclusioni e Sviluppi Futuri

Questo primo prototipo di LeMoNPC è stata per me più una scusa per sperimentare con la generazione sintetica di dati, modellare un LLM per fare roleplay e infine per mettere le mani in pasta facendo un finetuning.

La generazione automatica delle domande ha mostrato diverse limitazioni, probabilmente dovute ad un cattivo prompt engineering. In futuro dovrò trovare un modo migliore per modellare questo aspetto.
Sono invece rimasto molto stupito dalla capacità di Llama3.1 di fare roleplay e generare delle risposte abbastanza coerenti.
Di sicuro la vera qualità verrà da dati creati e curati da esseri umani.

Per quel che riguarda il finetuning, lo considero un successo. È vero che fuori distribuzione il modello risponde in maniera strana, ma questo è più un problema sui dati che sul modello. In futuro mi piacerebbe applicare Direct Preference Optimization (DPO) per rafforzare il training. Ovviamente questo complicherà in maniera aggiuntiva la raccolta di un dataset, ma di sicuro sarà divertente.
