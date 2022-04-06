import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AgregarcontratoComponent } from './agregarcontrato.component';

describe('AgregarcontratoComponent', () => {
  let component: AgregarcontratoComponent;
  let fixture: ComponentFixture<AgregarcontratoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AgregarcontratoComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AgregarcontratoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
