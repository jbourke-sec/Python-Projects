import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CloseTicketDialogComponent } from './close-ticket-dialog.component';

describe('CloseTicketDialogComponent', () => {
  let component: CloseTicketDialogComponent;
  let fixture: ComponentFixture<CloseTicketDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CloseTicketDialogComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CloseTicketDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
