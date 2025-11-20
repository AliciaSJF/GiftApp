import { Link, useParams } from 'react-router-dom'
import './SectionPlaceholder.css'

const sectionCopy: Record<
  string,
  { title: string; description: string; tip: string; action: string }
> = {
  'crear-lista': {
    title: 'Crear lista',
    description: 'Muy pronto podrás crear listas detalladas y compartirlas sin spoilers.',
    tip: 'Prepara enlaces, precios y notas personalizadas.',
    action: 'Volver al panel'
  },
  amigos: {
    title: 'Amigos',
    description: 'Gestiona tu red de confianza para coordinar regalos conjuntos.',
    tip: 'Invita a quienes siempre participan para que organicen todo contigo.',
    action: 'Ver panel'
  },
  'listas-amigos': {
    title: 'Listas de amigos',
    description: 'Consulta lo que otros esperan recibir y evita duplicados.',
    tip: 'Ten a la mano tus propias ideas para sugerir aportes.',
    action: 'Revisar accesos'
  },
  grupos: {
    title: 'Grupos',
    description: 'Coordina equipos y asigna responsabilidades con claridad.',
    tip: 'Define presupuestos y fechas clave para cada grupo.',
    action: 'Gestionar más tarde'
  },
  preferencias: {
    title: 'Añadir preferencias',
    description: 'Registra tallas, colores favoritos y gustos para acertar siempre.',
    tip: 'Cuanto más contexto, más fácil será comprar para ti.',
    action: 'Guardar después'
  }
}

const SectionPlaceholder = () => {
  const { sectionId = 'crear-lista' } = useParams()
  const copy = sectionCopy[sectionId] ?? {
    title: 'Sección en construcción',
    description: 'Estamos preparando esta experiencia para ti.',
    tip: 'Vuelve pronto para descubrir las novedades.',
    action: 'Regresar al inicio'
  }

  return (
    <div className="section-placeholder">
      <div className="section-card">
        <p className="section-eyebrow">En construcción</p>
        <h1>{copy.title}</h1>
        <p className="section-description">{copy.description}</p>
        <div className="section-tip">
          <span>Consejo</span>
          <p>{copy.tip}</p>
        </div>
        <Link to="/inicio" className="section-link">
          {copy.action}
        </Link>
      </div>
    </div>
  )
}

export default SectionPlaceholder



