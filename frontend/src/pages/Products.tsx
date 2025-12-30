import { useEffect, useState } from 'react'
import { productsAPI } from '../lib/api'
import ProductCard from '../components/ProductCard'

interface Product {
  id: string
  name: string
  description: string | null
  price: string
  stock: number
  is_active: boolean
  created_at: string
  updated_at: string
}

const Products = () => {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true)
        const response = await productsAPI.getAll({ limit: 100 })
        setProducts(response.data.items || [])
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Ошибка загрузки товаров')
      } finally {
        setLoading(false)
      }
    }
    fetchProducts()
  }, [])

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-2xl text-gray-600">Загрузка...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-4xl font-bold mb-8 text-gray-800">Каталог товаров</h1>
      
      {products.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-xl text-gray-600">Товары не найдены</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </div>
  )
}

export default Products

