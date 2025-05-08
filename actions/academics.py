from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json

# Load the JSON data globally
with open('dataset/academics.json', 'r', encoding='utf-8') as file:
    college_data = json.load(file)

# Extract Civil Engineering department data
civil_data = next((dept for dept in college_data if dept['department'].lower() == "civil engineering"), None)

class ActionRetrieveCivilInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_civil_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        attributes = [
            "description", "programs offered", "vision", "mission",
            "objectives", "program specific outcomes", "program outcomes"
        ]

        attribute = next((attr for attr in attributes if attr in user_message), None)

        if civil_data:
            if attribute:
                if attribute == "description":
                    response = civil_data['description']
                elif attribute == "programs offered":
                    response = "\n".join(civil_data['programs_offered'])
                elif attribute == "vision":
                    response = civil_data['vision']
                elif attribute == "mission":
                    response = "\n".join(civil_data['mission'])
                elif attribute == "objectives":
                    response = "\n".join([f"{k}: {v}" for k, v in civil_data['objectives'].items()])
                elif attribute == "program specific outcomes":
                    response = "\n".join([f"{k}: {v}" for k, v in civil_data['program_specific_outcomes'].items()])
                elif attribute == "program outcomes":
                    response = "\n".join([f"{k}: {v}" for k, v in civil_data['program_outcomes'].items()])
                else:
                    response = f"I'm sorry, I don't have information about {attribute} for the Civil Engineering department."
            else:
                response = "What specific information would you like about the Civil Engineering department? You can ask about the description, programs offered, vision, mission, objectives, program specific outcomes, or program outcomes."
        else:
            response = "I'm sorry, I couldn't find information about the Civil Engineering department."

        dispatcher.utter_message(text=response)
        return []


# Extract Mechanical Engineering department data
mech_data = next((dept for dept in college_data if dept['department'].lower() == "mechanical engineering"), None)

class ActionRetrieveMechanicalInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_mechanical_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        # Check if the query is about mechanical engineering
        if "mech" not in user_message and "mechanical" not in user_message:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about Mechanical Engineering. Could you please rephrase your question?")
            return []

        attributes = [
            "description", "programs offered", "vision", "mission", "placements",
            "objectives", "program specific outcomes",
            "program outcomes", "peos masters", "psos masters", "pos masters"
        ]

        attribute = next((attr for attr in attributes if attr in user_message), None)

        if mech_data:
            if attribute:
                if attribute == "description":
                    response = mech_data.get('description', "Description information not available.")
                elif attribute == "programs offered":
                    ug = "\nUG Programs:\n" + "\n".join(mech_data['programs_offered'].get('UG', []))
                    pg = "\nPG Programs:\n" + "\n".join(mech_data['programs_offered'].get('PG', []))
                    response = ug + pg
                elif attribute == "vision":
                    response = mech_data.get('vision', "Vision statement not available.")
                elif attribute == "mission":
                    response = "\n".join(mech_data.get('mission', ["Mission statements not available."]))
                elif attribute == "placements":
                    response = mech_data.get('placements', "Placement information not available.")
                elif attribute == "objectives":
                    be_mech = mech_data['objectives'].get('BE Mechanical Engineering', [])
                    be_prod = mech_data['objectives'].get('BE Production Engineering', [])
                    response = "\nBE Mechanical Engineering:\n" + "\n".join(be_mech)
                    response += "\n\nBE Production Engineering:\n" + "\n".join(be_prod)
                elif attribute == "program specific outcomes":
                    be_mech = mech_data['program_specific_outcomes'].get('BE Mechanical Engineering', [])
                    be_prod = mech_data['program_specific_outcomes'].get('BE Production Engineering', [])
                    response = "\nBE Mechanical Engineering:\n" + "\n".join(be_mech)
                    response += "\n\nBE Production Engineering:\n" + "\n".join(be_prod)
                elif attribute == "program outcomes":
                    response = "\n".join(mech_data['program_outcomes'].get('BE Program', []))
                elif attribute == "peos masters":
                    cad_cam = mech_data['PEOs_Masters'].get('M.E. CAD/CAM', [])
                    thermal = mech_data['PEOs_Masters'].get('M.E. Thermal Engineering', [])
                    response = "\nM.E. CAD/CAM:\n" + "\n".join(cad_cam)
                    response += "\n\nM.E. Thermal Engineering:\n" + "\n".join(thermal)
                elif attribute == "psos masters":
                    cad_cam = mech_data['PSOs_Masters'].get('M.E. CAD/CAM', [])
                    thermal = mech_data['PSOs_Masters'].get('M.E. Thermal Engineering', [])
                    response = "\nM.E. CAD/CAM:\n" + "\n".join(cad_cam)
                    response += "\n\nM.E. Thermal Engineering:\n" + "\n".join(thermal)
                elif attribute == "pos masters":
                    response = "\n".join(mech_data.get('POs_Masters', []))
                else:
                    response = f"I'm sorry, I don't have information about {attribute} for the Mechanical Engineering department."
            else:
                response = "What specific information would you like about the Mechanical Engineering department? You can ask about the overview, programs offered, vision, mission, placements, program educational objectives, program specific outcomes, program outcomes, PEOs for Masters, PSOs for Masters, or POs for Masters."
        else:
            response = "I'm sorry, I couldn't find information about the Mechanical Engineering department."

        dispatcher.utter_message(text=response)
        return []


# Extract Electrical and Electronics Engineering department data
eee_data = next((dept for dept in college_data if dept['department'].lower() == "electrical and electronics engineering"), None)

class ActionRetrieveEEEInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_eee_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        # Check if the query is about electrical and electronics engineering
        if "eee" not in user_message and "electrical" not in user_message and "electronics" not in user_message:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about Electrical and Electronics Engineering. Could you please rephrase your question?")
            return []

        attributes = [
            "vision", "mission", "programs offered", "placements",
            "program outcomes"
        ]

        attribute = next((attr for attr in attributes if attr in user_message), None)

        if eee_data:
            if attribute:
                if attribute == "vision":
                    response = eee_data.get('vision', "Vision statement not available.")
                elif attribute == "mission":
                    mission_list = eee_data.get('mission', [])
                    response = "\n".join([f"{k}: {v}" for item in mission_list for k, v in item.items()])
                elif attribute == "programs offered":
                    response = "\n".join(eee_data.get('programs_offered', ["Programs information not available."]))
                elif attribute == "placements":
                    response = eee_data.get('placements', "Placement information not available.")
                elif attribute == "program outcomes":
                    po_list = eee_data.get('program_outcomes', [])
                    response = "\n".join([f"{k}: {v}" for item in po_list for k, v in item.items()])
                else:
                    response = f"I'm sorry, I don't have information about {attribute} for the Electrical and Electronics Engineering department."
            else:
                response = "What specific information would you like about the Electrical and Electronics Engineering department? You can ask about the vision, mission, programs offered, placements, or program outcomes."
        else:
            response = "I'm sorry, I couldn't find information about the Electrical and Electronics Engineering department."

        dispatcher.utter_message(text=response)
        return []

# Extract Electronics and Communication Engineering department data
ece_data = next((dept for dept in college_data if dept['department'].lower() == "electronics and communication engineering"), None)

class ActionRetrieveECEInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_ece_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        # Check if the query is about electronics and communication engineering
        if "ece" not in user_message and "electronics" not in user_message and "communication" not in user_message:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about Electronics and Communication Engineering. Could you please rephrase your question?")
            return []

        attributes = [
            "vision", "mission", "programs offered", "program educational objectives",
            "program specific outcomes", "program outcomes"
        ]

        attribute = next((attr for attr in attributes if attr in user_message), None)

        if ece_data:
            if attribute:
                if attribute == "vision":
                    response = ece_data.get('vision', "Vision statement not available.")
                elif attribute == "mission":
                    response = "\n".join(ece_data.get('mission', ["Mission statements not available."]))
                elif attribute == "programs offered":
                    ug = "\nUndergraduate Programs:\n" + "\n".join(ece_data['programs_offered'].get('undergraduate', []))
                    pg = "\nPostgraduate Programs:\n" + "\n".join(ece_data['programs_offered'].get('postgraduate', []))
                    response = ug + pg
                elif attribute == "program educational objectives":
                    response = ""
                    for program, objectives in ece_data.get('program_educational_objectives', {}).items():
                        response += f"\n{program}:\n" + "\n".join(objectives)
                elif attribute == "program specific outcomes":
                    response = ""
                    for program, outcomes in ece_data.get('program_specific_outcomes', {}).items():
                        response += f"\n{program}:\n" + "\n".join(outcomes)
                elif attribute == "program outcomes":
                    response = "\n".join(ece_data.get('program_outcomes', {}).get('BE_ECE', []))
                else:
                    response = f"I'm sorry, I don't have information about {attribute} for the Electronics and Communication Engineering department."
            else:
                response = "What specific information would you like about the Electronics and Communication Engineering department? You can ask about the vision, mission, programs offered, program educational objectives, program specific outcomes, or program outcomes."
        else:
            response = "I'm sorry, I couldn't find information about the Electronics and Communication Engineering department."

        dispatcher.utter_message(text=response)
        return []

# Extract Computer Science and Engineering department data
cse_data = next((dept for dept in college_data if dept['department'].lower() == "computer science and engineering"), None)

class ActionRetrieveCSEInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_cse_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        # Check if the query is about computer science and engineering
        if "cse" not in user_message and "computer science" not in user_message:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about Computer Science and Engineering. Could you please rephrase your question?")
            return []

        # Define keywords for each attribute
        attribute_keywords = {
            "about": ["about", "information", "details"],
            "placements": ["placements", "placement", "jobs", "recruitment", "offers", "packages", "internships"],
            "vision": ["vision"],
            "mission": ["mission"],
            "programs": ["programs", "courses", "degrees"],
            "program outcomes": ["program outcomes", "learning outcomes", "outcomes"]
        }

        # Special handling for "about" and "placements"
        if "about" in user_message and "placement" in user_message:
            about_index = user_message.index("about")
            placement_index = user_message.index("placement")
            if placement_index > about_index:
                attribute = "placements"
            else:
                attribute = "about"
        else:
            # Determine the attribute based on keywords in the user message
            attribute = next((attr for attr, keywords in attribute_keywords.items() 
                              if any(keyword in user_message for keyword in keywords)), None)

        if cse_data:
            if attribute == "about":
                response = f"Established Year: {cse_data['about']['established_year']}\n"
                response += f"Initial Intake: {cse_data['about']['initial_intake']}\n"
                response += f"Current Intake: {cse_data['about']['current_intake']}\n"
                response += f"Programs Offered: {', '.join(cse_data['about']['programs_offered'])}\n"
                response += f"NBA Accreditation: Year {cse_data['about']['nba_accreditation'][0]['year']}, Grade {cse_data['about']['nba_accreditation'][0]['grade']}\n"
                response += f"Research Recognition: {cse_data['about']['research_recognition']}\n"
                response += f"Centers of Excellence: {', '.join(cse_data['about']['centers_of_excellence'])}\n"
                response += f"MoU Partners: {', '.join(cse_data['about']['mou_partners'])}\n"
                response += f"Faculty Research Areas: {', '.join(cse_data['about']['faculty_research_areas'])}\n"
                response += f"Collaborations: Professional Bodies - {', '.join(cse_data['about']['collaborations']['professional_bodies'])}, Workshops & Certifications - {', '.join(cse_data['about']['collaborations']['workshops_certifications'])}\n"
                response += f"Technical Clubs: {', '.join(cse_data['about']['technical_clubs'])}"
            elif attribute == "placements":
                response = "Placement Statistics:\n"
                for stats in cse_data['placements']['yearly_statistics']:
                    response += f"\nYear: {stats['year']}\n"
                    response += f"Students Placed: {stats['students_placed']}\n"
                    response += f"Total Jobs: {stats['total_jobs']}\n"
                    response += f"Highest Package: {stats['highest_package']}\n"
                    response += f"Average Package: {stats['average_package']}\n"
                
                response += "\nNotable Offers:\n"
                for offer in cse_data['placements']['notable_offers']:
                    response += f"{offer['students']} students received {offer['package']}"
                    if 'companies' in offer:
                        response += f" from {', '.join(offer['companies'])}"
                    response += "\n"
                
                response += f"\nTop Recruiters: {', '.join(cse_data['placements']['top_recruiters'])}\n"
                
                response += "\nInternships:\n"
                for internship in cse_data['placements']['internships']['statistics']:
                    response += f"Year {internship['year']}: {internship['total']} internships"
                    if 'stipend_offered' in internship:
                        response += f", Stipend offered: {internship['stipend_offered']}"
                    response += "\n"
            elif attribute == "vision":
                response = cse_data['vision']
            elif attribute == "mission":
                response = "\n".join(cse_data['mission'])
            elif attribute == "programs":
                ug = "\nUndergraduate Programs:\n" + "\n".join(cse_data['programs']['ug'])
                pg = "\nPostgraduate Programs:\n" + "\n".join(cse_data['programs']['pg'])
                minor = "\nMinor Degrees:\n" + "\n".join(cse_data['programs']['minor_degrees'])
                response = ug + pg + minor
            elif attribute == "program outcomes":
                response = "\n".join(cse_data['program_outcomes'])
            else:
                response = "What specific information would you like about the Computer Science and Engineering department? You can ask about the about, placements, vision, mission, programs, or program outcomes."
        else:
            response = "I'm sorry, I couldn't find information about the Computer Science and Engineering department."

        dispatcher.utter_message(text=response)
        return []


# Extract AI&ML department data
aiml_data = next((dept for dept in college_data if dept['department'].lower() == "artificial intelligence and machine learning (ai&ml)"), None)

class ActionRetrieveAIMLInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_aiml_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        # Check if the query is about AI&ML
        if "ai" not in user_message and "aiml" not in user_message and "ml" not in user_message and "artificial intelligence" not in user_message and "machine learning" not in user_message:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about Artificial Intelligence and Machine Learning. Could you please rephrase your question?")
            return []

        # Define keywords for each attribute
        attribute_keywords = {
            "about": ["about", "information", "details"],
            "mission": ["mission"],
            "vision": ["vision"],
            "programs": ["programs", "courses", "degrees", "peos", "psos"],
            "program outcomes": ["program outcomes", "learning outcomes", "outcomes"]
        }

        # Determine the attribute based on keywords in the user message
        attribute = next((attr for attr, keywords in attribute_keywords.items() 
                          if any(keyword in user_message for keyword in keywords)), None)

        if aiml_data:
            if attribute == "about":
                response = aiml_data['about']
            elif attribute == "mission":
                response = "\n".join(aiml_data['mission'])
            elif attribute == "vision":
                response = aiml_data['vision']
            elif attribute == "programs":
                response = "Programs Offered:\n"
                for program, details in aiml_data['programs_offered'].items():
                    response += f"\n{program} (Intake: {details['intake']}):\n"
                    response += "Program Educational Objectives (PEOs):\n"
                    response += "\n".join(f"- {peo}" for peo in details['PEOs'])
                    response += "\n\nProgram Specific Outcomes (PSOs):\n"
                    response += "\n".join(f"- {pso}" for pso in details['PSOs'])
                    response += "\n"
            elif attribute == "program outcomes":
                response = "Program Outcomes:\n" + "\n".join(f"- {po}" for po in aiml_data['program_outcomes'])
            else:
                response = "What specific information would you like about the AI&ML department? You can ask about the about, mission, vision, programs, or program outcomes."
        else:
            response = "I'm sorry, I couldn't find information about the AI&ML department."

        dispatcher.utter_message(text=response)
        return []


# Extract Information Technology department data
it_data = next((dept for dept in college_data if dept['department'].lower() == "information technology"), None)

class ActionRetrieveITInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_it_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        # Check if the query is about Information Technology
        if "it" not in user_message and "information technology" not in user_message:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about Information Technology. Could you please rephrase your question?")
            return []

        # Define keywords for each attribute
        attribute_keywords = {
            "overview": ["overview"],
            "description": ["description", "about"],
            "vision": ["vision"],
            "mission": ["mission"],
            "programs": ["programs", "courses", "degrees"],
            "program outcomes": ["program outcomes", "learning outcomes", "outcomes"]
        }

        # Determine the attribute based on keywords in the user message
        attribute = next((attr for attr, keywords in attribute_keywords.items() 
                          if any(keyword in user_message for keyword in keywords)), None)

        if it_data:
            if attribute == "overview":
                response = it_data['overview']
            elif attribute == "description":
                response = it_data['description']
            elif attribute == "vision":
                response = it_data['vision']
            elif attribute == "mission":
                response = "\n".join(it_data['mission'])
            elif attribute == "programs":
                program = it_data['programs_offered']['undergraduate']
                response = f"Undergraduate Program: {program['name']} (Intake: {program['intake']})"
            elif attribute == "program outcomes":
                response = "Program Outcomes:\n"
                for key, value in it_data['program_outcomes'].items():
                    response += f"- {key.replace('_', ' ').title()}: {value}\n"
            else:
                response = "What specific information would you like about the IT department? You can ask about the overview, description, vision, mission, programs, or program outcomes."
        else:
            response = "I'm sorry, I couldn't find information about the IT department."

        dispatcher.utter_message(text=response)
        return []


# Extract Computer Engineering and Technology department data
cet_data = next((dept for dept in college_data if dept['department'].lower() == "computer engineering and technology"), None)

class ActionRetrieveCETInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_cet_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        # Check if the query is about Computer Engineering and Technology
        if not any(keyword in user_message for keyword in ["computer engineering", "cet", "iot", "cs", "bct"]):
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about Computer Engineering and Technology. Could you please rephrase your question?")
            return []

        # Define keywords for each attribute
        attribute_keywords = {
            "overview": ["overview", "description", "about", "accreditation", "research", "centers of excellence"],
            "collaborations": ["collaborations", "mous", "workshops", "certifications", "professional bodies"],
            "faculty": ["faculty", "staff", "technical clubs"],
            "placements": ["placements", "recruiters", "salary", "internship"],
            "vision": ["vision"],
            "mission": ["mission"],
            "programs": ["programs", "courses", "degrees"]
        }

        # Determine the attribute based on keywords in the user message
        attribute = next((attr for attr, keywords in attribute_keywords.items() 
                          if any(keyword in user_message for keyword in keywords)), None)

        if cet_data:
            if attribute == "overview":
                response = f"Description: {cet_data['overview']['description']}\n\n"
                response += f"Accreditation: {cet_data['overview']['accreditation']}\n\n"
                response += f"Research: {cet_data['overview']['research']}\n\n"
                response += f"Centers of Excellence: {', '.join(cet_data['overview']['centers_of_excellence'])}"
            elif attribute == "collaborations":
                response = f"MOUs: {', '.join(cet_data['collaborations']['mous'])}\n\n"
                response += f"Workshops and Certifications: {', '.join(cet_data['collaborations']['workshops_and_certifications'])}\n\n"
                response += f"Professional Bodies: {', '.join(cet_data['collaborations']['professional_bodies'])}"
            elif attribute == "faculty":
                response = f"Faculty: {cet_data['faculty']['qualification']}\n\n"
                response += f"Technical Clubs: {', '.join(cet_data['faculty']['technical_clubs'])}"
            elif attribute == "placements":
                response = f"Placement Record: {cet_data['placements']['placement_record']}\n\n"
                response += f"Top Recruiters: {', '.join(cet_data['placements']['top_recruiters'])}\n\n"
                response += f"Highest Salary: {cet_data['placements']['highest_salary']}\n\n"
                response += f"Internship Trend: {cet_data['placements']['internship_trend']}"
            elif attribute == "vision":
                response = cet_data['vision']
            elif attribute == "mission":
                response = "\n".join(cet_data['mission'])
            elif attribute == "programs":
                response = f"Programs Offered: {', '.join(cet_data['programs_offered'])}"
            else:
                response = "What specific information would you like about the Computer Engineering and Technology department? You can ask about the overview, collaborations, faculty, placements, vision, mission, or programs."
        else:
            response = "I'm sorry, I couldn't find information about the Computer Engineering and Technology department."

        dispatcher.utter_message(text=response)
        return []

# Extract AI and Data Science department data
aids_data = next((dept for dept in college_data if dept['department'].lower() == "artificial intelligence and data science"), None)

class ActionRetrieveAIDSInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_aids_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        # Check if the query is about AI and Data Science
        if not any(keyword in user_message for keyword in ["ai", "artificial intelligence", "data science", "aids"]):
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about Artificial Intelligence and Data Science. Could you please rephrase your question?")
            return []

        # Define keywords for each attribute
        attribute_keywords = {
            "overview": ["overview", "about"],
            "vision": ["vision"],
            "mission": ["mission"],
            "programs": ["programs", "courses", "degrees"],
            "peos": ["peos", "program educational objectives"],
            "psos": ["psos", "program specific outcomes"],
            "pos": ["pos", "program outcomes"]
        }

        # Determine the attribute based on keywords in the user message
        attribute = next((attr for attr, keywords in attribute_keywords.items() 
                          if any(keyword in user_message for keyword in keywords)), None)

        if aids_data:
            if attribute == "overview":
                response = aids_data['overview']
            elif attribute == "vision":
                response = aids_data['vision']
            elif attribute == "mission":
                response = "\n".join(aids_data['mission'])
            elif attribute == "programs":
                response = f"Undergraduate: {aids_data['programs_offered']['undergraduate']}\n"
                response += f"Postgraduate: {aids_data['programs_offered']['postgraduate']}"
            elif attribute == "peos":
                if "b.e" in user_message or "undergraduate" in user_message:
                    response = "PEOs for B.E. (AI & DS):\n" + "\n".join(f"{i+1}. {peo}" for i, peo in enumerate(aids_data['PEOs_B.E_AI_DS']))
                elif "m.tech" in user_message or "postgraduate" in user_message:
                    response = "PEOs for M.Tech. (AI & DS):\n" + "\n".join(f"{i+1}. {peo}" for i, peo in enumerate(aids_data['PEOs_M.Tech_AI_DS']))
                else:
                    response = "Please specify if you want PEOs for B.E. or M.Tech. program."
            elif attribute == "psos":
                if "b.e" in user_message or "undergraduate" in user_message:
                    response = "PSOs for B.E. (AI & DS):\n" + "\n".join(f"{i+1}. {pso}" for i, pso in enumerate(aids_data['PSOs_B.E_AI_DS']))
                elif "m.tech" in user_message or "postgraduate" in user_message:
                    response = "PSOs for M.Tech. (AI & DS):\n" + "\n".join(f"{i+1}. {pso}" for i, pso in enumerate(aids_data['PSOs_M.Tech_AI_DS']))
                else:
                    response = "Please specify if you want PSOs for B.E. or M.Tech. program."
            elif attribute == "pos":
                if "b.e" in user_message or "undergraduate" in user_message:
                    response = "POs for B.E. (AI & DS):\n" + "\n".join(f"{i+1}. {po}" for i, po in enumerate(aids_data['POs_B.E_AI_DS']))
                elif "m.tech" in user_message or "postgraduate" in user_message:
                    response = "POs for M.Tech. (AI & DS):\n" + "\n".join(f"{i+1}. {po}" for i, po in enumerate(aids_data['POs_M.Tech_AI_DS']))
                else:
                    response = "Please specify if you want POs for B.E. or M.Tech. program."
            else:
                response = "What specific information would you like about the AI and Data Science department? You can ask about the overview, vision, mission, programs, PEOs, PSOs, or POs."
        else:
            response = "I'm sorry, I couldn't find information about the AI and Data Science department."

        dispatcher.utter_message(text=response)
        return []


# Extract Chemical Engineering department data
chem_eng_data = next((dept for dept in college_data if dept['department'].lower() == "chemical engineering"), None)

class ActionRetrieveChemEngInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_chem_eng_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        # Check if the query is about Chemical Engineering
        if "chemical" not in user_message and "chem" not in user_message:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about Chemical Engineering. Could you please rephrase your question?")
            return []

        # Define keywords for each attribute
        attribute_keywords = {
            "overview": ["overview", "about", "established", "intake", "accreditation", "career", "collaborations"],
            "initiatives": ["initiatives", "cells", "chapters"],
            "faculty_involvement": ["faculty involvement", "faculty initiatives"],
            "programs": ["programs", "courses", "degrees"],
            "vision": ["vision"],
            "mission": ["mission"],
            "peos": ["peos", "program educational objectives"],
            "psos": ["psos", "program specific outcomes"],
            "pos": ["pos", "program outcomes"]
        }

        # Determine the attribute based on keywords in the user message
        attribute = next((attr for attr, keywords in attribute_keywords.items() 
                          if any(keyword in user_message for keyword in keywords)), None)

        if chem_eng_data:
            if attribute == "overview":
                response = f"Established Year: {chem_eng_data['overview']['established_year']}\n"
                response += f"Initial Intake: {chem_eng_data['overview']['initial_intake']}\n"
                response += f"Current Intake: {chem_eng_data['overview']['current_intake']}\n"
                response += "Accreditation History:\n"
                for accred in chem_eng_data['overview']['accreditation_history']:
                    response += f"  - Year: {accred['year']}, Duration: {accred['duration']}\n"
                response += "Career Opportunities:\n"
                for career in chem_eng_data['overview']['career_opportunities']:
                    response += f"  - {career}\n"
                response += "Collaborations:\n"
                response += f"  Inter-departmental: {', '.join(chem_eng_data['overview']['collaborations']['inter_departmental'])}\n"
                response += f"  Research Centers: {', '.join(chem_eng_data['overview']['collaborations']['research_centers'])}\n"
                response += "  MoUs:\n"
                for mou in chem_eng_data['overview']['collaborations']['MoUs']:
                    response += f"    - {mou['organization']} ({mou['type']})\n"
            elif attribute == "initiatives":
                response = "Initiatives:\n" + "\n".join(f"- {initiative}" for initiative in chem_eng_data['initiatives'])
            elif attribute == "faculty_involvement":
                response = "Faculty Involvement:\n" + "\n".join(f"- {involvement}" for involvement in chem_eng_data['faculty_involvement'])
            elif attribute == "programs":
                response = "Programs Offered:\n"
                for program in chem_eng_data['programs_offered']:
                    response += f"- {program['name']} (Intake: {program['intake']})\n"
            elif attribute == "vision":
                response = chem_eng_data['vision']
            elif attribute == "mission":
                response = "Mission:\n" + "\n".join(f"- {mission}" for mission in chem_eng_data['mission'])
            elif attribute == "peos":
                response = "Program Educational Objectives:\n"
                for peo in chem_eng_data['program_educational_objectives']:
                    response += f"{peo['id']}: {peo['description']}\n\n"
            elif attribute == "psos":
                response = "Program Specific Outcomes:\n"
                for pso in chem_eng_data['program_specific_outcomes']:
                    response += f"{pso['id']}: {pso['description']}\n\n"
            elif attribute == "pos":
                response = "Program Outcomes:\n"
                for po in chem_eng_data['program_outcomes']:
                    response += f"{po['id']} - {po['title']}: {po['description']}\n\n"
            else:
                response = "What specific information would you like about the Chemical Engineering department? You can ask about the overview, initiatives, faculty involvement, programs, vision, mission, PEOs, PSOs, or POs."
        else:
            response = "I'm sorry, I couldn't find information about the Chemical Engineering department."

        dispatcher.utter_message(text=response)
        return []


# Extract Biotechnology department data
biotech_data = next((dept for dept in college_data if dept['department'].lower() == "biotechnology"), None)

class ActionRetrieveBiotechInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_biotech_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        # Check if the query is about Biotechnology
        if "biotech" not in user_message and "biotechnology" not in user_message:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about Biotechnology. Could you please rephrase your question?")
            return []

        # Define keywords for each attribute
        attribute_keywords = {
            "about": ["about", "overview"],
            "domains": ["domains", "areas", "fields"],
            "infrastructure": ["infrastructure", "facilities", "labs", "laboratories"],
            "faculty": ["faculty", "staff", "professors"],
            "student_engagement": ["student engagement", "clubs", "activities"],
            "placements": ["placements", "jobs", "companies", "higher education"],
            "programs": ["programs", "courses", "degrees"],
            "peos": ["peos", "program educational objectives"],
            "pos": ["pos", "program outcomes"],
            "psos": ["psos", "program specific outcomes"],
            "vision": ["vision"],
            "mission": ["mission"]
        }

        # Determine the attribute based on keywords in the user message
        attribute = next((attr for attr, keywords in attribute_keywords.items() 
                          if any(keyword in user_message for keyword in keywords)), None)

        if biotech_data:
            if attribute == "about":
                response = biotech_data['about']
            elif attribute == "domains":
                response = "Domains:\n" + "\n".join(f"- {domain}" for domain in biotech_data['domains'])
            elif attribute == "infrastructure":
                response = f"Infrastructure: {biotech_data['infrastructure']['laboratories']}"
            elif attribute == "faculty":
                response = f"Faculty: Total {biotech_data['faculty']['total']} faculty members. {biotech_data['faculty']['qualifications']}"
            elif attribute == "student_engagement":
                response = f"Student Engagement:\nClub: {biotech_data['student_engagement']['clubs']}\nActivities: {biotech_data['student_engagement']['activities']}"
            elif attribute == "placements":
                response = f"Placement Rate: {biotech_data['placements']['placement_rate']}\n"
                response += "Companies:\n" + "\n".join(f"- {company}" for company in biotech_data['placements']['companies'])
                response += "\n\nHigher Education:\n" + "\n".join(f"- {university}" for university in biotech_data['placements']['higher_education'])
            elif attribute == "programs":
                response = "Programs Offered:\n" + "\n".join(f"- {program}" for program in biotech_data['programs_offered'])
            elif attribute == "peos":
                response = "Program Educational Objectives:\n" + "\n".join(f"- {peo}" for peo in biotech_data['program_educational_objectives'])
            elif attribute == "pos":
                response = "Program Outcomes:\n" + "\n".join(f"- {po}" for po in biotech_data['program_outcomes'])
            elif attribute == "psos":
                response = "Program Specific Outcomes:\n" + "\n".join(f"- {pso}" for pso in biotech_data['program_specific_outcomes'])
            elif attribute == "vision":
                response = f"Vision: {biotech_data['vision']}"
            elif attribute == "mission":
                response = "Mission:\n" + "\n".join(f"- {mission}" for mission in biotech_data['mission'])
            else:
                response = "What specific information would you like about the Biotechnology department? You can ask about the about, domains, infrastructure, faculty, student engagement, placements, programs, PEOs, POs, PSOs, vision, or mission."
        else:
            response = "I'm sorry, I couldn't find information about the Biotechnology department."

        dispatcher.utter_message(text=response)
        return []


# Extract Physics department data
physics_data = next((dept for dept in college_data if dept['department'].lower() == "physics"), None)

class ActionRetrievePhysicsInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_physics_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        # Check if the query is about Physics
        if "physics" not in user_message:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about the Physics department. Could you please rephrase your question?")
            return []

        # Define keywords for each attribute
        attribute_keywords = {
            "overview": ["overview", "about"],
            "vision": ["vision"],
            "mission": ["mission"],
            "courses": ["courses", "offered", "subjects"],
            "academic_contributions": ["academic", "contributions", "curriculum", "events", "publications", "research", "funding"],
            "faculty_development": ["faculty", "development", "workshops", "conferences", "interdisciplinary"]
        }

        # Determine the attribute based on keywords in the user message
        attribute = next((attr for attr, keywords in attribute_keywords.items() 
                          if any(keyword in user_message for keyword in keywords)), None)

        if physics_data:
            if attribute == "overview":
                response = physics_data['overview']
            elif attribute == "vision":
                response = physics_data['vision']
            elif attribute == "mission":
                response = physics_data['mission']
            elif attribute == "courses":
                response = "Courses offered:\n" + "\n".join(f"- {course}" for course in physics_data['courses_offered'])
            elif attribute == "academic_contributions":
                ac = physics_data['academic_contributions']
                response = f"Role in curriculum: {ac['role_in_curriculum']}\n\n"
                response += "Events and initiatives:\n" + "\n".join(f"- {event}" for event in ac['events_and_initiatives']) + "\n\n"
                response += f"Journal publications: {ac['publications']['journal_publications']}\n"
                response += f"Conference proceedings: {ac['publications']['conference_proceedings']}\n\n"
                response += f"Research facilities: {ac['research_facilities']}\n\n"
                response += f"Total funding secured: {ac['funding']['total_amount_secured']}\n"
                response += "Funding agencies: " + ", ".join(ac['funding']['funding_agencies'])
            elif attribute == "faculty_development":
                fd = physics_data['faculty_development']
                response = f"Workshops and conferences: {fd['workshops_and_conferences']}\n\n"
                response += f"Interdisciplinary research: {fd['interdisciplinary_research']}"
            else:
                response = "What specific information would you like about the Physics department? You can ask about the overview, vision, mission, courses offered, academic contributions, or faculty development."
        else:
            response = "I'm sorry, I couldn't find information about the Physics department."

        dispatcher.utter_message(text=response)
        return []


# Extract Chemistry department data
chemistry_data = next((dept for dept in college_data if dept['department'].lower() == "chemistry"), None)

class ActionRetrieveChemistryInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_chemistry_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        # Check if the query is about Chemistry
        if "chemistry" not in user_message and "chem" not in user_message:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about the Chemistry department. Could you please rephrase your question?")
            return []

        # Define keywords for each attribute
        attribute_keywords = {
            "description": ["description", "about", "overview"],
            "objectives": ["objectives", "goals"],
            "vision": ["vision"],
            "mission": ["mission"],
            "peos": ["peos", "program educational objectives"],
            "pos": ["pos", "program outcomes"]
        }

        # Determine the attribute based on keywords in the user message
        attribute = next((attr for attr, keywords in attribute_keywords.items() 
                          if any(keyword in user_message for keyword in keywords)), None)

        if chemistry_data:
            if attribute == "description":
                response = chemistry_data['description']
            elif attribute == "objectives":
                response = "Objectives:\n" + "\n".join(f"- {obj}" for obj in chemistry_data['objectives'])
            elif attribute == "vision":
                response = f"Vision: {chemistry_data['vision']}"
            elif attribute == "mission":
                response = f"Mission: {chemistry_data['mission']}"
            elif attribute == "peos":
                response = "Program Educational Objectives:\n" + "\n".join(f"- {peo}" for peo in chemistry_data['program_educational_objectives'])
            elif attribute == "pos":
                response = "Program Outcomes:\n"
                for key, value in chemistry_data['program_outcomes'].items():
                    response += f"- {key}: {value}\n"
            else:
                response = "What specific information would you like about the Chemistry department? You can ask about the description, objectives, vision, mission, program educational objectives (PEOs), or program outcomes (POs)."
        else:
            response = "I'm sorry, I couldn't find information about the Chemistry department."

        dispatcher.utter_message(text=response)
        return []


# Extract Mathematics and Humanities department data
math_humanities_data = next((dept for dept in college_data if dept['department'].lower() == "mathematics and humanities"), None)

class ActionRetrieveMathHumanitiesInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_math_humanities_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        if "math" not in user_message and "humanities" not in user_message:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about the Mathematics and Humanities department. Could you please rephrase your question?")
            return []

        attribute_keywords = {
            "description": ["description", "about", "overview"],
            "vision": ["vision"],
            "mission": ["mission"]
        }

        attribute = next((attr for attr, keywords in attribute_keywords.items() 
                          if any(keyword in user_message for keyword in keywords)), None)

        if math_humanities_data:
            if attribute == "description":
                response = math_humanities_data['description']
            elif attribute == "vision":
                response = math_humanities_data['vision']
            elif attribute == "mission":
                response = "\n".join(f"- {mission}" for mission in math_humanities_data['mission'])
            else:
                response = "What specific information would you like about the Mathematics and Humanities department? You can ask about the description, vision, or mission."
        else:
            response = "I'm sorry, I couldn't find information about the Mathematics and Humanities department."

        dispatcher.utter_message(text=response)
        return []


# Extract English department data
english_data = next((dept for dept in college_data if dept['department'].lower() == "english"), None)

class ActionRetrieveEnglishInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_english_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        if "english" not in user_message and "language" not in user_message:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about the English department. Could you please rephrase your question?")
            return []

        attribute_keywords = {
            "overview": ["overview", "about", "description"],
            "research": ["research", "areas", "specializations"],
            "labs": ["labs", "laboratories", "facilities"],
            "courses": ["courses", "subjects", "offered"],
            "clubs": ["clubs", "student organizations", "activities"],
            "vision": ["vision"],
            "mission": ["mission", "goals", "objectives"]
        }

        attribute = next((attr for attr, keywords in attribute_keywords.items() 
                          if any(keyword in user_message for keyword in keywords)), None)

        if english_data:
            if attribute == "overview":
                response = english_data['overview']
            elif attribute == "research":
                response = "Research areas include: " + ", ".join(english_data['research_areas'])
            elif attribute == "labs":
                response = "Language labs: " + ", ".join(english_data['language_labs'])
            elif attribute == "courses":
                response = "Courses offered: " + ", ".join(english_data['courses_offered'])
                response += "\nSpecial courses: " + ", ".join(english_data['special_courses'])
            elif attribute == "clubs":
                response = "Student clubs: " + ", ".join(english_data['student_clubs'])
                response += "\nClub activities include: " + ", ".join(english_data['club_activities'])
            elif attribute == "vision":
                response = f"Vision: {english_data['department_vision']}"
            elif attribute == "mission":
                response = "Mission:\n" + "\n".join(f"- {mission}" for mission in english_data['department_mission'])
            else:
                response = "What specific information would you like about the English department? You can ask about the overview, faculty, research areas, labs, courses, student clubs, vision, or mission."
        else:
            response = "I'm sorry, I couldn't find information about the English department."

        dispatcher.utter_message(text=response)
        return []


# Extract MCA department data
mca_data = next((dept for dept in college_data if dept['department'].lower() == "master of computer applications (mca)"), None)

class ActionRetrieveMCAInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_mca_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        if "mca" not in user_message and "master of computer applications" not in user_message:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about the MCA department. Could you please rephrase your question?")
            return []

        attribute_keywords = {
            "vision": ["vision"],
            "mission": ["mission"],
            "programs": ["programs", "courses", "offered"],
            "placements": ["placements", "companies", "recruiters"],
            "peos": ["peos", "program educational objectives"],
            "pos": ["pos", "program outcomes"]
        }

        attribute = next((attr for attr, keywords in attribute_keywords.items() 
                          if any(keyword in user_message for keyword in keywords)), None)

        if mca_data:
            if attribute == "vision":
                response = f"Vision: {mca_data['vision']}"
            elif attribute == "mission":
                response = "Mission:\n" + "\n".join(f"- {mission}" for mission in mca_data['mission'])
            elif attribute == "programs":
                program = mca_data['programs_offered'][0]
                response = f"Program: {program['name']}\nInitial Intake: {program['initial_intake']}\nCurrent Intake: {program['current_intake']}"
            elif attribute == "placements":
                response = "Recruiting Companies:\n" + ", ".join(mca_data['placements']['companies'])
            elif attribute == "peos":
                response = "Program Educational Objectives:\n" + "\n".join(f"{peo}" for peo in mca_data['program_educational_objectives'])
            elif attribute == "pos":
                response = "Program Outcomes:\n" + "\n".join(f"{po}" for po in mca_data['program_outcomes'])
            else:
                response = "What specific information would you like about the MCA department? You can ask about the vision, mission, programs offered, placements, program educational objectives (PEOs), or program outcomes (POs)."
        else:
            response = "I'm sorry, I couldn't find information about the MCA department."

        dispatcher.utter_message(text=response)
        return []


# Extract School of Management Studies data
sms_data = next((dept for dept in college_data if dept['department'].lower() == "cbit-school of management studies"), None)

class ActionRetrieveSMSInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_sms_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        if "management" not in user_message and "mba" not in user_message and "sms" not in user_message:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about the School of Management Studies. Could you please rephrase your question?")
            return []

        attribute_keywords = {
            "overview": ["overview", "about", "description"],
            "vision": ["vision"],
            "mission": ["mission"],
            "programs": ["programs", "courses", "offered"],
            "peos": ["peos", "program educational objectives"],
            "pos": ["pos", "program outcomes"]
        }

        attribute = next((attr for attr, keywords in attribute_keywords.items() 
                          if any(keyword in user_message for keyword in keywords)), None)

        if sms_data:
            if attribute == "overview":
                response = sms_data['overview']
            elif attribute == "vision":
                response = f"Vision: {sms_data['vision']}"
            elif attribute == "mission":
                response = "Mission:\n" + "\n".join(f"- {mission}" for mission in sms_data['mission'])
            elif attribute == "programs":
                program = sms_data['programs_offered'][0]
                response = f"Program: {program['name']}\nDescription: {program['description']}"
            elif attribute == "peos":
                response = "Program Educational Objectives:\n" + "\n".join(f"- {peo}" for peo in sms_data['program_educational_objectives'])
            elif attribute == "pos":
                response = "Program Outcomes:\n" + "\n".join(f"- {po}" for po in sms_data['program_outcomes'])
            else:
                response = "What specific information would you like about the School of Management Studies? You can ask about the overview, vision, mission, programs offered, program educational objectives (PEOs), or program outcomes (POs)."
        else:
            response = "I'm sorry, I couldn't find information about the School of Management Studies."

        dispatcher.utter_message(text=response)
        return []

# Extract Physical Education department data
pe_data = next((dept for dept in college_data if dept['department'].lower() == "physical education"), None)

class ActionRetrievePEInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_pe_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text', '').lower()

        if "physical education" not in user_message and "pe" not in user_message and "sports" not in user_message:
            dispatcher.utter_message(text="I'm sorry, I couldn't understand if you're asking about the Physical Education department. Could you please rephrase your question?")
            return []

        attribute_keywords = {
            "description": ["description", "about", "overview"],
            "mission": ["mission"],
            "vision": ["vision"]
        }

        attribute = next((attr for attr, keywords in attribute_keywords.items() 
                          if any(keyword in user_message for keyword in keywords)), None)

        if pe_data:
            if attribute == "description":
                response = pe_data['description']
            elif attribute == "mission":
                response = f"Mission: {pe_data['mission']}"
            elif attribute == "vision":
                response = f"Vision: {pe_data['vision']}"
            else:
                response = "What specific information would you like about the Physical Education department? You can ask about the description, mission, or vision."
        else:
            response = "I'm sorry, I couldn't find information about the Physical Education department."

        dispatcher.utter_message(text=response)
        return []




