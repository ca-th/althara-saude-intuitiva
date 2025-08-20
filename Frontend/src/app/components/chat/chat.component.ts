// Arquivo: src/app/components/chat/chat.component.ts

// 1. ADICIONE ViewChild, ElementRef, e AfterViewChecked NAS IMPORTAÇÕES
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
// 2. FAÇA O COMPONENTE "IMPLEMENTAR" AfterViewChecked
export class ChatComponent implements AfterViewChecked {
  // 3. ADICIONE O @ViewChild PARA CRIAR UMA REFERÊNCIA AO ELEMENTO DO HTML
  @ViewChild('chatMessagesContainer') private chatContainer!: ElementRef;

  @Output() closeChat = new EventEmitter<void>();

  messages: Message[] = [];
  currentUserMessage = '';
  isLoading = false;

  constructor(private chatService: ChatService) {}

  // 4. ADICIONE ESTE MÉTODO: ele roda sempre que o Angular atualiza a tela
  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  sendMessage(): void {
    if (!this.currentUserMessage.trim()) {
      return;
    }

    this.messages.push({ text: this.currentUserMessage, sender: 'user' });
    const userMessageToSend = this.currentUserMessage;
    this.currentUserMessage = '';
    this.isLoading = true;

    this.chatService.sendMessage(userMessageToSend).subscribe({
      next: (apiResponse: ChatApiResponse) => {
        this.messages.push({ text: apiResponse.response, sender: 'bot' });
        this.isLoading = false;
      },
      error: (err: any) => {
        this.messages.push({ text: 'Erro ao conectar com o assistente. Tente novamente.', sender: 'bot' });
        this.isLoading = false;
        console.error(err);
      }
    });
  }

  close(): void {
    this.closeChat.emit();
  }

  // 5. SUA FUNÇÃO scrollToBottom, AGORA SEPARADA E NO LUGAR CORRETO
  private scrollToBottom(): void {
    try {
      this.chatContainer.nativeElement.scrollTop = this.chatContainer.nativeElement.scrollHeight;
    } catch (err) {
      // Apenas para evitar erros caso o container não exista ainda
    }
  }
}
