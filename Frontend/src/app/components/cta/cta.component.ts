import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-cta',
  standalone: true,
  imports: [],
  templateUrl: './cta.component.html',
  styleUrls: ['./cta.component.css']
})
export class CtaComponent {


  @Output() agendarConsulta = new EventEmitter<void>();

  constructor() { }


  onAgendarClick(): void {
    console.log('Botão do CTA clicado. Emitindo evento agendarConsulta...');

    this.agendarConsulta.emit();
    setTimeout(() => {
  const ctaSection = document.getElementById('cta-section');
  if (ctaSection) {
    ctaSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}, 300);
  }
}
