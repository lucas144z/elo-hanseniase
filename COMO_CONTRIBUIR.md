# Como contribuir

A avaliação confere a **participação visível de todos os integrantes**. O GitHub só mostra alguém
como contribuidor quando há um commit feito **pela conta dessa pessoa**. Por isso cada integrante
precisa fazer pelo menos um commit próprio, seguindo o passo a passo abaixo.

Dá para fazer tudo pelo site do GitHub, sem instalar nada.

## 1. Aceitar o convite

O dono do repositório envia o convite em *Settings → Collaborators → Add people*. Você recebe um
e-mail ou uma notificação em <https://github.com/notifications>. Clique em **Accept invitation**.

## 2. Criar sua ficha (seu primeiro commit)

1. Abra a pasta [`integrantes/`](integrantes/) no repositório.
2. Abra o arquivo `_modelo.md` e copie o conteúdo.
3. Volte para a pasta `integrantes/` e clique em **Add file → Create new file**.
4. Nomeie o arquivo com o seu usuário do GitHub: `integrantes/seu-usuario.md`.
5. Cole o modelo e preencha com os seus dados.
6. Clique em **Commit changes…**, escreva a mensagem `Adiciona ficha de <seu nome>` e confirme
   com **Commit directly to the main branch**.

## 3. Colocar seu nome na tabela do README

1. Abra o `README.md` e clique no ícone de lápis (✏️ *Edit this file*).
2. Na seção **8. Integrantes**, troque uma linha `_(nome)_ | _(RA)_ | _(@usuario)_` pelos seus dados.
3. **Commit changes…** com a mensagem `Adiciona <seu nome> aos integrantes`.

Se o GitHub avisar que o arquivo mudou enquanto você editava, recarregue a página e edite de novo.

## Conferindo

Em *Insights → Contributors* (ou na lista de commits) seu nome deve aparecer. O gráfico de
contribuidores do GitHub pode demorar alguns minutos para atualizar.

> **Atenção se usar o Git no computador:** o commit só conta para você se o e-mail configurado no
> Git (`git config user.email`) for um dos e-mails cadastrados na sua conta do GitHub. Pelo site isso
> já sai certo.

## Padrão de mensagens de commit

Verbo no presente, em português, dizendo o que mudou:

- `Adiciona gráfico de casos por UF`
- `Corrige fonte dos dados no README`
- `Atualiza paleta de cores`
