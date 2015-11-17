from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from ouija.core import assets, app
from ouija.api.base import base_api
from ouija.api.tables import tables_api


app.register_blueprint(base_api)
app.register_blueprint(tables_api)

manager = Manager(app)
manager.add_command('assets', ManageAssets(assets))


def main():
    manager.run()


if __name__ == "__main__":
    main()
