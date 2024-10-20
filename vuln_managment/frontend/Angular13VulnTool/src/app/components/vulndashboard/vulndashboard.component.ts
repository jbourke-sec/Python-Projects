import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TokenStorageService } from 'src/app/_services/token-storage.service';

@Component({
  selector: 'app-vulndashboard',
  templateUrl: './vulndashboard.component.html',
  styleUrls: ['./vulndashboard.component.css']
})
export class VulndashboardComponent implements OnInit {

  constructor(private route: ActivatedRoute,
    private router: Router,public tokenStorage: TokenStorageService,) { }

  ngOnInit(): void {
    if (!this.tokenStorage.getToken()) {
      this.router.navigate(['/login']);
    }
  }

}
