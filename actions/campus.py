import json
from typing import Text, Dict, List, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Declare the campus.json file globally
with open('dataset/campus.json', 'r', encoding='utf-8') as file:
    campus_data = json.load(file)

class ActionCampusInfo(Action):
    def name(self) -> Text:
        return "action_campus_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Access the first element of campus_data (assuming it's a list)
        campus_info = campus_data[0]  # Access the first dictionary in the list
        
        description = campus_info["description"]
        initiatives = campus_info["initiatives"]
        
        # Prepare the response message
        initiatives_list = ", ".join(initiatives)
        response = (
            f"Welcome to CBIT! Here's some information about our campus:\n\n"
            f"{description}\n\n"
            f"Our initiatives include: {initiatives_list}."
        )
        
        dispatcher.utter_message(text=response)
        return []


class ActionChaitanyaSudheeInfo(Action):
    def name(self) -> Text:
        return "action_chaitanya_sudhee_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Access Chaitanya Sudhee data from campus_data
        chaitanya_sudhee = campus_data[1]["chaitanya_sudhee"]  # Second element contains Chaitanya Sudhee info
        
        description = chaitanya_sudhee["description"]
        clubs_and_cells = chaitanya_sudhee["clubs_and_cells"]
        
        # Prepare clubs list for response in bullet-point format
        clubs_list = "\n".join([f"- {club['name']}" for club in clubs_and_cells])
        
        response = (
            f"{description}\n\n"
            f"The clubs and cells under Chaitanya Sudhee include:\n{clubs_list}"
        )
        
        dispatcher.utter_message(text=response)
        return []
    

class ActionChaitanyaSaahithiInfo(Action):
    def name(self) -> Text:
        return "action_chaitanya_saahithi_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Access Chaitanya Saahithi data from campus_data
        chaitanya_saahithi = campus_data[2]["chaitanya_saahithi"]  # Assuming this is the correct index
        
        description = chaitanya_saahithi["description"]
        clubs_and_activities = chaitanya_saahithi["clubs_and_activities"]
        
        # Prepare clubs list for response in bullet-point format
        clubs_list = "\n".join([f"- {club['name']}" for club in clubs_and_activities])
        
        response = (
            f"{description}\n\n"
            f"The clubs and activities under Chaitanya Saahithi include:\n{clubs_list}"
        )
        
        dispatcher.utter_message(text=response)
        return []
    
    
class ActionChaitanyaSamskruthiInfo(Action):
    def name(self) -> Text:
        return "action_chaitanya_samskruthi_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Access Chaitanya Samskruthi data from campus_data
        chaitanya_samskruthi = campus_data[3]["chaitanya_samskruthi"]  # Assuming this is the correct index
        
        description = chaitanya_samskruthi["description"]
        clubs = chaitanya_samskruthi["clubs"]
        
        # Prepare clubs list for response in bullet-point format with descriptions
        clubs_list = "\n".join([f"- {club['name']}: {club['description']}" for club in clubs])
        
        response = (
            f"{description}\n\n"
            f"The clubs under Chaitanya Samskruthi include:\n{clubs_list}"
        )
        
        dispatcher.utter_message(text=response)
        return []
    

class ActionChaitanyaKreedaInfo(Action):
    def name(self) -> Text:
        return "action_chaitanya_kreeda_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Access Chaitanya Kreeda data from campus_data
        chaitanya_kreeda = campus_data[4]["chaitanya_kreeda"]  # Assuming this is the correct index
        
        description = chaitanya_kreeda["description"]
        achievements = chaitanya_kreeda["achievements"]
        facilities = chaitanya_kreeda["facilities"]
        
        response = (
            f"{description}\n\n"
            f"Achievements:\n{achievements}\n\n"
            f"Facilities:\n{facilities}"
        )
        
        dispatcher.utter_message(text=response)
        return []


class ActionPhysicalEducationInfo(Action):
    def name(self) -> Text:
        return "action_physical_education_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Access Physical Education data from campus_data
        physical_education = campus_data[5]["Physical Education"]  # Assuming this is the correct index
        
        description = physical_education["description"]
        infrastructure = physical_education["infrastructure"]
        
        # Prepare infrastructure details in bullet-point format
        infrastructure_details = "\n".join([f"- {key.replace('_', ' ').capitalize()}: {value}" 
                                            for key, value in infrastructure.items()])
        
        response = (
            f"{description}\n\n"
            f"Infrastructure details:\n{infrastructure_details}"
        )
        
        dispatcher.utter_message(text=response)
        return []
    

class ActionChaitanyaSevaInfo(Action):
    def name(self) -> Text:
        return "action_chaitanya_seva_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Access Chaitanya Seva data from campus_data
        chaitanya_seva = campus_data[6]["chaitanya_seva"]  # Assuming this is the correct index
        
        description = chaitanya_seva["description"]
        clubs = chaitanya_seva["clubs"]
        
        # Prepare clubs list for response in bullet-point format with descriptions
        clubs_list = "\n".join([f"- {club['name']}: {club['description']}" for club in clubs])
        
        response = (
            f"{description}\n\n"
            f"The clubs under Chaitanya Seva include:\n{clubs_list}"
        )
        
        dispatcher.utter_message(text=response)
        return []

class ActionChaitanyaChaayaInfo(Action):
    def name(self) -> Text:
        return "action_chaitanya_chaaya_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Access Chaitanya Chaaya data from campus_data
        chaitanya_chaaya = campus_data[7]["chaitanya_chaaya"]  # Assuming this is the correct index
        
        description = chaitanya_chaaya["description"]
        clubs = chaitanya_chaaya["clubs"]
        
        # Prepare clubs list for response in bullet-point format with descriptions
        clubs_list = "\n".join([f"- {club['name']}: {club['description']}" for club in clubs])
        
        response = (
            f"{description}\n\n"
            f"The clubs under Chaitanya Chaaya include:\n{clubs_list}"
        )
        
        dispatcher.utter_message(text=response)
        return []
    

class ActionChaitanyaSmritiInfo(Action):
    def name(self) -> Text:
        return "action_chaitanya_smriti_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Access Chaitanya Smriti data from campus_data
        chaitanya_smriti = campus_data[8]["chaitanya_smriti"]  # Assuming this is the correct index
        
        description = chaitanya_smriti["description"]
        clubs = chaitanya_smriti["clubs"]
        
        # Prepare clubs list for response in bullet-point format with descriptions
        clubs_list = "\n".join([f"- {club['name']}: {club['description']}" for club in clubs])
        
        response = (
            f"{description}\n\n"
            f"The clubs under Chaitanya Smriti include:\n{clubs_list}"
        )
        
        dispatcher.utter_message(text=response)
        return []


class ActionStudentsClubsInfo(Action):
    def name(self) -> Text:
        return "action_students_clubs_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Access Students Clubs data from campus_data
        students_clubs = campus_data[9]["students_clubs"]
        description = students_clubs["description"]
        registrations = students_clubs["registrations"]
        extra_curricular_activities = students_clubs["extra_curricular_activities"]
        co_curricular_activities = students_clubs["co_curricular_activities"]["technical_clubs"]
        professional_bodies = students_clubs["students_chapters"]["professional_bodies"]

        # Extract user intent from tracker
        user_intent = tracker.latest_message['intent'].get('name')

        # Prepare responses based on user intent
        if user_intent == "ask_department_clubs":
            # Format department clubs response
            department_clubs_response = "\n".join([
                f"- {club['department']}:\n  {', '.join(club['clubs'])}"
                for club in co_curricular_activities
            ])
            response = f"The department-specific technical clubs are:\n\n{department_clubs_response}"

        elif user_intent == "ask_professional_bodies":
            # Format professional bodies response
            professional_bodies_response = "\n".join([f"- {body}" for body in professional_bodies])
            response = f"The professional bodies available for students are:\n\n{professional_bodies_response}"

        else:
            # General response for students' clubs
            extra_curricular_response = "\n".join([
                f"- {activity['name']}: {activity['description']}"
                for activity in extra_curricular_activities
            ])
            response = (
                f"{description}\n\n"
                f"Registrations:\n- Students: {registrations['students']}\n- Staff: {registrations['staff']}\n\n"
                f"Extra-Curricular Activities:\n{extra_curricular_response}\n\n"
                f"To know more about department-specific clubs or professional bodies, ask specifically!"
            )

        dispatcher.utter_message(text=response)
        return []
    

class ActionAntiRaggingInfo(Action):
    def name(self) -> Text:
        return "action_anti_ragging_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Access Anti-Ragging Information data from campus_data
        anti_ragging_info = campus_data[10]
        title = anti_ragging_info["title"]
        academic_year = anti_ragging_info["academic_year"]
        committees = anti_ragging_info["committees"]

        # Extract user intent from tracker
        user_intent = tracker.latest_message['intent'].get('name')

        # Prepare responses based on user intent
        if user_intent == "ask_anti_ragging_committee":
            committee = next(c for c in committees if c["name"] == "Anti-Ragging Committee")
            response = f"{committee['name']}:\n{committee['description']}"

        elif user_intent == "ask_anti_ragging_squad":
            squad = next(c for c in committees if c["name"] == "Anti-Ragging Squad")
            response = f"{squad['name']}:\n{squad['description']}"

        elif user_intent == "ask_anti_ragging_duties":
            duties = next(c for c in committees if c["name"] == "Anti-Ragging Duties")
            response = f"{duties['name']}:\n{duties['description']}"

        elif user_intent == "ask_anti_ragging_cell":
            cell = next(c for c in committees if c["name"] == "Anti-Ragging Cell (Help Desk)")
            contacts_list = "\n".join([
                f"- {contact['name']}, {contact.get('designation', 'N/A')}, Mobile: {contact['mobile']}"
                for contact in cell["contacts"]
            ])
            response = f"{cell['name']}:\n{cell['description']}\n\nContacts:\n{contacts_list}"

        elif user_intent == "ask_disciplinary_committee":
            disciplinary_committee = next(c for c in committees if c["name"] == "Disciplinary Committee")
            members_list = "\n".join([f"- {member}" for member in disciplinary_committee["members"]])
            response = f"{disciplinary_committee['name']}:\n{disciplinary_committee['description']}\n\nMembers:\n{members_list}"

        else:
            # General response for Anti-Ragging Information
            committees_list = "\n".join([f"- {committee['name']}: {committee['description']}" for committee in committees])
            response = (
                f"{title} ({academic_year}):\n\n"
                f"Committees:\n{committees_list}\n\n"
                f"To know more about specific committees, ask specifically!"
            )

        dispatcher.utter_message(text=response)
        return []
