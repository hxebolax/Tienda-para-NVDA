# Магазин для NVDA
## Как использовать

Плагин поставляется без назначенных ярлыков, и мы можем предоставить вам два, которые:

* Отображает окно со всеми плагинами и их информацией: нам будет показано окно со всеми плагинами, которые есть в https:www.nvda.es

* Проверьте наличие обновлений установленных плагинов: он проанализирует плагины, которые у нас есть, и те, которые он находит обновление, предложит нам возможность автоматически обновлять их.

Мы можем назначить жест ввода для этих двух параметров, перейдя в меню NVDA / настройки / жесты ввода и поиск NVDA Store.

### Отображает окно со всеми плагинами и их информацией

На этом экране у нас будут все плагины рядом с вкладкой и возможность перейти в ваш репозиторий и загрузить.

Если мы пройдем через окно, у нас будет список всех плагинов, поле только для чтения с выбранной вкладкой плагина, кнопка "Загрузить плагин", кнопка "посетить веб-страницу", чтобы перейти на страницу плагина, и кнопка "выйти".

Кроме того, у нас будет окно поиска, в котором вы можете поместить то, что вы хотите найти, и если вы нажмете Enter, результаты будут отображаться в списке.

Чтобы вернуть весь список плагинов, вам просто нужно вернуться в поле поиска, удалить его содержимое и нажать Enter с пустым полем.

В поле вкладки, если плагин имеет более одной ветви разработки, нам также будет показана информация.

Кнопка под названием "Загрузить плагин" развернет меню с различными ветвями разработки плагина, нам нужно будет выбрать один для загрузки. В случае, если у вас есть только один, нам будет предоставлен этот вариант.

На этом экране у нас есть следующие горячие клавиши для перемещения по интерфейсу:

* Alt + B: перейти в окно поиска.
* Alt+L: перейти к списку плагинов.
* Alt+I: перейдите в поле вкладки, чтобы просмотреть информацию о выбранном плагине.
* Alt+D: запустите кнопку "Загрузить плагин".
* Alt + P: перейти на страницу плагина.
* Alt+S, Escape, Alt+F4: Закрыть окно.

### Проверьте наличие обновлений установленных плагинов

Это позволит нам обновить те плагины, которые в https://www.nvda.es будьте новее, чем у нас в команде.

На этом экране вы можете выбрать, если есть обновления те плагины, которые вы хотите обновить.

Нам нужно будет пометить пробелом нужный плагин и нажать кнопку "Обновить".

На этом экране нам будет показано соответствующее обновление, если оно есть для выбранной ветви, перейдя в меню NVDA / Настройки / Параметры / магазин NVDA.Есть и там мы можем выбрать, есть ли более одной ветви развития, которую мы хотим (хорошо объяснено в следующем разделе)

На этом экране у нас есть следующие клавиши:

* Alt+S: выберите Все плагины из списка, чтобы установить все обновления наших плагинов, установленные на нашем компьютере.
* Alt+D: мы отменим выбор из списка всех обновлений всех плагинов, если они были ранее отмечены.
* Alt+A: начнется обновление тех плагинов, которые мы выбрали в списке.
* Alt+C, Alt+F4 или Escape: закроет окно.

### Панель параметров

Вы сможете настроить некоторые аспекты плагина Store, перейдя в меню NVDA / Настройки / Параметры и найдя категорию Store NVDA.ES.

* Включить или отключить проверку обновлений.

Если мы установим этот флажок, появится поле со списком, в котором мы сможем выбрать, сколько времени пройдет между одной проверкой и другой.

Сказать, что флажок" Включить или отключить проверку обновлений " отключен по умолчанию.

Поведение этой опции простое, он будет искать сервер, есть ли обновления в заданном временном диапазоне, и уведомлять нас системным уведомлением о том, сколько обновлений есть, и открыть соответствующую опцию в плагине NVDA Store для обновления.

Сказать, что если эта опция включена, она будет искать в 10 раз диапазон заданного времени, а затем отключена. Это делается для того, чтобы не загромождать вызовы на сервер.

Таким образом, если у нас есть 15 минут, выделенных и не найти обновления в 2h 30 min он перестанет проверять наличие обновлений.

В случае, если есть обновления, он искал в 5 раз больше заданного временного диапазона, а затем отключался, каждый раз он сообщал нам, что обновления были найдены, пока мы не обновим.

* Сортировка в алфавитном порядке дополнений магазина и поисков.

Если мы установим этот флажок, когда мы откроем магазин, нам будут показаны плагины в алфавитном порядке. Кроме того, если мы ищем какие-либо дополнения, Результаты поиска будут отображаться в алфавитном порядке.

* Установленные плагины на сервере.

Хорошо в этом списке нам будут показаны те плагины, которые у нас установлены и, в свою очередь, находятся на сервере.

Будут отображаться только те, которые также поддерживают текущий API NVDA.

В этом списке мы можем выбрать, какую ветку обновления мы хотим для плагина. Если мы нажмем пробел над плагином мы развернем все ветви разработки для этого плагина. Вы можете выбрать тот, который вы хотите с Intro, и выбор будет сохранен в списке.

Предупреждение: изменения в списке будут сохранены только в том случае, если мы нажмем кнопку OK или Apply в диалоге параметров.

Этот список обновляется каждый раз, когда мы перезапускаем NVDA, добавляя, Если есть новые плагины, или удаляя те, которых больше нет.

Поэтому, если мы удалим плагин, а затем переустановим его, нам придется снова выбрать ветку, которую мы хотим.

Этот список как при первом создании, так и при каждом добавлении плагина всегда будет по умолчанию ставить первую ветвь разработки на сервере.

## Наблюдения

Когда вы проверяете наличие обновлений, теперь у вас есть две защиты:

1-й проверит, есть ли плагины, которые будут удалены.

Если это так, эти плагины исключаются, даже если есть обновления.

2º будет проверено, что плагин на сервере соответствует требованиям API NVDA, которые мы установили.

Если это не выполняется, плагин не может быть установлен, даже если версия сервера более новая, и сервер предлагает нам этот плагин.

При установке также были включены различные средства защиты:

1º теперь сообщит нам, если какие-либо дополнения не могут быть обновлены, и даст нам свое имя.

2º на этом этапе также будет проверено, имеет ли плагин для установки минимальную версию для использования на установленном NVDA.

3º плагин NVDA Store не позволит продолжать проверять наличие обновлений, если мы уже сделали обновление одного или нескольких плагинов и не решили перезапустить NVDA.

4º если у нас включена опция "проверить наличие обновлений установленных плагинов" каждый раз, когда вы ищете и обнаруживаете, что мы не перезапустили NVDA, мы будем уведомлены системным уведомлением.

5-й точно так же, если мы попытаемся включить опцию под названием “проверить наличие обновлений установленных плагинов" и не перезапустили NVDA читатель будет вербализовать сообщение о том, что мы должны перезапустить NVDA, чтобы применить обновления.

6º в худшем случае, если книжные магазины не позволяют загружать, потому что у нас нет интернета, нам будут показаны информационные сообщения в реестре NVDA, а также, если мы попытаемся получить доступ к магазину, мы будем предупреждены разговорным сообщением.

Это улучшило функцию, которая проверяет наличие обновлений, теперь намного надежнее, а также добавляет, в свою очередь, вышеупомянутые защиты.

Было сделано много внутренних улучшений, чтобы сделать его более надежным.

Этот плагин находится в стадии тестирования, поэтому мы просим Вас понять, что могут быть ошибки.

Мы благодарим Вас за то, что вы связались, чтобы сообщить о них и исправить их как можно скорее.

Наслаждайтесь магазином для NVDA!
 