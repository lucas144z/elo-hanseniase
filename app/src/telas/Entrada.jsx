import { useState } from 'react'
import { entrar } from '../api'

export default function Entrada({ aoEntrar }) {
  const [codigo, setCodigo] = useState('')
  const [erro, setErro] = useState('')
  const [enviando, setEnviando] = useState(false)

  async function enviar(evento) {
    evento.preventDefault()
    setEnviando(true)
    setErro('')
    try {
      await entrar(codigo)
      aoEntrar()
    } catch (e) {
      setErro(e.message)
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="entrada">
      <div className="marca grande">
        <img src="/logo-icone.svg" alt="" />
        <span>elo</span>
      </div>
      <p className="slogan">cuidado que não se rompe</p>

      <form onSubmit={enviar} className="formulario">
        <label htmlFor="codigo">Seu código</label>
        <input
          id="codigo"
          value={codigo}
          onChange={(e) => setCodigo(e.target.value)}
          placeholder="ELO-001"
          autoComplete="off"
          autoCapitalize="characters"
          required
        />
        <button className="botao" disabled={enviando}>
          {enviando ? 'Entrando…' : 'Entrar'}
        </button>
        {erro && <p className="erro">{erro}</p>}
      </form>

      <p className="dica">O código é entregue pela sua UBS. Para testar: ELO-001 ou ELO-002.</p>
    </div>
  )
}
