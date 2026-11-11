import { useEffect, useState } from 'react'
import { sair, temSessao } from './api'
import Entrada from './telas/Entrada'
import Hoje from './telas/Hoje'
import Calendario from './telas/Calendario'
import ConfigLembrete from './lembretes/ConfigLembrete'

const ABAS = [
  { id: 'hoje', rotulo: 'Hoje', Tela: Hoje },
  { id: 'calendario', rotulo: 'Calendário', Tela: Calendario },
  { id: 'lembrete', rotulo: 'Lembrete', Tela: ConfigLembrete },
]

export default function App() {
  const [logado, setLogado] = useState(temSessao())
  const [aba, setAba] = useState('hoje')

  // Se o token expirar no meio do uso, volta para a tela de entrada
  useEffect(() => {
    const voltarParaEntrada = () => setLogado(false)
    window.addEventListener('elo:sessao-expirada', voltarParaEntrada)
    return () => window.removeEventListener('elo:sessao-expirada', voltarParaEntrada)
  }, [])

  if (!logado) {
    return <Entrada aoEntrar={() => { setAba('hoje'); setLogado(true) }} />
  }

  const { Tela } = ABAS.find((a) => a.id === aba)

  return (
    <div className="app">
      <header className="topo">
        <div className="marca">
          <img src="/logo-icone.svg" alt="" />
          <span>elo</span>
        </div>
        <button className="link" onClick={() => { sair(); setLogado(false) }}>Sair</button>
      </header>

      <main className="conteudo">
        <Tela />
      </main>

      <nav className="abas">
        {ABAS.map((a) => (
          <button
            key={a.id}
            className={a.id === aba ? 'aba ativa' : 'aba'}
            onClick={() => setAba(a.id)}
          >
            {a.rotulo}
          </button>
        ))}
      </nav>
    </div>
  )
}
