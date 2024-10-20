import { Component, Input, OnInit } from '@angular/core';
import { Tickets } from 'src/app/models/tickets.model';
import { TicketsService } from 'src/app/services/tickets.service';

@Component({
  selector: 'app-gaugechart',
  templateUrl: './gaugechart.component.html',
  styleUrls: ['./gaugechart.component.css']
})
export class GaugechartComponent implements OnInit {

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
  xAxisLabel = 'Weaknesses';
  showYAxisLabel = true;
  yAxisLabel = 'Technology';
  title = '';

  ngOnInit(): void {
    this.ticketService.ticketprogbreakdown().subscribe({
      next: (data) => {
        this.title = 'Tickets in Progress - Breakdown'
        this.outcome = data;

      },
      error: (e) => console.error(e)
    });
  }

}
