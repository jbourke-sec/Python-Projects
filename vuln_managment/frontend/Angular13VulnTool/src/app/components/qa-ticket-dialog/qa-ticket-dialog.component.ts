import { Component, Inject, Input, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { Tickets } from 'src/app/models/tickets.model';
import { TicketsService } from 'src/app/services/tickets.service';
import { TokenStorageService } from 'src/app/_services/token-storage.service';

@Component({
  selector: 'app-qa-ticket-dialog',
  templateUrl: './qa-ticket-dialog.component.html',
  styleUrls: ['./qa-ticket-dialog.component.css']
})
export class QaTicketDialogComponent implements OnInit {

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
      ecm: '',
      description: '',
      dayZero: '',
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
    public dialogRef: MatDialogRef<QaTicketDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: string,
    public matDialog: MatDialog, public tokenStorage: TokenStorageService,) { }

  ngOnInit(): void {
    if (!this.tokenStorage.getToken()) {
      this.router.navigate(['/login']);
    }
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
      this.updateTicket()
      this.dialogRef.close();
    }

}
