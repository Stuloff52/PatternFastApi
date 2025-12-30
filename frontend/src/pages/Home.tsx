import { Link } from 'react-router-dom'

const Home = () => {
  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary-600 to-primary-800 text-white rounded-2xl p-12 mb-12">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold mb-6">Добро пожаловать в наш магазин!</h1>
          <p className="text-xl mb-8 text-primary-100">
            Лучшие товары по выгодным ценам. Быстрая доставка и отличное качество.
          </p>
          <Link
            to="/products"
            className="inline-block px-8 py-4 bg-white text-primary-600 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-colors shadow-lg"
          >
            Перейти к товарам
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
        <div className="bg-white p-6 rounded-xl shadow-md text-center">
          <div className="text-4xl mb-4">🚚</div>
          <h3 className="text-xl font-bold mb-2">Быстрая доставка</h3>
          <p className="text-gray-600">Доставляем товары по всей стране за 1-3 дня</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-md text-center">
          <div className="text-4xl mb-4">💳</div>
          <h3 className="text-xl font-bold mb-2">Удобная оплата</h3>
          <p className="text-gray-600">Множество способов оплаты на ваш выбор</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-md text-center">
          <div className="text-4xl mb-4">✅</div>
          <h3 className="text-xl font-bold mb-2">Гарантия качества</h3>
          <p className="text-gray-600">Только оригинальные товары с гарантией</p>
        </div>
      </section>
    </div>
  )
}

export default Home

