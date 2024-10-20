import { Component, OnInit } from '@angular/core';
import { Assets } from 'src/app/models/assets.model';
import { TicketsService } from 'src/app/services/tickets.service';

@Component({
  selector: 'app-new-asset',
  templateUrl: './new-asset.component.html',
  styleUrls: ['./new-asset.component.css']
})
export class NewAssetComponent implements OnInit {
  message = '';
  submitted = false;
  hours: number;
  minutes: number;
  taglist: string[]= [];
  viewTag: boolean = false;
  vendor: string = '';
  tech: string = '';
  asset: Assets = {
    assetid: '',
    cpe: '',
    risk: '',
    baseSLA: undefined,
    policyid: '',
    hostname: '',
    category: '',
    tags: '',
  };

  risk: any[] = [
    {value: 'High', viewValue: 'High'},
    {value: 'Medium', viewValue: 'Medium'},
    {value: 'Low', viewValue: 'Low'},
    {value: 'Not Defined', viewValue: 'Not Defined'},
  ];

  constructor(private ticketService: TicketsService) { }

  ngOnInit(): void {
    this.viewTag= false;
  }

  newAsset(): void {
    this.submitted = false;
    this.asset = {
      assetid: '',
      cpe: '',
      risk: '',
      baseSLA: undefined,
      policyid: '',
      hostname: '',
      category: '',
      tags: '',
    }
    
    
    };
    saveAsset(): void 
    {
      if(this.taglist.length != 0){
        this.asset.tags = this.taglist.toString();
      }
      const data = 
      {
        cpe: this.asset.cpe,
        risk: this.asset.risk,
        baseSLA: (this.hours * 3600) + (this.minutes * 60),
        policyid: this.asset.policyid,
        hostname: this.asset.hostname,
        category: this.asset.category,
        tags: this.asset.tags
      }
      this.ticketService.createAsset(data)
      .subscribe({
        next: (res) => {
          console.log(res);
          this.submitted = true;
        },
        error: (e) => console.error(e)
      });
    };
    viewTags(): void {
      this.message = '';
        if(this.asset.tags !== '')
        {
          this.taglist = this.asset.tags.split(",");
          console.log(this.taglist);
        }

        this.viewTag=true;
  
    }
    removeTag(str: string){
      const index: number = this.taglist.indexOf(str);
      if (index !== -1) {
          this.taglist.splice(index, 1);
    }
  }
    addTag(vend: string, tech: string){
      this.message = '';
      vend.replace(',', '');
      tech.replace(',', '');
      if(vend == '' || tech == '')
      {
        this.message = "Vendor or Product missing values"
      }
      else
      {
        var str = "cpe:2.3:a:".concat(vend, ':', tech, ':*:*:*:*:*:*:*:*')
        const index: number = this.taglist.indexOf(str);
        if (index === -1) 
        {
          this.taglist.push(str);
        }
        else
        {
          this.message = "Duplicate Value";
        }  
      }
    }
}
