import { Component, Input, OnInit } from '@angular/core';
import { Tickets } from 'src/app/models/tickets.model';
import { TicketsService } from 'src/app/services/tickets.service';

@Component({
  selector: 'app-grouped-vertical-bar',
  templateUrl: './grouped-vertical-bar.component.html',
  styleUrls: ['./grouped-vertical-bar.component.css']
})
export class GroupedVerticalBarComponent implements OnInit {

  @Input() query: Object;
  tickets: Tickets[];
  acceptedRisk: number;
  outcome = [];
  constructor(private ticketService: TicketsService) { }

  

  showXAxis = true;
  showYAxis = true;
  gradient = false;
  showLegend = true;
  showXAxisLabel = true;
  xAxisLabel = 'Vectors';
  showYAxisLabel = true;
  yAxisLabel = 'Severity';
  title = '';

  ngOnInit(): void {
    this.ticketService.vulnbreakdown().subscribe({
      next: (data) => {
        this.title = 'Top 10 Vulnerable Applications - 365 Days'
        this.outcome = data;

      },
      error: (e) => console.error(e)
    });
  }

}
