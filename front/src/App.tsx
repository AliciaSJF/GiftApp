import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import OAuthCallback from './pages/OAuthCallback'
import Dashboard from './pages/Dashboard'
import Account from './pages/Account'
import SectionPlaceholder from './pages/SectionPlaceholder'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/oauth/callback" element={<OAuthCallback />} />
        <Route path="/inicio" element={<Dashboard />} />
        <Route path="/cuenta" element={<Account />} />
        <Route path="/panel/:sectionId" element={<SectionPlaceholder />} />
      </Routes>
    </Router>
  )
}

export default App

