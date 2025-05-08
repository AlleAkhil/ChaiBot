from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
import re
from rasa_sdk.events import EventType

# Load the JSON data
with open('dataset/about.json', 'r', encoding='utf-8') as file:
    college_data = json.load(file)

# Global abbreviation map
abbreviation_map = {
    "cse": "Computer Science and Engineering",
    "it": "Information Technology",
    "ece": "Electronics and Communications Engineering",
    "eee": "Electrical and Electronics Engineering",
    "mech": "Mechanical Engineering",
    "civil": "Civil Engineering",
    "aiml": "Artificial Intelligence and Machine Learning",
    "aids": "Artificial Intelligence and Data Science",
    "iot": "Computer Engineering and Technology (IOT, CS & BCT)",
    "cs": "Computer Engineering and Technology (IOT, CS & BCT)",
    "bct": "Computer Engineering and Technology (IOT, CS & BCT)",
    "biotech": "Biotechnology",
    "sms": "School of Management Studies",
    "mca": "Computer Applications",
    "management": "School of Management Studies",
    "physics": "Physics",
    "chemistry": "Chemistry",
    "maths": "Mathematics",
    "english": "English",
    "library": "Library and Information Center",
    "sports": "Physical Education"
}


class ActionCollegeInfo(Action):
    def name(self) -> Text:
        return "action_college_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        info = college_data["about"]
        dispatcher.utter_message(text=f"Here's some information about our college: {info}")
        return []

class ActionCollegeVision(Action):
    def name(self) -> Text:
        return "action_college_vision"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        vision = college_data["clg_vision"]
        dispatcher.utter_message(text=f"Our college's vision is: {vision}")
        return []

class ActionCollegeMission(Action):
    def name(self) -> Text:
        return "action_college_mission"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        mission = college_data["clg_mission"]
        dispatcher.utter_message(text=f"Our college's mission is: {mission}")
        return []

class ActionCollegeRecognitions(Action):
    def name(self) -> Text:
        return "action_college_recognitions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        recognitions = college_data["clg_recognitions"]
        response = "Our college has received the following recognitions:\n"
        for recognition in recognitions:
            response += f"- {recognition['type']} from {recognition['organization']}: {recognition['details']}\n"
        dispatcher.utter_message(text=response)
        return []

class ActionCollegeAtAGlance(Action):
    def name(self) -> Text:
        return "action_college_at_a_glance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        glance = college_data["clg_at_a_glance"]
        response = "Here's a quick glance at our college:\n"
        for category, items in glance.items():
            response += f"\n{category.replace('_', ' ').title()}:\n"
            for item in items:
                response += f"- {item}\n"
        dispatcher.utter_message(text=response)
        return []

class ActionCollegeManagement(Action):
    def name(self) -> Text:
        return "action_college_management"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the latest user message
        user_message = tracker.latest_message['text'].lower()
        
        # Get the management data
        management = college_data["clg_board_of_management"]
        
        # Check if the user is asking for a specific position
        for position, name in management.items():
            if position.lower() in user_message:
                response = f"The {position} in college board of management is {name}."
                dispatcher.utter_message(text=response)
                return []
        
        # If no specific position is found, return all management information
        response = "Our college's Board of Management:\n"
        for position, name in management.items():
            response += f"{position}: {name}\n"
        dispatcher.utter_message(text=response)
        return []


class ActionPresidentMessage(Action):
    def name(self) -> Text:
        return "action_president_message"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = college_data["president_message"]
        dispatcher.utter_message(text=f"Message from our President: {message}")
        return []

class ActionPrincipalMessage(Action):
    def name(self) -> Text:
        return "action_principal_message"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = college_data["principle_message"]
        dispatcher.utter_message(text=f"Message from our Principal: {message}")
        return []

class ActionDirectors(Action):
    def name(self) -> Text:
        return "action_directors"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Fetch directors data from the imported JSON file
        directors = college_data["directors"]

        # Generate a response listing all directors
        response = "Our college directors:\n"
        for position, name in directors.items():
            response += f"{position}: {name}\n"
        
        # Send the response
        dispatcher.utter_message(text=response)
        return []

class ActionFetchSpecificDirector(Action):
    def name(self) -> Text:
        return "action_specific_director"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the latest user message
        user_message = tracker.latest_message['text'].lower()

        # Fetch directors data from the imported JSON file
        directors = college_data["directors"]

        # Tokenize user message into words
        user_tokens = set(user_message.split())

        # Create a list to store potential matches with scores
        matches = []

        for position, name in directors.items():
            # Tokenize the position title
            position_tokens = set(position.lower().split())

            # Calculate the intersection of tokens (common words)
            common_tokens = user_tokens & position_tokens

            # Score based on the number of common tokens
            score = len(common_tokens)

            if score > 0:
                matches.append((position, name, score))

        # Sort matches by score in descending order (highest match first)
        matches.sort(key=lambda x: x[2], reverse=True)

        if matches:
            # Pick the best match (highest score)
            best_match_position, best_match_name, _ = matches[0]
            response = f"The {best_match_position} of our college is {best_match_name}."
            dispatcher.utter_message(text=response)
        else:
            # No match found
            dispatcher.utter_message(text="Sorry, I couldn't find the director you're looking for.")

        return []

class ActionShowCourses(Action):
    def name(self) -> Text:
        return "action_show_courses"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not college_data or "courses" not in college_data:
            dispatcher.utter_message(text="I'm sorry, but I couldn't retrieve the courses data.")
            return []

        courses = college_data["courses"]
        message = "Here are the available courses and departments:\n"
        for course in courses:
            message += f"- {course}\n"
        
        dispatcher.utter_message(text=message)
        return []

class ActionListAllHODs(Action):
    def name(self) -> Text:
        return "action_list_all_hods"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Load HODs data
        hods = college_data["hods"]

        # Generate the response
        response = "Here is the list of all Heads of Departments (HODs):\n\n"
        for department_name, hod_name in hods.items():
            response += f"• {department_name}: {hod_name}\n"

        # Send the response to the user
        dispatcher.utter_message(text=response)
        return []

# class ActionHODs(Action):
#     def name(self) -> Text:
#         return "action_hods"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         # Extract user query
#         user_query = tracker.latest_message['text'].lower()

#         # Load HODs data from JSON
#         hods = college_data["hods"]

#         # Normalize user query by replacing abbreviations with full forms
#         normalized_query = user_query
#         for abbr, full_form in abbreviation_map.items():
#             if abbr in normalized_query:
#                 normalized_query = normalized_query.replace(abbr, full_form)

#         # Preprocess department names to create a tokenized mapping
#         department_tokens = {}
#         for department_name in hods.keys():
#             # Normalize department names by removing unnecessary prefixes and splitting into tokens
#             normalized_name = re.sub(r"department of\s*", "", department_name.lower())
#             tokens = set(normalized_name.split())  # Tokenize into words
#             department_tokens[department_name] = tokens

#         # Tokenize the normalized query
#         user_tokens = set(normalized_query.split())

#         # Match user tokens with department tokens
#         best_match = None
#         best_score = 0

#         for department_name, tokens in department_tokens.items():
#             # Calculate the Jaccard similarity between user tokens and department tokens
#             intersection = len(user_tokens & tokens)
#             union = len(user_tokens | tokens)
#             score = intersection / union if union > 0 else 0

#             if score > best_score:
#                 best_match = department_name
#                 best_score = score

#         # If a match is found with sufficient similarity, return the result
#         if best_match and best_score > 0.3:  # Adjust this threshold as needed
#             hod_name = hods[best_match]
#             response = f"The Head of {best_match} is {hod_name}."
#             dispatcher.utter_message(text=response)
#         else:
#             # If no match is found, provide a fallback response
#             response = (
#                 f"Sorry, I couldn't find information about that department. Here are all the Heads of Departments:\n\n"
#                 + "\n".join([f"• {dept}: {hod}" for dept, hod in hods.items()])
#             )
#             dispatcher.utter_message(text=response)

#         return []

import logging
# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ActionHODDetails(Action):
    def name(self) -> Text:
        return "action_hods"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Extract department shortcut or name from user query
            department = tracker.get_slot("department")
            logger.debug(f"Extracted department slot: {department}")

            # Check if department slot is None
            if department is None:
                logger.warning("Department slot is None.")
                dispatcher.utter_message(text="Sorry, I couldn't understand the department name. Please specify it again.")
                return []

            # Convert department to lowercase and check in abbreviation map
            department_lower = department.lower()
            logger.debug(f"Converted department to lowercase: {department_lower}")

            if department_lower in abbreviation_map:
                full_department_name = abbreviation_map[department_lower]
                logger.debug(f"Mapped shortcut to full department name: {full_department_name}")
            else:
                full_department_name = department
                logger.debug(f"No mapping found for shortcut. Using full name: {full_department_name}")

            # Prepend "Department of" to match JSON keys
            formatted_department_name = f"Department of {full_department_name}"
            logger.debug(f"Formatted department name for matching: {formatted_department_name}")

            # Fetch HOD details from JSON data
            hods = college_data["hods"]
            logger.debug(f"HODs data loaded: {hods}")

            if formatted_department_name in hods:
                dispatcher.utter_message(text=f"The HOD for {formatted_department_name} is {hods[formatted_department_name]}.")
                logger.info(f"Successfully found HOD for {formatted_department_name}.")
            else:
                dispatcher.utter_message(text=f"Sorry, I couldn't find information for the department '{department}'.")
                logger.warning(f"HOD not found for department: {department}")
            
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            dispatcher.utter_message(text="An error occurred while processing your request. Please try again later.")
        
        return []

class ActionFaculty(Action):

    def name(self) -> str:
        return "action_faculty"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Dict[Text, Any],
            domain: Dict[Text, Any]) -> List[EventType]:

        # Get the user query
        user_query = tracker.latest_message.get('text', '').lower()

        # Tokenize the query into words
        tokens = user_query.split()

        # Extract department, staff type, and position from the query
        department = None
        staff_type = None
        position = None

        # Search for department abbreviation or full name in query
        for token in tokens:
            if token in abbreviation_map:
                department = abbreviation_map[token]
                break

        # Search for specific positions in query (e.g., "associate professors", "professors")
        if 'associate professors' in user_query:
            position = 'associate_professors'
        elif 'assistant professors' in user_query:
            position = 'assistant_professors'
        elif 'professors' in user_query:  # Check for "professors" last to avoid substring conflicts
            position = 'professors'

        # Search for staff type keywords in query
        if 'non teaching staff' in user_query or 'non-teaching staff' in user_query or 'nonteaching staff' in user_query:
            staff_type = 'non_teaching_staff'
        elif 'teaching staff' in user_query or position:  # Teaching staff includes positions like "professors"
            staff_type = 'teaching_staff'
        elif 'staff' in user_query:  # If only "staff" is mentioned
            staff_type = 'all'

        # Handle cases where department or staff type is not found
        if not department:
            dispatcher.utter_message(text="I couldn't identify the department. Please specify it clearly.")
            return []
        
        # Iterate through all departments under 'faculty'
        for dept_data in college_data.get('faculty', []):  # faculty is now a list
            if dept_data.get('department', '').lower() == department.lower():
                # Match found, retrieve data based on the requested staff type or position
                branch_name = dept_data.get('department', 'Unknown Branch')

                if position:  # If a specific position is requested (e.g., "associate professors")
                    teaching_staff = dept_data.get('teaching_staff', {})
                    specific_position_data = teaching_staff.get(position, [])
                    if specific_position_data:
                        response = f"Branch: {branch_name}\n\n"
                        response += self.format_position_details(specific_position_data, position)
                        dispatcher.utter_message(text=response)
                    else:
                        dispatcher.utter_message(text=f"No data found for {position.replace('_', ' ')} in {branch_name}.")
                elif staff_type == 'teaching_staff':
                    teaching_staff = dept_data.get('teaching_staff', {})
                    if teaching_staff:
                        response = f"Branch: {branch_name}\n\n"
                        response += self.format_staff_details(teaching_staff, 'teaching_staff')
                        dispatcher.utter_message(text=response)
                    else:
                        dispatcher.utter_message(text=f"No teaching staff data found for {branch_name}.")
                elif staff_type == 'non_teaching_staff':
                    non_teaching_staff = dept_data.get('non_teaching_staff', [])
                    if non_teaching_staff:
                        response = f"Branch: {branch_name}\n\n"
                        response += self.format_staff_details(non_teaching_staff, 'non_teaching_staff')
                        dispatcher.utter_message(text=response)
                    else:
                        dispatcher.utter_message(text=f"No non-teaching staff data found for {branch_name}.")
                elif staff_type == 'all':  # Both teaching and non-teaching staff requested
                    response = f"Branch: {branch_name}\n\n"
                    
                    teaching_staff = dept_data.get('teaching_staff', {})
                    if teaching_staff:
                        response += self.format_staff_details(teaching_staff, 'teaching_staff') + "\n\n"
                    else:
                        response += f"No teaching staff data found for {branch_name}.\n\n"
                    
                    non_teaching_staff = dept_data.get('non_teaching_staff', [])
                    if non_teaching_staff:
                        response += self.format_staff_details(non_teaching_staff, 'non_teaching_staff')
                    else:
                        response += f"No non-teaching staff data found for {branch_name}."

                    dispatcher.utter_message(text=response)

                return []

        # If no matching department is found
        dispatcher.utter_message(text=f"No data found for the {department} department.")
        return []

    def format_position_details(self, position_data: List[Dict], position: str) -> str:
        """Format the details of a specific position."""
        response = f"Here are the details of {position.replace('_', ' ').capitalize()}:\n\n"
        
        for member in position_data:
            name = member.get('name', 'N/A')
            position_title = member.get('position', '')
            details = f"- {name}"
            if position_title:
                details += f", Position: {position_title}"
            response += details + "\n"

        return response.strip()

    def format_staff_details(self, staff_data: Any, staff_type: str) -> str:
        """Format the details of teaching or non-teaching staff."""
        response = f"Here are the details of {staff_type.replace('_', ' ')}:\n\n"

        if staff_type == 'teaching_staff':
            for category, members in staff_data.items():
                response += f"{category.capitalize()}:\n"
                for member in members:
                    name = member.get('name', 'N/A')
                    position = member.get('position', '')
                    details = f"- {name}"
                    if position:
                        details += f", Position: {position}"
                    response += details + "\n"
                response += "\n"
        
        elif staff_type == 'non_teaching_staff':
            for member in staff_data:
                name = member.get('name', 'N/A')
                position = member.get('position', '')
                email = member.get('email', '')
                details = f"- {name}"
                if position:
                    details += f", Position: {position}"
                if email:
                    details += f", Email: {email}"
                response += details + "\n"

        return response.strip()



class ActionGetAECInfo(Action):
    def name(self) -> Text:
        return "action_get_aec_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        aec_info = college_data['aec_and_coe']['AEC_Management_Team']
        response = "AEC (Academic Excellence Center) Management Team:\n\n"
        
        for member in aec_info:
            response += f"Name: {member['name']}\n"
            response += f"Designation: {member['designation']}\n"
            response += f"Email: {member['email']}\n\n"
        
        dispatcher.utter_message(text=response)
        return []

class ActionGetCOEInfo(Action):
    def name(self) -> Text:
        return "action_get_coe_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        coe_info = college_data['aec_and_coe']['CoE_Management_Team']
        response = "COE (Controller of Examinations) Management Team:\n\n"
        
        for member in coe_info:
            response += f"Name: {member['name']}\n"
            response += f"Designation: {member['designation']}\n"
            response += f"Email: {member['email']}\n\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionHRTeam(Action):
    def name(self) -> Text:
        return "action_hr_team"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Dict[Text, Any],
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        hr_team = college_data.get("hr_team", [])
        if not hr_team:
            dispatcher.utter_message(text="No HR team data found.")
            return []

        response = "Here are the details of the HR Team:\n\n"
        for member in hr_team:
            name = member.get("name", "N/A")
            position = member.get("position", "N/A")
            email = member.get("email", "N/A")
            response += f"- Name: {name}, Position: {position}, Email: {email if email else 'N/A'}\n"

        dispatcher.utter_message(text=response.strip())
        return []


class ActionProjectOfficeTeam(Action):
    def name(self) -> Text:
        return "action_project_office_team"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Dict[Text, Any],
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        project_office_team = college_data.get("project_office_team", [])
        if not project_office_team:
            dispatcher.utter_message(text="No Project Office team data found.")
            return []

        response = "Here are the details of the Project Office Team:\n\n"
        for member in project_office_team:
            name = member.get("name", "N/A")
            designation = member.get("designation", "N/A")
            email = member.get("email", "N/A")
            response += f"- Name: {name}, Designation: {designation}, Email: {email if email else 'N/A'}\n"

        dispatcher.utter_message(text=response.strip())
        return []


class ActionAccountsOfficeStaff(Action):
    def name(self) -> Text:
        return "action_accounts_office_staff"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Dict[Text, Any],
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        acc_off_staff = college_data.get("acc_off_staff", [])
        if not acc_off_staff:
            dispatcher.utter_message(text="No Accounts Office staff data found.")
            return []

        response = f"Here are the details of the Accounts Office Staff:\n\n"
        for member in acc_off_staff:
            name = member.get("name", "")
            designation = member.get("designation", "")
            email = member.get("email", "")
            response += f"- Name: {name}, Designation: {designation}, Email: {email if email else 'N/A'}\n"

        dispatcher.utter_message(text=response.strip())
        return []


class ActionPurchaseOfficeTeam(Action):
    def name(self) -> Text:
        return "action_purchase_office_team"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Dict[Text, Any],
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        purchase_off_team = college_data.get("purchase_off_team", [])
        if not purchase_off_team:
            dispatcher.utter_message(text="No Purchase Office team data found.")
            return []

        response = "Here are the details of the Purchase Office Team:\n\n"
        for member in purchase_off_team:
            name = member.get("name", "N/A")
            designation = member.get("designation", "N/A")
            response += f"- Name: {name}, Designation: {designation}\n"

        dispatcher.utter_message(text=response.strip())
        return []


class ActionAlumniOfficeTeam(Action):
    def name(self) -> Text:
        return "action_alumni_office_team"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Dict[Text, Any],
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        alumni_off_team = college_data.get("alumni_off_team", [])
        if not alumni_off_team:
            dispatcher.utter_message(text="No Alumni Office team data found.")
            return []

        response = "Here are the details of the Alumni Office Team:\n\n"
        for member in alumni_off_team:
            name = member.get("name", "N/A")
            designation = member.get("designation", "N/A")
            response += f"- Name: {name}, Designation: {designation}\n"

        dispatcher.utter_message(text=response.strip())
        return []


class ActionAdvisoryBody(Action):
    def name(self) -> Text:
        return "action_advisory_body"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Dict[Text, Any],
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        advisory_body = college_data.get("advisory_body", [])
        if not advisory_body:
            dispatcher.utter_message(text="No Advisory Body data found.")
            return []

        response = "Here are the details of the Advisory Body:\n\n"
        for member in advisory_body:
            name = member.get("name", "N/A")
            department_and_institute = member.get("department_and_institute", "N/A")
            response += f"- Name: {name}, Department and Institute: {department_and_institute}\n"

        dispatcher.utter_message(text=response.strip())
        return []


class ActionGoverningBody(Action):
    def name(self) -> Text:
        return "action_governing_body"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Dict[Text, Any],
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        governing_body = college_data.get("governing_body", [])
        if not governing_body:
            dispatcher.utter_message(text="No Governing Body data found.")
            return []

        response = f"Here are the details of the Governing Body:\n\n"
        for member in governing_body:
            name = member.get("name", "")
            designation = member.get("designation", "")
            response += f"- Name: {name}, Designation: {designation}\n"

        dispatcher.utter_message(text=response.strip())
        return []


class ActionAcademicCouncilConstitution(Action):
    def name(self) -> Text:
        return "action_academic_council_constitution"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        constitution = college_data["academic_council_constitution"]
        
        response = f"The Academic Council Constitution is as follows:\n\n{constitution}"
        
        dispatcher.utter_message(text=response)
        return []

class ActionAcademicCouncilMembers(Action):
    def name(self) -> Text:
        return "action_academic_council_members"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        members = college_data["academic_council_mem"]
        
        response = "The Academic Council Members are:\n\n"
        response += f"Chairman: {members['chairman']['name']} ({members['chairman']['position']})\n\n"
        
        response += "Heads of Departments:\n"
        for head in members['heads_of_department']:
            response += f"- {head}\n"
        
        response += "\nTeachers from College:\n"
        for teacher in members['teachers_from_college']:
            response += f"- {teacher['name']}, {teacher['position']}\n"
        
        response += "\nExternal Experts:\n"
        for expert in members['external_experts']:
            response += f"- {expert['name']}, {expert['position']}\n"
        
        response += "\nUniversity Nominees:\n"
        for nominee in members['university_nominees']:
            response += f"- {nominee['name']}, {nominee['position']}\n"
        
        response += f"\nCII Member: {members['cii_member']['name']}, {members['cii_member']['position']}\n"
        response += f"Faculty Nominee: {members['faculty_nominee']['name']}, {members['faculty_nominee']['position']}"
        
        dispatcher.utter_message(text=response)
        return []

class ActionIQACInfo(Action):
    def name(self) -> Text:
        return "action_iqac_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        iqac_data = college_data["iqac"]
        
        response = "IQAC Information:\n\n"
        response += f"Introduction: {iqac_data['introduction']}\n\n"
        response += f"Vision: {iqac_data['vision']}\n\n"
        
        response += "Objectives:\n"
        for obj in iqac_data['objective']:
            response += f"- {obj}\n"
        
        response += "\nStrategies:\n"
        for strategy in iqac_data['strategies']:
            response += f"- {strategy}\n"
        
        response += "\nFunctions:\n"
        for function in iqac_data['functions']:
            response += f"- {function}\n"
        
        response += "\nBenefits:\n"
        for benefit in iqac_data['benefits']:
            response += f"- {benefit}\n"
        
        dispatcher.utter_message(text=response)
        return []


class ActionCollegeCommittees(Action):
    def name(self) -> Text:
        return "action_college_committees"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        committees = college_data["clg_committees"]
        
        response = "The college committees are:\n"
        for committee in committees:
            response += f"- {committee}\n"
        
        dispatcher.utter_message(text=response)
        return []

class ActionCollegeMOUs(Action):
    def name(self) -> Text:
        return "action_college_mous"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        mous = college_data["clg_mous"]
        
        response = "The college has MOUs with:\n"
        for mou in mous:
            response += f"- {mou}\n"
        
        dispatcher.utter_message(text=response)
        return []

class ActionShowCollegeContactInfo(Action):
    def name(self) -> Text:
        return "action_show_college_contact_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not college_data or "college_contact_info" not in college_data:
            dispatcher.utter_message(text="I'm sorry, but I couldn't retrieve the college contact information.")
            return []

        info = college_data["college_contact_info"]
        message = "College Contact Information:\n"
        message += f"Address: {info['address']}\n"
        message += f"PIN: {info['pin']}\n"
        message += f"Phone: {info['phone']}\n"
        message += f"Mobile: {info['mobile']}\n"
        message += f"Admissions Enquiry: {info['admissions_enquiry']}\n"
        message += f"Email: {info['email']}"
        
        dispatcher.utter_message(text=message)
        return []

class ActionShowSocialMediaLinks(Action):
    def name(self) -> Text:
        return "action_show_social_media_links"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not college_data or "social_media" not in college_data:
            dispatcher.utter_message(text="I'm sorry, but I couldn't retrieve the social media links.")
            return []

        social_media = college_data["social_media"]
        message = "College Social Media Links:\n"
        message += f"Facebook: {social_media['facebook']}\n"
        message += f"Instagram: {social_media['instagram']}\n"
        message += f"Twitter: {social_media['twitter']}\n"
        message += f"YouTube: {social_media['youtube']}"
        
        dispatcher.utter_message(text=message)
        return []