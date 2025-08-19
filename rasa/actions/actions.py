from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, ActiveLoop
from datetime import datetime, time
import re
import logging
import dateparser

# Nossos dois módulos customizados
from .gemini_integration import GeminiIntegration
from .db_connector import create_connection

# Constante com o nome da clínica para fácil manutenção
CLINICA_NOME = "Althara Saúde" 

logger = logging.getLogger(__name__)
gemini_service = GeminiIntegration()

class ActionAnalyzeSymptoms(Action):
    def name(self) -> Text:
        return "action_analyze_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        symptom_text = tracker.get_slot("symptoms")
        if not symptom_text:
            dispatcher.utter_message(text="Não consegui identificar sintomas. Poderia descrevê-los?")
            return []

        conn = create_connection()
        if not conn:
            dispatcher.utter_message(text="Estou com um problema para acessar o sistema de especialidades. Vamos agendar com um Clínico Geral para garantir.")
            return [
                SlotSet("recommended_specialty", "Clínico Geral"),
                SlotSet("requested_specialty", "Clínico Geral"),
                SlotSet("recommended_doctor_name", "um(a) de nossos(as) especialistas")
            ]

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT nome FROM especialidades ORDER BY nome ASC")
            available_specialties = [row['nome'] for row in cursor.fetchall()]
            specialties_list_str = ", ".join(available_specialties)
            
            if not available_specialties:
                raise ValueError("Nenhuma especialidade encontrada no banco de dados.")

            dispatcher.utter_message(response="utter_list_specialties_for_analysis", specialties_list=specialties_list_str)
            dispatcher.utter_message(response="utter_analyzing_symptoms")

            analysis = gemini_service.analyze_symptoms([symptom_text], available_specialties)

            if not analysis or not analysis.get('specialty'):
                raise ValueError("Análise do Gemini retornou vazia ou inválida.")

            recommended_specialty = analysis.get('specialty')
            cursor.execute("SELECT nome FROM especialidades WHERE nome = %s", (recommended_specialty,))
            specialty_exists = cursor.fetchone()
            
            if specialty_exists:
                query = "SELECT m.nome FROM medicos m JOIN especialidades e ON m.id_especialidade = e.id_especialidade WHERE e.nome = %s LIMIT 1"
                cursor.execute(query, (recommended_specialty,))
                result = cursor.fetchone()
                recommended_doctor = result['nome'] if result else "um(a) de nossos(as) especialistas"
                
                return [
                    SlotSet("recommended_specialty", recommended_specialty),
                    SlotSet("requested_specialty", recommended_specialty),
                    SlotSet("recommended_doctor_name", recommended_doctor),
                    SlotSet("symptoms_urgency", analysis.get('urgency')),
                    SlotSet("symptoms_explanation", analysis.get('explanation'))
                ]
            else:
                dispatcher.utter_message(text=f"A análise sugeriu '{recommended_specialty}', que não temos. As especialidades que podemos oferecer são: **{specialties_list_str}**. Alguma delas te interessa?")
                return [] 

        except Exception as e:
            logger.error(f"ERRO em ActionAnalyzeSymptoms: {e}")
            fallback_specialty = "Clínico Geral"
            fallback_doctor = "um(a) de nossos(as) especialistas"
            dispatcher.utter_message(
                text=f"Tive um problema ao analisar seus sintomas. Para garantir seu atendimento, a especialidade recomendada é **{fallback_specialty}**. Encontrei disponibilidade com **{fallback_doctor}**. Deseja agendar a consulta?"
            )
            return [
                SlotSet("recommended_specialty", fallback_specialty),
                SlotSet("requested_specialty", fallback_specialty),
                SlotSet("recommended_doctor_name", fallback_doctor)
            ]
        finally:
            if conn.is_connected():
                conn.close()


class ActionScheduleAppointment(Action):
    def name(self) -> Text:
        return "action_schedule_appointment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nome_paciente = tracker.get_slot("patient_name")
        email_paciente = tracker.get_slot("patient_email")
        especialidade_nome = tracker.get_slot("requested_specialty")
        data_str = tracker.get_slot("appointment_date")
        hora_str = tracker.get_slot("appointment_time")

        conn = create_connection()
        if not conn:
            dispatcher.utter_message(text="Desculpe, estou com um problema técnico. Por favor, tente novamente mais tarde.")
            return []

        try:
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT id_especialidade FROM especialidades WHERE nome = %s", (especialidade_nome,))
            especialidade = cursor.fetchone()
            if not especialidade:
                dispatcher.utter_message(text=f"Desculpe, ocorreu um erro: a especialidade '{especialidade_nome}' não foi encontrada no sistema.")
                return []
            id_especialidade = especialidade['id_especialidade']

            cursor.execute("SELECT id_medico, nome FROM medicos WHERE id_especialidade = %s LIMIT 1", (id_especialidade,))
            medico = cursor.fetchone()
            if not medico:
                dispatcher.utter_message(text=f"Desculpe, não há médicos para a especialidade '{especialidade_nome}'.")
                return []
            id_medico = medico['id_medico']
            nome_medico = medico['nome']

            data_db_format = datetime.strptime(data_str, "%d/%m/%Y").strftime("%Y-%m-%d")
            cursor.execute("SELECT id_data FROM datas WHERE data = %s", (data_db_format,))
            data = cursor.fetchone()
            if not data:
                dispatcher.utter_message(text=f"Desculpe, ocorreu um erro: a data '{data_str}' não foi encontrada no sistema.")
                return []
            id_data = data['id_data']

            hora_db_format = f"{hora_str}:00"
            cursor.execute("SELECT id_horario FROM horarios WHERE hora = %s", (hora_db_format,))
            horario = cursor.fetchone()
            if not horario:
                dispatcher.utter_message(text=f"Desculpe, ocorreu um erro: o horário '{hora_str}' não foi encontrado no sistema.")
                return []
            id_horario = horario['id_horario']

            motivo_consulta = tracker.get_slot("symptoms") or "Rotina"
            sql_insert = "INSERT INTO consultas (id_data, id_horario, id_especialidade, id_medico, motivo_consulta, nome_paciente, email_paciente) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_insert, (id_data, id_horario, id_especialidade, id_medico, motivo_consulta, nome_paciente, email_paciente))
            
            sql_update_agenda = "UPDATE agenda SET disponivel = FALSE WHERE id_data = %s AND id_horario = %s AND id_medico = %s"
            cursor.execute(sql_update_agenda, (id_data, id_horario, id_medico))
            conn.commit()

            patient_data_summary = {'patient_name': nome_paciente, 'requested_specialty': especialidade_nome, 'appointment_date': data_str, 'appointment_time': hora_str, 'doctor_name': nome_medico, 'clinic_name': CLINICA_NOME}
            summary = gemini_service.generate_appointment_summary(patient_data_summary)
            tips = gemini_service.generate_preparation_tips(especialidade_nome)

            confirmation_message = f"✅ Agendamento Salvo com Sucesso no sistema!\n\n{summary}\n\n"
            confirmation_message += "Ótimo! Antes de finalizarmos, aqui estão algumas dicas para sua consulta:\n"
            confirmation_message += tips

            dispatcher.utter_message(text=confirmation_message)
            
            # ▼▼▼ LINHA REMOVIDA DAQUI ▼▼▼
            # dispatcher.utter_message(response="utter_goodbye")

        except Exception as e:
            logger.error(f"Erro ao agendar no banco de dados: {e}")
            dispatcher.utter_message(text="Ocorreu um erro ao tentar salvar seu agendamento.")
        finally:
            if conn and conn.is_connected():
                conn.close()
                logger.info("Conexão com o MySQL foi fechada.")
        return [SlotSet(s, None) for s in tracker.slots if s not in ["session_started_metadata"]]

class ActionShowAvailableTimes(Action):
    def name(self) -> Text:
        return "action_show_available_times"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        specialty = tracker.get_slot("requested_specialty")
        date_str = tracker.get_slot("appointment_date")
        if not date_str or not specialty:
            dispatcher.utter_message(text="Para eu ver os horários, preciso que você me informe primeiro a data e a especialidade desejada.")
            return []
        conn = create_connection()
        if not conn:
            dispatcher.utter_message(text="Não consigo verificar a agenda no momento, estou com um problema técnico.")
            return []
        try:
            cursor = conn.cursor(dictionary=True)
            date_db = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
            query = """
                SELECT TIME_FORMAT(h.hora, '%H:%i') AS hora_formatada FROM agenda a
                JOIN medicos m ON a.id_medico = m.id_medico
                JOIN especialidades e ON m.id_especialidade = e.id_especialidade
                JOIN datas d ON a.id_data = d.id_data
                JOIN horarios h ON a.id_horario = h.id_horario
                WHERE e.nome = %s AND d.data = %s AND a.disponivel = TRUE
                ORDER BY h.hora ASC
            """
            cursor.execute(query, (specialty, date_db))
            available_times = [row['hora_formatada'] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Erro ao buscar horários disponíveis: {e}")
            dispatcher.utter_message(text="Tive um problema ao consultar os horários.")
            return []
        finally:
            if conn.is_connected():
                conn.close()
        if available_times:
            times_string = ", ".join(available_times)
            message = f"Claro! Para o dia {date_str}, tenho os seguintes horários livres para {specialty}: {times_string}."
            dispatcher.utter_message(text=message)
        else:
            message = f"Puxa, parece que não tenho horários disponíveis para {specialty} no dia {date_str}. Gostaria de tentar outra data?"
            dispatcher.utter_message(text=message)
        return []


class ValidateAppointmentForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_appointment_form"

    def validate_patient_name(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        name = slot_value.strip()
        if len(name.split()) >= 2:
            return {"patient_name": name}
        dispatcher.utter_message(text="Por favor, informe seu nome completo.")
        return {"patient_name": None}

    def validate_patient_email(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        if re.match(r"[^@]+@[^@]+\.[^@]+", slot_value):
            return {"patient_email": slot_value}
        dispatcher.utter_message(text="Por favor, informe um e-mail válido (ex: nome@exemplo.com).")
        return {"patient_email": None}

    def validate_appointment_date(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        try:
            settings = {'PREFER_DATES_FROM': 'future', 'DATE_ORDER': 'DMY'}
            date_obj = dateparser.parse(slot_value, languages=['pt'], settings=settings)
            if not date_obj:
                dispatcher.utter_message(text="Não consegui entender essa data. Por favor, tente novamente.")
                return {"appointment_date": None}
            if date_obj.date() < datetime.now().date():
                dispatcher.utter_message(text="Esta data já passou. Por favor, escolha uma data a partir de hoje.")
                return {"appointment_date": None}
            if date_obj.weekday() >= 5:
                dispatcher.utter_message(text="Desculpe, não funcionamos nos finais de semana (sábado e domingo).")
                return {"appointment_date": None}
            return {"appointment_date": date_obj.strftime("%d/%m/%Y")}
        except Exception as e:
            logger.error(f"Erro na validação da data: {e}")
            dispatcher.utter_message(text="Tive um problema ao processar a data. Tente de outra forma.")
            return {"appointment_date": None}

    def validate_appointment_time(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        try:
            time_obj = dateparser.parse(slot_value, languages=['pt'])
            if not time_obj:
                dispatcher.utter_message(text="Não consegui entender esse horário. Tente novamente (ex: '14:30').")
                return {"appointment_time": None}
            
            time_str = time_obj.strftime("%H:%M")
            date_str = tracker.get_slot("appointment_date")
            specialty = tracker.get_slot("requested_specialty")

            dispatcher.utter_message(response="utter_checking_availability", time=time_str)

            conn = create_connection()
            if not conn:
                dispatcher.utter_message(text="Não consigo verificar a agenda no momento.")
                return {"appointment_time": None}
            
            is_available = False
            try:
                cursor = conn.cursor(dictionary=True)
                date_db = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
                time_db = f"{time_str}:00"
                
                query = """
                    SELECT a.disponivel FROM agenda a
                    JOIN medicos m ON a.id_medico = m.id_medico
                    JOIN especialidades e ON m.id_especialidade = e.id_especialidade
                    JOIN datas d ON a.id_data = d.id_data
                    JOIN horarios h ON a.id_horario = h.id_horario
                    WHERE e.nome = %s AND d.data = %s AND h.hora = %s
                """
                cursor.execute(query, (specialty, date_db, time_db))
                result = cursor.fetchone()

                if result and result['disponivel']:
                    is_available = True

                if is_available:
                    return {"appointment_time": time_str}
                else:
                    query_disponiveis = """
                        SELECT TIME_FORMAT(h.hora, '%H:%i') AS hora_formatada FROM agenda ag
                        JOIN horarios h ON ag.id_horario = h.id_horario
                        JOIN datas d ON ag.id_data = d.id_data
                        WHERE d.data = %s AND ag.disponivel = TRUE
                        ORDER BY h.hora
                    """
                    cursor.execute(query_disponiveis, (date_db,))
                    horarios_disponiveis = [row['hora_formatada'] for row in cursor.fetchall()]

                    if horarios_disponiveis:
                        msg = f"O horário das {time_str} não está disponível. 😕\nMas para o dia {date_str}, tenho estes horários livres:\n**{', '.join(horarios_disponiveis)}**\n\nQual deles você prefere?"
                        dispatcher.utter_message(text=msg)
                    else:
                        dispatcher.utter_message(text=f"Puxa, não temos mais horários para {specialty} no dia {date_str}. Você gostaria de tentar outra data?")
                    return {"appointment_time": None}

            finally:
                if conn.is_connected():
                    conn.close()

        except Exception as e:
            logger.error(f"Erro na validação de horário: {e}")
            dispatcher.utter_message(text="Tive um problema ao processar o horário.")
            return {"appointment_time": None}

    def validate_requested_specialty(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        conn = create_connection()
        if not conn:
            dispatcher.utter_message(text="Não consigo verificar as especialidades no momento.")
            return {"requested_specialty": None}
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT nome FROM especialidades")
            especialidades_db = {esp['nome'].lower(): esp['nome'] for esp in cursor.fetchall()}
        finally:
            if conn.is_connected():
                conn.close()

        valor_normalizado = slot_value.lower().strip()
        if valor_normalizado in especialidades_db:
            return {"requested_specialty": especialidades_db[valor_normalizado]}
        
        dispatcher.utter_message(text=f"Desculpe, não temos a especialidade '{slot_value}'. Oferecemos: {', '.join(especialidades_db.values())}.")
        return {"requested_specialty": None}


class ActionHandleFormInterruption(Action):
    def name(self) -> Text:
        return "action_handle_form_interruption"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Ok, cancelei o agendamento. Se precisar de mais alguma coisa, é só chamar.")
        return [ActiveLoop(None), SlotSet("appointment_time", None), SlotSet("appointment_date", None)]


class ActionProvidePrepTips(Action):
    def name(self) -> Text:
        return "action_provide_prep_tips"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # A lógica de dicas agora está unificada na ActionScheduleAppointment
        # Mantemos a ação para não quebrar regras/histórias existentes
        return []
