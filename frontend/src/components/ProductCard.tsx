interface Product {
  id: string
  name: string
  description: string | null
  price: string
  stock: number
  is_active: boolean
}

interface ProductCardProps {
  product: Product
}

const ProductCard = ({ product }: ProductCardProps) => {
  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow">
      <div className="h-48 bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center">
        <span className="text-6xl">📦</span>
      </div>
      <div className="p-6">
        <h3 className="text-xl font-bold mb-2 text-gray-800">{product.name}</h3>
        {product.description && (
          <p className="text-gray-600 text-sm mb-4 line-clamp-2">{product.description}</p>
        )}
        <div className="flex items-center justify-between">
          <div>
            <p className="text-2xl font-bold text-primary-600">{product.price} ₽</p>
            <p className="text-sm text-gray-500">
              {product.stock > 0 ? `В наличии: ${product.stock}` : 'Нет в наличии'}
            </p>
          </div>
          <button
            className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
              product.stock > 0 && product.is_active
                ? 'bg-primary-600 text-white hover:bg-primary-700'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
            disabled={product.stock === 0 || !product.is_active}
          >
            В корзину
          </button>
        </div>
      </div>
    </div>
  )
}

export default ProductCard

