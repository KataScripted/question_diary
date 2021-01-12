import json

from flask import request

from Addons.Backend.Controllers.ComplaintController import ComplaintController
from Addons.Backend.Services.VKApi import *

ComplaintControllerS = ComplaintController()


class ComplaintService:
    def __init__(self):
        self.secret = "khKzTP7LbxqTqIcXrcTq"

    def complaint_service(self):
        headers = request.args.to_dict()
        valid = is_valid(query=headers, secret=self.secret)
        if not valid:
            return json.dumps(["Access Denied"])
        else:
            return ComplaintControllerS.complaint()
