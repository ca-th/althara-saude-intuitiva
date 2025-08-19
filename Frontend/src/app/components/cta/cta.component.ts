import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-cta',
  standalone: true, // <-- ADICIONAMOS ESTA LINHA
  imports: [],      // <-- E ESTA (pode ser necessária no futuro)
  templateUrl: './cta.component.html',
  styleUrls: ['./cta.component.css']
})
export class CtaComponent {

  // 1. Criamos o evento que será emitido para o componente pai (AppComponent)
  @Output() agendarConsulta = new EventEmitter<void>();

  constructor() { }

  // 2. Esta função é chamada quando o botão no HTML é clicado
  onAgendarClick(): void {
    console.log('Botão do CTA clicado. Emitindo evento agendarConsulta...');
    // 3. Aqui nós emitimos o sinal para abrir o chat
    this.agendarConsulta.emit();
    setTimeout(() => {
  const ctaSection = document.getElementById('cta-section');
  if (ctaSection) {
    ctaSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}, 300);
  }
}
