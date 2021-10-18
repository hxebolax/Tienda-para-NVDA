# Manuel de zUtilidades

* Auteur: Héctor J. Benítez Corredera
* Compatibilité NVDA: 2019.3 à 2021.1
* [télécharger l'extension:](https://nvda.es/files/get.php?file=zUtilidades)
* [Projet  sur GitHub:](https://github.com/hxebolax/zUtilidades-para-NVDA)

---

Sommaire<a id="Sommaire"></a>
-------------
- [Introduction](#mark0)
- [Module Lanceur d'applications](#mark1)
- [Écran principal](#mark2)
- [Liste des catégories](#mark3)
- [Liste des applications](#mark4)
- [Menu Ajouter une action](#mark5)
- [Modifier une action](#mark6)
- [Supprimer une action](#mark7)
- [Bouton Menu](#mark8)
- [Raccourcis clavier](#mark9)
- [Observations de l'auteur](#mark10)
- [Module Notes rapides](#mark11)
- [Ajouter une note rapide de n'importe où](#mark12)
- [Menus virtuels pour le Lanceur d'applications et pour les Notes rapides](#mark13)
- [Traducteurs et contributeurs](#mark14)
- [Journal des changements](#mark15)
- [Version 0.2.3](#mark0.2.3)
- [Version 0.2.2](#mark0.2.2)
- [Version 0.2.1](#mark0.2.1)
- [Version 0.2](#mark0.2)
- [Version 0.1.6](#mark0.1.6)
- [Version 0.1.5](#mark0.1.5)
- [Version 0.1](#mark0.1)

---

# Introduction<a id="mark0"></a>

zUtilidades vise à être un ensemble de petites applications pour NVDA.

Nous allons essayer d'ajouter des applications qui peuvent être intéressantes afin que nous puissions les consulter rapidement et que à son tour, soit faciles à gérer et clair dans son interface.

zUtilidades aura un menu dans Outils de NVDA, Dans ce menu ils seront ajoutés les différents modules.

Chaque module est préparé afin que nous puissions ajouter un raccourci allant dans le menu NVDA / Préférences /  Gestes de commandes dans la catégorie zUtilidades.

Par défaut, les modules viendront sans raccourci attribué.

Par conséquent, nous pouvons démarrer les modules en allant dans le menu Outils / zUtilidades ou en attribuant une combinaison de touches pour chaque module.

Il est actuellement composé des modules suivants:

* Lanceur d'applications.
* Notes rapides.

# Module Lanceur d'applications<a id="mark1"></a>

Ce module nous permettra rapidement et à partir de n'importe quelle partie de notre ordinateur lancer une application portable ou installé.

## Écran principal<a id="mark2"></a>

L'écran principal consiste en une liste de catégories, une liste d'applications et un bouton Menu.

Si nous faisons Tabulation nous passerons à travers les différents zones.

### Liste des catégories<a id="mark3"></a>

Dans cette zone, nous pouvons ajouter, modifier ou supprimer une catégorie, pouvant trier à notre goût et par catégories nos applications.

Nous pouvons accéder aux options Ajouter, Modifier ou Supprimer de deux manières.

Lorsque nous sommes dans la zone Catégories en appuyant sur la touche Application ou si nous n'avons pas la  touche Maj+F10, un menu sera affiché où nous pouvons choisir l'une des 3 options.

Les dialogues tantot pour ajouter comme pour modifier sont très simples disposant d'un seul champ de édition où nous pouvons mettre le nom de la nouvelle catégorie ou modifier la catégorie que nous avons choisie, deux boutons, OK et Annuler.

Si nous choisissons de supprimer, nous devons prendre en compte que le contenu de cette catégorie sera complètement effacée sans pouvoir refaire l'action, soyez donc prudent  car nous pourrons perdre les applications Que nous avons  dans la base de données et nous devrons re-entrez toutes les applications ou les commandes ou les accès à cette catégorie.

Nous pouvons également accéder à ces options en cliquant sur le bouton Menu, lorsque nous faisons Tabulation ou avec la combinaison Alt+M. Si nous le faisons, un menu sera affiché avec un sous-menu appelé Catégories où nous pouvons choisir l'une des 3 options précédentes.

Notez que Modifier et Supprimer seront toujours dans la catégorie qui a le focus, donnant les messages correspondants si nous n'avons pas de catégories.

Nous pouvons également utiliser les combinaisons de touches Alt + Flèche  haut et Flèche  bas pour déplacer la catégorie pour pouvoir les trier.

### Liste des applications<a id="mark4"></a>

Dans cette zone, c'est où les applications correspondantes à la catégorie que nous avons choisies seront placées.

Nous avons 3 options qui son Ajouter une action, Modifier une action ou Supprimer une action.

Nous pouvons obtenir ces options comme dans la liste des catégories soit avec la touche Applications ou dans se cas Maj+F10 ou accédez au bouton Menu (Alt+M) et chercher le sous-menu Applications.

Dans cette liste d'applications, nous pouvons lancer l'application qui a le focus en appuyant sur la barre d'espace.

Nous pouvons également utiliser les combinaisons de touches Alt + Flèche  haut et Flèche  bas  pour déplacer  l'entrée pour pouvoir les trier.

Dans cette zone, nous pouvons rapidement naviguer dans les différentes entrées, en appuyant sur la première lettre, afin que nous puissions trouver rapidement l'application que nous souhaitons exécuter si nous en avons beaucoup dans la base de données.

#### Menu Ajouter une action<a id="mark5"></a>

Dans ce menu, nous pouvons choisir entre les options suivantes:

* Ajouter une application:

Si nous ajoutons une application, il existe deux champs obligatoires et c'est le nom de l'application et le répertoire dans lequel notre application est située.

Actuellement, cette extension prend en charge les applications avec les extensions exe, bat et com.

Une fois que les champs obligatoires sont remplis, nous pouvons choisir si l'application nécessite des paramètres supplémentaires ou si nous voulons exécuter l'application en mode administrateur.

Si nous voulons exécuter une application en mode administrateur, on nous demandera l'autorisation correspondante lorsque nous démarrons l'application.

* Ajouter une commande CMD

Dans ce dialogue, nous pouvons ajouter des commandes de console.

Les champs nom pour identifier la commande et le champ commandes sont obligatoires.

Dans ce cas, en plus de lancer des commandes CMD, si nous maîtrisons Windows PowerShell, si nous mettons PowerShell en ligne de commande et suivi de ce que nous voulons, nous allons également exécuter des commandes PowerShell.

De même, si son des commandes CMD j'ajoute que nous pouvons exécuter plusieurs lignes de commande qui doivent être séparées par le symbole (et commercial) pouvant être effectuées avec  Maj+6, ceci avec un clavier QWERTY espagnol. Si un clavier QWERTY anglais est utilisé, Cela sera effectué avec Maj+7.

Par exemple, j'ai mis une ligne de commande pour redémarrer Windows Explorer, vous vérifierez que j'utilise le symbole (et commercial) pour séparer une ligne de commande de l'autre.

`taskkill /f /im explorer.exe & start explorer`

En outre, dans ce dialogue, nous pouvons mettre une pause de sorte que la console ne se ferme pas et nous pouvons voir les résultats.

Nous pouvons également exécuter en tant qu'administrateur.

* Ajouter des accès aux dossiers

Dans ce dialogue, nous devrons choisir un nom pour identifier l'accès au dossier et choisir un dossier.

Cela nous permettra d'ouvrir rapidement des dossiers de notre système de n'importe où.

* Ajouter Exécuter des raccourcis de Windows

Dans ce dialogue, nous pouvons choisir un raccourci pour le démarrer. Nous pouvons également choisir si nous voulons le démarrer en tant qu'administrateur.

Les champs pour identifier le nom du raccourci et le chemin sont obligatoires.

* Ajouter une application installée

Dans ce dialogue, toutes les applications installées sur notre ordinateur seront obtenues par l'utilisateur ou sont des applications qui sont déjà livrées avec Windows.

Également sur cet écran, nous pouvons choisir les applications installées à partir du Microsoft Store de Windows.

AVERTISSEMENT ceci n'est pas valide pour Windows 7.

Une fois qu'une application est ajoutée à partir de ce dialogue, notez qu'il ne peut pas être modifié, alors nous devrons supprimer l'entrée si nous voulons l'ajouter à nouveau.

L'option Exécuter en tant qu’administrateur dans ce dialogue ne fonctionnera pas pour toutes les applications. Fonctionnant uniquement pour celle qui vous permettent d'utiliser des privilèges d'administrateur.

Notez également que dans ce dialogue, les accès installés par les applications apparaissent également dans la zone de liste déroulante, nous pouvons les sélectionner, mais certains ne sont pas autorisés d'être ouvert, donnant une erreur.

Notez également que vous devez faire attention car dans cette liste, apparaîtront des applications qui peut être pour administrer ou des applications pour la gestion Que si nous ne savons pas à quoi servent il vaut mieux ne pas les toucher.

#### Modifier une action<a id="mark6"></a>

Le dialogue Modifier est exactement le même que le dialogue Ajouter une action Mais cela nous permettra de modifier l'entrée que nous choisissons.

Cela nous permettra de modifier tous les éléments, à l'exception de ceux qui ont été ajoutés par l'option  Ajouter une application installée, Les dialogue seront identiques que dans les options pour ajouter.

#### Supprimer une action<a id="mark7"></a>

Si nous supprimons une entrée, nous devons garder à l'esprit que l'action ne sera pas réversible.

### Bouton Menu<a id="mark8"></a>

Ce bouton sera accessible depuis n'importe quelle partie de l'interface en appuyant sur la combinaison  Alt+M.

Dans ce menu, nous trouverons quatre sous-menus qui sont  Catégories, Actions, Faire ou restaurer une sauvegarde et Options, dans ce menu nous trouvons aussi l'option Quitter.

Eh bien,  Catégories et Actions que j'ai expliquées auparavant, je n'expliquerai que le sous-menu Faire ou restaurer une sauvegarde et Options.

Eh bien, si nous choisissons Faire  une sauvegarde, une fenêtre d'enregistrement de Windows s'ouvre où nous devrons choisir où enregistrer notre sauvegarde de la base de données.

Par défaut, le nom du fichier est plus ou moins comme ceci:

`Backup-03052021230645.zut-zl`

Eh bien, l'extension est configurée par défaut et le nom correspond au module et contient la date à laquelle il a été créé, mais nous pouvons mettre le nom que nous souhaitons.

Une fois enregistré, nous pouvons la restaurer si notre base de données est corrompue ou tout simplement si celle-ci est supprimée par erreur ou nous souhaitons revenir à une version que nous avons précédemment enregistrée.

Si nous choisissons Restaurer une sauvegarde, une fenêtre Windows classique s'ouvrira, pour nous permettre d'ouvrir les fichiers respectifs.

Nous devons choisir la copiie que nous avons enregistrée qui aura l'extension *.zut-zl , veillez à ne pas modifier l'extension car sinon vous ne trouverez pas le fichier.

Une fois que vous avez choisi, la sauvegarde sera restaurée et lorsque nous avons appuyer sur OK l'extension sera fermé  et la prochaine fois que nous l'ouvrons, il aura notre copie restaurée.

Notez que les fichiers *.zut-zl sont en réalité des fichiers compressés, mais faites attention lorsque vous les modifiez, si elles sont modifiées, la signature ne correspondra pas et ne leur permettra pas d'être restaurer.

Avec cela, je tiens à dire que ces fichiers apportent une signature qui ne correspond pas au moment de la restauration, cela donnera une erreur et chaque signature est différente pour chaque fichier.

Dans le sous-menu Options maintenant il n'y a que l'option Réinitialiser le lanceur d'applications aux valeurs par défaut.

Si nous choisissons cette option, toute la base de données sera supprimée, laissant  l'extension comme s'il était nouvellement installé.

## Raccourcis clavier<a id="mark9"></a>

Dans les deux zones, Catégories et Applications, nous pouvons trier les entrées avec:

* Alt + Flèche  haut ou Flèche bas

Lorsqu'une catégorie ou une application atteint le début ou la fin de la liste, cela sera annoncé avec un son distinct pour savoir que nous ne pouvons pas ni monter ni descendre plus.

* Alt + C: Ça va nous amener rapidement à la zone des catégories.

* Alt + L: Ça va nous amener rapidement à la liste des applications.

* Alt + M: Cela nous ouvrira le menu.

* Touche Applications ou Maj + F10: Dans les zones des catégories et applications nous déploierons le menu contextuel avec des options.

* Espace: Dans la zone liste des applications s'exécutera l'application qui a le focus.

* Echap: Ferme tous les dialogues que l'application peut ouvrir même l'écran principal du lanceur d'applications, laissant le focus depuis l'endroit où elle a été appelée.

## Observations de l'auteur<a id="mark10"></a>

Prenez garde sur diverses choses, la première que le lanceur d'applications se fermera lorsque nous exécuterons une application, devant l'appeler à nouveau lorsque nous voulons exécuter une  autre.

Il a également été implémenté une fonction qui sauvegardera la position de la catégorie et les dernières applications visitées, alors lorsque nous ouvrons le lanceur d'applications, la dernière catégorie et la dernière application de cette catégorie seront toujours choisies.

Aussi il a été implémenté la sauvegarde du focus, alors lorsque nous appelons le lanceur d'applications, il nous laissera toujours dans la dernière position où le focus a était mis  avant de fermer.

Par exemple,  si le focus est mis sur le bouton  Menu et nous fermons le lanceur d'applications, la prochaine fois que nous l'ouvrons, le focus sera mis sur le bouton Menu.

Ces caractéristiques ne sont valables que lors de la session de NVDA, cela signifie que si nous redémarrons NVDA on va démarrer avec le focus mis dans la zone catégories.

Cette extension a été faite pour être utilisée avec Windows 10, de sorte que si vous utilisez des versions antérieures et que vous avez  un problème quelconque vous pouvez me le dire, mais je ne peux sûrement rien faire car certaines fonctionnalités ne sont trouvées que dans Windows 10.

# Module Notes rapides<a id="mark11"></a>

Ce module nous aidera à avoir de petites notes à portée de main que nous pouvons consulter, modifier, supprimer.

Ce module a la même façon de fonctionner que le lanceur d'applications mais varie sur certaines touches expliquées ci-dessous.

Je n'expliquerai plus le menu avec lequel nous pouvons faire ou restaurer une sauvegarde, réinitialiser le lanceur d'applications aux valeurs par défaut, gérer les catégories et les notes.

Je ne vais pas non plus expliquer le parcours de l'interface principale car c'est exactement la même chose.

Nous pouvons ajouter une note rapide et dans le dialogue qui s'ouvre, nous pouvons mettre le titre de la note et si nous faisons Tabulation le contenu.

Le  dialogue pour Modifier la note est exactement le même, mettre un titre ou modifier celui-ci qui est déjà et de pouvoir modifier la note.

Ce module diffère avec le lanceur d'applications dans lequel il utilise de nouvelles combinaisons de touches.

* F1: Lorsque nous sommes sur une note si nous appuyons F1 nous lira le contenu de la note.
* F2: Nous allons copier la note focalisé dans le presse-papiers afin que nous puissions la copier n'importe où tant que l'application qui admette l'écriture doit être focalisé, sinon, rien ne se passera.
* F3: Cette combinaison fermera la fenêtre des notes rapides et collera le contenu de la note que nous avons focalisé ayant le focus, c'est-à-dire que vous collez la note dans l'application qui s'ouvre chaque fois que cela vous permet de coller du texte par la dite application, par exemple, le Bloc-notes, le champ d'un E-mail, dans Word, etc.

Cela signifie que si nous appelons le module Notes rapides à partir du Bloc-notes ou quand Nous sommes situés  dans l'objet  d'un E-mail lorsque nous appuyons sur cette combinaison, le texte sera coller où nous avons eu le focus.

Par exemple, si nous lançons le module Notes rapides à partir du bureau et nous appuyons sur F3 sur une note, rien ne se passera, si nous ouvrons le Bloc-notes et nous appuyons sur F3 il collera le contenu de la note dans le bloc-notes.

Soyez prudent si nous sommes sur le bureau ou quelque part où vous ne pouvez pas coller directement, cela ne fera rien

Cela continue également de fonctionner tantôt dans la zone des catégories comme dans la zone de liste de notes pour pouvoir trier lesdites zones avec Alt+Flèches haut et bas pour déplacer ce que nous avons sélectionné.

Si nous appuyons sur espace, une fenêtre s'ouvrira où nous ne pouvons voir que notre note.

Je tiens à dire que ce module vient sans un raccourci défini, , nous devrons donc l'ajouter dans le dialogue Gestes de commandes.

Un dialogue Options est ajoutée dans le menu Options.

Il n'a actuellement qu'une option qui est la suivante:

* Capturer le titre de la fenêtre dans les notes rapides (de n'importe où)

Si nous cochons cette option lorsque nous appuyons soit sur Ajouter une nouvelle note rapide ou sur Ajouter une note rapide du texte sélectionné le titre de la note sera rempli avec le titre de la fenêtre que à ce moment est focalisée.

# Ajouter une note rapide de n'importe où<a id="mark12"></a>

De plus, le module Notes rapides a une fonctionnalité pour ajouter des notes rapides de n'importe où sans qu'il soit nécessaire d'ouvrir l'extension pour l'ajouter.

Dans le dialogue Gestes de commandes, nous pouvons maintenant configurer une nouvelle combinaison de   touches que vous trouverez dans:

NVDA / Préférences /  Gestes de commandes / zUtilidades / Avec un appui s'ajoute une note rapide du texte sélectionné, avec deux appuis s'ajoute une nouvelle note rapide

Lorsque nous avons une combinaison attribuée, nous ne devrons choisir un texte de n'importe où et appuyer sur la combinaison de touches.

Une fenêtre s'ouvrira dans laquelle la première chose que nous devrons choisir est dans quelle catégorie nous souhaitons sauvegarder notre note, seules les catégories que nous avons ajoutées apparaîtront.

Si nous faisons Tabulation, nous allons tomber dans le champ pour mettre le titre de la note et Si nous faisons à nouveau Tabulation, nous aurons le texte que nous avions sélectionné.

Lorsque nous appuyons sur OK, celle-ci se sauvegardera et nous aurons notre note Dans notre catégorie que nous aurons choisi.

Si nous appuyons sur cette combinaison deux fois, le même écran s'ouvrira mais pour ajouter une note à partir de zéro. Nous devrons sélectionner dans quelle catégorie sauvegarder la note, le titre de la note ainsi que le contenu de la note.

# Menus virtuels pour le Lanceur d'applications et pour les Notes rapides<a id="mark13"></a>

Eh bien, ces menus sont venus pour améliorer l'extension zUtilidades, ce qui la rendra maintenant beaucoup plus productive et plus rapide.

Eh bien, les gestes de commandes que nous avons affectés au Lanceur d'applications et Notes rapides ont maintenant une double pulsation.

Si nous appuyons une seule fois cette combinaison nous affichera l'interface graphique, Si nous appuyons deux fois nous affichera le menu virtuel.

Eh bien, dans ce menu, nous pouvons nous déplacer avec les flèches droite et gauche entre les catégories et avec les flèches haut et bas entre les éléments de cette catégorie s'il y en a.

Eh bien, il existe des différences entre le menu du Lanceur d'applications et Notes rapides.

Dans le menu virtuel du Lanceur d'applications avec les flèches nous nous déplaçons et avec entrée nous exécutons l'élément que nous avons sélectionné en faisant l'action correspondante.

S'il s'agit d'une commande CMD, donc, celle-ci s'exécutera, s'il s'agit d'un raccourci de la même façon et de même si c'était pour l'interface graphique.

Eh bien avec Échap, nous allons quitter le menu si nous ne voulons rien faire.

Nous pouvons également passer à travers les catégories en appuyant sur les touches commençant par le début de la lettre du nom sauf  la ñ qui n'est pas pris en charge par ce menu, tous les autres nous amèneront rapidement à la catégorie.

Eh bien, si cette lettre n'a pas de catégorie, cela nous donnera le message d'aide de la même façon que si nous appuyons sur une quelconque touche différente de celles mentionnées.

Je tiens à dire que lorsque le menu est actif, toutes les autres combinaisons de touches NVDA ne fonctionneront pas avant que nous quittions le menu.

Dans le menu  Notes rapides, la touche Barre d'espacement n'est pas valable du tout et si a des différences avec celle du lanceur d'applications.

Lorsque nous sommes sur un élément, si nous appuyons sur F1 nous verbalisera le contenu de la note, avec F2 nous copiera la note dans le presse-papiers et avec F3 nous collera le contenu de la note où nous avons le focus.

Également je vous dit aussi que le menu étant actif celui-ci a une priorité jusqu'à ce que nous appuyons sur la touche Échap pour quitter le menu en restaurant la fonctionnalité normale du clavier.

## Traducteurs et contributeurs:<a id="mark14"></a>

* Français: Rémy Ruiz
* Portugais: Ângelo Miguel Abrantes
* Italien: Alessio Lenzi
* Javi Domínguez: Mille merci de m'avoir appris à programmer le menu. Mieux dit pour l'expliquer pour les imbéciles comme moi.

# Journal des changements.<a id="mark15"></a>
## Version 0.2.3.<a id="mark0.2.3"></a>

Ajouté la possibilité de capturer le titre des fenêtres sur Ajouter une nouvelle note rapide ou sur Ajouter une note rapide du texte sélectionné.

Cette option peut être activée dans le menu du module Notes rapides dans la section Options / Options.

Si la case est cochée à partir de ce moment le titre des fenêtres sera capturé d'où il a été invoqué soit les options Ajouter une nouvelle note rapide ou Ajouter une note rapide du texte électionné.

## Version 0.2.2.<a id="mark0.2.2"></a>

* Ajouté la possibilité de déplacer entre les catégories tantôt pour les 'éléments du lanceur d'applications comme pour les notes.
* Ajout d'un double appui pour la touche Ajouter une note rapide du texte sélectionné. Maintenant, avec deux appui nous laissera créer une nouvelle note rapide à partir de zéro.
* Documentation française mise à jour.
* eAjout de la langue italienne

## Version 0.2.1.<a id="mark0.2.1"></a>

* Problème résolu avec le presse-papiers vides lorsque vous souhaitez coller un texte.

## Version 0.2.<a id="mark0.2"></a>

* De nombreuses erreurs internes ont été corrigées.
* Le module Lanceur d'applications a été stabilisé.
* Un nouveau module Notes rapides a été ajouté.
* Les menus virtuels ont été ajoutés pour les deux modules.

## Version 0.1.6.<a id="mark0.1.6"></a>

* Ajout de la traduction française et Portugaise (Portugal / Brésil).

## Version 0.1.5.<a id="mark0.1.5"></a>

* Menus restructurés.

Ajoutez la possibilité d'ajouter:

* Ajouter une commande CMD

* Ajouter des accès aux dossiers

* Ajouter Exécuter des raccourcis de Windows

* Ajouter une application installée

* Ajouté dans le bouton Menu la possibilité  dans Options Réinitialiser le lanceur d'applications aux valeurs par défaut

* Différentes erreurs ont été corrigées avec la base de données.

* Des erreurs internes ont été corrigées.

* L'extension a été préparée afin  d'être traduite.

## Version 0.1.<a id="mark0.1"></a>

* Module Lanceur d'applications ajouté.

* Version initiale.

