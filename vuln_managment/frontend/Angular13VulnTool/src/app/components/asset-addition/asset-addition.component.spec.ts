import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AssetAdditionComponent } from './asset-addition.component';

describe('AssetAdditionComponent', () => {
  let component: AssetAdditionComponent;
  let fixture: ComponentFixture<AssetAdditionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AssetAdditionComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AssetAdditionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
