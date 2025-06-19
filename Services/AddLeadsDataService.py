from Services.CallJavaApiService import CallJavaApiService
from Constants.constant import *


class AddLeadsDetails:
    def get_hubspot_id(self, token):
        try:
            request_body_to_get_userid = self.get_request_body(token, SIGN_IN_ENDPOINT, SIGN_IN_PAYLOAD, SAVE_METHOD)
            user_id_response = CallJavaApiService(BASE_URL).java_api_call(SAVE_METHOD, request_body_to_get_userid)
            user_id = user_id_response['id']
            if not user_id:
                return user_id_response
            request_body_to_get_hubspotid = self.get_request_body(user_id_response['token'],
                                                                  CONTACT_API_ENDPOINT.format(id=user_id), None,
                                                                  GET_METHOD)
            hubspot_id_response = CallJavaApiService(BASE_URL).java_api_call(SAVE_METHOD, request_body_to_get_hubspotid)
            hubspot_id = hubspot_id_response['contactDetails']['hubspotId']
            if not hubspot_id:
                return "hubspot id not found"
            return hubspot_id,request_body_to_get_hubspotid['auth']
        except Exception as e:
            return "hubspot id not found"

    def add_leads_details(self,lead_name, first_name, last_name, email, phone_number, token, message,company_name,state):
        try:
            hubspot_id,auth = AddLeadsDetails().get_hubspot_id(None)
            if hubspot_id == "hubspot id not found":
                return "Not Found"
            request_body = self.get_request_body(token, LEADS_API_ENDPOINT.format(id=hubspot_id), PAYLOAD, SAVE_METHOD)
            first_name = " " if first_name is None else first_name
            last_name = " " if last_name is None else last_name
            request_body['payload']['properties']['company_name'] = company_name
            request_body['payload']['properties']['state'] = state
            request_body['payload']['properties']['hs_lead_name'] = lead_name
            request_body['payload']['properties']['first_name'] = first_name
            request_body['payload']['properties']['last_name'] = last_name
            request_body['payload']['properties']['email'] = email
            request_body['payload']['properties']['phone_number'] = phone_number
            request_body['payload']['properties']['message'] = message
            request_body['auth'] = auth
            response = CallJavaApiService(BASE_URL).java_api_call(SAVE_METHOD, request_body)
            return response
        except Exception as e:
            return str(e)

    def get_request_body(self, token, endpoint, payload, method):
        data = {
            "endpoint": endpoint,
            "payload": payload,
            "type": method,
            "auth": token
        }
        return data
