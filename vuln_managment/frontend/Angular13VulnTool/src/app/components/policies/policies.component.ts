import { LiveAnnouncer } from '@angular/cdk/a11y';
import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort, Sort } from '@angular/material/sort';
import { MatTableDataSource, MatTable } from '@angular/material/table';
import { ActivatedRoute, Router } from '@angular/router';
import { Policy } from 'src/app/models/policy.model';
import { TicketsService } from 'src/app/services/tickets.service';
import { TokenStorageService } from 'src/app/_services/token-storage.service';
import { AddpolicyComponent } from '../addpolicy/addpolicy.component';
import { PolicyComponent } from '../policy/policy.component';

@Component({
  selector: 'app-policies',
  templateUrl: './policies.component.html',
  styleUrls: ['./policies.component.css']
})
export class PoliciesComponent implements OnInit {

  policies?: Policy[];
  isLoggedIn: boolean = false;
  create: boolean = false;
  displayedColumns: string[] = ['policyid', 'category', 'confidentialityreq', 'integrityreq', 'availabilityreq'];
  dataSource = new MatTableDataSource<Policy>();

  @ViewChild('dataTable') dataTable: MatTable<any>;
  @ViewChild(MatPaginator) paginator: MatPaginator
  @ViewChild(MatSort) sort: MatSort;

  constructor(private ticketService: TicketsService, public matDialog: MatDialog, private _liveAnnouncer: LiveAnnouncer, public tokenStorage: TokenStorageService, private route: ActivatedRoute, private router: Router,) { }

  ngOnInit(): void {
    if (!this.tokenStorage.getToken()) {
      this.router.navigate(['/login']);
    }
    this.retrievePolicies();
  }

  ngAfterViewInit (){
    this.dataSource.sort = this.sort;
  }
  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
}
  retrievePolicies(): void {
    this.ticketService.getPolicies()
      .subscribe({
        next: (data) => {
          this.policies = data;
          this.dataSource.data = data;
          this.dataSource.paginator = this.paginator;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
  }
  refreshList(): void {
    this.retrievePolicies();
  }
  openPolicy(num: string) {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = false;
    dialogConfig.id = "asset-details";
    dialogConfig.height = "350px";
    dialogConfig.width = "600px";
    const openDialog = this.matDialog.open(PolicyComponent,{ data: num })
    .afterClosed()
    .subscribe(result => this.policies = result);

  }
  newPolicy() {
    const newConfig = new MatDialogConfig();
    newConfig.disableClose = false;
    newConfig.id = "add-asset";
    newConfig.height = "350px";
    newConfig.width = "600px";
    const newDialog = this.matDialog.open(AddpolicyComponent)
  }
  announceSortChange(sortState: Sort) {
    if (sortState.direction) {
      this._liveAnnouncer.announce(`Sorted ${sortState.direction}ending`);
    } else {
      this._liveAnnouncer.announce('Sorting cleared');
    }
  }
}
