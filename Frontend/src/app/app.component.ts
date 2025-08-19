import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';

// Componentes standalone
import { NavbarComponent } from './components/navbar/navbar.component';
import { HeroComponent } from './components/hero/hero.component';
import { AboutComponent } from './components/about/about.component';
import { CtaComponent } from './components/cta/cta.component';
import { ContatoComponent } from './contato/contato.component';
import { ChatComponent } from './components/chat/chat.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    NavbarComponent,
    HeroComponent,
    AboutComponent,
    CtaComponent,
    ContatoComponent,
    ChatComponent
  ],
  template: `
    <!--
      Este é o template do componente raiz.
      Ele decide o que é exibido na tela.
    -->
    <ng-container *ngIf="!chatAberto">
      <app-navbar (scrollToRequest)="handleScroll($event)"></app-navbar>
      <app-hero (vamosComecar)="mostrarConteudoPrincipal()"></app-hero>
    </ng-container>

    <!-- Mostra as seções de conteúdo apenas se 'conteudoVisivel' for true -->
    <app-about *ngIf="conteudoVisivel && !chatAberto"></app-about>
    <app-cta *ngIf="conteudoVisivel && !chatAberto" (agendarConsulta)="abrirChat()"></app-cta>
    <app-contato *ngIf="conteudoVisivel && !chatAberto"></app-contato>

    <!-- O chat é exibido apenas quando chatAberto é true -->
    <app-chat *ngIf="chatAberto"></app-chat>
  `,
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  chatAberto = false;
  conteudoVisivel = false;

  abrirChat() {
    console.log('abrirChat() foi chamado');
    this.chatAberto = true;
  }

  fecharChat() {
    console.log('fecharChat() foi chamado');
    this.chatAberto = false;
  }

  mostrarConteudoPrincipal() {
    console.log('Evento "vamosComecar" recebido. Mostrando conteúdo e rolando a tela...');
    this.conteudoVisivel = true;

    // Pequeno delay para garantir que o conteúdo esteja renderizado antes da rolagem
    setTimeout(() => {
      const aboutSection = document.getElementById('sobre-nos');
      if (aboutSection) {
        aboutSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 100);
  }

  handleScroll(event: string) {
    const target = document.getElementById(event);
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  }
}
