import { Component, Inject, Input, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { Playbook } from 'src/app/models/playbook.model';
import { TicketsService } from 'src/app/services/tickets.service';
import { TokenStorageService } from 'src/app/_services/token-storage.service';

@Component({
  selector: 'app-playbook',
  templateUrl: './playbook.component.html',
  styleUrls: ['./playbook.component.css']
})
export class PlaybookComponent implements OnInit {

  @Input() viewMode = false;

  @Input() currentPlay: Playbook = {
    playbookid:'',
    category:'',
    patchvalidation:'',
    verification:'',
    rollout:'',
    notes:''
  };
  
  message = '';
  constructor(
    private ticketService: TicketsService,
    private route: ActivatedRoute,
    private router: Router,
    public dialogRef: MatDialogRef<PlaybookComponent>,
    @Inject(MAT_DIALOG_DATA) public data: string,
    public tokenStorage: TokenStorageService,) { }
    


  ngOnInit(): void {
    if (!this.tokenStorage.getToken()) {
      this.router.navigate(['/login']);
    }
    if (!this.viewMode) {
      this.message = '';
      this.getPlay(this.data);//may be number
    }
  }
  getPlay(playbookid: string): void {
    this.ticketService.getPlay(playbookid)
      .subscribe({
        next: (data) => {
          this.currentPlay = data;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
  }

  updatePlay(): void {
    this.message = '';

    this.ticketService.updatePlay(this.currentPlay.playbookid, this.currentPlay)
      .subscribe({
        next: (res) => {
          console.log(res);
          this.message = res.message ? res.message : 'This ticket was updated successfully!';
        },
        error: (e) => console.error(e)
      });
  }
  deletePlay(): void {
    this.ticketService.deleteTicket(this.currentPlay.playbookid)
      .subscribe({
        next: (res) => {
          console.log(res);
          this.router.navigate(['/playbook']);
        },
        error: (e) => console.error(e)
      });
  }
  closePlay() {
    this.dialogRef.close();
  }

}
