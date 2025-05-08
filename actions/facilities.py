from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json

with open('dataset/facilities.json', 'r', encoding='utf-8') as file:
    facilities_data = json.load(file)

class ActionHostelDescription(Action):
    def name(self) -> Text:
        return "action_hostel_description"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        description = facilities_data[0]["Hostel"]["description"]
        dispatcher.utter_message(text=f"Here's the description of the CBIT hostel: {description}")
        return []

class ActionHostelDetails(Action):
    def name(self) -> Text:
        return "action_hostel_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        junior_block = facilities_data[0]["Hostel"]["details"]["junior_block"]
        senior_block = facilities_data[0]["Hostel"]["details"]["senior_block"]
        total_capacity = facilities_data[0]["Hostel"]["details"]["total_capacity"]
        purpose = facilities_data[0]["Hostel"]["details"]["purpose"]

        details_message = (
            f"Junior Block:\n- Rooms: {junior_block['rooms']}\n- Occupancy: {junior_block['occupancy']}\n"
            f"- Description: {junior_block['description']}\n\n"
            f"Senior Block:\n- Rooms: {senior_block['rooms']}\n- Occupancy: {senior_block['occupancy']}\n"
            f"- Description: {senior_block['description']}\n\n"
            f"Total Capacity: {total_capacity}\nPurpose of Separation: {purpose}"
        )
        
        dispatcher.utter_message(text=f"Here are the details of the CBIT hostel:\n{details_message}")
        return []

class ActionHostelContact(Action):
    def name(self) -> Text:
        return "action_hostel_contact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        contacts = facilities_data[0]["Hostel"]["contact_info"]
        contact_details = "\n".join(
            [f"{contact['name']} ({contact['position']}): Phone - {contact['phone']}, Email - {contact.get('email', 'N/A')}" for contact in contacts]
        )
        
        dispatcher.utter_message(text=f"Here are the contact details for the CBIT hostel:\n{contact_details}")
        return []


class ActionTransportInstructions(Action):
    def name(self) -> Text:
        return "action_transport_instructions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        parent_instructions = "\n".join(facilities_data[1]["transport"]["instructions"]["parents"])
        student_instructions = "\n".join(facilities_data[1]["transport"]["instructions"]["students"])
        
        instructions_message = (
            f"Instructions for Parents:\n{parent_instructions}\n\n"
            f"Instructions for Students:\n{student_instructions}"
        )
        
        dispatcher.utter_message(text=f"Here are the transport instructions:\n{instructions_message}")
        return []

class ActionTransportHowToApply(Action):
    def name(self) -> Text:
        return "action_transport_how_to_apply"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        how_to_apply = "\n".join(facilities_data[1]["transport"]["how_to_apply"])
        
        dispatcher.utter_message(text=f"Here's how to apply for transport:\n{how_to_apply}")
        return []

class ActionTransportContactDetails(Action):
    def name(self) -> Text:
        return "action_transport_contact_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        contacts = facilities_data[1]["transport"]["contact_details"]
        contact_details = "\n".join(
            [f"{contact['name']} ({contact['designation']}): Phone - {contact['phone']}, Working Hours - {contact['working_hours']}, Email - {contact.get('email', 'N/A')}" for contact in contacts]
        )
        
        dispatcher.utter_message(text=f"Here are the transport contact details:\n{contact_details}")
        return []


class ActionDataCenterDescription(Action):
    def name(self) -> Text:
        return "action_data_center_description"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        description = facilities_data[2]["data_center_and_chnms"]["description"]
        dispatcher.utter_message(text=f"Here's the description of the Data Center and Campus Wide Networking (CWN): {description}")
        return []

class ActionWiFiFacilityDescription(Action):
    def name(self) -> Text:
        return "action_wifi_facility_description"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        wifi_description = facilities_data[2]["data_center_and_chnms"]["wifi_facility"]["description"]
        dispatcher.utter_message(text=f"Here's the description of the Wi-Fi facility: {wifi_description}")
        return []

class ActionDataCenterDetails(Action):
    def name(self) -> Text:
        return "action_data_center_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        data_center_description = facilities_data[2]["data_center_and_chnms"]["data_center"]["description"]
        dispatcher.utter_message(text=f"Here are the details of the Data Center: {data_center_description}")
        return []

class ActionCHNMSDetails(Action):
    def name(self) -> Text:
        return "action_chnms_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        chnms_description = facilities_data[2]["data_center_and_chnms"]["chnms"]["description"]
        contacts = facilities_data[2]["data_center_and_chnms"]["chnms"]["contacts"]
        
        contact_details = "\n".join(
            [f"{contact['name']} ({contact['position']})" for contact in contacts]
        )
        
        dispatcher.utter_message(text=f"Details about CHNMS:\n{chnms_description}\n\nContact Information:\n{contact_details}")
        return []
    

class ActionHealthCenterDescription(Action):
    def name(self) -> Text:
        return "action_health_center_description"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        description = facilities_data[3]["health_center"]["description"]
        dispatcher.utter_message(text=f"Here's the description of the CBIT Health Center: {description}")
        return []

class ActionMedicalStaffDetails(Action):
    def name(self) -> Text:
        return "action_medical_staff_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        medical_officer = facilities_data[3]["health_center"]["medical_staff"]["medical_officer"]
        staff_nurse = facilities_data[3]["health_center"]["medical_staff"]["staff_nurse"]
        
        medical_staff_message = (
            f"Medical Officer: {medical_officer}\n"
            f"Staff Nurse: {staff_nurse}"
        )
        
        dispatcher.utter_message(text=f"Here are the details of the medical staff:\n{medical_staff_message}")
        return []

class ActionAmbulanceServiceDetails(Action):
    def name(self) -> Text:
        return "action_ambulance_service_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        availability = facilities_data[3]["health_center"]["ambulance_service"]["availability"]
        purpose = facilities_data[3]["health_center"]["ambulance_service"]["purpose"]
        
        ambulance_service_message = (
            f"Availability: {availability}\n"
            f"Purpose: {purpose}"
        )
        
        dispatcher.utter_message(text=f"Here are the details of the ambulance service:\n{ambulance_service_message}")
        return []
    

class ActionMediaCenterDescription(Action):
    def name(self) -> Text:
        return "action_media_center_description"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        description = facilities_data[4]["media_center"]["description"]
        dispatcher.utter_message(text=f"Here's the description of the Media Center: {description}")
        return []

class ActionEContentDetails(Action):
    def name(self) -> Text:
        return "action_e_content_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        e_content = facilities_data[4]["media_center"]["e_content"]
        e_content_message = (
            f"Development: {e_content['development']}\n"
            f"Public Link: {e_content['public_link']}\n"
            f"Institute Domain Link: {e_content['institute_domain_link']}\n"
            f"Note: {e_content['note']}"
        )
        
        dispatcher.utter_message(text=f"Here are the details of e-Content:\n{e_content_message}")
        return []

class ActionAccessDetails(Action):
    def name(self) -> Text:
        return "action_access_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        access_details = facilities_data[4]["media_center"]["access_details"]
        access_message = (
            f"Sharing Initiation: {access_details['sharing_initiation']}\n"
            f"Recorded Lectures Link: {access_details['recorded_lectures_link']}\n"
            f"Additional Link: {access_details['additional_link']}\n"
            f"Access Requirements: {access_details['access_requirements']}"
        )
        
        dispatcher.utter_message(text=f"Here are the access details:\n{access_message}")
        return []


class ActionICTToolsDescription(Action):
    def name(self) -> Text:
        return "action_ict_tools_description"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        description = facilities_data[5]["ict_tools"]["description"]
        dispatcher.utter_message(text=f"Here's the description of ICT tools at CBIT: {description}")
        return []

class ActionICTInfrastructureDetails(Action):
    def name(self) -> Text:
        return "action_ict_infrastructure_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        infrastructure = facilities_data[5]["ict_tools"]["infrastructure"]
        infrastructure_message = (
            f"Computer Availability: {infrastructure['computer_availability']}\n"
            f"Internet Connectivity: {infrastructure['internet_connectivity']}\n"
            f"Faculty Training: {infrastructure['faculty_training']}"
        )
        
        dispatcher.utter_message(text=f"Here are the details of ICT infrastructure:\n{infrastructure_message}")
        return []

class ActionBlendedLearningDetails(Action):
    def name(self) -> Text:
        return "action_blended_learning_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        blended_learning = facilities_data[5]["ict_tools"]["blended_learning"]
        tools_used = "\n".join(blended_learning["tools_used"])
        
        blended_learning_message = (
            f"Approach: {blended_learning['approach']}\n"
            f"ICT Integration: {blended_learning['ict_integration']}\n"
            f"Tools Used:\n{tools_used}"
        )
        
        dispatcher.utter_message(text=f"Here are the details of blended learning:\n{blended_learning_message}")
        return []

class ActionLearningManagementSystemDetails(Action):
    def name(self) -> Text:
        return "action_learning_management_system_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        lms = facilities_data[5]["ict_tools"]["learning_management_system"]
        
        lms_message = (
            f"Platform: {lms['platform']}\n"
            f"URL: {lms['url']}\n"
            f"Cloud Storage URL: {lms['cloud_url']}\n"
            f"Account Management: {lms['account_management']}"
        )
        
        dispatcher.utter_message(text=f"Here are the details of the Learning Management System:\n{lms_message}")
        return []

class ActionLibraryInformationCenterDetails(Action):
    def name(self) -> Text:
        return "action_library_information_center_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        library_info = facilities_data[5]["ict_tools"]["library_and_information_center"]
        
        digital_resources = library_info["digital_resources"]
        remote_access = library_info["remote_access"]
        
        library_message = (
            f"Digital Resources:\n- Description: {digital_resources['description']}\n"
            f"- Access Method: {digital_resources['access_method']}\n"
            f"- Accessibility: {digital_resources['accessibility']}\n\n"
            
            f"Remote Access:\n- Introduction: {remote_access['introduction']}\n"
            f"- Purpose: {remote_access['purpose']}\n"
            f"- Usage: {remote_access['usage']}"
        )
        
        dispatcher.utter_message(text=f"Here are the details of the Library and Information Center:\n{library_message}")
        return []