import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { QueueComponent } from './components/queue/queue.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { TicketDetailsComponent } from './components/ticket-details/ticket-details.component';
import { authInterceptorProviders } from './_helpers/auth.interceptor';
import { LoginComponent } from './login/login.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { AddTicketComponent } from './components/new-ticket/new-ticket.component';
import { VulnerabilityComponent } from './components/vulnerability/vulnerability.component';
import { AssetComponent } from './components/asset/asset.component';
import { AssetlistComponent } from './components/assetlist/assetlist.component';
import { NewAssetComponent } from './components/new-asset/new-asset.component';
import { VulnerabilitiesComponent } from './components/vulnerabilities/vulnerabilities.component';
import { AddvulnerabilityComponent } from './components/addvulnerability/addvulnerability.component';
import { PoliciesComponent } from './components/policies/policies.component';
import { PolicyComponent } from './components/policy/policy.component';
import { AddpolicyComponent } from './components/addpolicy/addpolicy.component';
import { PlaybooksComponent } from './components/playbooks/playbooks.component';
import { AddplaybookComponent } from './components/addplaybook/addplaybook.component';
import { PlaybookComponent } from './components/playbook/playbook.component';
import {MatCommonModule, MatRippleModule } from '@angular/material/core';
import {MatSelectModule} from '@angular/material/select';
import {MatListModule} from '@angular/material/list';
import { CommonModule } from '@angular/common';
import { ListViewModule } from '@syncfusion/ej2-angular-lists';
import { MatTableModule } from '@angular/material/table' 
import { MatPaginatorModule } from '@angular/material/paginator';
import {MatSortModule} from '@angular/material/sort';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { CloseTicketDialogComponent } from './components/close-ticket-dialog/close-ticket-dialog.component';
import { ReopenTicketDialogComponent } from './components/reopen-ticket-dialog/reopen-ticket-dialog.component';
import { QaTicketDialogComponent } from './components/qa-ticket-dialog/qa-ticket-dialog.component';
import {MatCheckboxModule} from '@angular/material/checkbox';
import { AssetAdditionComponent } from './components/asset-addition/asset-addition.component';
import { SlatimerComponent } from './components/slatimer/slatimer.component';
import {MatToolbarModule} from '@angular/material/toolbar';
import { BarchartComponent } from './components/barchart/barchart.component';
import {ApolloModule, APOLLO_OPTIONS} from 'apollo-angular';
import {HttpLink} from 'apollo-angular/http';
import {InMemoryCache} from '@apollo/client/core';
import { NgxChartsModule }from '@swimlane/ngx-charts';
import { PiechartComponent } from './components/piechart/piechart.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import {MatCardModule} from '@angular/material/card';
import { NumberchartComponent } from './components/numberchart/numberchart.component';
import {MatGridListModule} from '@angular/material/grid-list';
import { LinechartComponent } from './components/linechart/linechart.component';
import { HorizontalbarchartComponent } from './components/horizontalbarchart/horizontalbarchart.component';
import { AdvancedpiechartComponent } from './components/advancedpiechart/advancedpiechart.component';
import { GaugechartComponent } from './components/gaugechart/gaugechart.component';
import { GroupedVerticalBarComponent } from './components/grouped-vertical-bar/grouped-vertical-bar.component';
import { VulndashboardComponent } from './components/vulndashboard/vulndashboard.component';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import { UserComponent } from './components/user/user.component';
import { UsersComponent } from './components/users/users.component';
import { NewuserComponent } from './components/newuser/newuser.component';


@NgModule({
  declarations: [
    AppComponent,
    QueueComponent,
    TicketDetailsComponent,
    LoginComponent,
    AddTicketComponent,
    VulnerabilityComponent,
    AssetComponent,
    AssetlistComponent,
    NewAssetComponent,
    VulnerabilitiesComponent,
    AddvulnerabilityComponent,
    PoliciesComponent,
    PolicyComponent,
    AddpolicyComponent,
    PlaybooksComponent,
    AddplaybookComponent,
    PlaybookComponent,
    CloseTicketDialogComponent,
    ReopenTicketDialogComponent,
    QaTicketDialogComponent,
    AssetAdditionComponent,
    SlatimerComponent,
    BarchartComponent,
    PiechartComponent,
    DashboardComponent,
    NumberchartComponent,
    LinechartComponent,
    HorizontalbarchartComponent,
    AdvancedpiechartComponent,
    GaugechartComponent,
    GroupedVerticalBarComponent,
    VulndashboardComponent,
    UserComponent,
    UsersComponent,
    NewuserComponent,
    
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatDialogModule,
    MatButtonToggleModule,
    FormsModule,
    ReactiveFormsModule,
    MatRippleModule,
    MatCommonModule,
    MatSelectModule,
    CommonModule,
    ListViewModule,
    MatListModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatExpansionModule,
    MatButtonModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatCheckboxModule,
    MatToolbarModule,
    ApolloModule,
    NgxChartsModule,
    MatCardModule,
    MatGridListModule,
    MatSidenavModule,
    MatToolbarModule,
    MatProgressSpinnerModule,
    

  ],
  providers: [ {
    provide: APOLLO_OPTIONS,
    useFactory: (httpLink: HttpLink) => {
      return {
        cache: new InMemoryCache(),
        link: httpLink.create({
          uri: 'http://localhost:8080/vulnApp/api/graphql',
        }),
      };
    },
    deps: [HttpLink],
  },
    authInterceptorProviders],
  bootstrap: [AppComponent],
  
})
export class AppModule { }
