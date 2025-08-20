import { Component } from '@angular/core';
import { RouterModule, Router } from '@angular/router'; // 1. IMPORTE O ROUTER
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {

  // 2. INJETE O ROUTER NO CONSTRUTOR
  constructor(private router: Router) { }

  // 3. CRIE A NOVA FUNÇÃO
  irParaHome(): void {
    // Verifica se a URL atual já é a da página inicial
    if (this.router.url === '/') {
      // Se for, apenas rola a janela para o topo suavemente
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      // Se não for, usa o roteador para navegar para a página inicial
      this.router.navigate(['/']);
    }
  }
}
