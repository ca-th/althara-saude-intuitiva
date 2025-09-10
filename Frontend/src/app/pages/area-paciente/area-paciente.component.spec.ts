import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AreaPacienteComponent } from './area-paciente.component';

describe('AreaPacienteComponent', () => {
  let component: AreaPacienteComponent;
  let fixture: ComponentFixture<AreaPacienteComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AreaPacienteComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AreaPacienteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
