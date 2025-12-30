import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { authAPI } from '../lib/api'

interface User {
  id: string
  username: string
  email: string
  full_name: string
  role: string
  is_active: boolean
}

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (username: string, password: string) => Promise<void>
  register: (data: RegisterData) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

interface RegisterData {
  username: string
  email: string
  full_name: string
  password: string
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadUser = async () => {
      const token = localStorage.getItem('access_token')
      if (token) {
        try {
          const response = await authAPI.getMe()
          setUser(response.data)
        } catch (error) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
        }
      }
      setLoading(false)
    }
    loadUser()
  }, [])

  const login = async (username: string, password: string) => {
    const response = await authAPI.login(username, password)
    const { access_token, refresh_token } = response.data
    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)
    const userResponse = await authAPI.getMe()
    setUser(userResponse.data)
  }

  const register = async (data: RegisterData) => {
    const response = await authAPI.register(data)
    const { access_token, refresh_token } = response.data
    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)
    const userResponse = await authAPI.getMe()
    setUser(userResponse.data)
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        register,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

