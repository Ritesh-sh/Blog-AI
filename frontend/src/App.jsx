import { Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Layout from './components/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Generate from './pages/Generate'
import History from './pages/History'
import HistoryDetail from './pages/HistoryDetail'
import { getToken, removeToken } from './lib/auth'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = getToken()
    setIsAuthenticated(!!token)
    setLoading(false)
  }, [])

  const handleLogin = () => {
    setIsAuthenticated(true)
  }

  const handleLogout = () => {
    removeToken()
    setIsAuthenticated(false)
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <Routes>
      <Route path="/login" element={
        isAuthenticated ? <Navigate to="/dashboard" /> : <Login onLogin={handleLogin} />
      } />
      <Route path="/register" element={
        isAuthenticated ? <Navigate to="/dashboard" /> : <Register onLogin={handleLogin} />
      } />
      
      {/* Protected routes */}
      <Route path="/" element={
        isAuthenticated ? <Layout onLogout={handleLogout} /> : <Navigate to="/login" />
      }>
        <Route index element={<Navigate to="/dashboard" />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="generate" element={<Generate />} />
        <Route path="history" element={<History />} />
        <Route path="history/:blogId" element={<HistoryDetail />} />
      </Route>
    </Routes>
  )
}

export default App
