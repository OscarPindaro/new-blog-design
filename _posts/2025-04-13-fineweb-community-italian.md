---
layout: post
title: Fineweb-Community - Analisi e Estrazione Topic
date: 2025-02-23 18:00:00
description: Un framework per convertire personaggi in Language Models
tags: llm ai transformers gen-ai
categories: [llm, transformers, generative-ai]
featured: true
toc:
  sidebar: left
tabs: true
thumbnail: /assets/img/limone32_bordo_colorato.png
pretty_table: true
related_publications: true
summary: "Uno studio su Fineweb-C, il dataset per la community di HuggingFace che permette di avere dati di qualità in ogni lingua"
---
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>

Allo stato attuale, la lingua principale parlata dagli LLM è l'inglese, mentre altre lingue sono molto più marginali e spesso trascurate dai creatori di modelli.

La tabella qua sotto riporta il numero di dataset e modelli NLP disponibili attualmente su [HuggingFace](https://huggingface.co/).
Ovviamente, la lingua inglese regna su tutti, con più di 15 mila dataset e 150 mila modelli allenati su diversi domini (generale, biomedico, legale, etc.).
La lingua italiana vede invece una rappresentazione molto più magra, addirittura sotto tutte le altre principali lingue europee.

| Lingua   |  Dataset   |   Modelli   |
| :------- | :--------: | :---------: |
| Italiano |    660     |    6,254    |
| Inglese  | **16,746** | **154,599** |
| Francese |   1,404    |    8,951    |
| Spagnolo |   1,167    |    8,092    |
| Tedesco  |    943     |    8,004    |

I grandi modelli privati (come ChatGPT e Claude) conversano abbastanza agilmente in italiano, mentre quelli open-source sono ancora acerbi. In particolare, manca una buona alternativa computazionalmente efficiente che possa conversare in italiano su hardware modesti.

La penuria di dataset open in lingua italiana rende lo sviluppo di modelli migliori poco conveniente e razionale, e le BigTech come Meta, Google e OpenAI preferiscono ottimizzare e sviluppare sulla lingua più parlata in Occidente.

## Fineweb-Edu

Nel maggio 2024 HuggingFace ha rilasciato Fineweb, un dataset di 15 trilioni (!!!) di token in lingua inglese.
Il dataset è stato creato a partire da [CommonCrawl](https://commoncrawl.org/), un dump di tutti i contenuti presenti su internet fino a quel momento.
Questo dataset contiene il codice sorgente di moltissime pagine web, e quindi HuggingFace ha dovuto innanzitutto trasformarlo in un formato leggibile da LLM e esseri umani.

Tuttavia, non basta avere accesso a questi dati. Internet infatti è pieno di siti web spam, di bassa qualità, generati automaticamente, e così via.
Nel report è riportato dettagliatamente come HuggingFace ha ripulito il dataset originario, concentrandosi su due aspetti principali:

- **Deduplicazione**: è un processo che si occupa di scartare contenuto ridondante. Questo viene fatto per evitare che contenuti presenti in molte copie monopolizzino i parametri dei modelli durante l'allenamento;
- **Qualità**: parte del contenuto risulta avere problemi di formattazione, testo generato automaticamente da bot, miscugli di lingue incoerenti. Questi campioni devono essere buttati visto che avrebbero su qualsiasi training un contributo estremamente negativo.

Insieme a questo dataset, è stata anche pubblicata una sotto-porzione di 1.3 trilioni di token chiamata [Fineweb-Edu](https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu).
Questo dataset ha un focus su contenuti educativi, come blogpost, paper, lezioni universitarie.

Per poter estrarre questi campioni di alta qualità, HuggingFace ha annotato un subset di Fineweb con Llama3-70B-Instruct, dividendo i campioni per contenuto e qualità informativa.
Da queste annotazioni ha costruito poi un classificatore molto più snello e rapido che si occupa di classificare su larga scala il resto del dataset.

La lingua principale di Llama è l'inglese, e quindi questo filtraggio non funziona molto bene su campioni in altre lingue, in quanto le performance di classificazione sarebbero molto più basse.

Per superare questa limitazione dei modelli generativi attuali, è stato quindi creato Fineweb-C.

## Fineweb-C

[Fineweb-C](https://huggingface.co/datasets/data-is-better-together/fineweb-c) può essere considerato il naturale passo successivo a FineWeb, estendendo l'analisi fatta in precedenza su tutte le restanti lingue (compreso il napoletano).
L'idea di base è sempre la stessa: trovare un modo per distinguere campioni di bassa qualità da campioni informativi. Se in FineWeb si usava un LLM, per questo dataset invece HuggingFace ha chiesto aiuto alla community. Per ogni lingua sono stati estratti 1000 campioni, che sono stati e stanno venendo annotati da dei volontari fluenti in quella lingua.

In particolare, gli annotatori devono classificare i campioni nelle seguenti classi:

- **None**: il campione non ha alcun contenuto informativo. Può essere pubblicità, spam, un post su un social che non parla di niente di particolare, news di gossip;
- **Minimal**: il campione contiene un contenuto informativo molto minimo, come ad esempio un articolo di giornale che parla di un particolare evento senza dilungarsi troppo;
- **Basic**: il campione ha un principio di intento educativo, come una definizione, una breve spiegazione;
- **Good**: il testo è una spiegazione abbastanza dettagliata, anche ben formattata. La maggior parte dei concetti sono esposti chiaramente;
- **Excellent**: il testo è di qualità sopraffina, molto ben formattato. Un esempio potrebbe essere un blogpost molto tecnico oppure una dispensa universitaria;
- **Problematic Content**: questa è una categoria ombrello in cui finiscono tutti quei test formattati male, oppure spam, pornografia, materiale sensibile, etc.

Lo split italiano è stato, ad oggi, annotato da 26 annotatori. Io personalmente ho contribuito annotando circa 400 campioni.
Questi 1000 campioni sono stati pescati casualmente dal dataset originale, pre-filtrando materiale problematico. Devo dire che la pipeline di pre-filtraggio ha funzionato molto bene, visto che non mi è capitato quasi mai di trovare campioni imbarazzanti. Ho letto che non è stato così semplice in altri casi, specialmente per le lingue del sud-est asiatico, in cui la pipeline ha fatto passare moltissimo contenuto esplicito.

### Perché è importante

Come già detto prima, l'Italiano è una lingua molto poco rappresentata.
Quando cerco modelli per il lavoro di tutti i giorni, sono sempre costretto a scegliere LLM generici allenati su dataset che iniziano a mostrare i segni del tempo.
Provo una grande invidia per chi sviluppa in inglese, che ha addirittura classificatori e retriever già pronti per il campo medico o altri campi estremamente specifici.

### Criticità

Mi sembra onesto parlare anche dei punti un po' più dolorosi della questione.
Mentre annotavo il dataset, ho avuto il sospetto di star leggendo materiale coperto da copyright.
La proprietà intellettuale è sempre un argomento caldo su cui c'è molta ipocrisia. Ci si interessa solo se si è vittime del fenomeno, mentre è facile ignorarlo se non si è un creatore di contenuti. Questo è ovviamente un tema molto ampio che inizia da ben prima dell'avvento dell'AI generativa.

Probabilmente cambierò idea altre 100 volte su questo. Attualmente penso che la natura open di questo progetto lo allevia un po' dalle inevitabili colpe di cui si macchierà quando verrà scalato sull'intero dataset. Spero però che parlandone il grande pubblico possa iniziare a capire un po' meglio l'origine di questi dati e inizi una conversazione attorno a questo argomento.

C'è poi ovviamente tutto un tema secondario sul fatto che i modelli generativi vengono utilizzati molto per generare fake news e scam. Di sicuro rendere gli LLM fluenti in multiple lingue aumenterà il raggio di questa piaga, ma almeno per design questo dataset prova a raccogliere campioni con contenuto educativo.

## Analisi del dataset

Mentre annotavo il dataset, mi è sembrato che i campioni di alta qualità fossero soprattutto in ambito teologico e politico.
Ho infatti trovato molti testi estratti dal Catechismo e da riflessioni sul capitale di Marx.

Per questo motivo, ho deciso di fare un'analisi del dataset per vedere la distribuzione dei topic.
L'analisi è strutturata nel seguente modo:

1. estrazioni di parole chiave dal testo;
2. utilizzo di un LLM per estrarre un topic generale;
3. visualizzazione dei dati e considerazioni.

Il codice sorgente lo trovate qua [nella mia repo](https://github.com/OscarPindaro/fineweb-c-analysis-ita).

## Estrazione delle parole chiave

Visto che ho intenzione di usare un LLM per estrarre dei topic di alto livello dal testo (come ad esempio "Moda", "Tecnologia", "Teologia"), ho deciso innanzitutto di estrarre delle parole chiave per ogni campione del dataset. Le parole chiave sono presenti all'interno dei campioni, e quindi io le considero di _basso livello_ in quanto sono spesso molto specifiche per il testo analizzato.
Questo passo è fondamentale perché mi permette:

- di conoscere meglio i contenuti del dataset;
- di capire che analisi devo fare;
- di dare informazioni aggiuntive all'LLM per aiutarlo nel suo lavoro.
  Purtroppo non sono riuscito a fare nessuno studio di ablazione che controlli quanto queste parole chiave aiutino l'LLM, ma mi sembra una intuizione ragionevole e comunque le avrei estratte in ogni caso.

Per trovare le parole chiave ho usato **TF-IDF** [(Term Frequency - Inverse Document Frequency)](https://it.wikipedia.org/wiki/Tf-idf).
L'intuizione dietro a questo algoritmo è la seguente: una parola non è importante se è molto o poco presente in termini assoluti, ma è importante se è presente solo in questo particolare campione e assente negli altri.
Questo permette di scovare per ogni documento le parole che lo identificano unicamente, considerando la loro frequenza assoluta ma anche la frequenza all'interno del singolo testo. Ad esempio, se ho due documenti diversi, uno che descrive la vita di uno scienziato, e un altro che descrive la vita dello scienziato Enrico Fermi, per entrambi la parola _scienziato_ è molto importante, ma per il secondo le parole "Enrico" e "Fermi" lo rendono unico.

Ecco degli esempi di parole chiave che ho estratto:

- dal campione 1 ho estratto le parole chiave `['fedi', 'oro', 'anello', 'fondere', 'anelli']`, quindi probabilmente parlerà di _Matrimonio_, o comunque _Religione_;
- dal campione 12 ho estratto le parole chiave `['plusvalore', 'capitale', 'produzione', 'merce', 'accumulazione']`, quindi probabilmente parlerà di _Economia_ (o di _Marxismo_).

Per questo algoritmo è molto importante fare un po' di data cleaning, rimuovendo articoli, preposizioni, numeri e altre parole ad alta frequenza ma poco interessanti.

## Estrazione dei Topic di alto livello

Una volta estratte le keyword, bisogna estrarre i topic generali. Per questi, ho deciso di utilizzare Llama3.1 quantizzato a 8 bit (`llama3.1:8b-instruct-q8_0`) e Gemma 2 (`gemma2:2b`), visto che riesco a lanciarli sulla mia **RTX 4070 12GB**. Ho anche provato a utilizzare una versione distillata di Deepseek (`deepseek-r1:8b-llama-distill-q8_0`), ma come mostrerò più avanti i tempi di calcolo erano un po' troppo lunghi e ho preferito ignorarlo.
Il prompt di sistema è strutturato nella seguente maniera:

- spiegazione delle classi di qualità di Fineweb-C;
- Indicazioni su quali informazioni il modello ha accesso (elenco di parole chiave, testo);
- Regole di categorizzazione: il modello deve dare categorie di alto livello e non specifiche. Ha accesso ad una lista di categorie pre-calcolate, ma può comunque scegliere di assegnare una nuova categoria non esistente;
- Formato dell'output: il modello deve scrivere tutto all'interno di tag xml, visto che sono semplici da parsare.

Il modello ha la libertà di scegliere una classe anche se non è presente tra quelle fornite. Questo mi permette di avere un po' di flessibilità, anche perché è un dataset che conosco poco.
Operativamente, quando il modello sceglie una classe non presente tra quelle esistenti, viene aggiunta alla lista delle classi possibili, condizionando le future generazioni.

Alla fine di questo processo, Llama ha estratto circa 142 topic. Ci sono alcuni casi in cui alcune categorie sono duplicate (singolare/plurale) ma per la visualizzazione di seguito non avrà molto peso.

Gemma invece ha estratto 94 categorie, ma ho preferito quelle estratte da Llama.

Per servire Llama e Gemma ho usato [ollama](https://ollama.com/). L'ultima versione di ollama ha introdotto il `prompt caching`, che permette di mantenere una cache delle ultime richieste fatte al modello. Nel caso di prompt molto simili tra una sessione all'altra, questa cache viene utilizzata per evitare di ricalcolare tutti i valori dell'attenzione del prompt di sistema, aumentando drammaticamente la velocità di generazione. Questo mi ha permesso di avere i topic generali in una decina di minuti. Purtroppo con DeepSeek questo vantaggio non si è presentato: poiché è un modello "reasoning", prima di dare una risposta, emette molti token di ragionamento, e il tempo di annotazione quindi è aumentato da 10 minuti a 4 ore.

Ancora una volta sono rimasto molto stupito dalle performance di Llama, mentre Gemma non mi ha reso particolarmente entusiasta.

{% details Prompt di sistema - Template Jinja %}
{% raw %}

```markdown
Sei un assistente specializzato nell'analisi e classificazione di testi in italiano. Il tuo compito è duplice:

1. Comprendere il livello qualitativo del contenuto informativo del testo, basandoti sulla seguente scala:

   - Problematic Content: contenuti inappropriati (pornografia, gambling, testo mal formattato)
   - None: assenza di contenuto informativo (es. pubblicità, post social)
   - Minimal: contenuto con minima valenza informativa non intenzionale
   - Basic: contenuto con discreto valore informativo
   - Good: contenuto ben strutturato con chiaro intento educativo
   - Basic: contenuto con elevato valore informativo e ottima strutturazione

2. Identificare una categoria tematica di alto livello che rappresenti l'argomento principale del testo.

CONTESTO OPERATIVO:

- Hai accesso a un elenco di parole chiave di basso livello estratte dal testo
- Hai accesso a un elenco di categorie tematiche già utilizzate in precedenza
- Puoi sia utilizzare categorie esistenti che crearne di nuove quando necessario

REGOLE DI CATEGORIZZAZIONE:

- Usa categorie ampie e generali (es. "Medicina", "Sport", "Tecnologia")
- Mantieni consistenza con le categorizzazioni precedenti
- Crea nuove categorie solo quando strettamente necessario
- Usa sempre singolare per le categorie (es. "Calcio" non "Calcistica")
- Usa nomi semplici e diretti (es. "Politica" non "Scienze Politiche")

OUTPUT:
Devi sempre rispondere utilizzando esclusivamente questo formato XML:
<classe="CATEGORIA" />

Dove CATEGORIA è la categoria tematica identificata.

ESEMPI DI CATEGORIZZAZIONE:

- Testi su malattie, cure, farmaci → "Medicina"
- Testi su partite, campionati → "Calcio"
- Testi su prodotti in vendita → "Pubblicità"
- Testi su smartphone, computer → "Tecnologia"
- Testi su ricette, cucina → "Gastronomia"
- Testi pubblicitari in cui singole persone promuovono il proprio lavoro-> "Autopromozione"

{% if examples%}

## Esempi

{% for ex in examples%}

### Esempio {{loop.index}}

Testo: {{ex.content}}
{% if ex.meta['quality']%}Qualità: {{ex.meta['quality']}}
{%endif%}{% if ex.meta['keywords']%}Parole Chiave: {{ex.meta['keywords']}}
{%endif%}Categoria: <classe="{{ex.meta['category']}}" />

---

{% endfor %}
{%endif%}
Categorie Esistenti:
{% for cat in categories%}

- "{{cat}}"
  {% endfor %}
  NOTA IMPORTANTE:
  Prima di creare una nuova categoria, verifica sempre se è possibile utilizzare una categoria esistente nell'elenco fornito. La creazione di nuove categorie deve essere l'ultima risorsa quando nessuna categoria esistente è appropriata.
```

{% endraw %}
{% enddetails %}

{% details Prompt dell'utente - Template Jinja %}
{% raw %}

```markdown
## Campione:

Testo: {{campione.content}}
{% if campione.meta['quality']%}Qualità: {{campione.meta['quality']}}
{%endif%}{% if campione.meta['keywords']%}Parole Chiave: {{campione.meta['keywords']}}
{%endif%}
```

{% endraw %}
{% enddetails %}

## Visualizzazione

<div class="l-page">
  <iframe src="{{ '/assets/plotly/class_distribution.html' | relative_url }}" frameborder='0' scrolling='no' height="610" width="810" style="border: 1px dashed grey;"></iframe>
</div>

Nel plot qua sopra sono riportati i 23 topic più frequenti scelti dall'LLM.
In generale il dataset contiene argomenti abbastanza variegati. E' interessante il grande numero di campioni marchiati con "Politica" (98). Questo è probabilmente dovuto al fatto che gran parte del testo consiste in articoli di giornale.
Già in questo plot si possono notare parole chiave che indicano in realtà la stessa categoria, come "Cronaca" e "Notizie".
In una futura iterazione potrebbe aver senso fissare dei topic e impedire al modello di generare topic aggiuntivi, così che possa essere catturata una migliore distribuzione.

<div class="l-page">
  <iframe src="{{ '/assets/plotly/sample_scatter.html' | relative_url }}" frameborder='0' scrolling='no' height="610" width="810" style="border: 1px dashed grey;"></iframe>
</div>

Questo scatter-plot mostra la distribuzione dei campioni rispetto ai topic a cui sono stati appaiati e rispetto alla qualità del loro contenuto informativo.
Il plot è interattivo, e si possono considerare i campioni di ogni qualità o anche un subset (magari si è interessati alla distribuzione di solo quelli con contenuto **Excellent**).

La posizione del testo all'interno del plot è calcolata utilizzando un BERT italiano. Questi modelli sono in grado di ottenere in input del testo e tradurli in un vettore di numeri, e sono utilizzati anche per modellare la similarità tra testi diversi. In generale, campioni con posizioni vicine hanno contenuto simile.
Per questo grafico in particolare, la posizione del campione dipende sia dal suo contenuto che dal suo topic.
In particolare, il vettore della visualizzazione è una combinazione convessa del vettore del contenuto e del vettore del topic.
Giocando un po' con i filtri si può notare che purtroppo la distribuzione della qualità non è migliore o peggiore attorno ad alcuni particolari topic. Al contrario, tutti i topic sembrano avere grossolanamente lo stesso rapporto di campioni di cattiva e buona qualità.

Ci sono 3 motivi per cui ho scelto di considerare nella visualizzazione non solo il contenuto, ma anche il topic.

Il primo è che per qualche motivo nel mio ambiente di sviluppo [t-SNE](https://distill.pub/2016/misread-tsne/) crasha ogni volta che provo ad utilizzarlo.
Questo algoritmo in generale dà delle buone visualizzazioni per testo e immagini, in quanto cattura relazioni non lineari tra i campioni.
Per questo, ho ripiegato sulla PCA, ma purtroppo le prima due dimensioni spiegano solo il 14% della varianza e il plot risultava essere molto confuso.
Considerare anche il topic mi permette di avere una visualizzazione più chiara e raggruppata attorno a dei "punti topici", mischiando il significato originale con quello del topic. Per mischiarli uso una combinazione convessa in cui mantengo il 40% degli embedding del contesto, assegnando il 60% ai topic.

Il secondo motivo è che non ho un BERT allenato specificatamente su questi dati e su questo task di estrazione topic. Di conseguenza le rappresentazioni non sono particolarmente ottimali, ma comunque comprendono le relazioni semantiche tra i diversi campioni.

Il terzo motivo è molto semplice: la visualizzazione risulta essere molto chiara e utile e mi ha permesso di trarre queste considerazioni.

## Conclusioni

Alla fine le mie preoccupazioni di uno sbilanciamento su _Teologia_ e _Marxismo_ si sono rivelate infondate, quindi possiamo stare certi che gli LLM allenati su questi dati saranno di ottima qualità (si scherza...).

Sono rimasto stupito dalla quantità di campioni segnati come **"Good"**, e pescandone qualcuno a caso non penso di essere d'accordo con alcuni annotatori. Se abbastanza persone annotano multiple volte lo stesso campione si potrebbero calcolare delle metriche di _agreement_ tra i diversi annotatori e trovare campioni controversi.

Sono rimasto un po' dispiaciuto dal fatto che la qualità è divisa abbastanza omogeneamente in tutto il grafico. Questo potrebbe implicare che un modello che predice la qualità avrà bisogno di ben più di 1000 campioni. Oppure, più probabilmente, implica che una visualizzazione su solo due dimensioni non riesce a catturare bene la differenza di qualità.

Spero in futuro di allenare questo classificatore, anche se devo dire che questa analisi mi ha lasciato con la pancia piena.
