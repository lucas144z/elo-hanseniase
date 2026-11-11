// Parte do Rodrigo: lembretes e PWA.
//
// O que já está ligado: a tela "Hoje" chama marcarDoseDeHoje() logo depois que
// o paciente toca em "Tomei". Use isso para não mostrar o lembrete do dia.
//
// O que falta (ver app/README.md):
//  1. guardar o horário escolhido em ConfigLembrete.jsx
//  2. pedir permissão de notificação (Notification.requestPermission)
//  3. no horário, se a dose de hoje não foi marcada, mostrar
//     "Hora do seu cuidado 💜" via service worker (registration.showNotification)

/** Chamada pela tela Hoje depois que a dose é registrada. */
export function marcarDoseDeHoje() {
  // TODO (Rodrigo): guardar que a dose de hoje já foi tomada e cancelar o lembrete do dia.
}
