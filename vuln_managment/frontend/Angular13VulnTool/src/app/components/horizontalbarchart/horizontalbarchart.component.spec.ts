import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HorizontalbarchartComponent } from './horizontalbarchart.component';

describe('HorizontalbarchartComponent', () => {
  let component: HorizontalbarchartComponent;
  let fixture: ComponentFixture<HorizontalbarchartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HorizontalbarchartComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HorizontalbarchartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
