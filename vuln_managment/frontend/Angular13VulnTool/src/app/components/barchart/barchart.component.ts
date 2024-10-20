import { Component, OnInit, Input } from '@angular/core';
import {formatDate, registerLocaleData} from "@angular/common"
import localeEn from '@angular/common/locales/en';
import { Tickets } from 'src/app/models/tickets.model';
import { TicketsService } from 'src/app/services/tickets.service';


registerLocaleData(localeEn);

@Component({
  selector: 'app-barchart',
  templateUrl: './barchart.component.html',
  styleUrls: ['./barchart.component.css']
})
export class BarchartComponent implements OnInit {
  @Input() query: Object;
  tickets: Tickets[];
  acceptedRisk: number;
  outcome = [];
  constructor(private ticketService: TicketsService) { }

  public barChartLabels = [];
  public barChartType = "bar";
  public barChartLegend = true;
  public barChartData = [];

  ngOnInit(): void {
    this.ticketService.returnAffectVulnBySev().subscribe({
      next: (data) => {
        this.outcome = data;

      },
      error: (e) => console.error(e)
    });
  }
  

}
