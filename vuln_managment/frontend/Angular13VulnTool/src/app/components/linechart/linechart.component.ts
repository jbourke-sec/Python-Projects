import { Component, Input, OnInit } from '@angular/core';
import { TicketsService } from 'src/app/services/tickets.service';

@Component({
  selector: 'app-linechart',
  templateUrl: './linechart.component.html',
  styleUrls: ['./linechart.component.css']
})
export class LinechartComponent implements OnInit {

  @Input() query: Object;
  outcome = [];
  constructor(private ticketService: TicketsService) { }
  public barChartLabels = [];
  public barChartType = "bar";
  public barChartLegend = true;
  public barChartData = [];

  showXAxis = true;
  showYAxis = true;
  gradient = false;
  showLegend = true;
  showXAxisLabel = true;
  xAxisLabel = 'Patch Management';
  showYAxisLabel = true;
  yAxisLabel = 'Hours';

  days: number = 7;
  current: number = 7;

  ngOnInit(): void {
    this.ticketService.returnRemTimes(this.days).subscribe({
      next: (data) => {
        this.outcome = data;

      },
      error: (e) => console.error(e)
    });
  }
  updateTime(): void {
    this.ticketService.returnRemTimes(this.days).subscribe({
      next: (data) => {
        this.outcome = data;
        this.current = this.days;

      },
      error: (e) => console.error(e)
    });
  }
}
