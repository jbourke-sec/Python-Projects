import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QaTicketDialogComponent } from './qa-ticket-dialog.component';

describe('QaTicketDialogComponent', () => {
  let component: QaTicketDialogComponent;
  let fixture: ComponentFixture<QaTicketDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ QaTicketDialogComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(QaTicketDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
