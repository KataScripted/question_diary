import json

from flask import request

from Addons.Backend.Connection.ComplaintDAO import ComplaintDAO

ComplaintC = ComplaintDAO()


class ComplaintController:
    def complaint(self):
        data = json.loads(request.data)
        new_data = []
        for i in data.values():
            new_data.append(i)
        return ComplaintC.complaint_dao(username=new_data[0], question_id=new_data[1], text=new_data[2])
