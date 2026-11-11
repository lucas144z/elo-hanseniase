// Datas chegam da API como texto 'AAAA-MM-DD'. Trabalhamos com o texto direto
// para não sofrer com fuso horário do navegador.

export const NOMES_MES = [
  'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
  'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro',
]

const doisDigitos = (n) => String(n).padStart(2, '0')

/** Mês atual no formato 'AAAA-MM'. */
export function mesAtual() {
  const agora = new Date()
  return `${agora.getFullYear()}-${doisDigitos(agora.getMonth() + 1)}`
}

/** Soma (ou subtrai) meses de um 'AAAA-MM'. */
export function somarMes(mes, quantos) {
  const [ano, numero] = mes.split('-').map(Number)
  const data = new Date(ano, numero - 1 + quantos, 1)
  return `${data.getFullYear()}-${doisDigitos(data.getMonth() + 1)}`
}

/** Data de hoje no formato 'AAAA-MM-DD'. */
export function dataDeHoje() {
  const agora = new Date()
  return `${mesAtual()}-${doisDigitos(agora.getDate())}`
}

/** 'AAAA-MM' -> 'Novembro de 2026' */
export function nomeDoMes(mes) {
  const [ano, numero] = mes.split('-').map(Number)
  const nome = NOMES_MES[numero - 1]
  return `${nome[0].toUpperCase()}${nome.slice(1)} de ${ano}`
}

/** 'AAAA-MM-DD' -> 'DD/MM' */
export function diaMes(data) {
  const [, mes, dia] = data.split('-')
  return `${dia}/${mes}`
}
