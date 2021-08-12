# Manuel de Boutique pour NVDA
## Mode d'utilisation

L'extension vient sans raccourcis assignés et nous pouvons vous donner deux qui sont:

* Affiche la fenêtre avec toutes les extensions et leurs informations: Ceci affichera une fenêtre avec toutes les extensions se trouvant sur https:www.nvda.es

* Recherche des mises à jour pour les extensions installées: Ceci analysera les extensions que nous avons et celles qui trouvent leurs mise à jour elles nous offrira la possibilité de les mettre à jour automatiquement.

Nous pouvons attribuer un geste de commande  pour ces deux options en allant dans le menu NVDA / Préférences / Gestes de commandes puis rechercher Tienda NVDA.

### Affiche la fenêtre avec toutes les extensions et leurs informations

Sur cet écran, nous aurons toutes les extensions à côté d'une fiche et la possibilité d'aller à son dépôt et de télécharger.

Si nous parcourons la fenêtre nous aurons une liste avec toutes les extensions, un dialogue en lecture seule avec la fiche de l'extension que nous avons sélectionnée, un bouton appelé "Télécharger l'extension", un bouton appelé "Visiter le site Web" pour aller au site Web de l'extension et un bouton appelé "Quitter".

Nous aurons également un champ de recherche dans lequell nous pouvons mettre ce que nous voulons rechercher et si nous appuyons sur Entrée, les résultats seront affichés dans la liste.

Eh bien, pour avoir toute la liste complète des extensions seulement nous devrons revenir au champ de recherche et effacer son contenu et appuyez sur Entrée avec le champ vide.

Dans le champ de la fiche, au cas où l'extension dispose de plus d'une branche de développement, les informations seront également affichées.

Le bouton appelé "Télécharger l'extension", nous déploiera un menu avec les différentes branches de développement de l'extension, nous devrons choisir une à télécharger. Au cas où nous n'aurions qu'une seul, ne nous donnera que cette option.

Sur cet écran, nous avons les raccourcis  clavier suivants pour nous déplacer à travers l'interface:

* Alt+R: Aller dans la zone de recherche.
* Alt+L: Aller à la liste des extensions.
* Alt+I: Aller au champ de la fiche pour voir les informations de l'extension sélectionnée.
* Alt+T: Exécutez le bouton "Télécharger l'extension".
* Alt+S: Aller au site Web de l'extension.
* Alt+Q, Échap, Alt+F4: Fermer la fenêtre.

### Recherche des mises à jour pour les extensions installées

Nous allons mettre à jour ces extensions  depuis https://www.nvda.es qui sont plus récentes que celles que nous avons sur notre ordinateur.

Sur cet écran, nous pouvons sélectionner au cas où nous aurons une mise à jour de ces extensions que nous souhaitons mettre à jour.

Nous devrons  cocher avec la barre d'espace l'extension souhaitée et appuyer sur le bouton "Mettre à jour".

Sur cet écran, nous sera affichée la mise à jour correspondante s'il y a la branche que nous avons choisie en allant dans le menu NVDA / Préférences / Paramètres / Boutique NVDA.ES et nous pouvons choisir s'il y a plus d'une branche de développement que nous voulons (expliqué bien dans la section suivante)

Sur cet écran, nous avons les raccourcis  clavier suivants:

* Alt+S: Sélectionnera toutes les extensions dans la liste pour installer toutes les mises à jour de nos extensions que nous avons installées sur notre ordinateur.
* Alt+D: Déselectionnera  dans la liste toutes les mises à jour de toutes les extensions s'ils avaient été cochés précédemment.
* Alt+M: Démarrage de la mise à jour de ces extensions que nous avons sélectionnées dans la liste.
* Alt+F, Alt+F4 ou Échap: Fermera la fenêtre.

### Écran de paramètres

Nous pouvons configurer certains aspects de l'extension Tienda NVDA en allant dans le menu NVDA / Préférences / Paramètres et rechercher la catégorie Boutique NVDA.ES.

* Activer ou désactiver la vérification des mises à jour.

Si nous activons cette case à cocher, une liste déroulante sera activée dans laquelle nous pouvons choisir la durée de temps qui va s'écouler entre une vérification et une autre.

Annoter que la case à cocher "Activer ou désactiver la vérification des mises à jour" elle est désactivée par défaut.

Le comportement de cette option est simple, elle recherchera sur le serveur s'il existe des mises à jour dans la plage de temps donnée et nous notifiera avec une notification système en disant combien de mises à jour y a-t-il et que nous ouvrions l'option correspondante dans l'extension Tienda NVDA afin de mettre à jour.

Annoter que si cette option est activée elle recherchera  10 fois la plage de temps donnée et ensuite, elle sera désactivée. Ceci est pour pas saturer les appels sur le serveur.

Par conséquent, si nous avons 15 minutes attribuées puis ne trouve pas de mises à jour à 2h 30 min cessera  de rechercher des mises à jour.

Au cas où il y a des mises à jour elle recherchera 5 fois plus la plage de temps donnée et ensuite, elle sera désactivée, chaque fois  elle nous avertira que des mises à jour ont été trouvées jusqu'à ce que nous mettrions à jour.

* Trier par ordre alphabétique Les extensions de la boutique et les recherches.

Si nous cochions cette case à cocher, lorsque nous ouvrons la boutique les extensions seront affichées par ordre alphabétique. De plus, si nous recherchons une extension, les résultats des recherches seront affichés dans l'ordre alphabétique.

* Extensions installées qui existent sur le serveur:.

Eh bien, dans cette liste, elles nous seront affichées ces extensions que nous avons installées et que, à son tour elles sont sur le serveur.

Seuls celles qui ont également une compatibilité avec l'API actuel de la NVDA seront affichés.

Dans cette liste, nous pouvons choisir quelle branche de mise à jour nous voulons pour l'extension. Si on appuie sur la barre d'espace lorsque nous sommes sur  une extension elle sera déployée toutes les branches de développement pour cette extension. Nous pouvons choisir celle que nous souhaitons avec Entrée et nous restera sauvegardée la sélection sur la liste.

AVERTISSEMENT: les changements de la liste ne seront sauvegardées que si Nous cliquons sur le bouton OK ou Appliquer  ddu dialogue Paramètres.

Cette liste est mise à jour à chaque fois que nous redémarrons NVDA en ajoutant s'il y a de nouvelles extensions ou en supprimant Celles qui ne sont plus.

Par conséquent, si nous supprimons une extension et que nous allons ensuite l'installer, nous devrons ré-sélectionner la branche que nous souhaitons à nouveau.

Cette liste tantôt la première fois qui est générée comme chaque fois qu'une extension est ajoutée, elle mettra toujours la première branche de développement du serveur par défaut.

## Remarques

Lorsque vous vérifier les mises à jour, vous avez deux protections:

1º Vérifiera s'il y a des extensions qui vont être désinstallées.

Si tel est le cas, ces extensions sont exclues, même s'il y a des mises à jour.

2º Il sera validé que l'extension du serveur répond aux exigences de l'API NVDA que nous avons installée.

Si cela n'est pas rempli, l'extension ne peut pas être installée, bien que la version du serveur soit plus récente et que le serveur nous offre cette extension.

Lors de l'installation plusieurs protections ont également été incluses:

1º Maintenant  nous informera si une extension n'a pas pu être mise à jour et nous donnera  son nom.

2º Dans cette étape, il sera également vérifié si l'extension à installer a la version minimale à utiliser dans notre NVDA que nous avons installée.

3º L'extension Tienda NVDA ne vous permettra pas de continuer à chercher des mises à jour si nous avons déjà effectué une mise à jour d'une extension ou de plusieurs et nous n'avons pas décidé de redémarrer NVDA.

4º Si nous avons activé cette option appelée "Recherche des mises à jour pour les extensions installées" chaque fois qu'elle recherche et détecte que nous n'avons pas redémarré NVDA nous serons notifiés avec une notification système.

5º De même, si nous essayons d'activer l'option appelée "Recherche des mises à jour pour les extensions installées" et que nous n'avons pas redémarré NVDA le lecteur nous verbalisera un message comme quoi nous devons redémarrer  NVDA pour que ces mises à jour prennent effet.

6º Dans le pire des cas si les librairies ne laissent pas  charger parce que nous n'avons pas Internet, nous serons affichés des messages d'informations dans le journal de NVDA et si nous essayons d'accéder à la boutique nous serons informé avec un message parlé.

La fonction qui recherche les mises à jour est améliorée, il est maintenant beaucoup plus fiable et ajoute également les protections mentionnées précédemment.

De nombreuses améliorations internes ont été faites pour la rendre plus robuste.

Cette extension est en phase de test donc c'est pour cela que nous vous demandons de comprendre qu'il peut y avoir des erreurs.

Nous vous remercions de bien vouloir nous contacter pour signaler ce désagrément et le résoudre dès que possible.

Profitez de la Boutique pour NVDA !
