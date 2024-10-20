import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SlatimerComponent } from './slatimer.component';

describe('SlatimerComponent', () => {
  let component: SlatimerComponent;
  let fixture: ComponentFixture<SlatimerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SlatimerComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SlatimerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
