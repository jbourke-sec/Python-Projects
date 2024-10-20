import { Component, Inject, Input, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { User } from 'src/app/models/user.model';
import { UserService } from 'src/app/_services/user.service';
import { PolicyComponent } from '../policy/policy.component';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {

  @Input() viewMode = false;

  @Input() currentUser: User = {
    email: '',
    username: '',
    password: '',
    token: '',
    is_staff: '',
  };

  message = '';
  constructor(private userService: UserService,
    private route: ActivatedRoute,
    private router: Router,
    public dialogRef: MatDialogRef<PolicyComponent>,
    @Inject(MAT_DIALOG_DATA) public data: string,) { }

  ngOnInit(): void {
    if (!this.viewMode) {
      this.message = '';
      this.getuser(this.data);//may be number
    }
  }
  getuser(user: string): void {
    this.userService.getUser(user)
      .subscribe({
        next: (data) => {
          this.currentUser = data;
          console.log(data);
        },
        error: (e) => console.error(e)
      });
  }

  updateUser(): void {
    this.message = '';

    this.userService.updateUser(this.currentUser.email, this.currentUser)
      .subscribe({
        next: (res) => {
          console.log(res);
          this.message = res.message ? res.message : 'This Policy was updated successfully!';
        },
        error: (e) => console.error(e)
      });
  }
  deleteUser(): void {
    this.userService.deleteUser(this.currentUser.email)
      .subscribe({
        next: (res) => {
          console.log(res);
          this.router.navigate(['/users']);
        },
        error: (e) => console.error(e)
      });
  }
  closeUser() {
    this.dialogRef.close();
  }
}
