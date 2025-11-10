import './Privacidad.css'

const Privacidad = () => {
  const features = [
    'Las sorpresas siguen siendo sorpresas.',
    'Controlas qué ve cada persona o grupo.',
    'Nada de spam, solo regalos con cariño',
  ]

  return (
    <section id="privacidad" className="privacidad">
      <div className="container">
        <h2 className="section-title">Privacidad y confianza</h2>
        <div className="features">
          {features.map((feature, index) => (
            <div key={index} className="feature">
              <div className="feature-icon">✓</div>
              <p className="feature-text">{feature}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default Privacidad

