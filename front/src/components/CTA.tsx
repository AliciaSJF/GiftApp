import './CTA.css'

interface CTAProps {
  onOpenAuth: () => void
}

const CTA = ({ onOpenAuth }: CTAProps) => {
  return (
    <section className="cta-section">
      <div className="container">
        <h2 className="cta-title">¿Lista para empezar?</h2>
        <p className="cta-subtitle">Crea tu primera lista y coordina regalos sin complicaciones</p>
        <button className="btn btn-primary btn-large" onClick={onOpenAuth}>
          Crear mi primera lista
        </button>
      </div>
    </section>
  )
}

export default CTA

