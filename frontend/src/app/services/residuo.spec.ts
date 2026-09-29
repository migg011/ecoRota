import { TestBed } from '@angular/core/testing';
import { Residuo } from './residuo';

describe('Residuo', () => {
  let service: Residuo;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Residuo);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
