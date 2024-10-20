import { Injectable } from '@angular/core';
import { Observable, Subject, tap } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { User } from '../models/user.model';


const api = 'http://localhost:8080/vulnApp/api';
@Injectable({
  providedIn: 'root'
})

export class UserService {

  constructor(private http: HttpClient) { }

  private _RefreshNeeded$=new Subject<void>();
  getRefreshNeeded(){
    return this._RefreshNeeded$;
  }
  

  getUser(email: any): Observable<any>{
    return this.http.get(`${api}/user/${email}`).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );;
  }
  updateUser(email: any, data: any): Observable<any>{
    return this.http.put(`${api}/user/${email}`, data).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  deleteUser(email: any): Observable<any> {
    return this.http.delete(`${api}/user/${email}`);
  }
  createUser(data: any): Observable<any> {
    return this.http.post(`${api}/userslist`, data).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${api}/userslist`).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
}
