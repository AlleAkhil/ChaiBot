from typing import Text, Dict, List, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json

with open('dataset/admissions.json', 'r', encoding='utf-8') as file:
    admission_data = json.load(file)

class ActionAdmissionsInfo(Action):
    def name(self) -> Text:
        return "action_admissions_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Access the first element of the list (assuming research_data is a list)
        admissions_data = admission_data[0]["admissions"]
        
        intent = tracker.get_intent_of_latest_message()
    
        if intent == "ask_why_cbit":
            intro = admissions_data["introduction"]
            dispatcher.utter_message(text=f"{intro}")
            why_cbit = admissions_data["why_cbit"]
            dispatcher.utter_message(text=f"{why_cbit}")
        
        elif intent == "ask_programs_offered":
            programs = admissions_data["programs_offered"]
            response = f"We offer the following programs:\n\nUndergraduate:\n- {', '.join(programs['undergraduate'])}\n\nPostgraduate:\n- {', '.join(programs['postgraduate'])}"
            dispatcher.utter_message(text=response)
        
        elif intent == "ask_admission_procedure":
            procedure = admissions_data["admission_procedure"]
            general_info = procedure["general"]
            be_btech_info = procedure["be_btech"]
            me_mtech_info = procedure["me_mtech"]
            mba_mca_info = procedure["mba_mca"]
            notes = procedure["notes"]

            response = (
                f"General Admission Info: {general_info}\n\n"
                f"B.E./B.Tech Admissions:\n"
                f"  A-Category (Convener Quota): {be_btech_info['a_category']['percentage']}% through {be_btech_info['a_category']['criteria']}\n"
                f"  B-Category (Management Quota): {be_btech_info['b_category']['percentage']}% ({be_btech_info['b_category']['criteria'][0]} and {be_btech_info['b_category']['criteria'][1]})\n\n"
                f"M.E./M.Tech Admissions:\n"
                f"  A-Category (Convener Quota): {me_mtech_info['a_category']['percentage']}% through {me_mtech_info['a_category']['criteria']}\n"
                f"  B-Category (Management Quota): {me_mtech_info['b_category']['percentage']}% through {me_mtech_info['b_category']['criteria']}\n\n"
                f"MBA/MCA Admissions:\n"
                f"  A-Category (Convener Quota): {mba_mca_info['a_category']['percentage']}% through {mba_mca_info['a_category']['criteria']}\n"
                f"  B-Category (Management Quota): {mba_mca_info['b_category']['percentage']}% through {mba_mca_info['b_category']['criteria']}"
                f"  \n\nNotes: {notes}"
            )
            
            dispatcher.utter_message(text=response)
        
        else:
            dispatcher.utter_message(text="Sorry, I couldn't understand your query.")
        
        return []


class ActionContactInfo(Action):
    def name(self) -> Text:
        return "action_contact_info_admissions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Access the first element of the list (assuming contact_data is a list)
        contact_info = admission_data[1]
        
        intent = tracker.get_intent_of_latest_message()
    
        if intent == "ask_contact_admissions":
            contact_message = contact_info["contact"]
            phone = contact_info["contact_details"]["phone"]
            email = contact_info["contact_details"]["email"]
            
            response = (
                f"{contact_message}\n\n"
                f"Contact Details:\n"
                f"Phone: {phone}\n"
                f"Email: {email}"
            )
            
            dispatcher.utter_message(text=response)
        
        else:
            dispatcher.utter_message(text="Sorry, I couldn't understand your query.")
        
        return []


class ActionCourseIntakeInfo(Action):
    def name(self) -> Text:
        return "action_course_intake_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Accessing the relevant data from the JSON
        intake_data = admission_data[2]["intake_approved_by_aicte"]
        
        intent = tracker.get_intent_of_latest_message()
        
        if intent == "ask_ug_course_intake":
            ug_courses = intake_data["ug_courses"]
            response = "Here is the AICTE-approved intake for UG courses for the academic year 2024-25:\n"
            for course in ug_courses:
                response += f"- {course['course_name']}: {course['intake']} seats\n"
            dispatcher.utter_message(text=response)
        
        elif intent == "ask_pg_course_intake":
            pg_courses = intake_data["pg_courses"]
            response = "Here is the AICTE-approved intake for PG courses for the academic year 2024-25:\n"
            for course in pg_courses:
                response += f"- {course['course_name']}: {course['intake']} seats\n"
            dispatcher.utter_message(text=response)
        
        else:
            dispatcher.utter_message(text="Sorry, I couldn't understand your query.")
        
        return []
    

class ActionTuitionFeeInfo(Action):
    def name(self) -> Text:
        return "action_tuition_fee_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Accessing the relevant data from the JSON
        fee_details = admission_data[3]["tuition_fee_details"]
        
        intent = tracker.get_intent_of_latest_message()
        
        if intent == "ask_tuition_fee_convener":
            convener_fee = next(item for item in fee_details["admission_categories"] if item["category"] == "Convener")
            response = (
                f"For the academic year {fee_details['academic_year']}, the tuition fee under Convener category is:\n"
                f"- B.E./B.Tech: {convener_fee['be_btech_fee']}\n"
                f"- M.E./M.Tech: {convener_fee['me_mtech_fee']}\n"
                f"- MCA: {convener_fee['mca_fee']}\n"
                f"- MBA: {convener_fee['mba_fee']}"
            )
            dispatcher.utter_message(text=response)
        
        elif intent == "ask_tuition_fee_b_category":
            b_category_fee = next(item for item in fee_details["admission_categories"] if item["category"] == "B-Category")
            response = (
                f"For the academic year {fee_details['academic_year']}, the tuition fee under B-Category is:\n"
                f"- B.E./B.Tech: {b_category_fee['be_btech_fee']}\n"
                f"- M.E./M.Tech: {b_category_fee['me_mtech_fee']}\n"
                f"- MCA: {b_category_fee['mca_fee']}\n"
                f"- MBA: {b_category_fee['mba_fee']}"
            )
            dispatcher.utter_message(text=response)
        
        elif intent == "ask_tuition_fee_nri":
            nri_fee = next(item for item in fee_details["admission_categories"] if item["category"] == "NRI")
            response = (
                f"For the academic year {fee_details['academic_year']}, the tuition fee under NRI category is:\n"
                f"- B.E./B.Tech: {nri_fee['be_btech_fee']}\n"
                f"- M.E./M.Tech: {nri_fee['me_mtech_fee']}\n"
                f"- MCA: {nri_fee['mca_fee']}\n"
                f"- MBA: {nri_fee['mba_fee']}"
            )
            dispatcher.utter_message(text=response)
        
        else:
            dispatcher.utter_message(text="Sorry, I couldn't understand your query.")
        
        return []


class ActionAdmissionFormInfo(Action):
    def name(self) -> Text:
        return "action_admission_form_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Accessing the relevant data from the JSON
        admission_form = admission_data[4]["admissionForm"]
        
        intent = tracker.get_intent_of_latest_message()
        
        if intent == "ask_certificates_required":
            certificates = admission_form["certificatesRequired"]
            response = "The following certificates are required for admission:\n"
            for certificate in certificates:
                response += f"- {certificate}\n"
            dispatcher.utter_message(text=response)
        
        elif intent == "ask_admission_guidelines":
            guidelines = admission_form["guidelines"]
            response = "Please follow these guidelines during the admission process:\n"
            for guideline in guidelines:
                response += f"- {guideline}\n"
            dispatcher.utter_message(text=response)
        
        else:
            dispatcher.utter_message(text="Sorry, I couldn't understand your query.")
        
        return []


class ActionScholarshipRenewalInfo(Action):
    def name(self) -> Text:
        return "action_scholarship_renewal_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Accessing the relevant data from the JSON
        scholarship_data = admission_data[5]["scholarshipRenewal"]
        
        intent = tracker.get_intent_of_latest_message()
        
        if intent == "ask_scholarship_eligibility":
            eligibility = scholarship_data["eligibility"]
            response = (
                f"Eligibility for scholarship renewal includes:\n"
                f"- Programs: {', '.join(eligibility['programs'])}\n"
                f"- Native: {eligibility['native']}\n"
                f"- Categories: {', '.join(eligibility['categories'])}"
            )
            dispatcher.utter_message(text=response)
        
        elif intent == "ask_scholarship_application":
            application = scholarship_data["application"]
            submission_process = application["submissionProcess"]
            response = (
                f"The scholarship application deadline is {application['deadline']}.\n"
                f"Apply online at: {application['website']}\n\n"
                f"Guidelines:\n"
                f"- {application['guidelines'][0]}\n"
                f"- {application['guidelines'][1]}\n\n"
                f"Submission Process:\n"
                f"1. {submission_process['step1']}\n"
                f"2. {submission_process['step2']}"
            )
            dispatcher.utter_message(text=response)
        
        elif intent == "ask_scholarship_documents":
            documents = scholarship_data["documentsRequired"]
            response = "The following documents are required for scholarship renewal:\n"
            for document in documents:
                response += f"- {document}\n"
            dispatcher.utter_message(text=response)
        
        else:
            dispatcher.utter_message(text="Sorry, I couldn't understand your query.")
        
        return []


