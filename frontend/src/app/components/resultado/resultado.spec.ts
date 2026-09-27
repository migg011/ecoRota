import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Resultado } from './resultado';

describe('Resultado', () => {
  let component: Resultado;
  let fixture: ComponentFixture<Resultado>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Resultado],
    }).compileComponents();

    fixture = TestBed.createComponent(Resultado);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
