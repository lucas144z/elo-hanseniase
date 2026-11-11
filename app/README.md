# App do paciente

PWA em React + Vite. Precisa do [Node.js](https://nodejs.org) (versão LTS) e da API rodando
(ver [`api/README.md`](../api/README.md)).

## Como rodar

```bash
cd app
npm install
npm run dev
```

Abra **http://localhost:5173** e entre com `ELO-001`. Para ver como celular no Chrome:
F12 e depois Ctrl+Shift+M.

Para testar a instalação e o modo offline (o service worker só funciona no build):

```bash
npm run build
npm run preview   # http://localhost:4173
```

## Telas

| Tela | Arquivo | Responsável |
|---|---|---|
| Entrada (código do paciente) | `src/telas/Entrada.jsx` | Lucas |
| Hoje (botão "Tomei") | `src/telas/Hoje.jsx` | Lucas |
| Calendário do mês | `src/telas/Calendario.jsx` | Lucas |
| Lembrete | `src/lembretes/ConfigLembrete.jsx` | Rodrigo |

`src/api.js` concentra as chamadas à API. Para apontar para outro endereço, crie `app/.env`
com `VITE_API_URL=http://endereco-da-api`.

## Lembretes e PWA (Rodrigo)

- `vite.config.js`: manifest do PWA. Falta gerar os ícones `public/icons/elo-192.png` e
  `elo-512.png` (a partir de `public/logo-icone.svg`) e descomentar as linhas dos ícones.
- `src/lembretes/index.js`: `marcarDoseDeHoje()` já é chamada quando o paciente toca em "Tomei".
- `src/lembretes/ConfigLembrete.jsx`: tela de escolher o horário.
- A notificação diz só "Hora do seu cuidado 💜", nunca o nome da doença.
