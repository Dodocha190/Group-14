from app import create_app, db
from app.config import DeploymentConfig, TestConfig
from flask_migrate import Migrate

application= create_app(DeploymentConfig)

if __name__ == '__main__':

    migrate = Migrate(application, db)
    application.run(debug=True)
  