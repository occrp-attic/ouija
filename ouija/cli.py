from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from ouija.core import assets, app
from ouija.api import base_api


app.register_blueprint(base_api)
manager = Manager(app)
manager.add_command('assets', ManageAssets(assets))


def main():
    manager.run()


if __name__ == "__main__":
    main()
