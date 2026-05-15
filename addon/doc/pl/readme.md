# Sklep z dodatkami dla NVDA

> **Ważna informacja dla testerów wersji beta:**
> Jeśli testowałeś dodatek **TiendaNVDA_Modern**, odinstaluj go przed instalacją tej wersji. Tamta wersja była wersją testową i beta, więc nie powinna działać równocześnie z tą wersją końcową. Aby ją odinstalować, przejdź do menu NVDA -> Narzędzia -> Sklep z dodatkami, wybierz "TiendaNVDA_Modern" i usuń go. Następnie uruchom NVDA ponownie i dopiero zainstaluj tę wersję.

Ujednolicony sklep dodatków dla NVDA: łączy **sklep społeczności hiszpańskojęzycznej (NVDA.ES)** oraz **oficjalny sklep NV Access** w jednym dostępnym interfejsie.

**Autor:** Héctor J. Benítez Corredera<br>
**Licencja:** GNU General Public License v2<br>
**Wersja:** 2026.05.09<br>
**Zgodność:** NVDA 2025.1 do NVDA 2026.1<br>
**Repozytorium:** [https://github.com/hxebolax/Tienda-para-NVDA](https://github.com/hxebolax/Tienda-para-NVDA)

---

## Spis treści

1. [Wprowadzenie](#introduccion)
2. [Instalacja](#instalacion)
3. [Pierwsze kroki](#primeros-pasos)
4. [Trzy sklepy](#las-tres-tiendas)
5. [Interfejs sklepu](#la-interfaz-de-la-tienda)
6. [Wskaźniki stanu](#indicadores-de-estado)
7. [Skróty klawiszowe i funkcje specjalne](#teclas-rapidas-y-funciones-especiales)
8. [Menu kontekstowe](#menu-contextual)
9. [Zarządzanie zainstalowanymi dodatkami](#gestion-de-complementos-instalados)
10. [Pakowarka dodatków](#empaquetador-de-complementos)
11. [Wyszukiwanie aktualizacji](#buscar-actualizaciones)
12. [Panel opcji](#panel-de-opciones)
13. [System pamięci podręcznej](#sistema-de-cache)
14. [Tryb offline](#modo-offline)
15. [Kopia zapasowa i przywracanie](#backup-y-restauracion)
16. [Tłumaczenie opisów](#traduccion-de-descripciones)
17. [Serwery niestandardowe](#servidores-personalizados)
18. [Uwagi i zabezpieczenia](#observaciones-y-protecciones)
19. [Podsumowanie skrótów klawiszowych](#resumen-de-teclas-rapidas)
20. [Rejestr zmian](#registro-de-cambios)

---

<a name="introduccion"></a>
## Wprowadzenie

**Sklep z dodatkami dla NVDA** jest kompletnym rozwinięciem dawnego sklepu dla NVDA.ES. Został przebudowany od podstaw, aby zapewnić nowocześniejsze, szybsze i ujednolicone korzystanie z dodatków.

### Co nowego w porównaniu z poprzednią wersją?

- **Ujednolicony sklep:** przeglądanie dodatków z NVDA.ES i oficjalnego sklepu NV Access w jednym oknie.
- **Wskaźniki stanu:** każdy dodatek pokazuje bieżący stan, na przykład zainstalowany, dostępna aktualizacja, wyłączony lub niezgodny.
- **Zarządzanie lokalne:** wyłączanie, włączanie i odinstalowywanie dodatków bez opuszczania sklepu.
- **Wielopoziomowa pamięć podręczna:** cache serwerów, cache tłumaczeń i cache list, co przyspiesza ładowanie.
- **Tryb offline:** przeglądanie sklepu bez połączenia z internetem przy użyciu danych zapisanych w pamięci podręcznej.
- **Kopia zapasowa i przywracanie:** tworzenie kopii listy dodatków i przywracanie ich po zmianie komputera.
- **Pakowarka:** tworzenie plików `.nvda-addon` z dowolnego zainstalowanego dodatku.
- **Cicha instalacja:** instalowanie dodatków w tle, bez dodatkowych okien dialogowych.
- **Inteligentny restart:** sklep sprawdza, czy faktycznie coś zainstalowano, zanim poprosi o ponowne uruchomienie NVDA.
- **Sprawdzanie zależności:** przed instalacją weryfikowane jest spełnienie wymaganych zależności.
- **Tłumaczenie z pamięcią podręczną:** opisy można tłumaczyć klawiszem F3, a wynik jest zapisywany, aby nie wykonywać tej samej operacji ponownie.
- **Lepsze powiadomienia:** powiadomienia o aktualizacjach pokazują źródło, czyli NVDA.ES albo sklep oficjalny, oraz nazwy dodatków.

---

<a name="instalacion"></a>
## Instalacja

1. Pobierz plik `.nvda-addon` ze strony [wydań repozytorium](https://github.com/hxebolax/Tienda-para-NVDA/releases).
2. Otwórz pobrany plik albo przeciągnij go na okno NVDA.
3. Potwierdź instalację, gdy NVDA o to poprosi.
4. Uruchom NVDA ponownie, aby aktywować dodatek.

---

<a name="primeros-pasos"></a>
## Pierwsze kroki

Dodatek jest dostarczany **bez przypisanych skrótów klawiszowych**. Własne skróty możesz przypisać w:

**Menu NVDA -> Preferencje -> Zdarzenia wejścia -> Sklep z dodatkami NVDA**

Znajdziesz tam następujące akcje:

- Pokaż okno ze wszystkimi dodatkami NVDA.ES
- Wyszukaj aktualizacje dodatków zainstalowanych z NVDA.ES
- Pokaż okno ze wszystkimi dodatkami z oficjalnego sklepu
- Wyszukaj aktualizacje oficjalnych dodatków
- Pokaż ujednolicony sklep ze wszystkimi źródłami dodatków

### Dostęp z menu

Do wszystkich funkcji można też przejść z menu NVDA:

**Menu NVDA -> Narzędzia -> Sklep z dodatkami NVDA**

W tym miejscu dostępne są następujące podmenu:

- **Sklep NVDA.ES:** lista dodatków i wyszukiwanie aktualizacji ze społeczności hiszpańskojęzycznej.
- **Oficjalny sklep NVDA:** lista dodatków i wyszukiwanie aktualizacji z oficjalnego sklepu.
- **Ujednolicony sklep (wszystkie źródła):** pokazuje wszystkie dodatki ze wszystkich źródeł na jednej liście.
- **Pakowarka dodatków:** pozwala spakować zainstalowane dodatki jako pliki `.nvda-addon`.
- **Dokumentacja dodatku:** otwiera tę dokumentację w domyślnej przeglądarce.

---

<a name="las-tres-tiendas"></a>
## Trzy sklepy

Nowa wersja integruje trzy tryby wyświetlania dodatków.

### Sklep NVDA.ES

Jest to sklep społeczności hiszpańskojęzycznej. Pobiera dodatki z serwera [https://nvda.es](https://nvda.es) oraz z dowolnego serwera niestandardowego, który dodasz samodzielnie.

### Oficjalny sklep NVDA

Zapewnia dostęp do oficjalnego sklepu dodatków NV Access ([https://addons.nvda-project.org](https://addons.nvda-project.org)). Dodatki z tego źródła są pobierane bezpośrednio z API oficjalnego sklepu i pokazywane z pełnymi informacjami o zgodności.

### Ujednolicony sklep

To widok łączony, który pokazuje **wszystkie dodatki ze wszystkich źródeł** na jednej liście. Dodatki są oznaczane etykietami `[ES]` (społeczność hiszpańskojęzyczna) i `[OF]` (sklep oficjalny), aby było wiadomo, skąd pochodzi dany dodatek.

---

<a name="la-interfaz-de-la-tienda"></a>
## Interfejs sklepu

Po otwarciu dowolnego sklepu pojawia się okno podzielone na dwa panele.

### Lewy panel, czyli obszar pracy

1. **Pole wyszukiwania:** po otwarciu sklepu fokus trafia właśnie tutaj. Wpisz dowolny tekst i naciśnij Enter, aby przefiltrować listę. Aby ponownie pokazać wszystkie dodatki, usuń zawartość pola i naciśnij Enter przy pustym polu.

2. **Lista dodatków:** pokazuje wszystkie dostępne dodatki wraz ze wskaźnikiem stanu w nawiasach kwadratowych, na przykład `[I]` albo `[U]`. Po liście poruszasz się strzałkami w górę i w dół.

3. **Przycisk akcji, Instaluj/Aktualizuj:** jest dynamiczny i automatycznie zmienia tekst zależnie od stanu zaznaczonego dodatku:
   - jeśli dodatek nie jest zainstalowany, pokazuje **"Instaluj"**;
   - jeśli jest dostępna aktualizacja, pokazuje **"Aktualizuj"**.

### Prawy panel, czyli karta informacyjna

Podczas poruszania się po liście dodatków ten panel wypełnia się pełnymi informacjami o zaznaczonym dodatku:

- nazwa i podsumowanie;
- wersja dostępna na serwerze;
- wersja zainstalowana, jeśli dotyczy;
- autor;
- pełny opis;
- zgodność z NVDA, czyli wersja minimalna i ostatnia przetestowana;
- liczba pobrań, jeśli jest dostępna;
- stan instalacji.

---

<a name="indicadores-de-estado"></a>
## Wskaźniki stanu

Podczas poruszania się po liście dodatków NVDA wypowiada litery w nawiasach kwadratowych. Oznaczają one stan danego dodatku.

| Wskaźnik | Znaczenie |
|:---------|:----------|
| **[I]** | **Zainstalowany:** dodatek jest zainstalowany i aktywny. |
| **[U]** | **Aktualizacja:** dostępna jest nowsza wersja. Warto zaktualizować. |
| **[U-I]** | **Niezgodna aktualizacja:** dostępna jest nowsza wersja, ale nie jest zgodna z Twoją wersją NVDA. |
| **[D]** | **Wyłączony:** dodatek jest zainstalowany, ale ręcznie wyłączony. |
| **[R]** | **Oczekuje na usunięcie:** dodatek zostanie usunięty po ponownym uruchomieniu NVDA. |
| **[I-I]** | **Zainstalowany niezgodny:** dodatek jest zainstalowany, ale zablokowany z powodu niezgodności z Twoją wersją NVDA. |
| **[X]** | **Niezgodny:** dodatek nie jest zgodny z Twoją wersją NVDA. |

W **ujednoliconym sklepie** widoczne jest również źródło dodatku.

| Etykieta | Źródło |
|:---------|:------|
| **[ES]** | Serwery NVDA.ES, czyli społeczność hiszpańskojęzyczna |
| **[OF]** | Oficjalny sklep NV Access |

---

<a name="teclas-rapidas-y-funciones-especiales"></a>
## Skróty klawiszowe i funkcje specjalne

Te klawisze działają wtedy, gdy fokus znajduje się na liście dodatków.

### F1 - bieżąca pozycja

Naciśnij **F1**, aby NVDA powiedział, na której pozycji listy jesteś, na przykład: "Dodatek 15 z 200".

### Ctrl+F1 - wyjaśnienie wskaźnika

Jeśli nie pamiętasz, co oznaczają wskaźniki `[I]` albo `[U]`, naciśnij **Ctrl+F1**. NVDA wyjaśni prostym językiem stan zaznaczonego dodatku.

### F2 - odczytanie całej karty

Naciśnij **F2**, aby NVDA przeczytał całą kartę techniczną i opis dodatku **bez przechodzenia tabulatorem do prawego panelu**. Działa to we wszystkich sklepach.

### F3 - tłumaczenie opisu

Jeśli opis jest po angielsku albo w innym języku, naciśnij **F3**, a sklep przetłumaczy go na język ustawiony w opcjach. Domyślnie jest to hiszpański, ale można wybrać też polski. Na początku i na końcu tłumaczenia odtworzony zostanie dźwięk.

> **Uwaga:** aby używać F3, musisz najpierw włączyć tłumacza w opcjach dodatku. Funkcja wymaga połączenia z internetem.

---

<a name="menu-contextual"></a>
## Menu kontekstowe

Na liście dodatków naciśnij **klawisz aplikacji** albo **Shift+F10**, aby otworzyć menu kontekstowe z następującymi opcjami.

### Filtry

- **Pokaż wszystkie dodatki:** pokazuje pełną listę. Jest to opcja domyślna.
- **Pokaż dodatki według zgodności API:** filtruje dodatki zgodne z określoną wersją NVDA.
- **Pokaż dodatki posortowane według autora:** sortuje listę według nazwy autora.
- **Pokaż według liczby pobrań od największej do najmniejszej:** sortuje dodatki według popularności.

> **Uwaga:** filtry nie łączą się ze sobą. Każdy filtr działa osobno, a tytuł okna informuje o aktywnym filtrze. Wybrany filtr pozostaje aktywny do czasu ponownego uruchomienia NVDA.

### Kopiowanie do schowka

- **Kopiuj informacje:** kopiuje pełną kartę zaznaczonego dodatku.
- **Kopiuj link do strony internetowej:** kopiuje oficjalny adres URL dodatku.
- **Kopiuj link pobierania:** podmenu z dostępnymi gałęziami rozwoju, z którego można skopiować bezpośredni adres pobierania.

---

<a name="gestion-de-complementos-instalados"></a>
## Zarządzanie zainstalowanymi dodatkami

Jedną z ważniejszych funkcji jest możliwość zarządzania już zainstalowanym dodatkiem **bez opuszczania sklepu**.

1. Wybierz na liście dodatek oznaczony jako `[I]`, `[D]` albo `[U]`.
2. Naciśnij **klawisz aplikacji** albo kliknij prawym przyciskiem.
3. W podmenu **Zarządzanie zainstalowanym** znajdziesz:

- **Wyłącz / Włącz:** tymczasowo wyłącza albo włącza dodatek.
- **Odinstaluj:** oznacza dodatek do usunięcia. Usunięcie nastąpi po ponownym uruchomieniu NVDA.
- **Zobacz dokumentację:** otwiera dokumentację dodatku w przeglądarce. Jeśli dokumentacja istnieje w Twoim języku, zostanie otwarta ta wersja; w przeciwnym razie użyty zostanie domyślny język dodatku.

---

<a name="empaquetador-de-complementos"></a>
## Pakowarka dodatków

Pakowarka pozwala tworzyć pliki `.nvda-addon` z dodatków, które są już zainstalowane. Przydaje się to do:

- udostępnienia dodatku innej osobie bez szukania go w sklepie;
- utworzenia kopii zapasowej konkretnego dodatku;
- zachowania wybranej wersji dodatku przed aktualizacją.

**Aby spakować dodatek:**

1. Przejdź do **Menu NVDA -> Narzędzia -> Sklep z dodatkami NVDA -> Pakowarka dodatków**.
2. Wybierz z listy dodatek, który chcesz spakować.
3. Wskaż katalog, w którym ma zostać zapisany plik.
4. Plik `.nvda-addon` zostanie utworzony automatycznie w formacie `nazwa_wersja_Gen.nvda-addon`.

---

<a name="buscar-actualizaciones"></a>
## Wyszukiwanie aktualizacji

Dodatek oferuje dwa sposoby wyszukiwania aktualizacji.

### Wyszukiwanie ręczne

W menu narzędzi wybierz **Szukaj aktualizacji** w jednym ze sklepów, NVDA.ES albo oficjalnym. Zostanie wyświetlone okno z dodatkami, dla których są dostępne aktualizacje.

W tym oknie możesz:

- **wybierać dodatki pojedynczo:** użyj spacji, aby zaznaczać lub odznaczać pozycje;
- **Alt+S:** zaznaczyć wszystkie dodatki do aktualizacji;
- **Alt+D:** odznaczyć wszystkie dodatki;
- **Alt+A:** rozpocząć aktualizowanie zaznaczonych dodatków;
- **Alt+C / Escape / Alt+F4:** zamknąć okno.

### Sprawdzanie automatyczne

Po włączeniu automatycznego sprawdzania w opcjach:

- sklep będzie szukał aktualizacji w tle zgodnie z ustawionym interwałem;
- pojawi się powiadomienie systemowe z liczbą aktualizacji i ich źródłem;
- wyszukiwanie zatrzyma się automatycznie po 10 sprawdzeniach bez wyniku albo po 5 sprawdzeniach po znalezieniu aktualizacji, aby nie przeciążać serwera.

Powiadomienia są bardziej szczegółowe, na przykład:

```text
Znaleziono 3 aktualizacje.
- NVDA.ES (2): Dodatek A, Dodatek B
- Oficjalny sklep (1): Dodatek C

Uruchom wyszukiwanie aktualizacji dodatków.
```

---

<a name="panel-de-opciones"></a>
## Panel opcji

Konfigurację dodatku otworzysz z:

**Menu NVDA -> Preferencje -> Opcje -> Sklep z dodatkami NVDA**

### A. Sklep NVDA.ES

- **Wybierz serwer dodatków:** wybiera domyślny serwer spośród skonfigurowanych serwerów.
- **Zarządzaj serwerami dodatków:** otwiera menedżer, w którym możesz dodawać, edytować i usuwać serwery niestandardowe.

### B. Oficjalny sklep NVDA

- **Włącz oficjalny sklep NVDA:** włącza albo wyłącza integrację z oficjalnym sklepem NV Access.
- **Zezwalaj na niezgodne dodatki z oficjalnego sklepu:** pozwala próbować instalować dodatki oznaczone jako niezgodne. **Używasz tej opcji na własną odpowiedzialność.**

### C. Aktualizacje

- **Włącz automatyczne sprawdzanie aktualizacji:** uruchamia wyszukiwanie w tle.
- **Interwał sprawdzania aktualizacji:** pozwala wybrać odstęp między sprawdzeniami:
  - 15 minut, 30 minut, 45 minut, 1 godzina, 12 godzin, 1 dzień, 1 tydzień.
- **Uwzględniaj aktualizacje z oficjalnego sklepu:** dodaje aktualizacje z oficjalnego sklepu do automatycznego sprawdzania.

### D. Tłumaczenie

- **Włącz tłumacza opisów:** włącza użycie klawisza F3 do tłumaczenia opisów.
- **Język tłumaczenia opisów:** wybierz jeden z 12 języków: niemiecki, arabski, chorwacki, hiszpański, francuski, angielski, włoski, polski, portugalski, rosyjski, turecki i ukraiński.

### E. Opcje ogólne

- **Sortuj dodatki alfabetycznie:** sortuje listę od A do Z.
- **Instaluj dodatki po pobraniu:** po zakończeniu pobierania automatycznie otwiera kreatora instalacji.
- **Instaluj po cichu:** dodatki są instalowane w tle, bez dodatkowych okien dialogowych. Na końcu pojawia się tylko prośba o ponowne uruchomienie.
- **Włącz pamięć podręczną serwerów:** zapisuje listy dodatków na dysku, aby szybciej je ładować.
- **Odświeżaj pamięć podręczną co...:** ustawia interwał odnawiania cache.
- **Używaj pamięci podręcznej dla tłumaczeń:** tłumaczenia wykonane klawiszem F3 są zapisywane, aby nie pytać ponownie Google.
- **Włącz tryb offline:** pozwala przeglądać sklep bez internetu, używając list zapisanych w cache.

### F. Kopia zapasowa i przywracanie

- **Utwórz kopię zapasową dodatków:** generuje plik JSON z listą wszystkich zainstalowanych dodatków.
- **Przywróć z kopii zapasowej:** wczytuje plik kopii zapasowej i pozwala ponownie zainstalować wymienione w nim dodatki.

### G. Zainstalowane dodatki dostępne na serwerze

Na dole opcji znajduje się lista Twoich dodatków, które są też dostępne na serwerze. Z tego miejsca możesz:

1. Wybrać dodatek i nacisnąć **spację**.
2. W menu podręcznym wybrać **kanał aktualizacji** (stabilny, beta, rozwojowy itd.) albo **Odrzuć aktualizacje**, aby sklep przestał informować o tym dodatku.

> **Ważne:** zmiany są zapisywane dopiero po naciśnięciu OK albo Zastosuj w oknie opcji.

---

<a name="sistema-de-cache"></a>
## System pamięci podręcznej

Sklep używa wielopoziomowego systemu pamięci podręcznej, aby przyspieszyć działanie.

### Cache serwerów

Listy dodatków są zapisywane na dysku. Jeśli cache nie wygasł, po otwarciu sklepu lista jest ładowana z dysku zamiast z serwera.

- Opcja znajduje się w ustawieniu **Włącz pamięć podręczną serwerów**.
- Interwał odświeżania można skonfigurować.

### Cache tłumaczeń

Tłumaczenia wykonane klawiszem F3 są zapisywane w trwałym pliku JSON. Przy kolejnym żądaniu tego samego tłumaczenia wynik zostanie odczytany natychmiast z cache.

- Opcja znajduje się w ustawieniu **Używaj pamięci podręcznej dla tłumaczeń**.

### Cache w pamięci RAM

Oprócz cache na dysku sklep przechowuje najczęstsze zapytania w pamięci RAM, co ogranicza dostęp do dysku podczas bieżącej sesji.

---

<a name="modo-offline"></a>
## Tryb offline

Tryb offline pozwala przeglądać sklep **bez połączenia z internetem**, używając wcześniej zapisanych danych.

Aby go używać:

1. Włącz opcje **Włącz pamięć podręczną serwerów** i **Włącz tryb offline**.
2. Otwórz sklep przynajmniej raz z działającym internetem, aby utworzyć cache.
3. Następnym razem, gdy otworzysz sklep bez internetu, dane zostaną wczytane z cache.

> **Uwaga:** w trybie offline nie można pobierać ani instalować dodatków, ale można czytać informacje o dodatkach, które wcześniej zostały zapisane w cache.

---

<a name="backup-y-restauracion"></a>
## Kopia zapasowa i przywracanie

### Tworzenie kopii zapasowej

1. Przejdź do **Opcje -> Sklep z dodatkami NVDA -> Utwórz kopię zapasową dodatków**.
2. Wybierz nazwę i miejsce zapisu pliku `.json`.
3. Zostanie utworzony plik z listą wszystkich zainstalowanych dodatków, obejmujący nazwę, wersję i podsumowanie.

### Automatyczna kopia przy zamykaniu

Sklep może automatycznie tworzyć kopię zapasową przy zamykaniu NVDA, jeśli odpowiednia opcja jest włączona.

### Przywracanie z kopii zapasowej

1. Przejdź do **Opcje -> Sklep z dodatkami NVDA -> Przywróć z kopii zapasowej**.
2. Wybierz plik `.json` kopii zapasowej.
3. Sklep pokaże kreatora, który wyszuka najnowsze wersje każdego dodatku na serwerach i pozwoli zainstalować je zbiorczo.

> **Przydatne do:** przeniesienia dodatków na nowy komputer albo odtworzenia konfiguracji po ponownej instalacji NVDA.

---

<a name="traduccion-de-descripciones"></a>
## Tłumaczenie opisów

Sklep ma wbudowanego tłumacza opartego o Google Translate.

1. **Włącz tłumacza** w opcjach dodatku.
2. **Wybierz język docelowy**, domyślnie jest to hiszpański.
3. **Naciśnij F3** na dowolnym dodatku na liście, aby przetłumaczyć jego opis.

Funkcje:

- dźwięk rozpoczęcia i zakończenia tłumaczenia;
- zapisywanie tłumaczeń w cache, aby nie powtarzać tych samych zapytań;
- tłumaczenie znika po przejściu do innego dodatku, więc w razie potrzeby naciśnij F3 ponownie;
- wymagane jest połączenie z internetem.

---

<a name="servidores-personalizados"></a>
## Serwery niestandardowe

Możesz dodać zewnętrzne repozytoria dodatków, jeśli używają formatu zgodnego z NVDA.ES.

### Dodawanie serwera

1. Przejdź do **Opcje -> Sklep z dodatkami NVDA -> Zarządzaj serwerami dodatków**.
2. Naciśnij **Dodaj**.
3. Wpisz opisową nazwę i adres URL serwera.
4. Zatwierdź, a serwer pojawi się w wyborze serwerów.

### Przykład: serwer społeczności rosyjskiej

- **Nazwa:** Społeczność rosyjska
- **URL:** `https://nvda-addons.ru/get.php?addonslist`

### Szybka zmiana serwera

W głównym oknie sklepu NVDA.ES naciśnij **Alt+C** albo przycisk **Zmień serwer**, aby rozwinąć menu z wszystkimi skonfigurowanymi serwerami. Zmiana działa natychmiast i tymczasowo; jako domyślna zostanie zapisana dopiero po zmianie w opcjach.

> **Uwaga:** domyślnego serwera społeczności hiszpańskojęzycznej nie można edytować ani usunąć.

---

<a name="observaciones-y-protecciones"></a>
## Uwagi i zabezpieczenia

Dodatek zawiera kilka zabezpieczeń, które mają zapewnić stabilne działanie:

1. **Dodatki oczekujące na odinstalowanie:** są automatycznie pomijane podczas sprawdzania aktualizacji.
2. **Walidacja zgodności API:** nawet jeśli wersja na serwerze jest nowsza, aktualizacja nie zostanie zaproponowana, jeśli nie jest zgodna z Twoją wersją NVDA.
3. **Powiadomienia o błędach instalacji:** jeśli któregoś dodatku nie uda się zaktualizować, pojawi się informacja z jego nazwą.
4. **Blokada po aktualizacji:** sklep nie pozwala szukać kolejnych aktualizacji, jeśli wykonano aktualizację i NVDA nie został jeszcze ponownie uruchomiony.
5. **Powiadomienie po restarcie:** jeśli automatyczne sprawdzanie wykryje, że po aktualizacji nie uruchomiono ponownie NVDA, pojawi się przypomnienie.
6. **Ochrona przy braku internetu:** jeśli biblioteki nie mogą zostać wczytane z powodu braku połączenia, informacja trafi do logu NVDA, a przy próbie wejścia do sklepu usłyszysz komunikat.
7. **Inteligentny restart:** sklep wykrywa, czy dodatek faktycznie został zainstalowany. Jeśli anulujesz instalator, nie będzie niepotrzebnej prośby o restart.
8. **Sprawdzanie zależności:** przed instalacją weryfikowane jest spełnienie wymaganych zależności.

---

<a name="resumen-de-teclas-rapidas"></a>
## Podsumowanie skrótów klawiszowych

### Główne okno sklepu

| Akcja | Klawisz |
|:------|:--------|
| Przejście do pola wyszukiwania | `Alt+B` |
| Przejście do listy dodatków | `Alt+L` |
| Instalacja / aktualizacja | `Alt+I` |
| Przejście do informacji o dodatku | `Alt+I` w prawym panelu |
| Przejście do strony internetowej dodatku | `Alt+P` |
| Zmiana serwera, tylko NVDA.ES | `Alt+C` |
| Zamknięcie sklepu | `Alt+S` / `Escape` / `Alt+F4` |

### Na liście dodatków

| Akcja | Klawisz |
|:------|:--------|
| Odczyt bieżącej pozycji na liście | `F1` |
| Wyjaśnienie wskaźnika stanu | `Ctrl+F1` |
| Odczyt pełnej karty dodatku | `F2` |
| Tłumaczenie opisu | `F3` |
| Menu kontekstowe, filtry, kopiowanie i zarządzanie | `Klawisz aplikacji` / `Shift+F10` |

### Okno aktualizacji

| Akcja | Klawisz |
|:------|:--------|
| Zaznaczenie wszystkich dodatków | `Alt+S` |
| Odznaczenie wszystkich | `Alt+D` |
| Rozpoczęcie aktualizacji | `Alt+A` |
| Zamknięcie okna | `Alt+C` / `Escape` / `Alt+F4` |

---

<a name="registro-de-cambios"></a>
## Rejestr zmian

### Wersja 2026.05.11

* Dodano cichy aktualizator języków dodatku (w fazie beta).
* Dodano język rosyjski (Valentín N. Kupriyanov).

### Wersja 2026.05.10

* Dodano język turecki (Umut Korkmaz).

### Wersja 2026.05.09

* Pierwsza wersja ujednoliconego sklepu dodatków dla NVDA.
* Pełna integracja sklepu NVDA.ES i oficjalnego sklepu NV Access.
* Nowy system wskaźników stanu: [I], [U], [D], [R], [I-I], [U-I], [X].
* Lokalne zarządzanie dodatkami: wyłączanie, włączanie i odinstalowywanie bez opuszczania sklepu.
* Wielopoziomowy system pamięci podręcznej: cache serwerów, cache tłumaczeń i cache list.
* Tryb offline: przeglądanie sklepu bez internetu przy użyciu danych zapisanych w cache.
* Kopia zapasowa i przywracanie zainstalowanych dodatków.
* Pakowarka dodatków: tworzenie plików `.nvda-addon` z zainstalowanych dodatków.
* Inteligentne sprawdzanie zależności i zgodności API.
* Cicha instalacja z inteligentnym restartem.
* Tłumaczenie opisów z trwałą pamięcią podręczną przez Google Translate.
* Obsługa niestandardowych serwerów dodatków.
* Interfejs ze skrótami F1, Ctrl+F1, F2 i F3 do szybkiego dostępu do funkcji.
* Szczegółowe powiadomienia wskazujące źródło aktualizacji, czyli ES albo oficjalne.

### Poprzednie wersje, sklep dla NVDA.ES

To repozytorium zawierało wcześniej klasyczną wersję **sklepu dla NVDA.ES** (wersje 0.1 do 0.10). Od wersji 2026.05.09 repozytorium zostało zastąpione nowym **ujednoliconym sklepem dodatków dla NVDA**, czyli kompletnym przepisaniem dodatku.

Jeśli chcesz sprawdzić kod źródłowy albo dokumentację starej wersji, możesz przejrzeć historię commitów w repozytorium GitHub:

1. Przejdź do [https://github.com/hxebolax/Tienda-para-NVDA](https://github.com/hxebolax/Tienda-para-NVDA).
2. Kliknij link **commits** albo licznik commitów widoczny u góry repozytorium.
3. Znajdź dowolny commit sprzed **9 maja 2026**, aby uzyskać dostęp do kodu i wydań klasycznego sklepu.
4. Po wejściu w wybrany commit możesz kliknąć **Browse files**, aby zobaczyć pełny stan repozytorium z tego momentu.

Alternatywnie starsze wydania z plikami `.nvda-addon` powinny pozostać dostępne w sekcji [Releases](https://github.com/hxebolax/Tienda-para-NVDA/releases), o ile nie zostaną ręcznie usunięte.

---

Miłego korzystania ze sklepu z dodatkami dla NVDA.

**Z pozdrowieniami:** Héctor J. Benítez Corredera.
