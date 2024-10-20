import { Component, Inject, Input, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { Tickets } from 'src/app/models/tickets.model';
import { TicketsService } from 'src/app/services/tickets.service';

@Component({
  selector: 'app-reopen-ticket-dialog',
  templateUrl: './reopen-ticket-dialog.component.html',
  styleUrls: ['./reopen-ticket-dialog.component.css']
})
export class ReopenTicketDialogComponent implements OnInit {

  @Input() currentTicket: Tickets = {
    ticketNumber: '',
    summary: '',
    validatedsummary: '',
    verifiedsummary: '',
    rolledsummary: '',
    progress: '',
    assignedTo: '',
    group: '',
    timeStarted: '',
    timeClosed: '',
    cve: '',
    vulnid: {
      vulnid: "",
      assetid: undefined,
      threat: "",
      cve: '',
      cpe: '',
      risk: '',
      baseSLA: undefined,
      cwe: '',
      mav: '',
      mac: '',
      mpr: '',
      mui: '',
      ms: '',
      mc: '',
      mi: '',
      ma: '',
      rl: '',
      rc: '',
      ecm: ''
    },
    cvss: '',
    qa: '',
    sla: undefined,
    exposure: '',
    threat: '',
    assets: [],
    outcome:'',
    playbookid: {
      playbookid: '',
    category: '',
    patchacquirement: '',
    patchvalidation: '',
    verification: '',
    rollout: '',
    notes: '',
    },
    acquired: undefined,
    validated: undefined,
    verified: undefined,
    rolledout: undefined,
    enscore: '',
    iscbase: '',
    temporal: '',
    exploitScore: '',
    iscmodified: '',
    impactModScore: '',
    impactScore: '',
    environmentalScore: '',
  };
  constructor(private ticketService: TicketsService,
    private route: ActivatedRoute,
    private router: Router,
    public dialogRef: MatDialogRef<ReopenTicketDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: string,
    public matDialog: MatDialog) { }

  ngOnInit(): void {
    this.getTicket(this.data);
  }
  getTicket(ticketnumber: string): void {
    this.ticketService.getTicket(ticketnumber)
      .subscribe({
        next: (data) => {
          this.currentTicket = data;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
    }
    updateTicket(): void {
      this.ticketService.updateTicket(this.currentTicket.ticketNumber, this.currentTicket)
        .subscribe({
          next: (res) => {
            console.log(res);
          },
          error: (e) => console.error(e)
        });
    }
    onNoClick(): void {
      this.dialogRef.close();
    }
    onClick(): void {
      this.currentTicket.progress='In Progress';
      this.currentTicket.qa='';
      this.currentTicket.group = this.currentTicket.playbookid!.patchacquirement!
      this.currentTicket.acquired = false;
      this.currentTicket.verified = false;
      this.currentTicket.validated = false;
      this.currentTicket.rolledout = false;
      this.updateTicket()
      this.dialogRef.close();
    }

}
