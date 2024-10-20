import { Component, OnInit } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { Playbook } from 'src/app/models/playbook.model';
import { TicketsService } from 'src/app/services/tickets.service';
import { TokenStorageService } from 'src/app/_services/token-storage.service';
import { AddplaybookComponent } from '../addplaybook/addplaybook.component';
import { PlaybookComponent } from '../playbook/playbook.component';

@Component({
  selector: 'app-playbooks',
  templateUrl: './playbooks.component.html',
  styleUrls: ['./playbooks.component.css']
})
export class PlaybooksComponent implements OnInit {

  playbooks?: Playbook[];
  isLoggedIn: boolean = false;
  create: boolean = false;
  constructor(private ticketService: TicketsService, public matDialog: MatDialog, public tokenStorage: TokenStorageService,private route: ActivatedRoute,
    private router: Router,) { }

  ngOnInit(): void {
    if (!this.tokenStorage.getToken()) {
      this.router.navigate(['/login']);
    }
    this.retrievePlays();
  }
  retrievePlays(): void {
    this.ticketService.getPlays()
      .subscribe({
        next: (data) => {
          this.playbooks = data;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
  }
  refreshList(): void {
    this.retrievePlays();
  }
  openPlay(num: string) {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = false;
    dialogConfig.id = "asset-details";
    dialogConfig.height = "350px";
    dialogConfig.width = "600px";
    const openDialog = this.matDialog.open(PlaybookComponent,{ data: num })
    .afterClosed()
    .subscribe(result => this.playbooks = result);

  }
  newPlay() {
    const newConfig = new MatDialogConfig();
    newConfig.disableClose = false;
    newConfig.id = "add-asset";
    newConfig.height = "350px";
    newConfig.width = "600px";
    const newDialog = this.matDialog.open(AddplaybookComponent)
  }

}
