import { Component, OnInit } from '@angular/core';
import { Playbook } from 'src/app/models/playbook.model';
import { TicketsService } from 'src/app/services/tickets.service';

@Component({
  selector: 'app-addplaybook',
  templateUrl: './addplaybook.component.html',
  styleUrls: ['./addplaybook.component.css']
})
export class AddplaybookComponent implements OnInit {

  submitted = false;
  playbook: Playbook = {
    category: '',
    patchvalidation: '',
    verification: '',
    rollout: '',
    notes: '',
  };

  constructor(private ticketService: TicketsService) { }

  ngOnInit(): void {
  }

  newPlay(): void {
    this.submitted = false;
    this.playbook = 
    {
      category: '',
      patchvalidation: '',
      verification: '',
      rollout: '',
      notes: '',
    }
    
    
    };
    savePlay(): void 
    {
      const data = 
      {
        category: this.playbook.category,
        patchvalidation: this.playbook.patchvalidation,
        verification: this.playbook.verification,
        rollout: this.playbook.rollout,
        notes: this.playbook.notes
      }
      this.ticketService.createPlay(data)
      .subscribe({
        next: (res) => {
          console.log(res);
          this.submitted = true;
        },
        error: (e) => console.error(e)
      });
    };

}
