import { Component, OnInit } from '@angular/core';
import { ModalController } from '@ionic/angular';
import { Storage } from '@ionic/storage'

@Component({
  selector: 'app-search-filter',
  templateUrl: './search-filter.page.html',
  styleUrls: ['./search-filter.page.scss'],
})
export class SearchFilterPage implements OnInit {
  public radiusmiles = 1;
  public minmaxprice = {
    upper: 500,
    lower: 10
  };
  public organizeby;
  public dishtype;
  public dishnationality;
  public zipcode;


  constructor(private modalCtrl: ModalController, private storage: Storage) { }

  ngOnInit() {
    this.storage.get("zipcode").then((zipcode) => {
      this.zipcode = zipcode;
    })
  }

  closeModal() {
    this.storage.set("zipcode", this.zipcode)
    this.modalCtrl.dismiss({
      radius: this.radiusmiles,
      minmaxprice: this.minmaxprice,
      organizeby: this.organizeby,
      dishtype: this.dishtype,
      dishnationality: this.dishnationality
    });
  }

}
