import './ComoFunciona.css'

const ComoFunciona = () => {
  const steps = [
    {
      number: 1,
      title: 'Crea tu lista',
      description: 'Añade manualmente o pega un enlace; autocompleta imagen/nombre/marca/precio.',
    },
    {
      number: 2,
      title: 'Comparte con personas o grupos',
      description: 'Control de visibilidad por ítem.',
    },
    {
      number: 3,
      title: 'Ellos reservan, tú no te enteras',
      description: 'El resto ve quién se apunta; la creadora no ve nada.',
    },
  ]

  return (
    <section id="como-funciona" className="como-funciona">
      <div className="container">
        <h2 className="section-title">Cómo funciona</h2>
        <div className="steps">
          {steps.map((step) => (
            <div key={step.number} className="step">
              <div className="step-number">{step.number}</div>
              <h3 className="step-title">{step.title}</h3>
              <p className="step-description">{step.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default ComoFunciona

