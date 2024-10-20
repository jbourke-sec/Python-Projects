import { Component, Input, OnInit } from '@angular/core';
import { TicketsService } from 'src/app/services/tickets.service';

@Component({
  selector: 'app-piechart',
  templateUrl: './piechart.component.html',
  styleUrls: ['./piechart.component.css']
})
export class PiechartComponent implements OnInit {

  @Input() query: Object;
  outcome = [];
  constructor(private ticketService: TicketsService) { }

 

  public barChartLabels = [];
  public barChartType = "bar";
  public barChartLegend = true;
  public barChartData = [];

  days: number = 7;
  current: number = 7;
  ngOnInit(): void {
    this.ticketService.returnClosedResults(this.days).subscribe({
      next: (data) => {
        this.outcome = data;

      },
      error: (e) => console.error(e)
    });
  }
  setTime(): void {
    this.ticketService.returnClosedResults(this.days).subscribe({
      next: (data) => {
        this.outcome = data;
        this.current = this.days;

      },
      error: (e) => console.error(e)
    });
  }

}
