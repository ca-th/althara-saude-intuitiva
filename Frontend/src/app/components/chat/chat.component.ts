// No arquivo: src/app/components/chat/chat.component.ts

import { Component, EventEmitter, Output, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
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
export class ChatComponent implements AfterViewChecked {
  @ViewChild('chatMessagesContainer') private chatContainer!: ElementRef;
  @Output() closeChat = new EventEmitter<void>();

  messages: Message[] = [];
  currentUserMessage = '';
  isLoading = false;
  private shouldScroll = false; // <-- Variável para controlar a rolagem

  constructor(private chatService: ChatService) {}

  ngAfterViewChecked() {
    // Só rola a tela se a gente pedir, para ser mais eficiente
    if (this.shouldScroll) {
      this.scrollToBottom();
      this.shouldScroll = false;
    }
  }

  sendMessage(): void {
    if (!this.currentUserMessage.trim()) return;

    this.addMessage(this.currentUserMessage, 'user');
    const userMessageToSend = this.currentUserMessage;
    this.currentUserMessage = '';
    this.isLoading = true;

    this.chatService.sendMessage(userMessageToSend).subscribe({
      next: (apiResponse: ChatApiResponse) => {
        this.isLoading = false;
        // --- ESTA É A MUDANÇA PRINCIPAL ---
        // Pega a resposta longa, divide pelas quebras de linha
        const botMessages = apiResponse.response.split('\n').filter(line => line.trim() !== '');

        // Adiciona cada parte como uma mensagem separada, com um pequeno atraso
        botMessages.forEach((msg, index) => {
          setTimeout(() => {
            this.addMessage(msg, 'bot');
          }, 400 * (index + 1)); // Atraso de 400ms entre cada mensagem
        });
      },
      error: (err: any) => {
        this.isLoading = false;
        this.addMessage('Erro ao conectar com o assistente. Tente novamente.', 'bot');
        console.error(err);
      }
    });
  }

  // Função auxiliar para adicionar mensagens e pedir a rolagem
  private addMessage(text: string, sender: 'user' | 'bot'): void {
    this.messages.push({ text, sender });
    this.shouldScroll = true;
  }

  close(): void {
    this.closeChat.emit();
  }

  private scrollToBottom(): void {
    try {
      this.chatContainer.nativeElement.scrollTop = this.chatContainer.nativeElement.scrollHeight;
    } catch (err) {}
  }
}
