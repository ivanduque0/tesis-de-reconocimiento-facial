import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SeleccionarcontratoComponent } from './seleccionarcontrato.component';

describe('SeleccionarcontratoComponent', () => {
  let component: SeleccionarcontratoComponent;
  let fixture: ComponentFixture<SeleccionarcontratoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SeleccionarcontratoComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SeleccionarcontratoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
