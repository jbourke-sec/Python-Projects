import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Subject, tap } from 'rxjs';
import { Observable } from 'rxjs';
import { Assets } from '../models/assets.model';
import { Playbook } from '../models/playbook.model';
import { Policy } from '../models/policy.model';
import { Tickets } from '../models/tickets.model';
import { Vulnerability } from '../models/vulnerability.model';

const baseUrl = 'http://localhost:8080/vulnApp/api/queue';
const mytickets = 'http://localhost:8080/vulnApp/api/mytickets';
const assets = 'http://localhost:8080/vulnApp/api/asset';
const vuln = 'http://localhost:8080/vulnApp/api/vuln';
const playbook = 'http://localhost:8080/vulnApp/api/playbook';
const policy = 'http://localhost:8080/vulnApp/api/policy';
const users = 'http://localhost:8080/vulnApp/api/users';
const api = 'http://localhost:8080/vulnApp/api';


@Injectable({
  providedIn: 'root'
})

export class TicketsService {

  constructor( private http: HttpClient) { }

  private _RefreshNeeded$=new Subject<void>();
  getRefreshNeeded(){
    return this._RefreshNeeded$;
  }
  
  getAll(): Observable<Tickets[]> {
    return this.http.get<Tickets[]>(baseUrl).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  getMyTickets(): Observable<Tickets[]> {
    return this.http.get<Tickets[]>(mytickets).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  getClosedTickets(): Observable<Tickets[]> {
    return this.http.get<Tickets[]>(`${baseUrl}/closed`).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  getGroupTickets(group: any): Observable<Tickets[]> {
    return this.http.get<Tickets[]>(`${baseUrl}/group/${group}`).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  getTicket(ticketNumber: any): Observable<any>{
    return this.http.get(`${baseUrl}/${ticketNumber}`).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );;
  }
  updateTicket(ticketNumber: any, data: any): Observable<any>{
    return this.http.put(`${baseUrl}/${ticketNumber}`, data).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  deleteTicket(ticketNumber: any): Observable<any> {
    return this.http.delete(`${baseUrl}/${ticketNumber}`);
  }
  createTicket(data: any): Observable<any> {
    return this.http.post(baseUrl, data).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  getAssets(): Observable<Assets[]> {
    return this.http.get<Assets[]>(assets).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  getAssetsNoPolicy(): Observable<Assets[]> {
    return this.http.get<Assets[]>(`${assets}/nopolicy`).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  getAsset(id: any): Observable<Assets>{
    return this.http.get(`${assets}/${id}`);
  }
  updateAsset(id: any, data: any): Observable<any>{
    return this.http.put(`${assets}/${id}`, data).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  deleteAsset(id: any): Observable<any> {
    return this.http.delete(`${assets}/${id}`);
  }
  createAsset(data: any): Observable<any> {
    return this.http.post(assets, data).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  getVulns(): Observable<Vulnerability[]> {
    return this.http.get<Vulnerability[]>(vuln).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  getVuln(id: any): Observable<any>{
    return this.http.get(`${vuln}/${id}`).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  updateVuln(id: any, data: any): Observable<any>{
    return this.http.put(`${vuln}/${id}`, data).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  deleteVuln(id: any): Observable<any> {
    return this.http.delete(`${vuln}/${id}`);
  }
  createVuln(data: any): Observable<any> {
    return this.http.post(vuln, data).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  unremediatedVuln(): Observable<Vulnerability[]> {
    return this.http.get<Vulnerability[]>(`${vuln}/unremediated`).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  affectedVuln(): Observable<Vulnerability[]> {
    return this.http.get<Vulnerability[]>(`${vuln}/affected`).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  lastWeekVuln(): Observable<Vulnerability[]> {
    return this.http.get<Vulnerability[]>(`${vuln}/lastweek`).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  closedVuln(): Observable<Vulnerability[]> {
    return this.http.get<Vulnerability[]>(`${vuln}/closed`).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  getPlays(): Observable<Playbook[]> {
    return this.http.get<Playbook[]>(playbook);
  }
  getPlay(playbookid: any): Observable<Playbook>{
    return this.http.get(`${playbook}/${playbookid}`);
  }
  updatePlay(id: any, data: any): Observable<any>{
    return this.http.put(`${playbook}/${id}`, data);
  }
  deletePlay(id: any): Observable<any> {
    return this.http.delete(`${playbook}/${id}`);
  }
  createPlay(data: any): Observable<any> {
    return this.http.post(playbook, data).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  getPolicies(): Observable<Policy[]> {
    return this.http.get<Policy[]>(policy).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );;
  }
  getPolicy(id: any): Observable<Playbook>{
    return this.http.get(`${policy}/${id}`).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  updatePolicy(id: any, data: any): Observable<any>{
    return this.http.put(`${policy}/${id}`, data).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );;
  }
  deletePolicy(id: any): Observable<any> {
    return this.http.delete(`${policy}/${id}`);
  }
  createPolicy(data: any): Observable<any> {
    return this.http.post(policy, data).pipe(
      tap(() =>{
        this._RefreshNeeded$.next();
      })
    );
  }
  getUsers(): Observable<any>{
    return this.http.get(<any>(users));
  }
  returnClosedResults(days: any): Observable<any>{
    return this.http.get(<any>(`${api}/closedresults/${days}`));
  }
  returnAffectVulnBySev(): Observable<any>{
    return this.http.get(<any>(`${api}/vulnbysev`));
  }
  returnHasMetSLA(days: any):  Observable<any>{
    return this.http.get(<any>(`${api}/slastats/${days}`));
  }
  returnRemTimes(days: any): Observable<any>{
    return this.http.get(<any>(`${api}/avgremtimes/${days}`));
  }
  returnvulnsbyos(days: any):  Observable<any>{
    return this.http.get(<any>(`${api}/vulnsbyos/${days}`));
  }
  returnvulnsbyapp(days: any): Observable<any>{
    return this.http.get(<any>(`${api}/vulnsbyapp/${days}`));
  }
  returnvulnsbyhardware(days: any): Observable<any>{
    return this.http.get(<any>(`${api}/vulnsbyhardware/${days}`));
  }
  returnAssetCpes(): Observable<any>{
    return this.http.get(<any>(`${api}/assetbycpe`));
  }
  ticketprogbreakdown(): Observable<any>{
    return this.http.get(<any>(`${api}/progbreakdown`));
  }
  vulnbreakdown(): Observable<any>{
    return this.http.get(<any>(`${api}/vulnbreakdown`));
  }
}
