<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
  <title>Éclat — стильний одяг</title>
  <!-- Підключення сучасного шрифту з Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500&display=swap" rel="stylesheet">
  <!-- Font Awesome для іконок -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: 'Inter', sans-serif;
      background-color: #faf9f7;
      color: #2c2b2b;
      line-height: 1.5;
      scroll-behavior: smooth;
    }

    .container {
      max-width: 1280px;
      margin: 0 auto;
      padding: 0 24px;
    }

    /* Типографіка */
    h1, h2, h3 {
      font-family: 'Playfair Display', serif;
      font-weight: 600;
    }

    /* Хедер */
    .site-header {
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(255, 255, 255, 0.8);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid rgba(0,0,0,0.03);
      padding: 18px 0;
    }

    .header-inner {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .logo {
      font-family: 'Playfair Display', serif;
      font-size: 32px;
      font-weight: 700;
      letter-spacing: 2px;
      color: #1e1e1e;
      text-decoration: none;
    }
    .logo span {
      color: #b5835a;
    }

    .nav-links {
      display: flex;
      gap: 36px;
      list-style: none;
    }

    .nav-links a {
      text-decoration: none;
      color: #3a3a3a;
      font-weight: 500;
      font-size: 15px;
      transition: color 0.25s;
      position: relative;
    }

    .nav-links a:hover {
      color: #b5835a;
    }

    .header-icons {
      display: flex;
      gap: 20px;
      font-size: 20px;
      color: #2c2b2b;
    }
    .header-icons i {
      cursor: pointer;
      transition: color 0.2s;
    }
    .header-icons i:hover {
      color: #b5835a;
    }

    /* Hero секція */
    .hero {
      display: grid;
      grid-template-columns: 1fr 1fr;
      min-height: 85vh;
      align-items: center;
      background: linear-gradient(135deg, #f7f3ee 0%, #ffffff 100%);
      margin-bottom: 64px;
      border-radius: 0 0 60px 60px;
      overflow: hidden;
    }

    .hero-content {
      padding: 40px 0 40px 40px;
    }

    .hero-content h1 {
      font-size: 64px;
      font-weight: 700;
      line-height: 1.1;
      margin-bottom: 24px;
      color: #1f1f1f;
    }

    .hero-content p {
      font-size: 18px;
      color: #4d4d4d;
      margin-bottom: 36px;
      max-width: 400px;
    }

    .btn {
      display: inline-block;
      background: #1e1e1e;
      color: white;
      padding: 16px 38px;
      border-radius: 40px;
      text-decoration: none;
      font-weight: 600;
      font-size: 15px;
      letter-spacing: 0.5px;
      transition: all 0.3s ease;
      border: none;
      cursor: pointer;
      box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    }

    .btn:hover {
      background: #b5835a;
      box-shadow: 0 12px 28px rgba(181, 131, 90, 0.3);
      transform: translateY(-2px);
    }

    .hero-image {
      height: 100%;
      background: url('https://images.unsplash.com/photo-1483985988355-763728e1935b?q=80&w=2070&auto=format&fit=crop') center/cover no-repeat;
      min-height: 500px;
    }

    /* Секція товарів */
    .section-title {
      text-align: center;
      margin-bottom: 48px;
    }
    .section-title h2 {
      font-size: 42px;
      color: #1e1e1e;
      margin-bottom: 12px;
    }
    .section-title p {
      color: #6b6b6b;
      font-weight: 400;
    }

    .product-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 32px;
      margin-bottom: 80px;
    }

    .product-card {
      background: white;
      border-radius: 24px;
      overflow: hidden;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      box-shadow: 0 10px 25px rgba(0,0,0,0.04);
      display: flex;
      flex-direction: column;
    }

    .product-card:hover {
      transform: translateY(-8px);
      box-shadow: 0 24px 40px rgba(0,0,0,0.08);
    }

    .product-img {
      width: 100%;
      aspect-ratio: 3/4;
      object-fit: cover;
      background: #f0ede8;
    }

    .product-info {
      padding: 22px 20px 28px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }

    .product-category {
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: #b5835a;
      font-weight: 600;
      margin-bottom: 6px;
    }

    .product-name {
      font-family: 'Playfair Display', serif;
      font-size: 22px;
      font-weight: 600;
      margin-bottom: 8px;
      color: #1e1e1e;
    }

    .price {
      font-weight: 700;
      font-size: 18px;
      color: #2c2b2b;
      margin-top: auto;
      padding-top: 12px;
      border-top: 1px solid #f0f0f0;
    }

    /* Банерна секція */
    .banner {
      background: #ede7df;
      border-radius: 40px;
      padding: 70px 60px;
      margin: 60px 0 80px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 30px;
    }

    .banner-text h3 {
      font-size: 36px;
      margin-bottom: 12px;
    }

    /* Футер */
    .footer {
      background: #1e1e1e;
      color: #d4d4d4;
      padding: 60px 0 30px;
      border-radius: 50px 50px 0 0;
      margin-top: 40px;
    }

    .footer-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 40px;
      margin-bottom: 50px;
    }

    .footer-col h4 {
      color: white;
      font-family: 'Playfair Display', serif;
      font-size: 20px;
      margin-bottom: 20px;
    }

    .footer-col a {
      display: block;
      color: #b0b0b0;
      text-decoration: none;
      margin-bottom: 12px;
      font-size: 15px;
      transition: color 0.2s;
    }
    .footer-col a:hover {
      color: #b5835a;
    }

    .social-icons i {
      font-size: 22px;
      margin-right: 18px;
      color: #ccc;
      transition: color 0.2s;
    }
    .social-icons i:hover {
      color: #b5835a;
    }

    .copyright {
      text-align: center;
      border-top: 1px solid #3a3a3a;
      padding-top: 28px;
      font-size: 14px;
      color: #888;
    }

    @media (max-width: 768px) {
      .hero {
        grid-template-columns: 1fr;
        text-align: center;
      }
      .hero-content {
        padding: 50px 24px;
        order: 2;
      }
      .hero-image {
        height: 400px;
        order: 1;
      }
      .nav-links {
        display: none;
      }
      .banner {
        flex-direction: column;
        text-align: center;
        padding: 40px 24px;
      }
    }
  </style>
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <a href="#" class="logo">Éclat<span>.</span></a>
      <ul class="nav-links">
        <li><a href="#">Новинки</a></li>
        <li><a href="#">Жінки</a></li>
        <li><a href="#">Чоловіки</a></li>
        <li><a href="#">Аксесуари</a></li>
        <li><a href="#">Розпродаж</a></li>
      </ul>
      <div class="header-icons">
        <i class="far fa-heart"></i>
        <i class="fas fa-shopping-bag"></i>
      </div>
    </div>
  </header>

  <main>
    <!-- Hero -->
    <section class="hero container">
      <div class="hero-content">
        <h1>Нова колекція<br>весна-літо</h1>
        <p>Вишукані силуети, натуральні тканини та позачасова елегантність.</p>
        <a href="#" class="btn">Переглянути</a>
      </div>
      <div class="hero-image"></div>
    </section>

    <!-- Продукти -->
    <div class="container">
      <div class="section-title">
        <h2>Популярне зараз</h2>
        <p>Те, що обирають наші клієнти</p>
      </div>
      <div class="product-grid">
        <!-- Картка 1 -->
        <div class="product-card">
          <img src="https://images.unsplash.com/photo-1591047139829-d91aecb6caea?q=80&w=1936&auto=format&fit=crop" alt="Лляна сукня" class="product-img">
          <div class="product-info">
            <span class="product-category">Сукні</span>
            <h3 class="product-name">Лляна міді</h3>
            <div class="price">3 200 ₴</div>
          </div>
        </div>
        <!-- Картка 2 -->
        <div class="product-card">
          <img src="https://images.unsplash.com/photo-1594938298603-c8148c4dae35?q=80&w=2080&auto=format&fit=crop" alt="Біла сорочка" class="product-img">
          <div class="product-info">
            <span class="product-category">Сорочки</span>
            <h3 class="product-name">Оверсайз біла</h3>
            <div class="price">2 450 ₴</div>
          </div>
        </div>
        <!-- Картка 3 -->
        <div class="product-card">
          <img src="https://images.unsplash.com/photo-1601924994987-69e26d50dc26?q=80&w=2070&auto=format&fit=crop" alt="Трикотажний светр" class="product-img">
          <div class="product-info">
            <span class="product-category">Трикотаж</span>
            <h3 class="product-name">Кашеміровий светр</h3>
            <div class="price">4 100 ₴</div>
          </div>
        </div>
        <!-- Картка 4 -->
        <div class="product-card">
          <img src="https://images.unsplash.com/photo-1544441893-675973e31985?q=80&w=2070&auto=format&fit=crop" alt="Штани палаццо" class="product-img">
          <div class="product-info">
            <span class="product-category">Штани</span>
            <h3 class="product-name">Палаццо кремові</h3>
            <div class="price">2 950 ₴</div>
          </div>
        </div>
      </div>

      <!-- Банер -->
      <div class="banner">
        <div class="banner-text">
          <h3>Літній розпродаж</h3>
          <p style="font-size: 18px; margin-bottom: 20px;">Знижки до -40% на обрану колекцію</p>
          <a href="#" class="btn" style="background: white; color: #1e1e1e;">Дивитись пропозиції</a>
        </div>
        <div>
          <i class="fas fa-tags" style="font-size: 70px; color: #b5835a; opacity: 0.7;"></i>
        </div>
      </div>

      <!-- Друга сітка товарів (аксесуари) -->
      <div class="section-title">
        <h2>Аксесуари</h2>
        <p>Деталі, що завершують образ</p>
      </div>
      <div class="product-grid">
        <div class="product-card">
          <img src="https://images.unsplash.com/photo-1584917865442-de89df76afd3?q=80&w=1935&auto=format&fit=crop" alt="Сумка" class="product-img">
          <div class="product-info">
            <span class="product-category">Сумки</span>
            <h3 class="product-name">Шкіряна сумка-тоут</h3>
            <div class="price">5 600 ₴</div>
          </div>
        </div>
        <div class="product-card">
          <img src="https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?q=80&w=1974&auto=format&fit=crop" alt="Капелюх" class="product-img">
          <div class="product-info">
            <span class="product-category">Головні убори</span>
            <h3 class="product-name">Фетровий капелюх</h3>
            <div class="price">1 850 ₴</div>
          </div>
        </div>
        <div class="product-card">
          <img src="https://images.unsplash.com/photo-1611085583191-a3b181a88401?q=80&w=1974&auto=format&fit=crop" alt="Шарф" class="product-img">
          <div class="product-info">
            <span class="product-category">Шарфи</span>
            <h3 class="product-name">Шовковий шарф</h3>
            <div class="price">1 250 ₴</div>
          </div>
        </div>
        <div class="product-card">
          <img src="https://images.unsplash.com/photo-1576158114254-3ba81558b168?q=80&w=2080&auto=format&fit=crop" alt="Прикраси" class="product-img">
          <div class="product-info">
            <span class="product-category">Прикраси</span>
            <h3 class="product-name">Мінімалістичний сет</h3>
            <div class="price">2 200 ₴</div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <h4>Éclat</h4>
          <p style="color: #b0b0b0; margin-bottom: 16px;">Стиль, що надихає.</p>
          <div class="social-icons">
            <i class="fab fa-instagram"></i>
            <i class="fab fa-pinterest"></i>
            <i class="fab fa-telegram"></i>
          </div>
        </div>
        <div class="footer-col">
          <h4>Колекції</h4>
          <a href="#">Новинки</a>
          <a href="#">Бестселери</a>
          <a href="#">Базовий гардероб</a>
        </div>
        <div class="footer-col">
          <h4>Допомога</h4>
          <a href="#">Доставка та оплата</a>
          <a href="#">Повернення</a>
          <a href="#">FAQ</a>
        </div>
        <div class="footer-col">
          <h4>Контакти</h4>
          <a href="#">hello@eclat.ua</a>
          <a href="#">+380 44 123 45 67</a>
          <a href="#">Київ, вул. Драгоманова 29</a>
        </div>
      </div>
      <div class="copyright">
        &copy; 2025 Éclat. Усі права захищені. Створено з любов’ю.
      </div>
    </div>
  </footer>
</body>
</html>
