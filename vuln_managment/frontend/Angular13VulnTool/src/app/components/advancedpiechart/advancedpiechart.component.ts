import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { Tickets } from 'src/app/models/tickets.model';
import { TicketsService } from 'src/app/services/tickets.service';

@Component({
  selector: 'app-advancedpiechart',
  templateUrl: './advancedpiechart.component.html',
  styleUrls: ['./advancedpiechart.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class AdvancedpiechartComponent implements OnInit {

  @Input() query: Object;
  tickets: Tickets[];
  acceptedRisk: number;
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
    this.ticketService.returnAssetCpes().subscribe({
      next: (data) => {
        this.title = 'Asset CPE Breakdown'
        this.outcome = data;

      },
      error: (e) => console.error(e)
    });
  }

}
