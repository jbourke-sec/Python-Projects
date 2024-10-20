import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NumberchartComponent } from './numberchart.component';

describe('NumberchartComponent', () => {
  let component: NumberchartComponent;
  let fixture: ComponentFixture<NumberchartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NumberchartComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NumberchartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
