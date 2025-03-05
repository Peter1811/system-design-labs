from app.auth import hash_password
from app.db_config import SessionLocal
from app.models import User, Presentation, Conference

session = SessionLocal()

# создание админа
admin = User(is_superuser=True,
             login='admin',
             first_name='admin',
             last_name='admin',
             hashed_password=hash_password('secret'))

session.add(admin)


# создание конференций
conferences = {
    "PyCon": "PyCon — крупнейшая мировая конференция для Python-разработчиков, на которой обсуждаются последние тренды в экосистеме Python, а также проводятся мастер-классы, лекции и сессии с участием известных специалистов.",
    "Google I/O": "Google I/O — ежегодная конференция разработчиков, организуемая Google. Основное внимание уделяется новинкам в области мобильных приложений, искусственного интеллекта, облачных технологий и решений для веб-разработчиков.",
    "WWDC (Apple Worldwide Developers Conference)": "WWDC — ежегодная конференция Apple для разработчиков, на которой представляются новые технологии и обновления для платформ Apple, таких как iOS, macOS, watchOS и tvOS.",
    "Microsoft Build": "Microsoft Build — конференция для разработчиков, организуемая Microsoft, на которой презентуются новинки в мире технологий и продуктов Microsoft, включая Azure, Visual Studio, .NET и других инструментов для разработки.",
    "Black Hat": "Black Hat — одна из крупнейших мировых конференций по безопасности, где обсуждаются вопросы хакерства, уязвимостей и защиты данных, а также проводятся тренинги по кибербезопасности.",
    "DockerCon": "DockerCon — конференция, посвященная Docker и контейнеризации. На ней обсуждаются лучшие практики работы с контейнерами, оркестрацией, а также новинки в экосистеме Docker и Kubernetes.",
    "KubeCon + CloudNativeCon": "KubeCon + CloudNativeCon — конференция для разработчиков, работающих с Kubernetes и другими облачными технологиями, включая микросервисы и контейнерные платформы.",
    "AWS re:Invent": "AWS re:Invent — ежегодная конференция, организованная Amazon Web Services. Она фокусируется на облачных решениях, новых продуктах AWS, инновациях в области облачных вычислений и инфраструктуры.",
    "DevOpsDays": "DevOpsDays — серия международных конференций, посвященных методологиям DevOps и практике непрерывной доставки. На конференциях обсуждаются темы автоматизации, сотрудничества команд и улучшения процесса разработки и эксплуатации.",
    "Strata Data Conference": "Strata Data Conference — конференция, посвященная обработке больших данных, аналитике и машинному обучению. Участники обсуждают новейшие тенденции в области анализа данных, искусственного интеллекта и обработки информации.",
}

presentations = {
    "PyCon": [
        {"title": "Python 3.10: New Features and Best Practices", "description": "Обзор новых возможностей в Python 3.10 и рекомендации по их использованию в реальных проектах."},
        {"title": "Machine Learning with TensorFlow and Python", "description": "Как использовать TensorFlow для разработки моделей машинного обучения с использованием Python."},
        {"title": "Asynchronous Programming in Python: A Deep Dive", "description": "Подробное изучение асинхронного программирования в Python с использованием `asyncio`, `aiohttp` и других библиотек."},
    ],
    
    "Google I/O": [
        {"title": "Building Progressive Web Apps with Firebase", "description": "Как создать прогрессивные веб-приложения с использованием Firebase для хранения данных и аутентификации."},
        {"title": "Introduction to Android Jetpack Compose", "description": "Обзор нового подхода к разработке UI в Android с использованием Jetpack Compose."},
        {"title": "AI and ML with Google Cloud: From Idea to Production", "description": "Как использовать инструменты и сервисы Google Cloud для разработки, развертывания и масштабирования моделей машинного обучения."},
    ],
    
    "WWDC (Apple Worldwide Developers Conference)": [
        {"title": "What's New in Swift 5.5", "description": "Изучаем новшества в языке программирования Swift 5.5, включая улучшения работы с асинхронностью и новые синтаксические возможности."},
        {"title": "Developing for ARKit: Building Augmented Reality Apps", "description": "Как создавать приложения дополненной реальности для iOS с использованием ARKit и других инструментов."},
        {"title": "Exploring New Features in iOS 15", "description": "Обзор новых функций iOS 15, включая улучшения в безопасности, интерфейсе и интеграции с Siri."},
    ],
    
    "Microsoft Build": [
        {"title": "Building Cloud-Native Applications with Azure", "description": "Как использовать платформу Microsoft Azure для создания облачных решений и масштабируемых приложений."},
        {"title": "Improving Developer Productivity with GitHub Actions", "description": "Как автоматизировать CI/CD процессы с использованием GitHub Actions для ускорения разработки."},
        {"title": "Creating Cross-Platform Apps with .NET 6", "description": "Как разработать кроссплатформенные приложения с использованием .NET 6 и Blazor."},
    ],
    
    "Black Hat": [
        {"title": "Exploiting Zero-Day Vulnerabilities in Web Applications", "description": "Анализ уязвимостей нулевого дня в веб-приложениях и способы защиты от них."},
        {"title": "Advanced Threat Hunting Techniques", "description": "Техники обнаружения и анализа сложных киберугроз в корпоративных системах."},
        {"title": "Ransomware: Anatomy of an Attack", "description": "Как работают современные атаки с использованием программ-вымогателей и как от них защититься."},
    ],
    
    "DockerCon": [
        {"title": "Docker for DevOps: Simplifying the CI/CD Pipeline", "description": "Как использовать Docker для упрощения процесса CI/CD и создания эффективных DevOps-процессов."},
        {"title": "Scaling Kubernetes with Helm Charts", "description": "Как использовать Helm для управления приложениями и масштабирования в Kubernetes."},
        {"title": "Securing Docker Containers: Best Practices", "description": "Лучшие практики по безопасности контейнеров Docker и защите от возможных угроз."},
    ],
    
    "KubeCon + CloudNativeCon": [
        {"title": "Building Cloud-Native Applications with Kubernetes", "description": "Как разрабатывать облачные приложения с использованием Kubernetes и других современных инструментов."},
        {"title": "Service Mesh with Istio: A Hands-On Introduction", "description": "Как внедрить и настроить сервисную сетку с помощью Istio для улучшения связи между сервисами."},
        {"title": "Scaling Kubernetes: From Development to Production", "description": "Лучшие практики для масштабирования Kubernetes-решений с учётом производительности и надежности."},
    ],
    
    "AWS re:Invent": [
        {"title": "Building Serverless Applications with AWS Lambda", "description": "Как создать серверлес-приложения с использованием AWS Lambda и других связанных сервисов."},
        {"title": "Optimizing AWS Costs: Best Practices and Tools", "description": "Как эффективно управлять расходами на AWS и использовать инструменты для их оптимизации."},
        {"title": "Machine Learning at Scale with Amazon SageMaker", "description": "Как разрабатывать и масштабировать модели машинного обучения с использованием Amazon SageMaker."},
    ],
    
    "DevOpsDays": [
        {"title": "Continuous Integration and Continuous Delivery: Best Practices", "description": "Обзор лучших практик CI/CD для улучшения автоматизации и качества разработки."},
        {"title": "Monitoring and Observability in Modern DevOps", "description": "Как использовать мониторинг и инструменты наблюдаемости для управления системами и приложениями в DevOps."},
        {"title": "Microservices in DevOps: Challenges and Solutions", "description": "Как внедрить и поддерживать микросервисы в рамках DevOps-подхода."},
    ],
    
    "Strata Data Conference": [
        {"title": "Data Engineering with Apache Kafka", "description": "Как использовать Apache Kafka для построения масштабируемых и высокоскоростных систем обработки данных."},
        {"title": "Machine Learning for Big Data: Tools and Techniques", "description": "Обзор инструментов и методов для работы с большими данными и построения моделей машинного обучения."},
        {"title": "Data Privacy and Ethics: Navigating the Modern Landscape", "description": "Как учитывать этические и правовые аспекты при работе с большими данными и машинным обучением."},
    ],
}

conf_id = 1
for conference in conferences:
    new_conference = Conference(name=conference,
                                description=conferences[conference])
    
    session.add(new_conference)

    for presentation in presentations[conference]:
        new_presentation = Presentation(name=presentation['title'],
                                        description=presentation['description'],
                                        conference_id=conf_id)
        
        session.add(new_presentation)

    conf_id += 1

session.commit()
session.close()
