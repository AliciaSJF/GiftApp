import './Footer.css'

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-section">
            <h4 className="footer-title">Legal</h4>
            <ul className="footer-links">
              <li><a href="#privacidad">Política de Privacidad</a></li>
              <li><a href="#terminos">Términos de Servicio</a></li>
              <li><a href="#cookies">Política de Cookies</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4 className="footer-title">Contacto</h4>
            <ul className="footer-links">
              <li><a href="mailto:hola@whisy.com">hola@whisy.com</a></li>
              <li><a href="#soporte">Soporte</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h4 className="footer-title">Whisy</h4>
            <p className="footer-text">Evita regalos duplicados. Coordina sin chats eternos.</p>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; {new Date().getFullYear()} Whisy. Todos los derechos reservados.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer

