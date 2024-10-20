import { Component, OnInit, ViewChild } from '@angular/core';
import { Tickets } from 'src/app/models/tickets.model';
import { TicketsService } from 'src/app/services/tickets.service';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { TicketDetailsComponent } from '../ticket-details/ticket-details.component';
import { AddTicketComponent } from '../new-ticket/new-ticket.component';
import { NavigationEnd, Router } from '@angular/router';
import { MatTable, MatTableDataSource } from '@angular/material/table';
import { MatSort, Sort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { QaTicketDialogComponent } from '../qa-ticket-dialog/qa-ticket-dialog.component';
import { ReopenTicketDialogComponent } from '../reopen-ticket-dialog/reopen-ticket-dialog.component';
import { VulnerabilityComponent } from '../vulnerability/vulnerability.component';
import { TokenStorageService } from 'src/app/_services/token-storage.service';


@Component({
  selector: 'app-queue',
  templateUrl: './queue.component.html',
  styleUrls: ['./queue.component.css']
})
export class QueueComponent implements OnInit {
  displayedColumns: string[] = ['ticketNumber', 'timeStarted', 'sla', 'progress', 'cve', 'cvss'];
  Tickets?: Tickets[];
  queue: boolean = true;
  myticket: boolean = false;
  closedtickets: boolean = false;
  patchacq: boolean = false;
  patchver: boolean = false;
  patchval: boolean = false;
  patchrol: boolean = false;
  isLoggedIn: boolean = false;
  dataSource = new MatTableDataSource<Tickets>();

  mySubscription: any;

  @ViewChild('dataTable') dataTable: MatTable<any>;
  @ViewChild(MatPaginator) paginator: MatPaginator
  @ViewChild(MatSort) sort: MatSort;
  

  constructor(private ticketService: TicketsService, public matDialog: MatDialog, private router: Router,private _liveAnnouncer: LiveAnnouncer, public tokenStorage: TokenStorageService) 
  { 
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {    
          this.refreshList();
    }});
  }

  ngOnInit(): void {
    if (!this.tokenStorage.getToken()) {
      this.router.navigate(['/login']);
    }
    this.queue = true;
    this.retrieveTickets();
    
  }
  ngAfterViewInit (){
    this.dataSource.sort = this.sort;
  }
  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
}
  retrieveTickets(): void {
    this.displayedColumns = ['ticketNumber', 'timeStarted', 'sla', 'progress', 'cve', 'cvss'];
    this.queue = true;
    this.myticket = false;
    this.closedtickets= false;
    this.patchacq = false;
    this.patchver = false;
    this.patchval = false;
    this.patchrol = false;
    this.ticketService.getAll()
      .subscribe({
        next: (data) => {
          this.Tickets = data;
          this.dataSource.data = data;
          console.log(this.dataSource);
          console.log(data);
          this.dataSource.paginator = this.paginator;
        },
        error: (e) => console.error(e)
      });
  }
  retrievePatchacq(): void {
    this.displayedColumns = ['ticketNumber', 'timeStarted', 'sla', 'progress', 'cve', 'cvss'];
    this.queue = false;
    this.myticket = false;
    this.closedtickets= false;
    this.patchacq = true;
    this.patchver = false;
    this.patchval = false;
    this.patchrol = false;
    this.ticketService.getGroupTickets('Patch-Acquirement')
      .subscribe({
        next: (data) => {
          this.Tickets = data;
          this.dataSource.data = data;
          console.log(this.dataSource);
          console.log(data);
          this.dataSource.paginator = this.paginator;
        },
        error: (e) => console.error(e)
      });
  }
  retrievePatchval(): void {
    this.displayedColumns = ['ticketNumber', 'timeStarted', 'sla', 'progress', 'cve', 'cvss'];
    this.queue = false;
    this.myticket = false;
    this.closedtickets= false;
    this.patchacq = false;
    this.patchver = false;
    this.patchval = true;
    this.patchrol = false;
    this.ticketService.getGroupTickets('Patch-Validation')
      .subscribe({
        next: (data) => {
          this.Tickets = data;
          this.dataSource.data = data;
          console.log(this.dataSource);
          console.log(data);
          this.dataSource.paginator = this.paginator;
        },
        error: (e) => console.error(e)
      });
  }
  retrievePatchver(): void {
    this.displayedColumns = ['ticketNumber', 'timeStarted', 'sla', 'progress', 'cve', 'cvss'];
    this.queue = false;
    this.myticket = false;
    this.closedtickets= false;
    this.patchacq = false;
    this.patchver = true;
    this.patchval = false;
    this.patchrol = false;
    this.ticketService.getGroupTickets('Patch-Verification')
      .subscribe({
        next: (data) => {
          this.Tickets = data;
          this.dataSource.data = data;
          console.log(this.dataSource);
          console.log(data);
          this.dataSource.paginator = this.paginator;
        },
        error: (e) => console.error(e)
      });
  }
  retrievePatchRol(): void {
    this.displayedColumns = ['ticketNumber', 'timeStarted', 'sla', 'progress', 'cve', 'cvss'];
    this.queue = false;
    this.myticket = false;
    this.closedtickets= false;
    this.patchacq = false;
    this.patchver = false;
    this.patchval = false;
    this.patchrol = true;
    this.ticketService.getGroupTickets('Patch-Rollout')
      .subscribe({
        next: (data) => {
          this.Tickets = data;
          this.dataSource.data = data;
          console.log(this.dataSource);
          console.log(data);
          this.dataSource.paginator = this.paginator;
        },
        error: (e) => console.error(e)
      });
  }
  refreshList(): void {
    this.retrieveTickets();
  }
  retrieveMyTickets(): void {
    this.displayedColumns = ['ticketNumber', 'timeStarted', 'sla', 'progress', 'cve', 'cvss'];
    this.queue = false;
    this.myticket = true;
    this.closedtickets= false;
    this.patchacq = false;
    this.patchver = false;
    this.patchval = false;
    this.patchrol = false;
    this.ticketService.getMyTickets()
      .subscribe({
        next: (data) => {
          this.Tickets = data;
          this.dataSource.data = data;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
  }
  retrieveClosedTickets(): void {
    this.displayedColumns = ['ticketNumber', 'timeStarted', 'sla', 'progress', 'cve', 'cvss','outcome', 'reopen', 'qa'];
    this.queue = false;
    this.myticket = false;
    this.closedtickets= true;
    this.patchacq = false;
    this.patchver = false;
    this.patchval = false;
    this.patchrol = false;
    this.ticketService.getClosedTickets()
      .subscribe({
        next: (data) => {
          this.Tickets = data;
          this.dataSource.data = data;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
  }
  retrieveGroupTickets(str: string): void {

  }
  openVuln(num: string) {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = false;
    dialogConfig.id = "asset-details";
    dialogConfig.height = "350px";
    dialogConfig.width = "600px";
    const openDialog = this.matDialog.open(VulnerabilityComponent,{ data: num })
    .afterClosed()
   // .subscribe(result => this.vulnerability = result);
   this.refreshConfig();
  }
  openTicket(num: string) {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = false;
    dialogConfig.id = "ticket-details";
    dialogConfig.height = "350px";
    dialogConfig.width = "1000px";
    const ticketDialog = this.matDialog.open(TicketDetailsComponent,{ data: num })
    .afterClosed()
    .subscribe(result => this.Tickets = result)
    this.refreshConfig();
  }
  createTicket() {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = false;
    dialogConfig.id = "add-ticket";
    dialogConfig.height = "350px";
    dialogConfig.width = "600px";
    const ticketDialog = this.matDialog.open(AddTicketComponent)
    .afterClosed()
    .subscribe(() => this.refreshConfig())
  }
  qaTicket(num: string) {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = false;
    dialogConfig.id = "qa-ticket";
    dialogConfig.height = "350px";
    dialogConfig.width = "1000px";
    const ticketDialog = this.matDialog.open(QaTicketDialogComponent,{ data: num })
    .afterClosed()
    .subscribe(result => this.Tickets = result);
    this.refreshConfig()
    
  }
  reopenTicket(num: string) {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = false;
    dialogConfig.id = "ticket-details";
    dialogConfig.height = "350px";
    dialogConfig.width = "1000px";
    const ticketDialog = this.matDialog.open(ReopenTicketDialogComponent,{ data: num })
    .afterClosed()
    .subscribe(result => this.Tickets = result)
    this.refreshConfig()
    
  }

  refreshConfig(): void {
    if(this.queue==true)
    {
      this.retrieveTickets();
    }
    if(this.myticket == true)
    {
      this.retrieveMyTickets();
    }
    if(this.patchacq == true)
    {
      this.retrievePatchacq();
    }
    if(this.patchval == true)
    {
      this.retrievePatchval();
    }
    if(this.patchver == true)
    {
      this.retrievePatchver()
    }
    if(this.patchrol == true)
    {
      this.retrievePatchRol();
    }
    if(this.closedtickets == true)
    {
      this.retrieveClosedTickets();
    }
  }
  announceSortChange(sortState: Sort) {
    if (sortState.direction) {
      this._liveAnnouncer.announce(`Sorted ${sortState.direction}ending`);
    } else {
      this._liveAnnouncer.announce('Sorting cleared');
    }
  }
  };