import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { User } from 'src/app/models/user.model';
import { UserService } from 'src/app/_services/user.service';
import { UserComponent } from '../user/user.component';

@Component({
  selector: 'app-newuser',
  templateUrl: './newuser.component.html',
  styleUrls: ['./newuser.component.css']
})
export class NewuserComponent implements OnInit {

  user: User = {
    email: '',
    username: '',
    password: '',
  };
  message = '';
  submitted = false;
  constructor(private userService: UserService,
    private route: ActivatedRoute,
    private router: Router,
    public dialogRef: MatDialogRef<UserComponent>,
    @Inject(MAT_DIALOG_DATA) public data: string,) { }

  ngOnInit(): void {
  }

  newUser(): void {
    this.submitted = false;
    this.user = {
      email: '',
    username: '',
    password: '',
    }
    
    
    };
    saveUser(): void 
    {
      const data = 
      {
        email: this.user.email,
        username: this.user.username,
        password: this.user.password,
      }
      this.userService.createUser(data)
      .subscribe({
        next: (res) => {
          console.log(res);
          this.submitted = true;
        },
        error: (e) => console.error(e)
      });
    };
    closeUser() {
      this.dialogRef.close();
    }
}
