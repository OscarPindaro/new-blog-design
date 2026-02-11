---
layout: post
title: Imparando Manim
date: 2024-11-25 18:00:00
description: Una raccolta di animazioni per imparare ad usare meglio manim
tags: code
categories: animations
featured: true
thumbnail: 'assets/gif/linestar/light/LinestarScene_onedark_vivid_rainbow_f0ead6.gif' 
---

Come si può intuire dal titolo, questo post non ha un vero proprio tema, ma è più una raccolta di animazioni che ho fatto per diventare un po' più disinvolto con [Manim](https://www.manim.community/), la libreria python che utilizzo per creare le gif del blog.

## Cos'è Manim

Manim (Mathematical Animation Engine) è una libreria python progettata per creare animazioni matematiche in maniera programmatica.

La trovo molto comoda perchè sono un pessimo artista ma mi trovo molto a mio agio a scrivere codice.

L'autore di questa libreria è Grant Sanderson, uno dei più famosi divulgatori di matematica.
La libreria è nata inizialmente da un suo progetto personale, in cui pubblica video divulgativi suo canale YouTube [3Blue1Brown](https://www.youtube.com/c/3blue1brown).

Le animazioni che vedrete sono abbastanza semplici.
L'obiettivo è diventare abbastanza disinvolto nell'utilizzo della libreria, e allo stesso tempo trovare una palette che mi permetta di distanziarmi dallo stile di _3Blue1Brown_.

Per adesso ci sono pochi esempi, ma spero di aggiungerne altri in futuro.

## Stella di linee

Questa è una sorta di illusione ottica. Anche se per disegnare questa stella si usano solo linee rette, il risultato sembra una stella con i lati curvi, che ricordano rami di iperboli. Per costruire questa stella bisogna:

1. Scegliere due assi adiacenti (ad esempio l'asse x positivo e y positivo).
2. Dividere entrambi gli assi in N parti.
3. Partire dal punto più lontano dall'origine su un asse e collegarlo al punto più vicino sull'altro asse.
4. Disegnare la retta successiva avvicinandosi sull'asse su cui si era più lontani e allontanandosi su quello su cui si era più vicini.

### Palette chiare

Le palette chiare sono state quelle più difficili da creare.
L'idea originale era quella di avere tante stelle con i colori dell'arcobaleno: tuttavia non tutte si mischiano bene con uno sfondo chiaro.

In particolare, l'arcobaleno con i colori pastello è in assoluto il peggiore. Riflettendoci meglio il motivo è abbastanza chiaro: essendo i colori pastellati molto vicini al bianco, tenderanno a mischiarsi meglio con uno sfondo scuro.

I miei preferiti sono le animazioni con le palette calde, che ricordano il tramonto.

<div class="carousel">
  <button class="carousel-btn prev" onclick="moveCarousel(this, -1)">‹</button>
  <div class="carousel-container">
    <div class="carousel-track">
      <img src="{{ 'assets/gif/linestar/light/LinestarScene_golden_sunset_f0ead6.gif' | relative_url }}" alt="Golden sunset palette">
      <img src="{{ 'assets/gif/linestar/light/LinestarScene_onedark_classic_f0ead6.gif' | relative_url }}" alt="Onedark classic palette">
      <img src="{{ 'assets/gif/linestar/light/LinestarScene_pastel_rainbow_f0ead6.gif' | relative_url }}" alt="Pastel rainbow palette">
      <img src="{{ 'assets/gif/linestar/light/LinestarScene_high_saturation_rainbow_f0ead6.gif' | relative_url }}" alt="High saturation rainbow palette">
      <img src="{{ 'assets/gif/linestar/light/LinestarScene_onedark_class_rainbow_f0ead6.gif' | relative_url }}" alt="Onedark classic rainbow palette">
      <img src="{{ 'assets/gif/linestar/light/LinestarScene_sunset_skyline_f0ead6.gif' | relative_url }}" alt="Sunset skyline palette">
      <img src="{{ 'assets/gif/linestar/light/LinestarScene_muted_rainbow_f0ead6.gif' | relative_url }}" alt="Muted rainbow palette">
      <img src="{{ 'assets/gif/linestar/light/LinestarScene_neon_rainbow_f0ead6.gif' | relative_url }}" alt="Neon rainbow palette">
      <img src="{{ 'assets/gif/linestar/light/LinestarScene_onedark_f0ead6.gif' | relative_url }}" alt="Onedark palette">
    </div>
  </div>
  <button class="carousel-btn next" onclick="moveCarousel(this, 1)">›</button>
</div>

### Palette scure

Queste sono le palette che mi hanno dato in assoluto più soddisfazioni, quindi godetevele.

<div class="carousel">
  <button class="carousel-btn prev" onclick="moveCarousel(this, -1)">‹</button>
  <div class="carousel-container">
    <div class="carousel-track">
      <img src="{{ 'assets/gif/linestar/dark/LinestarScene_golden_sunset_282c33.gif' | relative_url }}" alt="Golden sunset dark palette">
      <img src="{{ 'assets/gif/linestar/dark/LinestarScene_onedark_282c33.gif' | relative_url }}" alt="Onedark dark palette">
      <img src="{{ 'assets/gif/linestar/dark/LinestarScene_pastel_rainbow_282c33.gif' | relative_url }}" alt="Pastel rainbow dark palette">
      <img src="{{ 'assets/gif/linestar/dark/LinestarScene_high_saturation_rainbow_282c33.gif' | relative_url }}" alt="High saturation rainbow dark palette">
      <img src="{{ 'assets/gif/linestar/dark/LinestarScene_onedark_classic_282c33.gif' | relative_url }}" alt="Onedark classic dark palette">
      <img src="{{ 'assets/gif/linestar/dark/LinestarScene_sunset_skyline_282c33.gif' | relative_url }}" alt="Sunset skyline dark palette">
      <img src="{{ 'assets/gif/linestar/dark/LinestarScene_muted_rainbow_282c33.gif' | relative_url }}" alt="Muted rainbow dark palette">
      <img src="{{ 'assets/gif/linestar/dark/LinestarScene_neon_rainbow_282c33.gif' | relative_url }}" alt="Neon rainbow dark palette">
      <img src="{{ 'assets/gif/linestar/dark/LinestarScene_onedark_class_rainbow_282c33.gif' | relative_url }}" alt="Onedark classic rainbow dark palette">
      <img src="{{ 'assets/gif/linestar/dark/LinestarScene_onedark_vivid_rainbow_282c33.gif' | relative_url }}" alt="Onedark vivid rainbow dark palette">
    </div>
  </div>
  <button class="carousel-btn next" onclick="moveCarousel(this, 1)">›</button>
</div>


## Polinomi

Queste animazioni erano per capire come utilizzare il `NumberPlane` (Piano Cartesiano) di manim.
Purtroppo ci sono ancora alcune sbavature (le funzioni vengono plottate anche fuori dai limiti degli assi). Devo ancora capire se c'è qualche parametro da settare oppure bisogna solo essere un po' smart quando si disegnano le funzioni.

Durante lo sviluppo tendo a fare animazioni molto rapide, ma ora che le riguardo mi rendo conto che bisogna lasciar tempo all'osservatore di capire cosa sta succedendo sullo schermo.


<div class="carousel carousel-with-captions">
  <button class="carousel-btn prev" onclick="moveCarousel(this, -1)">‹</button>
  <div class="carousel-container">
    <div class="carousel-track">
      <div class="carousel-slide">
        <img src="{{ '/assets/gif/manim-experiments/StraightLinePoly_ManimCE_v0.18.1.gif' | relative_url }}" alt="Plot di due rette">
        <div class="carousel-caption">Plot di due rette.</div>
      </div>
      <div class="carousel-slide">
        <img src="{{ '/assets/gif/manim-experiments/ParabolePoly_ManimCE_v0.18.1.gif' | relative_url }}" alt="Plot di due parabole">
        <div class="carousel-caption">Plot di due parabole, una convessa e una concava. I colori di questa palette mi piacciono molto.</div>
      </div>
      <div class="carousel-slide">
        <img src="{{ '/assets/gif/manim-experiments/PolynomialTransformation_ManimCE_v0.18.1.gif' | relative_url }}" alt="Trasformazione polinomiale">
        <div class="carousel-caption">Trasformazione da un polinomio di quarto grado a uno di terzo. La palette originale di 3Blue1Brown mantiene sempre il suo fascino.</div>
      </div>
      <div class="carousel-slide">
        <img src="{{ '/assets/gif/manim-experiments/RandomCubics_ManimCE_v0.18.1.gif' | relative_url }}" alt="Cubiche casuali">
        <div class="carousel-caption">Una serie di cubiche casuali. Ho usato una palette dai colori caldi del tramonto. Provo sensazioni miste, probabilmente il nero dovrebbe essere meno saturo. Inoltre i rossi usati per le funzioni sono troppo vicini nello spettro.</div>
      </div>
    </div>
  </div>
  <button class="carousel-btn next" onclick="moveCarousel(this, 1)">›</button>
</div>
## Regressione Lineare

Questo è un esempio di regressione lineare, utilizzando però solo feature polinomiali.
I dati sono campionati dalla distribuzione rossa, un polinomio di quarto grado. Successivamente, un polinomio di terzo grado è fittato usando Stochastic Gradient Descent.

La regressione lineare è un _problema a forma chiusa_, ovvero esiste una soluzione che può essere calcolata analiticamente senza alcuna approssimazione dell'errore. Tuttavia, la Discesa del Gradiente ha un nome molto più divertente ed è anche più bello da animare.

I colori lasciano un po' a desiderare, ma avevo già perso troppo tempo a giocherellare con i parametri della regressione.

<div class="row mt-3">
    <img src="/assets/gif/manim-experiments/PolynomialFitting_ManimCE_v0.18.1.gif" alt="Polynomial fitting" style="width: 100%; border-radius: 4px;">
</div>
<div class="caption" style="font-size: 18px; font-style: italic;">
    Dei punti vengono campionati dalla distribuzione rossa. In bianco, i diversi polinomi di terzo grado che vengono creati durante la Discesa del gradiente. Più passa il tempo, meglio approssimano la funzione originale
</div>

### Formula matematica

$$\theta_{t+1} = \theta_t + \alpha \nabla_{\theta} f(\theta_t)$$

Dove:

- $$\theta$$ rappresenta i parametri della regressione (ovvero i coefficienti del polinomio),
- $$\alpha$$ è il tasso di apprendimento (cioè quanto del gradiente considerare durante l'aggiornamento dei parametri),
- $$\nabla_{\theta}f(\theta_t)$$ è il gradiente dell'errore rispetto ai parametri della regressione. Se il regressore è un polinomio di grado 3, allora il gradiente sarà un vettore di 4 elementi, uno per ciascun coefficiente del polinomio. Il valore del gradiente per un parametro corrisponde al valore della potenza associata a quel parametro.

### Implementazione
```python
def gradient_ascent_fit(self) -> Tuple[np.ndarray, np.ndarray]:
    import math

    errors: List[float] = []
    fitted_polys = []

    # if the gradients become too big, the loop may become numerically unstable
    clip_val = self.clip_val0

    # a preliminary solution can be a random polynomial
    estimator = Polynomial.random(self.max_degree, -5,5)
    # estimator = Polynomial((1,)*5)

    # first iteration
    fitted_polys.append(estimator)
    errors.append(estimator.compute_error(self.X,self.y_true))

    for i in range(self.n_steps):
        # the learning weight gets smaller the more time passes. It helps convergence
        lr = self.lr0 / math.log(i+2)
        # lr = self.lr0
        estimator = estimator.gradient_ascent_step(self.X, self.y_true, lr, clip_val)
        fitted_polys.append(estimator)
        errors.append(estimator.compute_error(self.X,self.y_true))

    return fitted_polys[::self.save_every]+[fitted_polys[-1]], errors[::self.save_every]+[errors[-1]]
```

**Spiegazione del codice:**

- **Inizializzazione**: Si crea un polinomio casuale e si calcola il suo errore iniziale.
- **Iterazioni**: Per un certo numero di passi, il polinomio viene aggiornato usando gradient ascent (spostandosi nella direzione del gradiente per ridurre l'errore). Il learning rate diminuisce nel tempo per favorire la convergenza.
- **Output**: Restituisce i polinomi e gli errori ad intervalli regolari e alla fine.