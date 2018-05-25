from app_kkp import app, db

#from posts.blueprint import posts
from clients.controllers import clients_blu
from orders.controllers import orders_blu
from couriers.controllers import couriers_blu
from managers.controllers import managers_blu

import view


#Регистрируем blueprint для работы с разными url

app.register_blueprint(clients_blu)
app.register_blueprint(orders_blu)
app.register_blueprint(couriers_blu)
app.register_blueprint(managers_blu)

if __name__ == '__main__':
    app.run()