import './Contacto.css'

const Contacto = () => {
  return (
    <section id="contacto" className="contacto">
      <div className="container">
        <h2 className="section-title">Habla conmigo</h2>
        <p className="section-subtitle">
          ¿Tienes alguna pregunta o quieres saber más sobre Whisy? Estaré encantada de ayudarte.
        </p>
        <div className="contacto-content">
          <div className="contacto-info">
            <div className="contacto-item">
              <svg className="contacto-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
              <div>
                <h3>Email</h3>
                <a href="mailto:hola@whisy.com">hola@whisy.com</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Contacto

