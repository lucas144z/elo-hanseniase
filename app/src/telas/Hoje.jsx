import { useEffect, useState } from 'react'
import { nomeDoPaciente, registrarDose, verTratamento } from '../api'
import { diaMes } from '../datas'
import { marcarDoseDeHoje } from '../lembretes'

function textoSupervisionada(t) {
  if (t.proxima_supervisionada === null) return 'Todas feitas'
  if (t.dias_para_supervisionada === 0) return 'Hoje'
  if (t.dias_para_supervisionada === 1) return `Amanhã (${diaMes(t.proxima_supervisionada)})`
  return `${diaMes(t.proxima_supervisionada)} · em ${t.dias_para_supervisionada} dias`
}

export default function Hoje() {
  const [tratamento, setTratamento] = useState(null)
  const [erro, setErro] = useState('')
  const [enviando, setEnviando] = useState(false)
  const primeiroNome = nomeDoPaciente().split(' ')[0]

  async function carregar() {
    try {
      setTratamento(await verTratamento())
    } catch (e) {
      setErro(e.message)
    }
  }

  useEffect(() => {
    carregar()
  }, [])

  async function tomei() {
    setEnviando(true)
    setErro('')
    try {
      await registrarDose()
      marcarDoseDeHoje() // avisa a parte de lembretes para não tocar hoje
      await carregar()
    } catch (e) {
      setErro(e.message)
    } finally {
      setEnviando(false)
    }
  }

  if (!tratamento) {
    return erro ? <p className="erro">{erro}</p> : <p className="carregando">Carregando…</p>
  }

  const t = tratamento

  return (
    <section className="tela">
      <h1 className="saudacao">Olá{primeiroNome ? `, ${primeiroNome}` : ''}</h1>

      {t.em_andamento ? (
        <div className={t.tomou_hoje ? 'cartao-dose feita' : 'cartao-dose'}>
          <span className="rotulo">
            {t.hoje_eh_supervisionada ? 'Dose do mês, na UBS' : 'Dose de hoje'}
          </span>
          {t.tomou_hoje ? (
            <>
              <span className="icone-ok" aria-hidden="true">✓</span>
              <p>Dose registrada. Até amanhã!</p>
            </>
          ) : (
            <button className="botao-tomei" onClick={tomei} disabled={enviando}>
              {enviando ? 'Registrando…' : 'Tomei'}
            </button>
          )}
        </div>
      ) : (
        <div className="cartao-dose feita">
          <p>{t.dia_atual === 0 ? 'Seu cuidado ainda não começou.' : 'Tratamento concluído. Parabéns!'}</p>
        </div>
      )}

      {erro && <p className="erro">{erro}</p>}

      <dl className="resumo">
        <div>
          <dt>Próxima dose na UBS</dt>
          <dd>{textoSupervisionada(t)}</dd>
        </div>
        <div>
          <dt>Seu cuidado</dt>
          <dd>Dia {t.dia_atual} de {t.doses_total}</dd>
        </div>
        <div>
          <dt>Doses registradas</dt>
          <dd>{t.doses_tomadas}</dd>
        </div>
        <div>
          <dt>Sua unidade</dt>
          <dd>{t.ubs}</dd>
        </div>
      </dl>
    </section>
  )
}
