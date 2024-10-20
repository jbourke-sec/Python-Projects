import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReopenTicketDialogComponent } from './reopen-ticket-dialog.component';

describe('ReopenTicketDialogComponent', () => {
  let component: ReopenTicketDialogComponent;
  let fixture: ComponentFixture<ReopenTicketDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ReopenTicketDialogComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ReopenTicketDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
