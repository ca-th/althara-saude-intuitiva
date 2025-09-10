import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-hero',
  templateUrl: './hero.component.html',
  styleUrls: ['./hero.component.css']
})
export class HeroComponent {
  @Output() vamosComecar = new EventEmitter<void>();

  constructor() { }

  onComecarClick(): void {
    console.log('Botão "Começar" clicado no HeroComponent (filho). Emitindo evento...');
    this.vamosComecar.emit();
  }
}
