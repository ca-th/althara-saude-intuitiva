// Arquivo: src/app/components/chat/chat.component.ts

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
// CORREÇÃO 1: Ajustado o caminho para voltar duas pastas (de components/chat para app/)
import { ChatService, ChatApiResponse } from '../../services/chat.service';

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent {
  messages: Message[] = [];
  currentUserMessage = '';
  isLoading = false;

  constructor(private chatService: ChatService) {}

  sendMessage(): void {
    if (!this.currentUserMessage.trim()) {
      return;
    }

    this.messages.push({ text: this.currentUserMessage, sender: 'user' });
    const userMessageToSend = this.currentUserMessage;
    this.currentUserMessage = '';
    this.isLoading = true;

    this.chatService.sendMessage(userMessageToSend).subscribe({
      // CORREÇÃO 2: Adicionado o tipo para a resposta da API
      next: (apiResponse: ChatApiResponse) => {
        this.messages.push({ text: apiResponse.response, sender: 'bot' });
        this.isLoading = false;
      },
      // CORREÇÃO 3: Adicionado o tipo 'any' para o erro (pode ser mais específico se quiser)
      error: (err: any) => {
        this.messages.push({ text: 'Erro ao conectar com o assistente. Tente novamente.', sender: 'bot' });
        this.isLoading = false;
        console.error(err);
      }
    });
  }
}
