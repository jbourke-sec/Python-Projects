import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VulndashboardComponent } from './vulndashboard.component';

describe('VulndashboardComponent', () => {
  let component: VulndashboardComponent;
  let fixture: ComponentFixture<VulndashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ VulndashboardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(VulndashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
