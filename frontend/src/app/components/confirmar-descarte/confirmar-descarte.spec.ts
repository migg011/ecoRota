import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ConfirmarDescarte } from './confirmar-descarte';

describe('ConfirmarDescarte', () => {
  let component: ConfirmarDescarte;
  let fixture: ComponentFixture<ConfirmarDescarte>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConfirmarDescarte],
    }).compileComponents();

    fixture = TestBed.createComponent(ConfirmarDescarte);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
