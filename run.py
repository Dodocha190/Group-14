from app import create_app, db
from app.config import DeploymentConfig, TestConfig
from flask_migrate import Migrate

application= create_app(DeploymentConfig)
migrate = Migrate(application, db)

if __name__ == '__main__':
    application.run(debug=True)
  