# Manual da loja para o NVDA
## Modo de uso

O extra vem sem atalhos e podemos atribuir-lhe dois, que são:

* Mostrar a janela com todos os extras e suas informações: Será exibida uma janela com todos os extras que estão em https: www.nvda.es

* Procurar actualizações dos extras instalados: Analisará os extras que temos e, para aqueles que  encontre uma actualização, oferecer-nos-á a possibilidade de actualizá-los automaticamente.

### Mostrar a janela com todos os extras e suas informações

Neste ecrã teremos todos os extras acompanhados de um separador de informações e a possibilidade de ir ao seu repositório e fazer o download.

Se navegarmos pela janela, teremos uma lista com todos os extras, uma caixa somente leitura com a guia do extra que seleccionamos, um botão de download, um botão para ir para a página do extra e um botão Fechar.

Teremos também uma caixa de pesquisa na qual podemos colocar o que queremos pesquisar e, se pressionarmos enter, os resultados serão mostrados na lista.

Para voltarmos a ter toda a lista de extras, teremos apenas que voltar à caixa de pesquisa, apagar o texto que tínhamos escrito anteriormente e pressionar "enter", com a caixa vazia.

No campo do ficheiro, caso o extra possua mais de um ramo de desenvolvimento, a informação também será mostrada.

O botão de download mostrará um menu com os diferentes ramos de desenvolvimento do extra, teremos que escolher um para fazer o download. Caso haja apenas um, só teremos essa opção.

Neste ecrã, temos as seguintes teclas rápidas para navegar pela interface:

* Alt + B: Ir para a caixa de pesquisa.
* Alt + L: Ir para a lista de extras.
* Alt + I: Ir até ao campo do separador para ver as informações do extra selecionado.
* Alt + D: Executar o botão de download.
* Alt + P: Ir para a página do extra.
* Alt + C, Escape, Alt + F4: Fechar a janela.

#### menu de contexto na lista de extras

Na lista de extras, pode aceder ao menu de contexto, com a tecla de Aplicações ou Shift + F10, para aqueles teclados que não têm esta tecla.

Este menu consiste em dois submenus:

 Filtros e copiar para a área de transferência.

No submenu de  filtros temos as seguintes opções:

 * Mostrar todos os extras: Esta opção surge como padrão, enquanto o extra está a ser executado pela primeira vez.
Esta opção irá mostrar-nos todos os extras no banco de dados.
Se tivermos marcada a opção "mostrar por ordem alfabética", Esta opção deixará de estar activa, tanto nas listas como nas pesquisas.

 * Mostrar extras com compatibilidade de API 2021: Esta opção irá mostrar-nos apenas os extras que tenham marcada esta compatibilidade no manifesto.ini.
Não serão respeitados os extras para os quais os seus autores tenham indicado a compatibilidade para versões que ainda não chegaram.
 
* Mostrar extras classificados por autor: Esta opção mostrará os extras ordenados por autor.

 * Mostrar por downloads do maior para o menor número: mostrará a ordenação dos extras pelo número de downloads de cada um, do que tenha mais para o que tenha menos.
 Estas opções são executadas individualmente, não sendo o seu resultado cumulativo.
Quando escolhemos uma destas opções, o título da janela indica-nos qual delas se encontra activa.
Estas opções manter-se-ão até que o NVDA seja reiniciado, voltando, então, à forma inicial (mostrar todos os extras)

Excepto para a opção "Mostrar todos os extras", o resto das opções são filtradas apenas pelo primeiro ramo de desenvolvimento. Se um extra tem mais de um ramo, o ramo principal não será tido em conta para filtrar os resultados de cada opção.

 No submenu  de cópia para a área de transferência, temos as seguintes opções:

 * Copiar informações: Todas as informações do extra serão copiadas para a área de transferência.

 * Copiar o Link para a página web do extra: Se escolhermos esta opção, o endereço da página do extra será copiado para a área de transferência.

 * Copiar o link de download do extra: Se o extra tiver vários ramos, depois de escolhermos um deles, a ligação de descarga será copiada para a área de transferência.

### Verificar se há actualizações para os extras instalados

Isto permitirá actualizar os extras que são mais recentes, em https://www.nvda.es do que os que temos no nosso computador.

Neste ecrã poderemos seleccionar, em caso de actualizações, os extras que queremos actualizar.

Teremos que marcar o extra, com um espaço, e clicar em Actualizar.

Neste ecrã será mostrada a actualização correspondente, se houver alguma para o ramo que escolhemos em NVDA / Preferências / configurações do extra /   e aí podemos escolher se houver mais de um  ramo. (isto será melhor explicado na secção seguinte).

Neste ecrã, temos as seguintes teclas:

* Alt+S: Seleccionará, para instalar, todas as actualizações que tenhamos.
* Alt+D: Retirará todas as selecções que tivermos feito.
* Alt + A: A actualização dos extras que seleccionámos começará.
* Alt + C, Alt + F4 ou Escape: Fecha a janela.


### Painel de opções

Podemos configurar alguns aspectos da loja em NVDA / Preferências / definir comandos e procurar a categoria Loja NVDA.ES.

* Activar ou desactivar a verificação de actualizações.

Se activarmos esta caixa, será activada uma caixa de combinação na qual podemos escolher quanto tempo irá decorrer entre uma verificação e outra.

Activar ou desactivar a verificação de actualizações está desactivado por padrão.

O comportamento desta opção é simples: pesquisará, no servidor, se há actualizações no intervalo de tempo determinado e nos notificará, com uma notificação do sistema, dizendo quantas actualizações existem e abrir-nos-á a opção de loja correspondente para atualizar.

Se esta opção estiver activada, pesquisará 10 vezes, no intervalo de tempo determinado, e depois será desactivada. Isto evita chamadas saturadas para o servidor.

Portanto, se tivermos 15 minutos atribuídos e  não encontrar actualizações às 2h30, parará de procurar por actualizações.
No caso de haver actualizações, irá pesquisar mais 5 vezes o intervalo de tempo determinado e, em seguida, desativá-lo, a cada vez que iniciemos o computador, nos notificará que as atualizações foram encontradas até que atualizemos.

* Ordenar por orden alfabético los complementos de la tienda y las búsquedas.

Si marcamos esta casilla, cuando abramos la tienda se nos mostrara por orden alfabético. También si buscamos las búsquedas se mostrarán en orden alfabético.

* Complementos instalados que hay en el servidor.

Bien en esta lista se nos mostrarán aquellos complementos que tengamos instalados y que a su vez se encuentren en el servidor.

Solo se mostrarán aquellos que además tengan compatibilidad con la Api actual de NVDA.

En esta lista podremos elegir que rama de actualización queremos para el complemento. Si pulsamos espacio encima de un complemento se nos desplegara todas las ramas de desarrollo para ese complemento. Podremos elegir la que deseemos con intro y se nos quedara guardada la selección en la lista.

ADVERTENCIA: Los cambios en la lista solo se guardarán si damos al botón aceptar o aplicar del dialogo de opciones.

Esta lista se actualiza cada vez que reiniciemos NVDA añadiendo si hay nuevos complementos o eliminando aquellos que ya no estén.

Por lo tanto si eliminamos un complemento y luego lo volvemos a instalar tendremos que volver a seleccionar la rama que deseamos de nuevo.

* Classificar por ordem alfabética os extras da loja e as pesquisas.

Se marcarmos esta caixa, ao abrirmos a loja ela será mostrada em ordem alfabética. Além disso, se pesquisarmos, as pesquisas serão mostradas em ordem alfabética.

* Instalar extras depois de descarregar
 Se marcarmos esta caixa, quando a descarga acabar, ser-nos-á perguntado se desejamos instalar.

* Extras instalados no nosso computador que estão no servidor.

esta lista mostrará os extras que temos instalados e que, por sua vez, estão no servidor.

Só serão mostrados aqueles que  têm compatibilidade com a Api do NVDA actual.

Nesta lista, podemos escolher qual o ramo de actualização do extra queremos. Se pressionarmos a barra de espaço em cima de um extra, todos os ramos de desenvolvimento desse extra serão mostrados. Podemos escolher o que queremos   e a selecção será guardada na lista.

AVISO: As alterações na lista só serão guardadas se clicarmos no botão "aceitar" ou "aplicar", na caixa de diálogo de configurações.

Esta lista é actualizada de cada vez que reiniciamos o NVDA adicionando novos extras, se os houver, ou removendo aqueles que já lá não estão.

Portanto, se removermos um  extra e, depois, voltarmos a reinstalá-lo, teremos que selecionar, novamente o ramo que queremos.

Esta lista, quando o NVDA for reinciado ou façamos alterações, sempre assumirá, por padrão, o ramo de desenvolvimento.

## Observações

Ao verificar se há atualizações, agora tem duas protecções:

1 ° Verifica se há complementos que foram desinstalados.

 Nesse caso, os extras  serão excluídos, mesmo se houver actualizações.

2º Será validado se o complemento que se encontra no servidor cumpre os requisitos da API do NVDA que temos instalado.

Se isso não for verdade, o extra não pode ser instalado, mesmo se a versão do servidor for mais recente e o servidor nos oferecer esse extra.

Ao instalar, várias proteções também foram incluídas:

1º Se algum dos extras não puder ser instalado, seremos informados desse facto.

2º Neste passo também será verificado se o extra a instalar tem a versão mínima a ser utilizada no NVDA que temos instalado.

Foi adicionada uma protecção que não permitirá continuar a procurar por actualizações se já tivermos feito uma actualização de um ou mais extras e não tivermos decidido reiniciar o NVDA.
Se tivermos activado a pesquisa por actualizações automáticas, toda a vez que ela pesquisar e detectar que não reiniciámos o NVDA, seremos notificados com uma notificação do sistema.

Da mesma forma, se tentarmos activar o ecrã de verificação de actualizações e não reiniciarmos o NVDA, o leitor nos dirá a mensagem de que precisamos reiniciar o NVDA para aplicar as atualizações.

Foi adicionada uma protecção caso as bibliotecas não nos permitam carregar por não termos internet, serão mostradas mensagens de informação no registo do NVDA e também se tentarmos aceder à loja, seremos avisados , com uma mensagem falada.

A função de busca por actualizações foi aprimorada, agora é muito mais confiável e também adiciona as protecções mencionadas acima.

Muitas melhorias internas foram feitas para tornar o extra mais robusto.

Este extra está em fase de teste, por isso pedimos que entenda que pode haver erros.

Agradecemos  que entre em contato conosco, para relatá-los e podermos resolvê-los o mais rápido possível.

Equipa Portuguesa do NVDA: Ângelo Abrantes <ampa4374@gmail.com> e Rui Fontes <Rui Fontes <rui.fontes@tiflotecnia.com>

11 de Agosto de 2021.