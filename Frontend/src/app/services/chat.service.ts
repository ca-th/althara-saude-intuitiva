import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ChatApiResponse {
  response: string;
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {

  private apiUrl = 'http://localhost:8000/chat';

  constructor(private http: HttpClient) { }

  /**
   * Envia uma mensagem do usuário para a API do chatbot.
   * @param userMessage A mensagem digitada pelo usuário.
   * @returns Um Observable com a resposta da API.
   */
  sendMessage(userMessage: string): Observable<ChatApiResponse> {

    const payload = { message: userMessage };

    return this.http.post<ChatApiResponse>(this.apiUrl, payload);
  }
}
