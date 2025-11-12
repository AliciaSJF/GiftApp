import { useState, FormEvent } from 'react'
import './Feedback.css'

const Feedback = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    type: 'sugerencia',
    message: '',
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle')

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setSubmitStatus('idle')

    // Aquí puedes agregar la lógica para enviar el feedback
    // Por ahora simulamos el envío
    setTimeout(() => {
      setIsSubmitting(false)
      setSubmitStatus('success')
      setFormData({ name: '', email: '', type: 'sugerencia', message: '' })
      
      // Resetear el mensaje de éxito después de 5 segundos
      setTimeout(() => {
        setSubmitStatus('idle')
      }, 5000)
    }, 1000)
  }

  return (
    <section id="feedback" className="feedback">
      <div className="container">
        <h2 className="section-title">Sugerencias y Feedback</h2>
        <p className="section-subtitle">
          ¿Tienes alguna sugerencia, quieres reportar un error o simplemente quieres compartir
          tu opinión? ¡Me encantaría escucharte!
        </p>
        <div className="feedback-content">
          <form onSubmit={handleSubmit} className="feedback-form">
            <div className="form-group">
              <label htmlFor="name">Nombre</label>
              <input
                type="text"
                id="name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
                placeholder="Tu nombre"
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
                placeholder="tu@email.com"
              />
            </div>
            <div className="form-group">
              <label htmlFor="type">Tipo</label>
              <select
                id="type"
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                required
              >
                <option value="sugerencia">Sugerencia</option>
                <option value="error">Reportar Error</option>
                <option value="otro">Otro</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="message">Mensaje</label>
              <textarea
                id="message"
                value={formData.message}
                onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                required
                rows={6}
                placeholder="Escribe tu mensaje aquí..."
              ></textarea>
            </div>
            {submitStatus === 'success' && (
              <div className="form-message form-message-success">
                ¡Gracias por tu feedback! Te responderé pronto.
              </div>
            )}
            {submitStatus === 'error' && (
              <div className="form-message form-message-error">
                Hubo un error al enviar. Por favor, intenta de nuevo.
              </div>
            )}
            <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
              {isSubmitting ? 'Enviando...' : 'Enviar'}
            </button>
          </form>
        </div>
      </div>
    </section>
  )
}

export default Feedback

