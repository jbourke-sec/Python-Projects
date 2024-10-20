import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AddplaybookComponent } from './components/addplaybook/addplaybook.component';
import { AddpolicyComponent } from './components/addpolicy/addpolicy.component';
import { AddvulnerabilityComponent } from './components/addvulnerability/addvulnerability.component';
import { AssetComponent } from './components/asset/asset.component';
import { AssetlistComponent } from './components/assetlist/assetlist.component';
import { BarchartComponent } from './components/barchart/barchart.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { NewAssetComponent } from './components/new-asset/new-asset.component';
import { AddTicketComponent } from './components/new-ticket/new-ticket.component';
import { PlaybookComponent } from './components/playbook/playbook.component';
import { PlaybooksComponent } from './components/playbooks/playbooks.component';
import { PoliciesComponent } from './components/policies/policies.component';
import { PolicyComponent } from './components/policy/policy.component';
import { QueueComponent } from './components/queue/queue.component';
import { TicketDetailsComponent } from './components/ticket-details/ticket-details.component';
import { UsersComponent } from './components/users/users.component';
import { VulndashboardComponent } from './components/vulndashboard/vulndashboard.component';
import { VulnerabilitiesComponent } from './components/vulnerabilities/vulnerabilities.component';
import { VulnerabilityComponent } from './components/vulnerability/vulnerability.component';
import { LoginComponent } from './login/login.component';

const routes: Routes = [
  { path: 'queue', component: QueueComponent },
  { path: 'queue/newticket', component: AddTicketComponent},
  { path: 'queue/tickets/:ticketNumber', component: TicketDetailsComponent },
  { path: 'mytickets', component: QueueComponent },
  { path: 'login', component: LoginComponent },
  { path: 'assets/:assetid', component: AssetComponent},
  { path: 'newasset', component: NewAssetComponent},
  { path: 'assets',component: AssetlistComponent},
  { path: 'vuln', component: VulnerabilitiesComponent},
  { path: 'vuln/:vulnid', component:VulnerabilityComponent },
  { path: 'vuln/new', component:AddvulnerabilityComponent},
  { path: 'playbook', component:PlaybooksComponent},
  { path: 'playbook/:playbookid', component:PlaybookComponent},
  { path: 'playbook/new', component:AddplaybookComponent},
  { path: 'policy', component:PoliciesComponent},
  { path: 'policy/:policyid', component:PolicyComponent},
  { path: 'policy/new', component:AddpolicyComponent},
  { path: 'dashboard', component:DashboardComponent},
  { path: 'vulndashboard', component:VulndashboardComponent},
  { path: 'users', component:UsersComponent},
  { path: '', component:LoginComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
