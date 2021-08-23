from flask_restful import Resource

class UserAPIView(Resource):
    def get(self):
        return {"message": "Hello Worlds"}

    def post(self):
        return {"message": "Hahah"}