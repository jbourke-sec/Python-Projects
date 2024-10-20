import { Component, OnInit } from '@angular/core';
import { Policy } from 'src/app/models/policy.model';
import { TicketsService } from 'src/app/services/tickets.service';

@Component({
  selector: 'app-addpolicy',
  templateUrl: './addpolicy.component.html',
  styleUrls: ['./addpolicy.component.css']
})
export class AddpolicyComponent implements OnInit {
  submitted = false;
  policy: Policy = {
    cpe: '',
    confidentialityreq: '',
    integrityreq: '',
    availabilityreq: '',
    category: ''
  };

  req: any[] = [
    {value: 'High', viewValue: 'High Requirement'},
    {value: 'Medium', viewValue: 'Medium Requirement'},
    {value: 'Low', viewValue: 'Low Requirement'},
    {value: 'Not Defined', viewValue: 'Not Defined'},
  ];

  constructor(private ticketService: TicketsService) { }

  ngOnInit(): void {
    
  }
  newPolicy(): void {
    this.submitted = false;
    this.policy = {
      cpe: '',
      confidentialityreq: '',
      integrityreq: '',
      availabilityreq: '',
      category: ''
    }
    
    
    };
    savePolicy(): void 
    {
      const data = 
      {
          cpe: this.policy.cpe,
          confidentialityreq: this.policy.confidentialityreq,
          integrityreq: this.policy.integrityreq,
          availabilityreq: this.policy.availabilityreq,
          category: this.policy.category,
      }
      this.ticketService.createPolicy(data)
      .subscribe({
        next: (res) => {
          console.log(res);
          this.submitted = true;
        },
        error: (e) => console.error(e)
      });
    };

}
