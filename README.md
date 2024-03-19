# Yu-Gi-Oh! Deck Builder

Bem-vindo ao Yu-Gi-Oh! Deck Builder, um aplicativo web simples para construir decks do jogo de cartas Yu-Gi-Oh!

## Funcionalidades

- **Construção de Deck:** Adicionar, remover e visualizar cartas no seu deck.
- **Explorar Cartas:** Pesquisar e descubrir informações sobre diferentes cartas disponíveis.
- **Salvar/Carregar Deck:** Salvar seus decks em andamento para continuar mais tarde.
- **Integração com API:** Utilizamos uma API de cartas para obter informações atualizadas.  [Link API](https://ygoprodeck.com/api-guide/)

## Ambientação e instalação

<strong> Instruções - windows</strong> <br>

Instalar o python em <https://www.python.org/>
Instalando pelo site, a ferramenta ja com vem o PIP e o VENV instalados nativamente.
podemos sempre verificar a versão atual do PIP com:

```pip --version```

e atualizar o PIP com:

```python.exe -m pip install --upgrade pip```

Observação: No Linux, deve-se instalar essas ferramentas

Voltando ao Windows...
Para criar o ambiente de desenvolvimento VENV para que não corramos o risco de alterar o python nativo instalado no windows, devemos...

1. criar o ambiente de densenvolvimento.
Para criar devemos ir (de preferencia) na raiz da pasta onde concentraremos nosso projeto.
código:

```python -m venv venv```

note que o último venv é referente ao nome que damos ao ambiente de desenvolvimento..fica livre a escolha do mesmo porém se adota venv como padrão.

2. Ativando o ambiente de densenvolvimento no windows.

```venv/scripts/activate```

2. Ativando o ambiente de densenvolvimento no Linux.

```source venv/bin/activate```

Ao ser ativado o terminal ficaria com um (nome verde) e passara a usar tds as dependencias dentro do python do ambiente recem criado

Podemos inclusive verificar a versao do PIP instalado neste python do venv e atualiza-lo.

```pip --version```

```python.exe -m pip install --upgrade pip```

    Ativando o ambiente de densenvolvimento no Linux.

source venv/bin/activate
