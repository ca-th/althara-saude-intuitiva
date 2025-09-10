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


  constructor(private router: Router) { }


  irParaHome(): void {

    if (this.router.url === '/') {

      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {

      this.router.navigate(['/']);
    }
  }
}
