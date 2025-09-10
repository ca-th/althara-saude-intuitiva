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
  private shouldScroll = false;

  constructor(private chatService: ChatService) {}

  ngAfterViewChecked() {

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

        const botMessages = apiResponse.response.split('\n').filter(line => line.trim() !== '');


        botMessages.forEach((msg, index) => {
          setTimeout(() => {
            this.addMessage(msg, 'bot');
          }, 400 * (index + 1));
        });
      },
      error: (err: any) => {
        this.isLoading = false;
        this.addMessage('Erro ao conectar com o assistente. Tente novamente.', 'bot');
        console.error(err);
      }
    });
  }


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
