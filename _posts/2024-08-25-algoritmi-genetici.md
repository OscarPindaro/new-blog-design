---
layout: post
title: Algoritmi Genetici e Le 8 Regine
date: 2024-09-30 18:00:00
description: Modellare utilizzando algoritmi genetici, applicato al problema delle 8 regine
tags: matematica code
categories: animations
featured: true
thumbnail: /assets/gif/gen_alg_eight_queens/QueenAttacking_ManimCE_v0.18.1.gif
summary: Gli _algoritmi genetici_ sono degli algoritmi il cui funzionamento si ispira al processo di _selezione naturale_, in cui gli individui di una popolazione continuano a cambiare e a riprodursi.  
---
Gli _algoritmi genetici_ sono una classe di algoritmi utilizzati per prototipare rapidamente soluzioni a problemi complessi. Il loro funzionamento si ispira al processo di _selezione naturale_, in cui gli individui di una popolazione continuano a cambiare e a riprodursi. Solo gli individui più adatti riescono a sopravvivere.

Godono di grande popolarità, in quanto il loro funzionamento è molto intuitivo e sono molto semplici da progettare e implementare. Infatti, permettono di prototipare rapidamente soluzioni di qualità discreta a problemi più o meno difficili.

Per spiegare il loro funzionamento, userò come esempio il problema delle 8 regine.

## Problema delle 8 regine

[Il problema delle 8 regine](<https://it.wikipedia.org/wiki/Rompicapo_delle_otto_regine#:~:text=Il%20rompicapo%20(o%20problema)%20delle,i%20movimenti%20standard%20della%20regina.>) è un puzzle che consiste nel posizionare 8 regine su una scacchiera 8x8 senza che nessuna di queste minacci le altre.
La "difficoltà" del problema consiste nel fatto che le regine minacciano gli altri pezzi che si trovano sulla stessa riga, colonna o diagonali. Tradizionalmente il problema viene risolto utilizzando un algoritmo _Depth-First Search (DFS)_ di backtracking.

<div class="row mt-3">
    <img src="{{'assets/gif/gen_alg_eight_queens/QueenAttacking_ManimCE_v0.18.1.gif' | relative_url }}" alt="Queen attacking pattern" style="width: 100%; border-radius: 4px;">
</div>
<div class="caption" style="font-size: 18px; font-style: italic;">
    La regina è un pezzo molto aggressivo. Può attaccare in orizzontale, verticale e diagonale e muoversi di quanti passi vuole.
</div>


In DFS, le regine vengono posizionate una alla volta, in maniera tale che l'ultima regina non minacci nessuna delle precedenti, fino a quando non si trova una soluzione o non è possibile posizionare una regina. In questo ultimo caso, l'ultima mossa viene annullata, e si prova in maniera ricorsiva a cambiare le posizioni delle precedenti regine fino alla risoluzione. Questo algoritmo è basato su _state space search (ricerca nello spazio di stato)_, in cui vengono provate tutte le possibili configurazioni.

Il problema delle 8 regine può essere generalizzato a N regine su una scacchiera NxN. Tuttavia, la complessità cresce esponenzialmente, e calcolare una soluzione con DFS diventa computazionalmente intrattabile.

## Componenti di un algoritmo genetico

Gli algoritmi genetici considerano possibili _soluzioni_ ad un problema come individui in una popolazione.
In questo caso, la parola _soluzione_ non assume il significato classico di _risoluzione_, ovvero quella soluzione che risolve il problema.
Ha invece una accezione molto più ampia: è infatti un qualsiasi assegnamento alle variabili del problema.
Esistono quindi soluzioni di qualità più o meno alta, ammissibili e inammissibili, e l'obiettivo dell'algoritmo genetico è quello di trovare una soluzione di qualità abbastanza alta (possibilmente la migliore).

In un algoritmo genetico, gli individui possono mutare spontaneamente o riprodursi l'un l'altro. Tuttavia, solo gli individui migliori riescono a sopravvivere e a generare "soluzioni" figlie di qualità sempre migliori.

I componenti di un algoritmo genetico sono:

- La funziona di fitness
- La rappresentazione delle soluzione
- La mutazione
- Il crossover
- La popolazione

### Funzione di Fitness

La funziona di Fitness è una funzione che assegna un punteggio ad una particolare soluzione.
Questa funzione può essere complicata a piacere, e può contenere penalizzazioni per alcuni casi patologici o forti premi per caratteristiche desiderabili.

La funzione di fitness condiziona quanto una soluzione riesce a sopravvivere tra una generazione e l'altra. Infatti, gli individui con fitness più alta sono quelli che avranno più probabilità di riprodursi e passare i propri geni positivi alle prossime generazione. In questa maniera soluzioni con fitness bassa hanno una bassa probabilità di generare figli, mentre le migliori soluzioni riescono a generare anche multipli figli con soluzioni altrettanto buone.

### Rappresentazione della soluzione

La _rappresentazione_ è l'astrazione che sintetizza i dettagli essenziali del problema, ed è realizzata attraverso una specifica _struttura dati_. Questa scelta è cruciale perché influisce direttamente sulle operazioni che possono essere eseguite durante la mutazione e il crossover, insieme all'efficienza con cui tali operazioni vengono eseguite.

Ad esempio, nel caso del problema delle 8 regine, la scacchiera potrebbe essere rappresentata come una lista di quadrati, una lista di righe o persino come un grafo di quadrati collegati. Ogni struttura dati offre vantaggi e svantaggi a seconda delle operazioni richieste: alcune possono facilitare certi tipi di mutazioni o controlli di validità, mentre altre potrebbero renderli più complessi o inefficienti.

Scegliere la giusta rappresentazione facilita la ricerca di soluzioni di qualità e può accelerare notevolmente il processo evolutivo all'interno dell'algoritmo genetico. Al contrario, una rappresentazione inadeguata può portare alla generazione di soluzioni inammissibili, rallentando l'intero processo evolutivo e facendo perdere individui potenzialmente validi.

### Mutazione

La _mutazione_ è una perturbazione casuale del genoma dell'individuo. Questo è un processo che serve a creare nuove soluzioni da una soluzione pre-esistente, senza cambiarla troppo. L'idea di fondo è che se l'individuo originale ha già una buona fitness,anche individui "adiacenti" avranno una fitness simile. In questa maniera è molto semplice trovare la soluzione ottimale nel caso si abbia già un individuo molto promettente.

Nel caso il genoma sia composto da numeri, la soluzione può essere una piccola perturbazione. Nel caso invece il genoma contenga valori categorici (come ad esempio "rosso", "giallo", "blu"), basta scegliere casualmente uno degli altri valori.

La mutazione è un processo stocastico. Il designer dell'algoritmo genetico deve decidere quanto alta deve essere la probabilità di mutazione. Se troppo bassa, nella popolazione saranno presenti sempre gli stessi individui. Se troppo alta invece la popolazione cambierà troppo frequentemente e le soluzioni ottimali verranno diluite.

### Crossover

In biologia il _crossover_ è il processo per cui durante la produzione dei gameti, i cromosomi materni e paterni si intersecano e mischiano. Questo permette ad un individuo di creare gameti molto più diversi da sé stesso, aumentando la variabilità genetica e la probabilità di creare della prole migliore.

Negli algoritmi genetici il crossover è molto simile. Infatti le soluzioni di due diversi individui vengono mischiati, e due nuovi individui con caratteristiche di entrambi i genitori vengono creati. Mentre la mutazione causa delle piccole perturbazioni locali attorno ad una soluzione, il crossover permette di generare individui molto diversi da quelli originali e superare quindi minimi locali per trovare soluzioni ottime globalmente. Il crossover è così efficace perché permette a individui molto promettenti di mischiarsi e generare con alta probabilità una soluzione molto migliore, ma permette anche a individui con poca fitness ma con alcune caratteristiche vincenti di unirsi a soluzioni di buona qualità.

## Applicazione al problema delle 8 Regine

Per il problema delle 8 regine, ho deciso di usare come _funzione di fitness_ il numero di regine minacciate da altre regine.
L'obiettivo è quindi quello di minimizzare la fitness. Infatti, l'individuo ottimale avrà fitness pari a 0, in quanto nessuna delle sue regine minaccia le altre.

Per quel che riguarda _la rappresentazione della soluzione_, una scacchiera è rappresentata come una matrice di dimensione NxN i cui elementi possono essere 0 o 1.
Se una cella ha valore 0, allora è vuota, altrimenti contiene una regina.
Per generare una scacchiera casuale, si potrebbero pescare a caso 8 celle e posizionare le regine. Questo è un esempio di _cattiva rappresentazione_, in quanto può selezionare con alta frequenza regine sulla stessa riga, colonna o diagonale.
Per ovviare a questo problema, si può posizionare una regina su ciascuna riga. In questa maniera si è sicuri che le regine possono essere attaccate solo verticalmente o diagonalmente, riducendo drasticamente il numero di cattive soluzioni.

Ora che è stato definita la rappresentazione, è abbastanza ovvio come scegliere mutazione e crossover.
Il processo di _mutazione_ seleziona una riga a caso e cambia la posizione della regina, sperando che lo spostamento orizzontale sia abbastanza per migliorare la fitness.
Questo mutazione può essere considerato un _bit-flip_, in quanto la scacchiera rappresenta le posizioni in bit e lo spostamento della regina consiste nel cambiamento di due celle da 0 a 1 e viceversa.

<div class="row mt-3">
    <img src="{{ 'assets/gif/gen_alg_eight_queens/QueenMutating_ManimCE_v0.18.1.gif' | relative_url}}" alt="Queen mutation sequence" style="width: 100%; border-radius: 4px;">
</div>
<div class="caption" style="font-size: 18px; font-style: italic;">
    Una sequenza di mutazioni. La fitness può migliorare, peggiorare o rimanere invariata. Essendo una piccola perturbazione, la fitness non cambia drasticamente, ma rimane nell'intorno del valore originale.
</div>

Il _crossover_ invece consiste nel scegliere uno a più righe a caso e scambiarle tra due diverse scacchiere.
Esistono altri tipi di crossover per matrici in cui, ad esempio, si considerano sub-matrici quadrate o rettangolari.
Tuttavia la rappresentazione che è stata scelta permette di utilizzare la prima versione, più semplice, che inoltre continua a garantire la presenza di una sola regina per riga.

<div class="row mt-3">
    <img src="{{ '/assets/gif/gen_alg_eight_queens/QueenCrossover_ManimCE_v0.18.1.gif' | relative_url }}" alt="Queen crossover" style="width: 100%; border-radius: 4px;">
</div>
<div class="caption" style="font-size: 18px; font-style: italic;">
    Un crossover tra due scacchiere. Il numero di righe selezionate è arbitrario, e può essere fino a N-1 (N in questo caso è 8).
</div>

## Pro e Contro degli Algoritmi Genetici

Come tutte le tecniche, gli Algoritmi Genetici non sono il Sacro Gral, e bisogna valutare di volta in volta se sono o meno lo strumento corretto.

### Pro

Il grande vantaggio degli algoritmi genetici è la loro flessibilità. Il design della soluzione si affida molto all'intuito del progettista, che potrebbe già avere un'idea di quale forma debba avere una buona soluzione. Questo rende anche la fase di design molto leggera, poiché il codice da scrivere non è particolarmente complicato e non richiede l'uso di framework o librerie complesse. È senza dubbio un ottimo modo per incorporare all'interno di un modello la propria intuizione, ed è il motivo per cui è così accessibile.

Un altro grande vantaggio è l'elevata velocità di prototipizzazione. In caso di scadenze molto strette, rappresentano un buon modo per produrre una soluzione decente e funzionante, rimandando l'adozione di tecniche più sofisticate ad un momento successivo.

Infine, le regole di mutazione e crossover possono essere definite per qualsiasi tipo di dato, senza particolari vincoli. Questo consente di descrivere soluzioni con strutture esotiche, difficilmente o per nulla riproducibili con altri tipi di algoritmi. Offre anche grande flessibilità nella definizione di vincoli e soluzioni non ammissibili, che possono essere penalizzate nella funzione di fitness o scartate a priori quando vengono generate.

### Contro

Il processo di ottimizzazione negli Algoritmi Genetici dipende fortemente dalla robustezza e dalla qualità della _rappresentazione_ scelta. La _funzione di fitness_ è cruciale, e spesso in un progetto è necessario iterare diverse versioni della funzione prima di trovarne una soddisfacente. Inoltre, non sempre le _mutazioni e i crossover_ selezionati sono efficaci nel superare minimi locali poco soddisfacenti.

### Possibili Alternative

I contro derivano dal fatto che gli Algoritmi Genetici non imparano esplicitamente dagli errori che commettono, ma necessitano di molti tentativi per esplorare efficacemente lo spazio di stato.

Esistono altri algoritmi in grado di sfruttare una caratteristica molto utile di alcune funzione di fitness chiamata _differenziabilità_. Una funzione di fitness differenziabile infatti non solo comunica la qualità di una soluzione, ma è anche in grado di descrivere come la soluzione deve cambiare per migliorare. Gli algoritmi che sfruttano questa proprietà sono _algoritmi basati su gradienti_, e tendono a essere molto più efficienti in quanto non provano perturbazioni a caso.

Un'altra possibile alternativa sono gli algoritmi di _ottimizzazione bayesiana_. Come gli algoritmi genetici, anche loro esplorano lo spazio di stato casualmente perturbando la soluzione. Tuttavia, la perturbazione è applicata in maniera intelligente, in quanto in maniera sistematica provano a esplorare soluzioni mai esplorate senza però allontanarsi da soluzioni promettenti. Oltre ad aver bisogno della differenziabilità, questi algoritmi ipotizzano anche che soluzioni molto simili hanno fitness simile, senza grandi discontinuità.
