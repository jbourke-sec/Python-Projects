import { LiveAnnouncer } from '@angular/cdk/a11y';
import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort, Sort } from '@angular/material/sort';
import { MatTable, MatTableDataSource } from '@angular/material/table';
import { ActivatedRoute, Router } from '@angular/router';
import { Assets } from 'src/app/models/assets.model';
import { TicketsService } from 'src/app/services/tickets.service';
import { TokenStorageService } from 'src/app/_services/token-storage.service';
import { AssetComponent } from '../asset/asset.component';
import { NewAssetComponent } from '../new-asset/new-asset.component';

@Component({
  selector: 'app-assetlist',
  templateUrl: './assetlist.component.html',
  styleUrls: ['./assetlist.component.css']
})
export class AssetlistComponent implements OnInit {

  displayedColumns: string[] = ['assetid', 'hostname',  'cpe', 'risk', 'baseSLA', 'policyid', 'category'];
  Assets?: Assets[];
  isLoggedIn: boolean = false;
  create: boolean = false;
  all: boolean = false;
  noPolicy: boolean = false;
  dataSource = new MatTableDataSource<Assets>();
  secsinhour: number = 3600;
  secsinmin: number = 60;

  @ViewChild('dataTable') dataTable: MatTable<any>;
  @ViewChild(MatPaginator) paginator: MatPaginator
  @ViewChild(MatSort) sort: MatSort;

  constructor(private ticketService: TicketsService, public matDialog: MatDialog, private _liveAnnouncer: LiveAnnouncer, private route: ActivatedRoute,
    private router: Router,public tokenStorage: TokenStorageService,) { }

  ngOnInit(): void {
    if (!this.tokenStorage.getToken()) {
      this.router.navigate(['/login']);
    }
    this.all = true;
    this.retrieveAssets();
  }
  calcHours(time: number){
    return Math.floor((time)/(this.secsinhour));
  }
  calcMins(time: number){
    return Math.floor((time % this.secsinhour)/this.secsinmin);
  }
  ngAfterViewInit (){
    this.dataSource.sort = this.sort;
  }
  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
}
  retrieveAssets(): void {
    this.all=true;
    this.noPolicy=false;
    this.ticketService.getAssets()
      .subscribe({
        next: (data) => {
          this.Assets = data;
          this.dataSource.data = data;
          this.dataSource.paginator = this.paginator;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
  }
  retrieveAssetsNoPolicy(): void {
    this.noPolicy=true;
    this.all=false;
    this.ticketService.getAssetsNoPolicy()
      .subscribe({
        next: (data) => {
          this.Assets = data;
          this.dataSource.data = data;
          this.dataSource.paginator = this.paginator;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
  }
  refreshList(): void {
    this.retrieveAssets();
  }
  openAsset(num: string) {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = false;
    dialogConfig.id = "asset-details";
    dialogConfig.height = "350px";
    dialogConfig.width = "600px";
    const assetDialog = this.matDialog.open(AssetComponent,{ data: num })
    .afterClosed()
    .subscribe(result => this.Assets = result);

  }
  newAsset() {
    const newConfig = new MatDialogConfig();
    newConfig.disableClose = false;
    newConfig.id = "add-asset";
    newConfig.height = "350px";
    newConfig.width = "600px";
    const newassetDialog = this.matDialog.open(NewAssetComponent)
  }
  announceSortChange(sortState: Sort) {
    if (sortState.direction) {
      this._liveAnnouncer.announce(`Sorted ${sortState.direction}ending`);
    } else {
      this._liveAnnouncer.announce('Sorting cleared');
    }
  }
}
