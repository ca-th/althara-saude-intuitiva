import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, Especialidade, Medico } from '../../services/api.service';

@Component({
  selector: 'app-especialidades',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './especialidades.component.html',
  styleUrls: ['./especialidades.component.css']
})
export class EspecialidadesComponent implements OnInit {

  especialidades: Especialidade[] = [];


  especialidadeSelecionadaId: number | null = null;
  medicosDaEspecialidade: Medico[] = [];
  isLoadingMedicos = false;

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.apiService.getEspecialidades().subscribe(dados => {
      this.especialidades = dados;
    });
  }


  onEspecialidadeClick(especialidade: Especialidade): void {

    if (this.especialidadeSelecionadaId === especialidade.id_especialidade) {
      this.especialidadeSelecionadaId = null;
      this.medicosDaEspecialidade = [];
      return;
    }

    this.isLoadingMedicos = true;
    this.especialidadeSelecionadaId = especialidade.id_especialidade;
    this.medicosDaEspecialidade = [];

    this.apiService.getMedicosPorEspecialidade(especialidade.id_especialidade)
      .subscribe(medicos => {
        this.medicosDaEspecialidade = medicos;
        this.isLoadingMedicos = false;
      });
  }
}
