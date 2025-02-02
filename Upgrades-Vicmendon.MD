Branch **ConfirmacaoUpgrade1** - 31/01/2025

1 - Novo 'pip freeze > requirements.txt' para incluir 'python-decouple' e 'python-dotenv'.

2 - RSVP de Convidado e Parente modificados para "Vai", "Não vai" e "Indefinido" (default). Antes estava com Boolean de default True.

3 - Adicionada opção de alterar RSVP do Parente no Admin do Convidado.

4 - Página "confirmacao.html" - criação de Spinner para quando clica nos botões Pesquisar e Confirmar, para evitar cliques repetidos do usuário.

5 - Página "confirmacao.html" - mudança na tabela de exibição de Convidado e Parentes a serem confirmados. Ao invés do checkbox, agora existem dois ícones (Positivo e Negativo) que começam com o estado carregado do banco (INDEFINIDO - Cinza) e ao serem clicados, ativam. Se clicado o Positivo (Vai) ele fica verde e o Negativo (Não vai) fica cinza. O inverso também acontece.

5.1 - O elemento Pai de cada svg, no caso a DIV, guarda o status do botão, carregado pelo sistema no carregamento da página, de acordo com o banco. Se estiver pendente (cinza), confirmado (verde), recusado (vermelho).

6 - Adicionada a contagem de Convidados que recusaram o convite, no Admin do Evento.

7 - Adicionado um Try/Except ao envio de mensagens por whatsapp., pro caso dos ervidor de msg cair.

8 - Alterada a lógica na pesquisa pelo nome, para desconsiderar maiúscula e minúsculas.

9 - Convidado models e Parente models modificado para telefone Unique.

10 - Implementação de envio de mensagem no whatsapp de forma assíncrona, com Threads, pois estava demorando a carregar a página de confirmação.


Futuras atualizações

- Alterar o link de confirmação de **/convidado/evento/<hash-evento>/confirmacao** para **/confirmacao/<hash-evento>**.

- Adicionar um campo ACESSOU no convidado, pra contar quantas vezes ele fez login no evento. Cada login com data e hora.

- Os IDs de Convidados e Parentes devem seguir a mesma sequencia, não se repetindo entre eles.

- Implementar fila para não estourar limite da API, ao enviar mensagem pelo whatsapp.