const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white mt-auto">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">О нас</h3>
            <p className="text-gray-400">
              Современный интернет-магазин с лучшими товарами и качественным сервисом.
            </p>
          </div>
          <div>
            <h3 className="text-xl font-bold mb-4">Контакты</h3>
            <p className="text-gray-400">Email: info@shop.ru</p>
            <p className="text-gray-400">Телефон: +7 (999) 123-45-67</p>
          </div>
          <div>
            <h3 className="text-xl font-bold mb-4">Следите за нами</h3>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-white">VK</a>
              <a href="#" className="text-gray-400 hover:text-white">Telegram</a>
              <a href="#" className="text-gray-400 hover:text-white">Instagram</a>
            </div>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2024 Интернет-магазин. Все права защищены.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer

