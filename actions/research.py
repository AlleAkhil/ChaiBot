import json
import re
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from datetime import datetime

# Declare the file globally
with open('dataset/research.json', 'r', encoding='utf-8') as file:
    research_data = json.load(file)

class ActionResearchInfo(Action):
    def name(self) -> Text:
        return "action_research_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        info = research_data["about"]
        dispatcher.utter_message(text=f"Here's information about our research facilities: {info}")
        return []

class ActionCollegeVision(Action):
    def name(self) -> Text:
        return "action_research_vision"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        vision = research_data["vision"]
        dispatcher.utter_message(text=f"Our college's R&D center vision is: {vision}")
        return []

class ActionCollegeMission(Action):
    def name(self) -> Text:
        return "action_research_mission"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        mission = research_data["mission"]
        dispatcher.utter_message(text=f"Our college's R&D center mission is: {mission}")
        return []
    
class ActionRAndETeamInfo(Action):
    def name(self) -> Text:
        return "action_r_and_e_team_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        team_info = research_data["r&e_team"]
        
        response = "Here's the R&E team information:\n\n"
        for member in team_info:
            response += f"Name: {member['Name_of_the_Staff']}\n"
            response += f"Designation: {member['Designation']}\n"
            if member['Email_ID']:
                response += f"Email: {member['Email_ID']}\n"
            response += "\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionAllDepartmentalCoordinators(Action):
    def name(self) -> Text:
        return "action_all_departmental_coordinators"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        coordinators_info = research_data["departmental_research_coordinators"]
        response = "Here are the departmental research coordinators:\n\n"
        
        for dept in coordinators_info:
            response += f"## {dept['department']} Department\n"
            for coordinator in dept["coordinators"]:
                response += f"- {coordinator['name']} ({coordinator['designation']})\n"
            response += "\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionSpecificDepartmentCoordinator(Action):
    def name(self) -> Text:
        return "action_specific_department_coordinator"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        department = tracker.get_slot("department")
        coordinators_info = research_data["departmental_research_coordinators"]
        
        if department:
            department = department.lower()
            for dept in coordinators_info:
                if dept["department"].lower() == department:
                    response = f"Research coordinators for {dept['department']} department:\n\n"
                    for coordinator in dept["coordinators"]:
                        response += f"Name: {coordinator['name']}\n"
                        response += f"Designation: {coordinator['designation']}\n"
                        response += f"Email: {coordinator['email']}\n\n"
                    dispatcher.utter_message(text=response)
                    return []
            
            dispatcher.utter_message(text=f"Sorry, I couldn't find information for the {department} department.")
        else:
            dispatcher.utter_message(text="Please specify a department to get coordinator information.")
        
        return []


class ActionResearchInfrastructure(Action):
    def name(self) -> Text:
        return "action_research_infrastructure"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        infrastructure = research_data["Infrastructure"]
        description = infrastructure["description"]
        features = "\n".join(f"- {feature}" for feature in infrastructure["features"])
        response = f"{description}\n\nKey Features:\n{features}"
        
        dispatcher.utter_message(text=response)
        return []

class ActionResearchInfrastructureImages(Action):
    def name(self) -> Text:
        return "action_research_infrastructure_images"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        image_links = research_data["Infrastructure"]["image_links"]
        response = "Here are some images of the R&E Hub infrastructure:\n\n"
        response += "\n".join(image_links)
        
        dispatcher.utter_message(text=response)
        return []


class ActionGetFundedInfo(Action):
    def name(self) -> Text:
        return "action_get_funded_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        funded_url = research_data.get("Funded", None)
        if funded_url:
            response = (
                "CBIT encourages both undergraduate and postgraduate students to carry out quality and application-oriented projects. "
                "Funding up to Rs. 10,000/- can be sanctioned, and in exceptional cases, higher funding can also be considered.\n\n"
                "For detailed guidelines on applying for funding, please refer to the document at the following link:\n"
                f"{funded_url}"
            )
        else:
            response = "Sorry, I couldn't find information about the 'Get Funded' program."
        
        dispatcher.utter_message(text=response)
        return []
    

class ActionResearchPolicies(Action):
    def name(self) -> Text:
        return "action_research_policies"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        policies = research_data.get("policies", [])
        response = "Here are the research policies available at CBIT:\n\n"
        
        for policy in policies:
            response += f"**{policy['policy_name']}**\n"
            response += f"{policy['description']}\n"
            response += f"More details: {policy['url']}\n\n"
        
        dispatcher.utter_message(text=response)
        return []

class ActionSpecificResearchPolicy(Action):
    def name(self) -> Text:
        return "action_specific_research_policy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        policy_name = tracker.get_slot("policy_name")
        policies = research_data.get("policies", [])
        
        if policy_name:
            for policy in policies:
                if policy_name.lower() in policy["policy_name"].lower():
                    response = f"Here is the information about the {policy['policy_name']}:\n\n"
                    response += f"{policy['description']}\n"
                    response += f"More details: {policy['url']}\n"
                    dispatcher.utter_message(text=response)
                    return []
            
            dispatcher.utter_message(text=f"Sorry, I couldn't find details about the '{policy_name}' policy.")
        else:
            dispatcher.utter_message(text="Please specify the name of the policy you want to know about.")
        
        return []


class ActionSpecificResearchCommittee(Action):
    def name(self) -> Text:
        return "action_specific_research_committee"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        department = tracker.get_slot("department")
        committees = research_data["Research Committees"]["committees"]
        
        if department:
            for committee in committees:
                if committee["committee_name"] == "Departmental Research Committees":
                    for dept in committee["departments"]:
                        if department.lower() == dept["department"].lower():
                            response = f"Here is the Departmental Research Committee for {dept['department']}:\n"
                            response += f"Details: {dept['url']}\n"
                            dispatcher.utter_message(text=response)
                            return [SlotSet("department", None)]  # Clear the slot after responding
            
            dispatcher.utter_message(text=f"Sorry, I couldn't find information for the {department} department.")
        else:
            dispatcher.utter_message(text="Please specify which department's research committee you'd like to know about.")
        
        return [SlotSet("department", None)]  # Clear the slot to avoid stale data

class ActionResearchCommittees(Action):
    def name(self) -> Text:
        return "action_research_committees"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        committees = research_data["Research Committees"]["committees"]
        response = "Here are the research committees at CBIT:\n\n"
        
        for committee in committees:
            response += f"**{committee['committee_name']}**\n"
            if "url" in committee:
                response += f"Details: {committee['url']}\n\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionResearchDayDetails(Action):
    def name(self) -> Text:
        return "action_research_day_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extract year from user's message
        user_message = tracker.latest_message.get('text', '')
        year_match = re.search(r'\b(20\d{2})\b', user_message)
        year = year_match.group(1) if year_match else None

        research_day_data = research_data.get("research_day", {})

        if year:
            # Find the matching key in research_day_data
            matching_key = next((key for key in research_day_data if year in key), None)
            
            if matching_key:
                response = f"Here are the details for Research Day {matching_key}:\n\n"
                if research_day_data[matching_key]:
                    response += research_day_data[matching_key]
                else:
                    response += f"Details for Research Day {matching_key} are currently unavailable."
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find details for Research Day {year}.")
        else:
            response = "Here are the available Research Day events:\n\n"
            for event_year in research_day_data:
                response += f"- {event_year}\n"
            response += "\nPlease specify a year to get more details."
            dispatcher.utter_message(text=response)

        return []
    

class ActionInnovationPolicy(Action):
    def name(self) -> Text:
        return "action_innovation_policy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        policy_data = research_data.get("Innovation_and_Incubation", {}).get("Policy", {})
        
        if policy_data:
            response = "Here are the details of the Innovation and Incubation Policy:\n\n"
            response += f"Document URL: {policy_data['document_url']}\n\n"
            response += "Key Points:\n"
            response += "\n".join(f"- {point}" for point in policy_data["key_points"])
            response += "\n\nObjectives:\n"
            response += "\n".join(f"- {objective}" for objective in policy_data["objectives"])
        else:
            response = "Sorry, I couldn't retrieve the Innovation and Incubation Policy details."
        
        dispatcher.utter_message(text=response)
        return []

class ActionInnovationActivities(Action):
    def name(self) -> Text:
        return "action_innovation_activities"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        activities_data = research_data.get("Innovation_and_Incubation", {}).get("Activities", {})
        
        if activities_data:
            response = "Here are the details of the Innovation and Incubation Activities:\n\n"
            response += f"Document URL: {activities_data['document_url']}\n\n"
            response += "Key Initiatives:\n"
            response += "\n".join(f"- {initiative}" for initiative in activities_data["key_initiatives"])
            response += "\n\nAchievements:\n"
            response += "\n".join(f"- {achievement}" for achievement in activities_data["achievements"])
            
            startups = activities_data.get("startups", {})
            if startups:
                response += "\n\nStartups:\n"
                response += f"Total Mentored: {startups['total_mentored']}\n"
                response += "Focus Areas:\n"
                response += "\n".join(f"- {area}" for area in startups["focus_areas"])
        else:
            response = "Sorry, I couldn't retrieve the Innovation and Incubation Activities details."
        
        dispatcher.utter_message(text=response)
        return []


class ActionIPRPolicy(Action):
    def name(self) -> Text:
        return "action_ipr_policy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ipr_policy = research_data.get("IPR", {}).get("Policy", {})
        
        if ipr_policy:
            response = "Here are the details of the IPR Policy:\n\n"
            response += f"Description: {ipr_policy['description']}\n"
            response += f"Document URL: {ipr_policy['url']}"
        else:
            response = "Sorry, I couldn't retrieve the IPR Policy details."
        
        dispatcher.utter_message(text=response)
        return []

class ActionIPRPatents(Action):
    def name(self) -> Text:
        return "action_ipr_patents"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ipr_patents = research_data.get("IPR", {}).get("Patents", {})
        
        if ipr_patents:
            response = "Here are the details of Patents related to IPR:\n\n"
            response += f"Document URL: {ipr_patents['url']}"
        else:
            response = "Sorry, I couldn't retrieve the Patents details."
        
        dispatcher.utter_message(text=response)
        return []

class ActionIPRCopyrights(Action):
    def name(self) -> Text:
        return "action_ipr_copyrights"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ipr_copyrights = research_data.get("IPR", {}).get("Copyrights", {})
        
        if ipr_copyrights:
            response = "Here are the details of Copyrights related to IPR:\n\n"
            response += f"Description: {ipr_copyrights['description']}\n"
            response += f"Document URL: {ipr_copyrights['url']}"
        else:
            response = "Sorry, I couldn't retrieve the Copyrights details."
        
        dispatcher.utter_message(text=response)
        return []