import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DescricaoResiduo } from './descricao-residuo';

describe('DescricaoResiduo', () => {
  let component: DescricaoResiduo;
  let fixture: ComponentFixture<DescricaoResiduo>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DescricaoResiduo],
    }).compileComponents();

    fixture = TestBed.createComponent(DescricaoResiduo);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
