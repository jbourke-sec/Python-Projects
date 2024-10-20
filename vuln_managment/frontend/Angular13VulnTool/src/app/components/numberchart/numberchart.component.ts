import { Component, Input, OnInit } from '@angular/core';
import { TicketsService } from 'src/app/services/tickets.service';

@Component({
  selector: 'app-numberchart',
  templateUrl: './numberchart.component.html',
  styleUrls: ['./numberchart.component.css']
})
export class NumberchartComponent implements OnInit {

@Input() query: Object;
  outcome = [];
  constructor(private ticketService: TicketsService) { }
  current: number = 7;
  days: number = 7;

  ngOnInit(): void {
    this.ticketService.returnHasMetSLA(this.days).subscribe({
      next: (data) => {
        this.outcome = data;

      },
      error: (e) => console.error(e)
    });
  }
  setTime(): void {
    this.ticketService.returnHasMetSLA(this.days).subscribe({
      next: (data) => {
        this.current = this.days;
        this.outcome = data;

      },
      error: (e) => console.error(e)
    });
  }
}
