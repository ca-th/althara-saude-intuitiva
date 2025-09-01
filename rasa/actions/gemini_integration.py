import google.generativeai as genai
import json
import os

class GeminiIntegration:
    def __init__(self):
        """
        Inicializa a integração com a API do Gemini.
        """
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("A variável de ambiente GEMINI_API_KEY não foi definida.")
            genai.configure(api_key=api_key)
            
            self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
        except Exception as e:
            print(f"Erro ao inicializar o Gemini: {e}")
            self.model = None

    def analyze_symptoms(self, symptoms: list, available_specialties: list):
        """
        Analisa os sintomas e recomenda uma especialidade médica a partir de uma lista fornecida.
        """
        if not self.model:
            return None

        specialties_list_str = ", ".join(f"'{item}'" for item in available_specialties)

        prompt = f"""
            Você é um assistente de triagem médica. Analise os seguintes sintomas: {', '.join(symptoms)}.
            Com base neles, recomende a especialidade médica mais apropriada da seguinte lista ESTRITA: [{specialties_list_str}].
            NÃO recomende, sob NENHUMA hipótese, uma especialidade que não esteja nesta lista.
            Se os sintomas forem muito genéricos, como 'febre' ou 'mal-estar', priorize 'Clínico Geral' se estiver na lista.
            
            Retorne um JSON com as seguintes chaves:
            - "specialty": A especialidade escolhida da lista.
            - "urgency": A urgência (Baixa, Média, Alta).
            - "explanation": Uma breve explicação do porquê a especialidade foi recomendada (máximo 2 frases).
        """
        try:
            response = self.model.generate_content(prompt)
            cleaned_response = response.text.strip().replace('`', '').replace('json', '')
            return json.loads(cleaned_response)
        except Exception as e:
            print(f"Erro ao analisar sintomas com Gemini: {e}")
            return None

    def generate_appointment_summary(self, data: dict):
        """
        Gera um resumo de confirmação de agendamento.
        """
        if not self.model:
            return "Resumo indisponível no momento."

        prompt = f"""
            Crie um breve e-mail de confirmação de agendamento em tom formal e amigável.
            Use os seguintes dados:
            - Nome do Paciente: {data.get('patient_name')}
            - Especialidade: {data.get('requested_specialty')}
            - Médico: {data.get('doctor_name')}
            - Data: {data.get('appointment_date')}
            - Hora: {data.get('appointment_time')}
            - Nome da Clínica: {data.get('clinic_name')}

            O texto deve incluir uma saudação (Ex: Prezado(a) Sr(a).), confirmar os detalhes, mencionar para entrar em contato se precisar reagendar, e uma despedida cordial assinada pelo nome da clínica.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Erro ao gerar resumo com Gemini: {e}")
            return "Ocorreu um erro ao gerar a confirmação."

    def generate_preparation_tips(self, specialty: str):
        """
        Gera dicas de preparação para uma consulta com base na especialidade.
        """
        if not self.model:
            return "Dicas indisponíveis no momento."
            
        prompt = f"""
            Liste 2 ou 3 dicas breves e úteis para um paciente que se prepara para uma consulta de {specialty}.
            As dicas devem ser práticas (ex: 'anote seus sintomas', 'leve exames anteriores', 'faça uma lista de medicamentos').
            Formate como um parágrafo único.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Erro ao gerar dicas com Gemini: {e}")
            return "Não foi possível gerar as dicas de preparação."