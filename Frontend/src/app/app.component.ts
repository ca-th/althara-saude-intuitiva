import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';

// Importa apenas os componentes da "moldura"
import { NavbarComponent } from './components/navbar/navbar.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,     // <-- Essencial para o roteamento funcionar
    NavbarComponent
  ],
  // O template agora é apenas a "moldura" do site
  template: `
    <app-navbar></app-navbar>
    <router-outlet></router-outlet>
  `,
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  // A classe AppComponent fica vazia.
  // Toda a lógica de página foi movida para os componentes específicos.
}
