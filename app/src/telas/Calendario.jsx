import { useEffect, useState } from 'react'
import { verMes } from '../api'
import { dataDeHoje, mesAtual, nomeDoMes, somarMes } from '../datas'

const DIAS_SEMANA = ['D', 'S', 'T', 'Q', 'Q', 'S', 'S']

const LEGENDA = [
  { classe: 'tomada', texto: 'Tomada' },
  { classe: 'esquecida', texto: 'Não registrada' },
  { classe: 'supervisionada', texto: 'Dose na UBS' },
  { classe: 'hoje', texto: 'Hoje' },
]

export default function Calendario() {
  const [mes, setMes] = useState(mesAtual())
  const [dias, setDias] = useState(null)
  const [erro, setErro] = useState('')

  useEffect(() => {
    let ativo = true // evita mostrar o mês errado se o usuário trocar de mês rápido
    setDias(null)
    setErro('')
    verMes(mes)
      .then((resposta) => ativo && setDias(resposta))
      .catch((e) => ativo && setErro(e.message))
    return () => {
      ativo = false
    }
  }, [mes])

  // Quantas casas vazias antes do dia 1 (0 = domingo)
  const [ano, numero] = mes.split('-').map(Number)
  const vazios = new Date(ano, numero - 1, 1).getDay()
  const hoje = dataDeHoje()

  function classesDoDia(d) {
    const classes = ['dia', d.status]
    if (d.tipo === 'supervisionada') classes.push('supervisionada')
    if (d.data === hoje) classes.push('dia-de-hoje')
    return classes.join(' ')
  }

  return (
    <section className="tela">
      <div className="cabecalho-mes">
        <button className="seta" onClick={() => setMes(somarMes(mes, -1))} aria-label="Mês anterior">‹</button>
        <h1>{nomeDoMes(mes)}</h1>
        <button className="seta" onClick={() => setMes(somarMes(mes, 1))} aria-label="Próximo mês">›</button>
      </div>

      {erro && <p className="erro">{erro}</p>}

      <div className="grade">
        {DIAS_SEMANA.map((d, i) => (
          <span key={i} className="dia-semana">{d}</span>
        ))}
        {Array.from({ length: vazios }, (_, i) => (
          <span key={`v${i}`} />
        ))}
        {dias
          ? dias.map((d) => (
              <span
                key={d.data}
                className={classesDoDia(d)}
                title={d.tipo === 'supervisionada' ? 'Dose na UBS' : undefined}
              >
                {Number(d.data.slice(8))}
              </span>
            ))
          : !erro && <p className="carregando grade-carregando">Carregando…</p>}
      </div>

      <ul className="legenda">
        {LEGENDA.map((item) => (
          <li key={item.classe}>
            <span className={`amostra ${item.classe}`} />
            {item.texto}
          </li>
        ))}
      </ul>
    </section>
  )
}
