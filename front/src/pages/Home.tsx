import { useState } from 'react'
import Header from '../components/Header'
import Hero from '../components/Hero'
import ComoFunciona from '../components/ComoFunciona'
import VideoDemo from '../components/VideoDemo'
import Privacidad from '../components/Privacidad'
import CasosUso from '../components/CasosUso'
import SobreMi from '../components/SobreMi'
import Feedback from '../components/Feedback'
import Footer from '../components/Footer'
import AuthModal from '../components/AuthModal'
import { authService } from '../services/authService'

const Home = () => {
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false)

  const handleAuthSuccess = () => {
    setIsAuthModalOpen(false)
    // Aquí puedes agregar lógica adicional después del login exitoso
    // Por ejemplo, actualizar el estado del usuario, redirigir, etc.
    window.location.reload() // Recargar para actualizar el estado de autenticación
  }

  return (
    <>
      <Header onOpenAuth={() => setIsAuthModalOpen(true)} />
      <Hero onOpenAuth={() => setIsAuthModalOpen(true)} />
      <ComoFunciona />
      <VideoDemo />
      <Privacidad />
      <CasosUso />
      <SobreMi />
      <Feedback />
      <Footer />
      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onSuccess={handleAuthSuccess}
      />
    </>
  )
}

export default Home

