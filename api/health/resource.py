from flask_restful import Resource


class Health(Resource):
    @staticmethod
    def get():
        return {
            "status": "OK"
        }
