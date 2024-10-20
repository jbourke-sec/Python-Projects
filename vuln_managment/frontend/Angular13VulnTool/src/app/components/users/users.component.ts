import { LiveAnnouncer } from '@angular/cdk/a11y';
import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort, Sort } from '@angular/material/sort';
import { MatTableDataSource, MatTable } from '@angular/material/table';
import { Router } from '@angular/router';
import { User } from 'src/app/models/user.model';
import { TokenStorageService } from 'src/app/_services/token-storage.service';
import { UserService } from 'src/app/_services/user.service';
import { NewuserComponent } from '../newuser/newuser.component';
import { UserComponent } from '../user/user.component';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css']
})
export class UsersComponent implements OnInit {

  users?: User[];
  isLoggedIn: boolean = false;
  create: boolean = false;
  displayedColumns: string[] = ['email', 'username'];
  dataSource = new MatTableDataSource<User>();

  @ViewChild('dataTable') dataTable: MatTable<any>;
  @ViewChild(MatPaginator) paginator: MatPaginator
  @ViewChild(MatSort) sort: MatSort;

  constructor(private userService: UserService, public matDialog: MatDialog, private router: Router,private _liveAnnouncer: LiveAnnouncer, public tokenStorage: TokenStorageService) { }


  ngOnInit(): void {
    if (!this.tokenStorage.getToken()) {
      this.router.navigate(['/login']);
    }
    this.retrieveUsers();
  }

  ngAfterViewInit (){
    this.dataSource.sort = this.sort;
  }
  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
}
  retrieveUsers(): void {
    this.userService.getUsers()
      .subscribe({
        next: (data) => {
          this.users = data;
          this.dataSource.data = data;
          this.dataSource.paginator = this.paginator;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
  }
  newUser() {
    const newConfig = new MatDialogConfig();
    newConfig.disableClose = false;
    newConfig.id = "add-user";
    newConfig.height = "350px";
    newConfig.width = "600px";
    const newDialog = this.matDialog.open(NewuserComponent)
  }

  openUser(email: string) {
    const newConfig = new MatDialogConfig();
    newConfig.disableClose = false;
    newConfig.id = "user";
    newConfig.height = "350px";
    newConfig.width = "600px";
    const newDialog = this.matDialog.open(UserComponent, { data: email });
  }
  announceSortChange(sortState: Sort) {
    if (sortState.direction) {
      this._liveAnnouncer.announce(`Sorted ${sortState.direction}ending`);
    } else {
      this._liveAnnouncer.announce('Sorting cleared');
    }
  }
}
