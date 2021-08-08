# Manual da loja para o NVDA
## Modo de uso

O extra vem sem atalhos e podemos atribuir-lhe dois, que são:

* Mostrar a janela com todos os extras e suas informações: Será exibida uma janela com todos os extras que estão em https: www.nvda.es

* Procurar actualizações dos extras instalados: Analisará os extras que temos e, para aqueles que  encontre uma actualização, oferecer-nos-á a possibilidade de actualizá-los automaticamente.

### Mostrar a janela com todos os extras e suas informações

Neste ecrã teremos todos os extras acompanhados de um separador de informações e a possibilidade de ir ao seu repositório e fazer o download.

Se navegarmos pela janela, teremos uma lista com todos os extras, uma caixa somente leitura com a guia do extra que seleccionamos, um botão de download, um botão para ir para a página do extra e um botão Fechar.

Teremos também uma caixa de pesquisa na qual podemos colocar o que queremos pesquisar e, se pressionarmos enter, os resultados serão mostrados na lista.

Para voltarmos a ter toda a lista de extras, teremos apenas que voltar à caixa de pesquisa, apagar o texto que anteriormente e pressionar "enter", com a caixa vazia.

No campo do ficheiro, caso o extra possua mais de um ramo de desenvolvimento, a informação também será mostrada.

O botão de download mostrará um menu com os diferentes ramos de desenvolvimento do extra, teremos que escolher um para fazer o download. Caso haja apenas um, só teremos essa opção.

Neste ecrã, temos as seguintes teclas rápidas para navegar pela interface:

* Alt + B: Ir para a caixa de pesquisa.
* Alt + L: Ir para a lista de extras.
* Alt + I: Ir até ao campo do separador para ver as informações do extra selecionado.
* Alt + D: Executar o botão de download.
* Alt + P: Ir para a página do extra.
* Alt + C, Escape, Alt + F4: Fechar a janela.

### Verificar se há actualizações para os extras instalados

Isto permitirá actualizar os extras que são mais recentes, em https://www.nvda.es do que os que temos no nosso computador.

Neste ecrã poderemos seleccionar, em caso de actualizações, os extras que queremos actualizar.

Teremos que marcar o extra, com um espaço, e clicar em Actualizar.

Actualmente, apenas o ramo principal do extra pode ser actualizado. Se tivermos um extra que possui vários ramos e estivermos no ramo de desenvolvimento, teremos que actualizar manualmente.

No caso de ser apenas um extra que possui um ramo de desenvolvimento que e é o seu único ramo, ele pode ser atualizado sem problemas.

Apenas o ramo principal do extra será actualizado.

Estamos a trabalhar para podermos oferecer a escolha de qual o ramo queremos para cada extra.

Neste ecrã, temos as seguintes teclas:

* Alt + A: A actualização dos extras que seleccionámos começará.
* Alt + C, Alt + F4 ou Escape: Fecha a janela.

### Painel de opções

Podemos configurar alguns aspectos da loja em NVDA / Preferências / definir comandos e procurar a categoria Loja NVDA.ES.

Actualmente podemos seleccionar se queremos activar ou desactivar a verificação de actualizações.

Se activarmos esta caixa, será activada uma caixa de combinação na qual podemos escolher quanto tempo irá decorrer entre uma verificação e outra.

Activar ou desactivar a verificação de actualizações está desactivado por padrão.

O comportamento desta opção é simples: pesquisará, no servidor, se há actualizações no intervalo de tempo determinado e nos notificará, com uma notificação do sistema, dizendo quantas actualizações existem e abrir-nos-á a opção de loja correspondente para atualizar.

Se esta opção estiver activada, pesquisará 10 vezes, no intervalo de tempo determinado, e depois será desactivada. Isto evita chamadas saturadas para o servidor.

Portanto, se tivermos 15 minutos atribuídos e  não encontrar actualizações às 2h30, parará de procurar por actualizações.
No caso de haver actualizações, irá pesquisar mais 5 vezes o intervalo de tempo determinado e, em seguida, desativá-lo, a cada vez que iniciemos o computador, nos notificará que as atualizações foram encontradas até que atualizemos.

## Observações

Foi adicionada uma protecção que não permitirá continuar a procurar por actualizações se já tivermos feito uma actualização de um ou mais extras e não tivermos decidido reiniciar o NVDA.
Se activarmos a busca automática de atualizações, toda a vez que busca e detecta que não reiniciámos o NVDA, seremos notificados com uma notificação do sistema.

Da mesma forma, se tentarmos activar o ecrã de verificação de actualizações e não reiniciarmos o NVDA, o leitor dirá a mensagem de que precisamos de reiniciar o NVDA para aplicar as actualizações.

Este extra está em fase de teste, por isso pedimos que entenda que pode haver erros.

Agradecemos  que entre em contato conosco, para relatá-los e podermos resolvê-los o mais rápido possível.

Equipa Portuguesa do NVDA: Ângelo Abrantes <ampa4374@gmail.com> e Rui Fontes <Rui Fontes <rui.fontes@tiflotecnia.com>

7 de Agosto de 2021.