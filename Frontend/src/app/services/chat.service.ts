import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// Esta interface define o formato da resposta que esperamos da sua API
export interface ChatApiResponse {
  response: string;
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  // URL da sua API FastAPI. Verifique se a porta (8000) está correta.
  private apiUrl = 'http://localhost:8000/chat';

  constructor(private http: HttpClient) { }

  /**
   * Envia uma mensagem do usuário para a API do chatbot.
   * @param userMessage A mensagem digitada pelo usuário.
   * @returns Um Observable com a resposta da API.
   */
  sendMessage(userMessage: string): Observable<ChatApiResponse> {
    // O corpo (payload) da requisição, conforme esperado pela sua API
    const payload = { message: userMessage };

    // Faz a requisição POST para a sua API e espera uma resposta do tipo ChatApiResponse
    return this.http.post<ChatApiResponse>(this.apiUrl, payload);
  }
}
