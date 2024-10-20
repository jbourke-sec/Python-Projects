import { Component, Inject, OnInit } from '@angular/core';
import { MatCheckboxChange } from '@angular/material/checkbox';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { Assets } from 'src/app/models/assets.model';
import { TicketsService } from 'src/app/services/tickets.service';

@Component({
  selector: 'app-asset-addition',
  templateUrl: './asset-addition.component.html',
  styleUrls: ['./asset-addition.component.css']
})
export class AssetAdditionComponent implements OnInit {

  addAssets?: Assets[];
  assets?: Assets[];

  constructor(public dialogRef: MatDialogRef<AssetAdditionComponent>,
    @Inject(MAT_DIALOG_DATA) public data: Assets[],
    public matDialog: MatDialog,
    private ticketService: TicketsService,
    private route: ActivatedRoute,
    private router: Router,) { }

  ngOnInit(): void {
    console.log(this.data);
    this.getAssets();
    
  }
  getAssets(): void {
    this.ticketService.getAssets()
      .subscribe({
        next: (res) => {
          this.assets = res;
          console.log(res);
        },
        error: (e) => console.error(e)
      });
  }
  initialAssets(): void {
    this.addAssets = this.data;
  }
  contains(value: Assets): boolean{
    console.log(value);
    console.log(this.data)
    console.log(this.data!.indexOf(value))
    return this.data.findIndex( element => element.assetid == value.assetid) !== -1;
 }
 onChange(ob: MatCheckboxChange, value: Assets) {
  if(this.contains(value))
  {
    this.data.splice(this.data.findIndex( element => element.assetid == value.assetid), 1);
  }
  else
  {
    this.data!.push(value);
  }
  console.log(this.data);
}
closeDialog(){
  this.assets = this.data
  this.dialogRef.close({assets: this.data});
}

  
}
