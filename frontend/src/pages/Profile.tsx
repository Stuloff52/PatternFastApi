import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const Profile = () => {
  const { user, loading, isAuthenticated } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      navigate('/login')
    }
  }, [loading, isAuthenticated, navigate])

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-2xl text-gray-600">Загрузка...</div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-4xl font-bold mb-8 text-gray-800">Профиль</h1>
      
      <div className="bg-white rounded-xl shadow-lg p-8">
        <div className="flex items-center mb-6">
          <div className="w-20 h-20 bg-primary-600 rounded-full flex items-center justify-center text-white text-3xl font-bold mr-6">
            {user.full_name.charAt(0).toUpperCase()}
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-800">{user.full_name}</h2>
            <p className="text-gray-600">@{user.username}</p>
          </div>
        </div>

        <div className="space-y-4">
          <div className="border-b border-gray-200 pb-4">
            <label className="text-sm font-medium text-gray-500">Email</label>
            <p className="text-lg text-gray-800">{user.email}</p>
          </div>

          <div className="border-b border-gray-200 pb-4">
            <label className="text-sm font-medium text-gray-500">Роль</label>
            <p className="text-lg text-gray-800 capitalize">{user.role}</p>
          </div>

          <div className="border-b border-gray-200 pb-4">
            <label className="text-sm font-medium text-gray-500">Статус</label>
            <p className="text-lg">
              <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                user.is_active
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800'
              }`}>
                {user.is_active ? 'Активен' : 'Неактивен'}
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Profile

