<template>
  <div>
    <br>

    <div class="d-flex justify-content-between">
      <!-- PRVI -->

      <div class="card col-md-8">
        <div class="card-header">
          <h4 class="text-center">LEKARSKI I BZR OBUKA</h4>
          
        </div>
        <div class="card-body">
          
          
          <table class="table table-bordered table-light">
            <thead>
              <tr>
                <th class="text-center" scope="col">ID</th>
                <th class="text-center" scope="col">Ime</th>
                <th class="text-center" scope="col">Lekarski</th>
                <th class="text-center" scope="col">BZR</th>
                <th class="text-center" scope="col">Opcije</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="radnik,index in filtriraniKorisnici" :key="index">
                <td class="text-center" scope="row">{{ radnik.id }}</td>
                <td  class="text-center">{{ radnik.ime }}</td>
                <td class="text-center"  :class="proveriDatum(radnik.lekarski)">{{radnik.lekarski}}</td>
                <td class="text-center"  :class="proveriDatum(radnik.bzr)">{{ radnik.bzr }}</td>
                <td class="text-center d-flex justify-content-center gap-1">
                  <button @click="azurirajRadnika(radnik)" class="btn btn-outline-primary btn-sm" style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .79rem;">Ažuriraj</button>
                  <span><button @click="obrisiRadnika(radnik.id)" class="btn btn-outline-danger btn-sm" style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .79rem;">Obriši</button></span>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="d-flex justify-content-center">
            <nav aria-label="Page navigation example">
              <ul class="pagination">
                <li :class="{disabled : trenutnaStrana == 1}" @click="prethodnaStrana" class="page-item"><a class="page-link" href="#">Previous</a></li>
                <li @click="idiNaStranu(strana)" v-for="strana in ukupnoStrana" class="page-item"><a class="page-link" href="#">{{ strana }}</a></li>
                <li :class="{disabled : trenutnaStrana == ukupnoStrana}" @click="sledecaStrana" class="page-item"><a class="page-link" href="#">Next</a></li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
      <!-- DRUGI -->
      <div class="card col-md-4 desniDiv">
        <div class="card-header">
          <form class="d-flex" role="search">
              <input v-model="pretraga" class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
              <button class="btn btn-outline-success" type="submit">Pretrazi</button>
          </form>
        </div>
        <div class="card-body">
          <div v-if="prikaziUpdate">
            <h5 class="text-center"><i>Ažuriranje radnika</i></h5>
            <hr>
            <form @submit.prevent="azurirajRadnikaNaServeru" method="POST">
              <div class="mb-3">
                <label for="exampleInputEmail1" class="form-label">Ime i prezime</label>
                <input v-model="radnik.ime" type="text" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
              </div>
              <div class="mb-3">
                <label for="exampleInputPassword1" class="form-label">Lekarski (dd.mm.yyyy)</label>
                <input v-model="radnik.lekarski" type="text" class="form-control" id="exampleInputPassword1">
              </div>
              <div class="mb-3">
                <label for="exampleInputPassword1" class="form-label">BZR (dd.mm.yyyy)</label>
                <input v-model="radnik.bzr" type="text" class="form-control" id="exampleInputPassword1">
              </div>
              <hr>
              <div class="d-flex justify-content-between">
                <span class=""><button type="submit" class="btn  btn-primary btn-sm">Sačuvaj izmene</button></span>
                <span><button @click="zatvoriProzor" type="submit" class="btn btn-danger btn-sm">Zatvori prozor</button></span>
              </div>
            </form>
          </div>
          <br>
          <ul class="list-group">
            <div class="card" style="">

              <div class="card-header">
                <b>FILTER</b>
              </div>
              <ul class="list-group list-group-flush">
                <li class="list-group-item d-flex justify-content-between align-items-center text-secondary">
                  <a class="klik" @click="izmeniFilter('istekliLekarski')"><b><i>Istekli lekarski</i></b></a>
                  <span class="badge text-bg-success rounded-pill" :class="{'text-bg-danger' : brojIsteklihLekarskih > 0}">{{ brojIsteklihLekarskih }}</span>
                </li>
                <li :class="{'list-group-item disabled' : brojLekarskihPredIstek == 0}" class="list-group-item d-flex justify-content-between align-items-center text-secondary">
                  <a class="klik" @click="izmeniFilter('lekarskiPred')"><b><i>Lekarski pred istek</i></b></a>
                  <span class="badge text-bg-success rounded-pill"  :class="{'text-bg-danger' : brojLekarskihPredIstek > 0}">{{ brojLekarskihPredIstek }}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center text-secondary">
                  <a class="klik" @click="izmeniFilter('istekliBzr')"><b><i>Istekli BZR</i></b></a>
                  <span class="badge text-bg-success rounded-pill" :class="{'text-bg-danger' : brojIsteklihBzr > 0}">{{ brojIsteklihBzr }}</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center text-secondary">
                  <a class="klik" @click="izmeniFilter('bzrPred')"><b><i>BZR pred istek</i></b></a>
                  <span class="badge text-bg-success rounded-pill" :class="{'text-bg-danger' : brojBzrPredIstek > 0}">{{ brojBzrPredIstek }}</span>
                </li>

              </ul>
              <div  class="d-flex justify-content-end align-items-center p-2" v-if="filter != ''">
                <button @click="izmeniFilter('')" class="btn btn-danger btn-sm" style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem;">PONIŠTI FILTER</button>
              </div>
            </div>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
// Importovanje komponenti
import Navigacija from '@/components/Navigacija.vue';
import Tabela from '@/components/Tabela.vue';
import axios from 'axios';
import moment from 'moment'; 

export default {
  components: {
    Navigacija,
    Tabela,
  },
  
  data() {
    return {
      radnici : [],
      // Za Paginaciju
      trenutnaStrana : 1,
      poStrani: 10,
      // Za Azuriranje Radnika
      radnik : {
        id : null,
        ime : '',
        lekarski : '',
        bzr : '',
      },
      // Za prikazivanje menija za azuriranje
      prikaziUpdate : false,
      // Pretraga
      pretraga : '',
      // Filter
      filter : '',

    }
  },
  methods: {
    // Funkcija za dohvatanje podataka iz baze
    async dohvatiPodatke(){
      const response = await axios.get('http://127.0.0.1:5000')
      if(response){
        console.log(response)
        this.radnici = response.data.data.radnici
      }
    },
    // Funkcija za promenu strane
    idiNaStranu(strana){
      this.trenutnaStrana = strana
    },
    // Logika za datume
    proveriDatum(datum) {
      const danas = moment();
      const lekarskiDatum = moment(datum, 'DD.MM.YYYY');
      const razlikaUMesecima = danas.diff(lekarskiDatum, 'months');

      if (razlikaUMesecima >= 12) {
        return 'crveno';
      } else if (razlikaUMesecima >= 11) {
        return 'zuto';
      } else {
        return '';
      }
    },
    // Funkcija koja salje na prethodnu stranu
    prethodnaStrana(){
      if(this.trenutnaStrana == 1){
        return
      }
      this.trenutnaStrana -= 1
    },
    // Funkcija koja salje na sledecu stranu
    sledecaStrana(){
      if(this.trenutnaStrana == this.ukupnoStrana){
        return
      }
      this.trenutnaStrana += 1 
    },
    // Funkcija koja dohvata radnika i unosi njegove vrednosti u meni za azuriranje
    azurirajRadnika(radnik){
      console.log(radnik)
      this.radnik = radnik
      this.prikaziUpdate = true   
    },
    // Funkcija koja salje api zahtev serveru i azurira radnika
    azurirajRadnikaNaServeru() {
    // Formatiranje datuma pre slanja na server
    const formattedRadnik = {
      id: this.radnik.id,
      ime: this.radnik.ime,
      lekarski: moment(this.radnik.lekarski, 'DD.MM.YYYY').format('YYYY-MM-DD'), // formatirati datum ako je potrebno
      bzr: moment(this.radnik.bzr, 'DD.MM.YYYY').format('YYYY-MM-DD'), // isto za BZR
    };

    // Slanje POST zahteva sa podacima
    axios.post('http://127.0.0.1:5000/azuriraj-radnika', formattedRadnik)
      .then(response => {
        console.log('Podaci su uspešno poslati:', response);
        // Možete dodati logiku za obaveštavanje korisnika ili ažuriranje UI-a
        // location.reload()
        this.$toast.success(`Usešno ste ažurirali korisnika ${formattedRadnik.ime}`)
      })
      .catch(error => {
        console.error('Greška prilikom slanja podataka:', error);
      });
      
  },
  zatvoriProzor(){
    this.prikaziUpdate = false
    return
  },
  izmeniFilter(filter){
    this.filter = filter
  }


    
  },
  computed: {
    filtriraniKorisnici(){
      if(this.filter == ''){
        return this.pretrazeniRadnici 
      }else if(this.filter == 'istekliLekarski'){
        console.log( this.radnici.filter((radnik) => this.proveriDatum(radnik.lekarski) == 'crveno'))
        return this.radnici.filter((radnik) => this.proveriDatum(radnik.lekarski) == 'crveno')
      }else if(this.filter == 'lekarskiPred'){
        return this.radnici.filter((radnik) => this.proveriDatum(radnik.lekarski) == 'zuto')
      }else if(this.filter == 'istekliBzr'){
        return this.radnici.filter((radnik) => this.proveriDatum(radnik.bzr) == 'crveno')      
      }else if(this.filter == 'bzrPred'){
        return this.radnici.filter((radnik) => this.proveriDatum(radnik.bzr) == 'zuto')
      }
      
    },
    paginisaniRadnici(){
      const startIndex = (this.trenutnaStrana - 1) * this.poStrani
      const lastIndex = this.trenutnaStrana * this.poStrani
      return this.radnici.slice(startIndex,lastIndex)
    },
    ukupnoStrana(){
      return Math.ceil(this.radnici.length / 10)
    },
    pretrazeniRadnici(){
      if(this.pretraga == ''){
        return this.paginisaniRadnici
      }
      return this.radnici.filter((radnik) => radnik.ime.toLowerCase().includes(this.pretraga.toLowerCase()) )
    },
    brojIsteklihLekarskih(){
      let istekliLekarski = 0
      const danas = moment()
      for (const radnik of this.radnici) {
        let lekarskiDatum = moment(radnik.lekarski, 'DD.MM.YYYY')
        let razlikaUMesecima = danas.diff(lekarskiDatum, 'months')
        if(razlikaUMesecima >= 12){
          istekliLekarski += 1
        }
      }
      return istekliLekarski
    },
    brojIsteklihBzr(){
      let istekliLekarski = 0
      const danas = moment()
      for (const radnik of this.radnici) {
        let lekarskiDatum = moment(radnik.bzr, 'DD.MM.YYYY')
        let razlikaUMesecima = danas.diff(lekarskiDatum, 'months')
        if(razlikaUMesecima >= 12){
          istekliLekarski += 1
        }
      }
      return istekliLekarski
    },
    brojLekarskihPredIstek(){
      
      let predIstek = 0
      const danas = moment()
      for (const radnik of this.radnici) {
        let lekarskiDatum = moment(radnik.lekarski, 'DD.MM.YYYY')
        let razlikaUMesecima = danas.diff(lekarskiDatum, 'months')
        if(razlikaUMesecima >= 11 && razlikaUMesecima < 12){
          predIstek += 1
        }
      }
      return predIstek
    },
    brojBzrPredIstek(){
      
      let predIstek = 0
      const danas = moment()
      for (const radnik of this.radnici) {
        let lekarskiDatum = moment(radnik.bzr, 'DD.MM.YYYY')
        let razlikaUMesecima = danas.diff(lekarskiDatum, 'months')
        if(razlikaUMesecima >= 11 && razlikaUMesecima < 12){
          predIstek += 1
        }
      }
      return predIstek
    }

  },
  mounted() {
    this.dohvatiPodatke()
  },
}
</script>
<style scoped>
  .klik{
    cursor: pointer;
  }
  .zuto {
    background-color: rgb(255, 234, 0);
  }
  .crveno {
    background-color: red;
  }
  table {
    width: 100%;
    border-collapse: separate; 
    /* border-spacing: 0 10px;  */
  }
  th, td {
    padding: 8px 12px;
    text-align: left;
  }
  th {
    background-color: #f2f2f2;
  }
  tbody tr:nth-child(even) {
    background-color: #f9f9f9;
  }
  .desniDiv{
    height: auto;
  }
  .klik{
    text-decoration: underline;
    color: rgb(33, 167, 235);
  }
</style>