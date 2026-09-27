import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Processamento } from './processamento';

describe('Processamento', () => {
  let component: Processamento;
  let fixture: ComponentFixture<Processamento>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Processamento],
    }).compileComponents();

    fixture = TestBed.createComponent(Processamento);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
