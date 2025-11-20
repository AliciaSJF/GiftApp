import { useState } from 'react'
import './Header.css'

interface HeaderProps {
  onOpenAuth: () => void
}

const Header = ({ onOpenAuth }: HeaderProps) => {
  const scrollToSection = (id: string) => {
    const element = document.getElementById(id)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <header className="header">
      <div className="header-container">
        <div className="logo" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
          <span className="logo-text">Whisy</span>
        </div>
        <nav className="nav">
          <button className="nav-link" onClick={() => scrollToSection('como-funciona')}>
            Cómo funciona
          </button>
          <button className="nav-link" onClick={() => scrollToSection('casos-uso')}>
            Casos de uso
          </button>
          <button className="nav-link" onClick={() => scrollToSection('sobre-mi')}>
            Sobre el proyecto
          </button>
          <button className="nav-link nav-link-primary" onClick={onOpenAuth}>
            Entrar
          </button>
        </nav>
      </div>
    </header>
  )
}

export default Header

