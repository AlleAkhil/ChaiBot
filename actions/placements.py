import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# Load the JSON data
with open('dataset/placements.json', 'r', encoding='utf-8') as file:
    college_data = json.load(file)

class ActionCDCVision(Action):
    def name(self) -> Text:
        return "action_cdc_vision"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        vision = college_data["Vision"]
        dispatcher.utter_message(text=f"Our vision is: {vision}")
        return []

class ActionCDCMission(Action):
    def name(self) -> Text:
        return "action_cdc_mission"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        mission = college_data["Mission"]
        dispatcher.utter_message(text="Our mission:")
        for item in mission:
            dispatcher.utter_message(text=f"- {item}")
        return []

class ActionCDCGuidelines(Action):
    def name(self) -> Text:
        return "action_cdc_guidelines"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        guidelines = college_data["Guidelines"]
        dispatcher.utter_message(text="Guidelines:")
        for item in guidelines:
            dispatcher.utter_message(text=f"- {item}")
        return []

class ActionCDCPlacementPolicy(Action):
    def name(self) -> Text:
        return "action_cdc_placement_policy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        policy = college_data["Placement_Policy"]
        dispatcher.utter_message(text="Placement Policy:")
        for item in policy:
            dispatcher.utter_message(text=f"- {item}")
        return []

class ActionCDCInternshipGuidelines(Action):
    def name(self) -> Text:
        return "action_cdc_internship_guidelines"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        guidelines = college_data["Internship_guidelines"]
        dispatcher.utter_message(text="Internship guidelines can be found at:")
        for item in guidelines:
            dispatcher.utter_message(text=f"- {item}")
        return []

class ActionCDCLORFormat(Action):
    def name(self) -> Text:
        return "action_cdc_lor_format"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        lor_format = college_data["LOR_Format"][0]
        dispatcher.utter_message(text=f"The LOR format can be found at: {lor_format}")
        return []


class ActionShowPlacementData(Action):
    # Class variable to store the placement data
    placement_data = None

    def __init__(self):
        # Load the data if it hasn't been loaded yet
        if ActionShowPlacementData.placement_data is None:
            with open('dataset/placements.json', 'r', encoding='utf-8') as file:
                ActionShowPlacementData.placement_data = json.load(file)

    def name(self) -> Text:
        return "action_show_placement_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        year = tracker.get_slot("year")
        if year:
            for data in self.placement_data["facets"]["placement_data"]:
                if data["year"] == year:
                    message = f"For the year {year}:\n"
                    message += f"Placements secured: {data['placements_secured']}\n"
                    message += f"More details: {data['link']}"
                    dispatcher.utter_message(text=message)
                    return []
            dispatcher.utter_message(text=f"No placement data found for the year {year}.")
        else:
            message = "Placement data for recent years:\n"
            for data in self.placement_data["facets"]["placement_data"]:
                message += f"{data['year']}: {data['placements_secured']} placements\n"
            dispatcher.utter_message(text=message)
        return []


class ActionShowCDCTeam(Action):
    # Class variable to store the CDC team data
    cdc_team_data = None

    def __init__(self):
        # Load the data if it hasn't been loaded yet
        if ActionShowCDCTeam.cdc_team_data is None:
            with open('dataset/placements.json', 'r', encoding='utf-8') as file:
                ActionShowCDCTeam.cdc_team_data = json.load(file)

    def name(self) -> Text:
        return "action_show_cdc_team"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if self.cdc_team_data and "cdc_team" in self.cdc_team_data:
            message = ""
            for member in self.cdc_team_data["cdc_team"]:
                message += f"- Name: {member['name']}\n"
                message += f"  Designation: {member['designation']}\n"
                message += f"  Contact: {member['contact_no']}\n"
                if member['email']:
                    message += f"  Email: {', '.join(member['email'])}\n"
                message += "\n"
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text="I'm sorry, but I couldn't access the CDC team data. Please try again later.")
        return []


class ActionShowCDCMemberByDesignation(Action):
    # Class variable to store the CDC team data
    cdc_team_data = None

    def __init__(self):
        # Load the data if it hasn't been loaded yet
        if ActionShowCDCMemberByDesignation.cdc_team_data is None:
            with open('dataset/placements.json', 'r', encoding='utf-8') as file:
                ActionShowCDCMemberByDesignation.cdc_team_data = json.load(file)

    def name(self) -> Text:
        return "action_show_cdc_member_by_designation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        designation = tracker.get_slot("designation")
        
        if not designation:
            dispatcher.utter_message(text="I'm sorry, but I couldn't understand the designation you're asking about. Could you please specify the designation?")
            return []

        if self.cdc_team_data and "cdc_team" in self.cdc_team_data:
            matching_members = []
            for member in self.cdc_team_data["cdc_team"]:
                if designation.lower() in member['designation'].lower():
                    matching_members.append(member)
            
            if matching_members:
                if len(matching_members) == 1:
                    message = "I found 1 person with this designation:\n\n"
                else:
                    message = f"I found {len(matching_members)} people with this designation:\n\n"
                
                for member in matching_members:
                    message += f"- Name: {member['name']}\n"
                    message += f"  Designation: {member['designation']}\n"
                    message += f"  Contact: {member['contact_no']}\n"
                    if member['email']:
                        message += f"  Email: {', '.join(member['email'])}\n"
                    message += "\n"
                
                dispatcher.utter_message(text=message.strip())
            else:
                dispatcher.utter_message(text=f"I'm sorry, but I couldn't find anyone with the designation '{designation}' in the CDC team.")
        else:
            dispatcher.utter_message(text="I'm sorry, but I couldn't access the CDC team data. Please try again later.")
        return []


class ActionShowSkillDevelopmentPrograms(Action):
    def name(self) -> Text:
        return "action_show_skill_development_programs"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        year = tracker.get_slot("year")

        if not college_data or "skill_development_programmes" not in college_data:
            dispatcher.utter_message(text="I'm sorry, but I couldn't retrieve the skill development program data.")
            return []

        if year:
            programs = college_data["skill_development_programmes"].get(year)
            if programs:
                dispatcher.utter_message(text=f"The skill development programs for {year} can be found here: {programs}")
            else:
                dispatcher.utter_message(text=f"I'm sorry, but I couldn't find the skill development programs for the year {year}.")
        else:
            message = "Here are the skill development programs available for different years:\n"
            for year, link in college_data["skill_development_programmes"].items():
                message += f"- {year}: {link}\n"
            dispatcher.utter_message(text=message)
        return []


class ActionShowStudentPlacementCoordinators(Action):
    def name(self) -> Text:
        return "action_show_student_placement_coordinators"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        year = tracker.get_slot("year")

        if not college_data or "student_placement_coordinators" not in college_data:
            dispatcher.utter_message(text="I'm sorry, but I couldn't retrieve the student placement coordinators data.")
            return []

        if year:
            coordinator_list = college_data["student_placement_coordinators"].get(year)
            if coordinator_list:
                dispatcher.utter_message(text=f"The student placement coordinators list for {year} can be found here: {coordinator_list}")
            else:
                dispatcher.utter_message(text=f"I'm sorry, but I couldn't find the student placement coordinators list for the year {year}.")
        else:
            message = "Here are the student placement coordinators lists available for different years:\n"
            for year, link in college_data["student_placement_coordinators"].items():
                message += f"- {year}: {link}\n"
            dispatcher.utter_message(text=message)
        return []


class ActionShowInfrastructure(Action):
    def name(self) -> Text:
        return "action_show_infrastructure"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not college_data or "infrastructure" not in college_data:
            dispatcher.utter_message(text="I'm sorry, but I couldn't retrieve the infrastructure data.")
            return []

        message = f"Infrastructure Description: {college_data['infrastructure']['description']}\n\n"
        message += "Available Facilities:\n"
        for item in college_data["infrastructure"]["facilities"]:
            message += f"- {item['facility']}:\n"
            for key, value in item.items():
                if key != "facility":
                    message += f"  {key.capitalize()}: {value}\n"
            message += "\n"
        dispatcher.utter_message(text=message)
        return []


class ActionShowCDCEvents(Action):
    def name(self) -> Text:
        return "action_show_cdc_events"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        year = tracker.get_slot("year")

        if not college_data or "events" not in college_data:
            dispatcher.utter_message(text="I'm sorry, but I couldn't retrieve the CDC events data.")
            return []

        # Check if the intent is to list all events
        intent = tracker.latest_message['intent'].get('name')
        if intent == "ask_cdc_events" or not year:
            message = "Here are the CDC events available for different years:\n"
            for year, link in college_data["events"].items():
                message += f"- {year}: {link}\n"
            dispatcher.utter_message(text=message)
            return [SlotSet("year", None)]  # Reset the year slot
        else:
            event_link = college_data["events"].get(year)
            if event_link:
                dispatcher.utter_message(text=f"The CDC events for {year} can be found here: {event_link}")
            else:
                dispatcher.utter_message(text=f"I'm sorry, but I couldn't find the CDC events for the year {year}.")
        return []


class ActionShowCDCContact(Action):
    def name(self) -> Text:
        return "action_show_cdc_contact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not college_data or "contact" not in college_data:
            dispatcher.utter_message(text="I'm sorry, but I couldn't retrieve the CDC contact information.")
            return []

        contact = college_data["contact"]
        message = f"CDC Contact Information:\n"
        message += f"Name: {contact['name']}\n"
        message += f"Designation: {contact['designation']}\n"
        message += f"Email: {contact['email']}\n"
        message += f"Phone: {contact['phone']}"
        
        dispatcher.utter_message(text=message)
        return []