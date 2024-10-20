import { Component, Inject, Input, OnInit} from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { Tickets } from 'src/app/models/tickets.model';
import { TicketsService } from 'src/app/services/tickets.service';

@Component({
  selector: 'app-close-ticket-dialog',
  templateUrl: './close-ticket-dialog.component.html',
  styleUrls: ['./close-ticket-dialog.component.css']
})
export class CloseTicketDialogComponent implements OnInit{

  closeOptions: any[] = [
    {value: 'Remediated', viewValue: 'Remediated'},
    {value: 'Mitigated', viewValue: 'Mitigated'}, 
    {value: 'Accepted Risk', viewValue: 'Accepted Risk'},
  ];
  closeOptionsUncomplete: any = {value: 'Accepted Risk', viewValue: 'Accepted Risk'}

  constructor(private ticketService: TicketsService,
    private route: ActivatedRoute,
    private router: Router,
    public dialogRef: MatDialogRef<CloseTicketDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: string,
    @Inject(MAT_DIALOG_DATA) public rollout: boolean,
    public matDialog: MatDialog) { }
  ngOnInit(): void {
    console.log(this.data);
  }

  onClose(): void {

  }

}
