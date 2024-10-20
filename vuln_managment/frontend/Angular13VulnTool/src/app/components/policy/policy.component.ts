import { Component, Inject, Input, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { Policy } from 'src/app/models/policy.model';
import { TicketsService } from 'src/app/services/tickets.service';

@Component({
  selector: 'app-policy',
  templateUrl: './policy.component.html',
  styleUrls: ['./policy.component.css']
})
export class PolicyComponent implements OnInit {

  @Input() viewMode = false;

  @Input() currentPolicy: Policy = {
    policyid: '',
    cpe: '',
    confidentialityreq: '',
    integrityreq: '',
    availabilityreq: '',
    category: '',
  };

  req: any[] = [
    {value: 'High', viewValue: 'High Requirement'},
    {value: 'Medium', viewValue: 'Medium Requirement'},
    {value: 'Low', viewValue: 'Low Requirement'},
    {value: 'Not Defined', viewValue: 'Not Defined'},
  ];
  
  message = '';
  constructor(
    private ticketService: TicketsService,
    private route: ActivatedRoute,
    private router: Router,
    public dialogRef: MatDialogRef<PolicyComponent>,
    @Inject(MAT_DIALOG_DATA) public data: string,) { }
    


  ngOnInit(): void {
    if (!this.viewMode) {
      this.message = '';
      this.getPolicy(this.data);//may be number
    }
  }
  getPolicy(policyid: string): void {
    this.ticketService.getPolicy(policyid)
      .subscribe({
        next: (data) => {
          this.currentPolicy = data;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
  }

  updatePolicy(): void {
    this.message = '';

    this.ticketService.updatePolicy(this.currentPolicy.policyid, this.currentPolicy)
      .subscribe({
        next: (res) => {
          console.log(res);
          this.message = res.message ? res.message : 'This Policy was updated successfully!';
        },
        error: (e) => console.error(e)
      });
  }
  deletePolicy(): void {
    this.ticketService.deletePolicy(this.currentPolicy.policyid)
      .subscribe({
        next: (res) => {
          console.log(res);
          this.router.navigate(['/policy']);
        },
        error: (e) => console.error(e)
      });
  }
  closePolicy() {
    this.dialogRef.close();
  }
}
