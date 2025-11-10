import './CasosUso.css'

const CasosUso = () => {
  const casos = [
    { emoji: '🎂', name: 'Cumpleaños' },
    { emoji: '🎄', name: 'Navidad' },
    { emoji: '👶', name: 'Baby shower' },
    { emoji: '🎁', name: 'Amigos invisibles' },
  ]

  return (
    <section className="casos-uso">
      <div className="container">
        <h2 className="section-title">Casos de uso</h2>
        <div className="casos-grid">
          {casos.map((caso, index) => (
            <div key={index} className="caso-card">
              <div className="caso-emoji">{caso.emoji}</div>
              <h3 className="caso-name">{caso.name}</h3>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default CasosUso

