from app import create_app, db
from app.config import DeploymentConfig, TestConfig
from flask_migrate import Migrate



if __name__ == '__main__':
    application= create_app(DeploymentConfig)
    migrate = Migrate(application, db)
    application.run(debug=True)
  