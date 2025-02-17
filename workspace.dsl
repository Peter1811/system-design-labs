workspace {
    model {
        user = person "Слушатель" "Зритель конференции."
        presentation_provider = person "Исполнитель" "Спикер конференции."

        web_application = softwareSystem "Веб-приложение" "Позволяет пользователям взаимодействовать с системой." {
            web_ui = container "Веб-интерфейс" "Обеспечивает интерфейс для взаимодействия пользователей с системой." "HTML, CSS, JavaScript"
            web_backend = container "Серверная часть веб-приложения" "Обрабатывает запросы от веб-интерфейса и взаимодействует с API других сервисов." "Python (FastAPI)"
        }

        users_service = softwareSystem "Сервис пользователей" "Управляет данными пользователей и их аутентификацией." {
            users_api = container "API пользователей" "Обеспечивает функционал аутентификации и управления пользователями." "Python (FastAPI)"
            users_database = container "База данных пользователей" "Хранит данные о пользователях." "PostgreSQL"
        }

        presentations_service = softwareSystem "Сервис докладов" "Управляет данными о докладах." {
            presentations_api = container "API услуг" "Обеспечивает функционал управления докладами." "Python (FastAPI)"
            presentations_database = container "База данных докладов" "Хранит данные о докладах." "PostgreSQL"
        }

        conferences_service = softwareSystem "Сервис конференций" "Управляет созданием и обработкой конференций." {
            conferences_api = container "API конференций" "Обеспечивает функционал создания и управления конференциями." "Python (FastAPI)"
            conferences_database = container "База данных конференций" "Хранит данные о конференциях." "PostgreSQL"
        }
 
        user -> web_ui "Ищет конференции, подключается для прослушивания"
        presentation_provider -> web_ui "Добавляет доклад в конференцию и зачитывает доклад"
        web_ui -> web_backend "Передает запросы"
        
        web_backend -> users_api "Передает запросы на исполнение"
        web_backend -> presentations_api "Передает запросы на исполнение"
        web_backend -> conferences_api "Передает запросы на исполнение"
    
        users_api -> users_database "Читает и записывает данные о пользователях"
        presentations_api -> presentations_database "Читает и записывает данные о докладах"
        conferences_api -> conferences_database "Читает и записывает данные о конференциях"

        users_database -> users_api "Возвращает данные о пользователях"
        presentations_database -> presentations_api "Возвращает данные о докладах"
        conferences_database -> conferences_api "Возвращает данные о конференциях"

        users_api -> web_backend "Отправляет результаты запросов"
        presentations_api -> web_backend "Отправляет результаты запросов"
        conferences_api -> web_backend "Отправляет результаты запросов" 

        web_backend -> web_ui "Отправляет результаты запросов для отображения"
    }

    views {
        systemContext web_application {
            include *
            autolayout lr
        }

        systemContext users_service {
            include *
            autolayout lr
        }

        systemContext presentations_service {
            include *
            autolayout lr
        }

        systemContext conferences_service {
            include *
            autolayout lr
        }

        container web_application {
            include *
            autolayout lr
        }

        container users_service {
            include *
            autolayout lr
        }

        container presentations_service {
            include *
            autolayout lr
        }

        container conferences_service {
            include *
            autolayout lr
        }

        dynamic users_service "conference_search" {
            user -> web_ui "Вводит параметры поиска конференции"
            web_ui -> web_backend "Передает запрос на поиск"
            web_backend -> conferences_api "Запрашивает поиск"
            conferences_api -> conferences_database "Запрашивает данные о нужной конференции"
            conferences_database -> conferences_api "Возвращает результат поиска"
            conferences_api -> web_backend "Возвращает результат поиска"
            web_backend -> web_ui "Передает результат поиска"
            web_ui -> user "Отображает найденную конференцию"
        }
    }
}