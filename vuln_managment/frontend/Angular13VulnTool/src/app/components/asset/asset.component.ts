import { Component, Inject, Input, OnInit, ViewChild } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { Assets } from 'src/app/models/assets.model';
import { TicketsService } from 'src/app/services/tickets.service';
import { TokenStorageService } from 'src/app/_services/token-storage.service';

@Component({
  selector: 'app-asset',
  templateUrl: './asset.component.html',
  styleUrls: ['./asset.component.css']
})
export class AssetComponent implements OnInit {

  @Input() viewMode = false;
  @Input() currentAsset: Assets = {
    assetid: '',
    cpe: '',
    risk: '',
    baseSLA: 0,
    policyid: '',
    category: '',
    hostname: '',
    tags: '',
  };
  vendor: string = '';
  tech: string = '';
  taglist: string[]= []
  message = '';
  viewTag: boolean = false;
  hours: number = 0;
  minutes: number = 0;
  secsinhour: number = 3600;
  secsinmin: number = 60;

  risk: any[] = [
    {value: 'High', viewValue: 'High'},
    {value: 'Medium', viewValue: 'Medium'},
    {value: 'Low', viewValue: 'Low'},
    {value: 'Not Defined', viewValue: 'Not Defined'},
  ];

  constructor(
    private ticketService: TicketsService,
    private route: ActivatedRoute,
    private router: Router,
    public dialogRef: MatDialogRef<AssetComponent>,
    @Inject(MAT_DIALOG_DATA) public data: string,
    public tokenStorage: TokenStorageService,) { }
    
  ngOnInit(): void {
    if (!this.tokenStorage.getToken()) {
      this.router.navigate(['/login']);
    }
    if (!this.viewMode) {
      this.message = '';
      this.getAsset(this.data);//may be number
      this.hours!=this.calcHours(this.currentAsset!.baseSLA!);
      this.minutes!=this.calcMins(this.currentAsset!.baseSLA!);
      this.viewTag= false;
      
    }
  }
  calcHours(time: number){
    return Math.floor((time)/(this.secsinhour));
  }
  calcMins(time: number){
    return Math.floor((time % this.secsinhour)/this.secsinmin);
  }
  getAsset(id: string): void {
    this.ticketService.getAsset(id)
      .subscribe({
        next: (data) => {
          this.currentAsset = data;
          this.hours=this.calcHours(data['baseSLA']!);
          this.minutes=this.calcMins(data['baseSLA']!);
          console.log(data);
        },
        error: (e) => console.error(e)
      });
      
  }

  updateAsset(): void {
    this.message = '';
    if(this.taglist.length != 0){
      this.currentAsset.tags = this.taglist.toString();
    }
    else
    {
      this.currentAsset.tags = '';
    }
    this.currentAsset.baseSLA = (this.hours * this.secsinhour) + (this.minutes * this.secsinmin);
    this.ticketService.updateAsset(this.currentAsset.assetid, this.currentAsset)
      .subscribe({
        next: (res) => {
          console.log(res);
          this.message = res.message ? res.message : 'This Asset was updated successfully!';
        },
        error: (e) => console.error(e)
      });
  }
  deleteAsset(): void {
    this.ticketService.deleteAsset(this.currentAsset.assetid)
      .subscribe({
        next: (res) => {
          console.log(res);
          this.router.navigate(['/assets']);
        },
        error: (e) => console.error(e)
      });
  }
  closeAsset() {
    this.dialogRef.close();
  }
  viewTags(): void {
    this.message = '';
      if(this.currentAsset.tags !== '')
      {
        this.taglist = this.currentAsset.tags.split(",");
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
