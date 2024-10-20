import { formatDate } from '@angular/common';
import { Component, Inject, Input, OnInit } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Playbook } from 'src/app/models/playbook.model';
import { Tickets } from 'src/app/models/tickets.model';
import { Vulnerability } from 'src/app/models/vulnerability.model';
import { TicketsService } from 'src/app/services/tickets.service';


@Component({
  selector: 'app-new-ticket',
  templateUrl: './new-ticket.component.html',
  styleUrls: ['./new-ticket.component.css']
})


export class AddTicketComponent implements OnInit {


  @Input() currentVuln: Vulnerability = {
    vulnid: "",
    assetid: [],
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
  };
  ticket: Tickets = {
    ticketNumber: '',
    summary: '',
    validatedsummary: '',
    verifiedsummary: '',
    rolledsummary: '',
    progress: '',
    assignedTo: '',
    group: '',
    timeStarted: undefined,
    timeClosed: undefined,
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
    outcome: '',
    playbookid: {},
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

  currentCve = '';

  vulnerabilities?: Vulnerability[];

  playbooks?: Playbook[];

  submitted = false;
  vulnqueue: boolean = false;
  hours: number = 0;
  minutes: number = 0;
  secsinhour: number = 3600;
  secsinmin: number = 60;
  constructor(private ticketService: TicketsService, public dialogRef: MatDialogRef<AddTicketComponent>,
    @Inject(MAT_DIALOG_DATA) public data: string,
    public matDialog: MatDialog) { }

  ngOnInit(): void {console.log(this.data);
    if (this.data)
    {
      this.getVuln(this.data);
      this.vulnqueue = true;

    }
    this.getVulnerabilities();
    this.getPlaybooks();
  }

  saveTicket(): void {
    if(this.vulnqueue)
    {
      this.ticket.cve = this.currentVuln.cve;
    }
    const data = {
      ticketNumber: this.ticket.ticketNumber,
      summary: this.ticket.summary,
      progress: this.ticket.progress,
      assignedTo: this.ticket.playbookid!.patchacquirement!,
      group: this.ticket.playbookid!.patchacquirement!,
      timeStarted: this.ticket.timeStarted,
      timeClosed: this.ticket.timeClosed,
      cve: this.ticket.cve,
      vulnid: undefined,
      cvss: 0,
      qa: this.ticket.qa,
      sla: ((this.hours * this.secsinhour) + (this.minutes * this.secsinmin)),
      exposure: this.ticket.exposure,
      threat: this.ticket.threat,
      playbookid: this.ticket.playbookid
    };
    console.log(data)

    this.ticketService.createTicket(data)
      .subscribe({
        next: (res) => {
          console.log(res);
          this.submitted = true;
        },
        error: (e) => console.error(e)
      });
  }
  getVulnerabilities(): void {
    this.ticketService.unremediatedVuln()
    .subscribe({
      next: (data) => {
        this.vulnerabilities = data;
        console.log(data);
      },
      error: (e) => console.error(e)
    });
  }
  getPlaybooks(): void {
    this.ticketService.getPlays()
    .subscribe({
      next: (data) => {
      this.playbooks = data;
      console.log(data);
    },
    error: (e) => console.error(e)
   });
  }
  getVuln(id: any): void {
    this.ticketService.getVuln(id)
    .subscribe({
      next: (data) => {
      this.currentVuln = data;
      console.log(data);
    },
    error: (e) => console.error(e)
   });
  }
  newTicket(): void {
    this.submitted = false;
    this.ticket = {
      ticketNumber: '',
      summary: '',
      validatedsummary: '',
      verifiedsummary: '',
      rolledsummary: '',
      progress: '',
      assignedTo: '',
      group: '',
      timeStarted: '',
      timeClosed: undefined,
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
      },
      cvss: '',
      qa: '',
      sla: undefined,
      exposure: '',
      threat: '',
      assets: [],
      outcome: '',
      playbookid: {},
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
  }

}