from Services.EntityFormationInfoExtractor import EntityFormationInfoExtractor


class UpdateCompanyDetails:
    def update_company_details(self, path,file):
        payload = EntityFormationInfoExtractor().get_json_of_entity_formation(path,file)
        if payload == "Unsupported file format":
            return "Not Found"
        return payload
