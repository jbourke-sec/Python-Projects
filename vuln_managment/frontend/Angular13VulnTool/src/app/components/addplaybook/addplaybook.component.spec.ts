import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddplaybookComponent } from './addplaybook.component';

describe('AddplaybookComponent', () => {
  let component: AddplaybookComponent;
  let fixture: ComponentFixture<AddplaybookComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddplaybookComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddplaybookComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
