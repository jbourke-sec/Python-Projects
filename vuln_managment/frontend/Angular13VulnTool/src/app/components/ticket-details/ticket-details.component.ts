import { Component, OnInit, Input, Inject } from '@angular/core';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { Tickets } from 'src/app/models/tickets.model';
import { TicketsService } from 'src/app/services/tickets.service';
import { MatDialog, MatDialogConfig, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { AssetComponent } from '../asset/asset.component';
import { CloseTicketDialogComponent } from '../close-ticket-dialog/close-ticket-dialog.component';
import { Assets } from 'src/app/models/assets.model';
import { AssetAdditionComponent } from '../asset-addition/asset-addition.component';
import { TokenStorageService } from 'src/app/_services/token-storage.service';

@Component({
  selector: 'app-ticket-details',
  templateUrl: './ticket-details.component.html',
  styleUrls: ['./ticket-details.component.css']
})
export class TicketDetailsComponent implements OnInit {
  submit = false;

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
    patchacquirement: '',
    patchvalidation: '',
    verification: '',
    rollout: '',
    notes: '',
    },
    acquired: false,
    validated: false,
    verified: false,
    rolledout: false,
    enscore: '',
    iscbase: '',
    temporal: '',
    exploitScore: '',
    iscmodified: '',
    impactModScore: '',
    impactScore: '',
    environmentalScore: '',
  };

  args?: {
    outcome: '',
    rolledout: false,
  }
  assignList = [];
  Users?: string[];
  
  message = '';
  mySubscription: any;

  togglePa: boolean = true;
  toggleVa: boolean = false;
  toggleVe: boolean = false;
  toggleRo: boolean = false;

  addAssets?: Assets[];
  assettemp?: Assets[];

  constructor(
    private ticketService: TicketsService,
    private route: ActivatedRoute,
    private router: Router,
    public dialogRef: MatDialogRef<TicketDetailsComponent>,
    @Inject(MAT_DIALOG_DATA) public data: string,
    public matDialog: MatDialog,
    public tokenStorage: TokenStorageService) {
     }
    


  ngOnInit(): void {
    if (!this.tokenStorage.getToken()) {
      this.router.navigate(['/login']);
    }
      this.message = '';
      this.getTicket(this.data);//may be number
      this.getUsers();
      console.log(this.data)
      
  }
  ngOnDestroy() {
    if (this.mySubscription) {
      this.mySubscription.unsubscribe();
    }
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
    this.message = '';

    this.ticketService.updateTicket(this.currentTicket.ticketNumber, this.currentTicket)
      .subscribe({
        next: (res) => {
          console.log(res);
          this.message = res.message ? res.message : 'This ticket was updated successfully!';
        },
        error: (e) => console.error(e)
      });
  }
  stageCompleted(): void{
    if(this.currentTicket.acquired! == false)
    {
      console.log(this.currentTicket.playbookid!.patchvalidation!)
      this.currentTicket.group = this.currentTicket.playbookid!.patchvalidation!;
      this.currentTicket.assignedTo = "unassigned";
      this.currentTicket.acquired = true;
      this.updateTicket();
    }
    else if(this.currentTicket.validated! == false)
    {
      console.log(this.currentTicket);
      this.currentTicket.group = this.currentTicket.playbookid!.verification!;
      this.currentTicket.assignedTo = "unassigned";
      this.currentTicket.validated = true;
      this.updateTicket();
    }
    else if(this.currentTicket!.verified! == false)
    {
      this.currentTicket.group = this.currentTicket.playbookid!.rollout!;
      this.currentTicket.assignedTo = "unassigned";
      this.currentTicket.verified = true;
      this.updateTicket();
    }
    else if(this.currentTicket!.rolledout == false)
    {
      this.currentTicket.rolledout = true;
      this.updateTicket();
    }
  }
  closeTiket(): void {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = false;
    dialogConfig.id = "ticket-details";
    dialogConfig.height = "350px";
    dialogConfig.width = "1000px";
    const ticketDialog = this.matDialog.open(CloseTicketDialogComponent,{ data: this.currentTicket.outcome})
    ticketDialog.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      console.log(result);
      if(result)
      {
        
        this.currentTicket.outcome = result;
        this.currentTicket.progress = 'Closed';
        this.currentTicket.group = '';
        this.ticketService.updateTicket(this.currentTicket.ticketNumber, this.currentTicket);
      }
    })
  }
  deleteTicket(): void {
    this.ticketService.deleteTicket(this.currentTicket.ticketNumber)
      .subscribe({
        next: (res) => {
          console.log(res);
          this.router.navigate(['/tickets']);
        },
        error: (e) => console.error(e)
      });
  }
  closeTicket() {
    this.dialogRef.close();
  }
  getUsers(): void {
    this.ticketService.getUsers()
      .subscribe({
        next: (data) => {
          this.Users = data;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
  }
  getAssets(): void {
    this.ticketService.getAssets()
      .subscribe({
        next: (data) => {
          this.addAssets = data;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
  }
  openAsset(num: string) {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = false;
    dialogConfig.id = "ticket-details";
    dialogConfig.height = "350px";
    dialogConfig.width = "1000px";
    const ticketDialog = this.matDialog.open(AssetComponent,{ data: num })

  }
  openAssetAddition(num: Assets[]) {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = false;
    dialogConfig.id = "ticket-details";
    dialogConfig.height = "350px";
    dialogConfig.width = "1000px";
    const ticketDialog = this.matDialog.open(AssetAdditionComponent,{ data: num })
    .afterClosed().subscribe({
      next: (data) => {
        this.addAssets = data;
      },
      error: (e) => console.error(e)
    });
      
      //result => this.currentTicket.assets = result);

  }
  sumPa(): void {
    this.togglePa = true;
    this.toggleVe = false;
    this.toggleVa = false;
    this.toggleRo = false;
    console.log(this.addAssets);
    console.log(this.currentTicket.assets);
  }
  sumVe(): void {
    this.togglePa = false;
    this.toggleVe = true;
    this.toggleVa = false;
    this.toggleRo = false;
  }
  sumVa(): void {
    this.togglePa = false;
    this.toggleVe = false;
    this.toggleVa = true;
    this.toggleRo = false;
  }
  sumRo(): void {
    this.togglePa = false;
    this.toggleVe = false;
    this.toggleVa = false;
    this.toggleRo = true;
  }
}
