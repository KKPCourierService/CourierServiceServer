from app_kkp import app, db

import os
from clients.controllers import clients_blu
# from clients.controllersBrouser import clients_brouser_blu
from orders.controllers import orders_blu
# from orders.controllersBrouser import orders_brouser_blu
from couriers.controllers import couriers_blu
# from couriers.controllersBrouser import couriers_brouser_blu
from managers.controllers import managers_blu
# from managers.controllersBrouser import managers_brouser_blu

import view


# Регистрируем blueprint для работы с разными url

app.register_blueprint(clients_blu)
# app.register_blueprint(clients_brouser_blu)
app.register_blueprint(orders_blu)
# app.register_blueprint(orders_brouser_blu)
app.register_blueprint(couriers_blu)
# app.register_blueprint(couriers_brouser_blu)
app.register_blueprint(managers_blu)
# app.register_blueprint(managers_brouser_blu)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
