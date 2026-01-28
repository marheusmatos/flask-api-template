from flask import Flask
from flask_restx import Api
from dotenv import load_dotenv

import config

from routes.qa_email import api as qa_email_ns

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    api = Api(
        app,
        title="QA Email Review API",
        version="1.0",
        description="API para analistas QA controlarem e auditarem revisões de e-mail feitas por IA"
    )

    api.add_namespace(qa_email_ns)


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
