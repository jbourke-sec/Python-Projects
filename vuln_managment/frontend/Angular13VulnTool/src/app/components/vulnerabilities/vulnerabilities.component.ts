import { LiveAnnouncer } from '@angular/cdk/a11y';
import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort, Sort } from '@angular/material/sort';
import { MatTable, MatTableDataSource } from '@angular/material/table';
import { ActivatedRoute, Router } from '@angular/router';
import { Vulnerability } from 'src/app/models/vulnerability.model';
import { TicketsService } from 'src/app/services/tickets.service';
import { TokenStorageService } from 'src/app/_services/token-storage.service';
import { AddvulnerabilityComponent } from '../addvulnerability/addvulnerability.component';
import { AddTicketComponent } from '../new-ticket/new-ticket.component';
import { VulnerabilityComponent } from '../vulnerability/vulnerability.component';

@Component({
  selector: 'app-vulnerabilities',
  templateUrl: './vulnerabilities.component.html',
  styleUrls: ['./vulnerabilities.component.css']
})
export class VulnerabilitiesComponent implements OnInit {

  vulnerability?: Vulnerability[];
  isLoggedIn: boolean = false;
  create: boolean = false;
  loading: boolean = true;
  displayedColumns: string[] = ['cve', 'cpeVendor', 'cpeTech', 'description', 'risk'];
  dataSource = new MatTableDataSource<Vulnerability>();
  unremediated: boolean = false;
  all: boolean = false;
  lw: boolean = false;
  aff: boolean = false;
  closed: boolean =false;
  cpeArr: string[];
  cpeVendor: string[];
  venStrings: string[];
  currentCve: string = '';


  @ViewChild('dataTable') dataTable: MatTable<any>;
  @ViewChild(MatPaginator) paginator: MatPaginator
  @ViewChild(MatSort) sort: MatSort;

  constructor(private ticketService: TicketsService, public matDialog: MatDialog, private _liveAnnouncer: LiveAnnouncer, private route: ActivatedRoute,
    private router: Router, public tokenStorage: TokenStorageService,) { }

  ngOnInit(): void {
    if (!this.tokenStorage.getToken()) {
      this.router.navigate(['/login']);
    }
    this.all = true;
    this.unremediated = false;
    this.closed = false;
    this.aff = false;
    this.lw = false;
    this.retrieveVulns();
  }
  ngAfterViewInit (){
    this.loading = true;
    this.dataSource.sort = this.sort;
    this.loading = false;
  }
  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
}
  retrieveVulns(): void {
    this.loading = true;
    this.displayedColumns= [ 'cve', 'cpeVendor','cpeTech','description', 'risk'];
    this.all = true;
    this.unremediated = false;
    this.closed = false;
    this.aff = false;
    this.lw = false;
    this.ticketService.getVulns()
      .subscribe({
        next: (data) => {
          this.vulnerability = data;
          this.dataSource.data = data;
          this.dataSource.paginator = this.paginator;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
      this.loading = false;
  }
  retrieveUnremVulns(): void {
    this.loading = true;
    this.all = false;
    this.unremediated = true;
    this.closed = false;
    this.aff = false;
    this.lw = false;
    this.displayedColumns= ['cve', 'cpeVendor', 'cpeTech','description', 'Create Ticket', 'risk'];
    this.ticketService.unremediatedVuln()
      .subscribe({
        next: (data) => {
          this.vulnerability = data;
          this.dataSource.data = data;
          this.dataSource.paginator = this.paginator;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
      this.loading = false;
  }
  retrieveVulnsLastWeek(): void {
    this.loading = true;
    this.all = false;
    this.unremediated = false;
    this.closed = false;
    this.aff = false;
    this.lw = true;
    this.displayedColumns= ['cve', 'cpeVendor', 'cpeTech','description', 'Create Ticket', 'risk'];
    this.ticketService.lastWeekVuln()
      .subscribe({
        next: (data) => {
          this.vulnerability = data;
          this.dataSource.data = data;
          this.dataSource.paginator = this.paginator;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
      this.loading = false;
  }
  retrieveVulnAffectAssets(): void {
    this.loading = true;
    this.all = false;
    this.unremediated = false;
    this.closed = false;
    this.aff = true;
    this.lw = false;
    this.displayedColumns= ['cve', 'cpeVendor', 'cpeTech','description', 'Create Ticket', 'risk'];
    this.ticketService.affectedVuln()
      .subscribe({
        next: (data) => {
          this.vulnerability = data;
          this.dataSource.data = data;
          this.dataSource.paginator = this.paginator;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
      this.loading = false;
  }
  createTicket(currentV: string) {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = false;
    dialogConfig.id = "add-ticket";
    dialogConfig.height = "350px";
    dialogConfig.width = "600px";
    const ticketDialog = this.matDialog.open(AddTicketComponent, {data: currentV})
  }
  closedVulns(): void {
    this.loading = true;
    this.displayedColumns= ['cve', 'cpeVendor','cpeTech', 'description', 'risk'];
    this.all = false;
    this.unremediated = false;
    this.closed = true;
    this.aff = false;
    this.lw = false;
    this.ticketService.closedVuln()
      .subscribe({
        next: (data) => {
          this.vulnerability = data;
          this.dataSource.data = data;
          this.dataSource.paginator = this.paginator;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
      this.loading = false;
  }
  refreshList(): void {
    this.loading = true;
    this.retrieveVulns();
    this.loading = false;
  }
  openVuln(num: string) {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = false;
    dialogConfig.id = "asset-details";
    dialogConfig.height = "350px";
    dialogConfig.width = "600px";
    const openDialog = this.matDialog.open(VulnerabilityComponent,{ data: num })
    .afterClosed()
    .subscribe(result => this.vulnerability = result);

  }
  newVuln() {
    const newConfig = new MatDialogConfig();
    newConfig.disableClose = false;
    newConfig.id = "add-asset";
    newConfig.height = "350px";
    newConfig.width = "600px";
    const newDialog = this.matDialog.open(AddvulnerabilityComponent)
  }
  announceSortChange(sortState: Sort) {
    if (sortState.direction) {
      this._liveAnnouncer.announce(`Sorted ${sortState.direction}ending`);
    } else {
      this._liveAnnouncer.announce('Sorting cleared');
    }
  }
  cpeVendors(cpeUri: string, cpePos: number)  {
    if(cpeUri == 'None'){
      return cpeUri;
    }
    else
    {
      this.cpeVendor = [];
      this.cpeArr = cpeUri.split(" ");
      for(let x = 0; x < this.cpeArr.length; x++)
      {
        this.venStrings = this.cpeArr[x].split(':');
        const index: number = this.cpeVendor.indexOf(this.venStrings[cpePos]);
        if (index === -1) 
        {
          this.cpeVendor.push(this.venStrings[cpePos]);
        }
      }
      return this.cpeVendor.toString();
    }
    
  }
}
