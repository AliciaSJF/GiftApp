import './Hero.css'

interface HeroProps {
  onOpenAuth: () => void
}

const Hero = ({ onOpenAuth }: HeroProps) => {
  const scrollToDemo = () => {
    const element = document.getElementById('como-funciona')
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <section className="hero">
      <div className="hero-container">
        <div className="hero-content">
          <div className="hero-text">
            <h1 className="hero-title">
              Comparte tus deseos, sin arruinar la sorpresa.<br />
            </h1>
            <p className="hero-subtitle">
            Evita regalos duplicados y coordina sin chats eternos.
            </p>
            <div className="hero-cta">
              <button className="btn btn-primary" onClick={onOpenAuth}>
                Empieza gratis
              </button>
              <button className="btn btn-secondary" onClick={scrollToDemo}>
                Ver demo
              </button>
            </div>
          </div>
          <div className="hero-image">
            <img src="/Gift-bro.svg" alt="Ilustración de personas" />
          </div>
        </div>
      </div>
    </section>
  )
}

export default Hero

