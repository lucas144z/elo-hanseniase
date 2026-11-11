// Todas as chamadas do app para a API ficam aqui.
const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
const CHAVE_TOKEN = 'elo.token'
const CHAVE_NOME = 'elo.nome'

function ler(chave) {
  try {
    return localStorage.getItem(chave)
  } catch {
    return null
  }
}

function gravar(chave, valor) {
  try {
    localStorage.setItem(chave, valor)
  } catch {
    // navegador bloqueou o armazenamento: o app segue, só não lembra o login
  }
}

export function temSessao() {
  return Boolean(ler(CHAVE_TOKEN))
}

export function nomeDoPaciente() {
  return ler(CHAVE_NOME) ?? ''
}

export function sair() {
  try {
    localStorage.removeItem(CHAVE_TOKEN)
    localStorage.removeItem(CHAVE_NOME)
  } catch {
    // nada a fazer
  }
}

async function chamar(caminho, opcoes = {}) {
  const token = ler(CHAVE_TOKEN)
  let resposta
  try {
    resposta = await fetch(BASE + caminho, {
      ...opcoes,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    })
  } catch {
    throw new Error('Sem conexão com o servidor. Tente de novo em instantes.')
  }

  if (resposta.status === 401 && token) {
    sair()
    window.dispatchEvent(new Event('elo:sessao-expirada'))
  }

  const corpo = await resposta.json().catch(() => null)
  if (!resposta.ok) {
    const detalhe = corpo?.detail
    throw new Error(typeof detalhe === 'string' ? detalhe : 'Algo deu errado. Tente de novo.')
  }
  return corpo
}

export async function entrar(codigo) {
  const dados = await chamar('/login', { method: 'POST', body: JSON.stringify({ codigo }) })
  gravar(CHAVE_TOKEN, dados.access_token)
  gravar(CHAVE_NOME, dados.nome)
  return dados
}

export const verTratamento = () => chamar('/tratamento')

export const verMes = (mes) => chamar(`/doses?mes=${mes}`)

export const registrarDose = () => chamar('/doses', { method: 'POST', body: '{}' })
