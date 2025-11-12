import './SobreMi.css'

const SobreMi = () => {
  return (
    <section id="sobre-mi" className="sobre-mi">
      <div className="container">
        <h2 className="section-title">Sobre el Proyecto</h2>
        <div className="sobre-mi-content">
          <div className="sobre-mi-text">
            <p className="intro-text">
              Soy <strong>Alicia</strong>, una desarrolladora de software a la que le encanta crear
              soluciones que resuelvan problemas reales del día a día.
            </p>
            <p>
              Me encontré con dificultades para organizar los regalos entre mis amigos y familia,
              y decidí empezar este proyecto para facilitar la coordinación sin arruinar las
              sorpresas.
            </p>
            <p>
              He usado tecnologías modernas como <strong>React</strong> y <strong>TypeScript</strong>{' '}
              en el frontend, <strong>FastAPI</strong> y <strong>Python</strong> en el backend,
              junto con <strong>PostgreSQL</strong> para la base de datos. La aplicación incluye
              autenticación con JWT y OAuth, y está diseñada con una arquitectura escalable y
              mantenible.
            </p>
            <div className="github-link">
              {/* Actualiza este enlace con la URL de tu repositorio de GitHub */}
              <a
                href="https://github.com/tu-usuario/GiftApp"
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-github"
              >
                <svg
                  className="github-icon"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
                </svg>
                Ver código en GitHub
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default SobreMi

