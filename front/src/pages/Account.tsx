import { Link } from 'react-router-dom'
import './Account.css'

const Account = () => {
  return (
    <div className="account-page">
      <div className="account-card">
        <div className="account-avatar">
          <img src="https://i.pravatar.cc/160?img=5" alt="Foto de perfil" />
        </div>
        <h1>Tu cuenta</h1>
        <p>
          Aquí verás tu información personal, ajustes de privacidad y preferencias guardadas.
          Estamos preparando esta sección para que puedas controlarlo todo desde un solo lugar.
        </p>
        <Link to="/inicio" className="account-button">
          Volver al panel
        </Link>
      </div>
    </div>
  )
}

export default Account



