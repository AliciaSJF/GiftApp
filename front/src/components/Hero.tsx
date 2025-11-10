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
      <div className="hero-decoration hero-decoration-1">🎁</div>
      <div className="hero-decoration hero-decoration-2">🎁</div>
      <div className="hero-decoration hero-decoration-3">🎁</div>
      <div className="hero-container">
        <h1 className="hero-title">
          Evita regalos duplicados. Coordina sin chats eternos.
        </h1>
        <p className="hero-subtitle">
          Comparte lo que te gustaría, sin arruinar la sorpresa.
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
    </section>
  )
}

export default Hero

