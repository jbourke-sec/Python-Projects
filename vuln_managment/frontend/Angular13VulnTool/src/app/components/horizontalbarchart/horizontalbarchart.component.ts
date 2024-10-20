import { Component, Input, OnInit } from '@angular/core';
import { Tickets } from 'src/app/models/tickets.model';
import { TicketsService } from 'src/app/services/tickets.service';

@Component({
  selector: 'app-horizontalbarchart',
  templateUrl: './horizontalbarchart.component.html',
  styleUrls: ['./horizontalbarchart.component.css']
})
export class HorizontalbarchartComponent implements OnInit {

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

  days: number = 365;
  current: number = 365;
  app: boolean = false;
  os: boolean = false;
  hardware: boolean = false;

  ngOnInit(): void {
    this.ticketService.returnvulnsbyapp(this.current).subscribe({
      next: (data) => {
        this.title = 'Top 10 Applications with Most Vulnerabilities- ' + this.current + ' Days';
        this.outcome = data;
        this.app = true;
      },
      error: (e) => console.error(e)
    });
  }

  vulnbyApp(): void {
    this.ticketService.returnvulnsbyapp(this.current).subscribe({
      next: (data) => {
        this.title = 'Top 10 Applications with Most Vulnerabilities- ' + this.current + ' Days';
        this.outcome = data;
        this.app = true;
        this.os = false;
        this.hardware = false;

      },
      error: (e) => console.error(e)
    });
  }
  vulnByOs(): void {
    this.ticketService.returnvulnsbyos(this.current).subscribe({
      next: (data) => {
        this.title = 'Top 10 Operating Systems with Most Vulnerabilities- '  + this.current + ' Days';
        this.outcome = data;
        this.app = false;
        this.os = true;
        this.hardware = false;

      },
      error: (e) => console.error(e)
    });
  }
  vulnByHardware(): void {
    this.ticketService.returnvulnsbyhardware(this.current).subscribe({
      next: (data) => {
        this.title = 'Top 10 Hardware with Most Vulnerabilities- '  + this.current + ' Days';
        this.outcome = data;
        this.app = false;
        this.os = false;
        this.hardware = true;

      },
      error: (e) => console.error(e)
    });
  }
  updateTime(): void {
    if(this.app)
    {
      this.current = this.days;
      this.vulnbyApp();
    }
    if(this.os)
    {
      this.current = this.days;
      this.vulnByOs();
    }
    if(this.hardware)
    {
      this.current = this.days;
      this.vulnByHardware();
    }
  }
}
