import { Component } from '@angular/core';
import { CommonModule } from '@angular/common'; // Para usar *ngIf
import { trigger, state, style, transition, animate } from '@angular/animations';

// Importa todos os componentes que o home.component.html usa
import { HeroComponent } from '../components/hero/hero.component';
import { AboutComponent } from '../components/about/about.component';
import { CtaComponent } from '../components/cta/cta.component';
import { ChatComponent } from '../components/chat/chat.component';
import { EspecialidadesComponent } from '../components/especialidades/especialidades.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,    // <-- Adicionado
    HeroComponent,   // <-- Adicionado  // <-- Adicionado
    CtaComponent,
    EspecialidadesComponent,    // <-- Adicionado
    ChatComponent    // <-- Adicionado
  ],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  animations: [
    trigger('fadeIn', [
      state('void', style({ opacity: 0, transform: 'translateY(20px)' })),
      transition('void => *', [
        animate('800ms ease-out')
      ])
    ])
  ]
})
export class HomeComponent {
  conteudoVisivel = false;
  chatAberto = false;

  mostrarConteudoPrincipal() {
    this.conteudoVisivel = true;
    setTimeout(() => {
      document.getElementById('conteudo-principal')?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  }

  abrirChat() {
    this.chatAberto = true;
  }

  fecharChat() {
    this.chatAberto = false;
  }
}
