import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TokenStorageService } from './_services/token-storage.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent 
{
  title = 'Angular13VulnTool';

  isLoggedIn = false;
  email?: string;
  username?: string;
  super?: boolean;

  constructor(private tokenStorageService: TokenStorageService, private route: ActivatedRoute,
    private router: Router) { }

  ngOnInit(): void 
  {
    this.isLoggedIn = !!this.tokenStorageService.getToken();

    if (this.isLoggedIn) {
      const user = this.tokenStorageService.getUser();
      this.username = user.username;
      this.email = user.email;
      this.super = user.is_staff;
    }
    if (!this.tokenStorageService.getToken()) {
      this.router.navigate(['/login']);
    }
  }
  logout(): void 
  {
    this.tokenStorageService.signOut();
    window.location.reload();
  }
}
