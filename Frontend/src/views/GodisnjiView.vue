<template>
    <div>
        <br>
        <div class="d-flex justify-content-between">
            <div class="card col-md-8" >
                <div class="card-header">
                    
                    <div class="d-flex justify-content-center">
                        <form class="d-flex col-md-8" role="search">
                            <input v-model="pretraga" class="form-control me-2" type="search" placeholder="Pretrazi po imenu..." aria-label="Search">
                            <button class="btn btn-outline-primary" type="submit">Pretrazi</button>
                        </form>
                    </div>
                </div>
                <div class="card-body">
                    <table class="table table-bordered table-light">
                        <thead>
                        <tr>
                            <th class="text-center" scope="col">ID</th>
                            <th class="text-center" scope="col">Opcije</th>
                            <th class="text-center" scope="col" style="width: 9em">Ime radnika</th>
                            <th class="text-center" scope="col">Ukupno 2024</th>
                            <th class="text-center" scope="col">Ukupno 2025</th>
                            <th class="text-center" scope="col">Iskorišćeni 2024</th>
                            <th class="text-center" scope="col">Iskorišćeni 2025</th>
                            <th class="text-center" scope="col">Preostali 2024</th>
                            <th class="text-center" scope="col">Preostali 2025</th>
                            
                        </tr>
                        </thead>
                        <tbody>
                        <tr v-for="godisnji,index in pretrazeniGodisnji" :key="index">
                            <td class="text-center" scope="row">{{ godisnji.id }}</td>
                            <td class="text-center d-flex justify-content-center gap-1">
                                <button @click="azurirajGodisnji(godisnji)" class="btn btn-outline-primary btn-sm" style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem;">Iskoristi</button>
                            
                            </td>
                            <td class="text-center" :class="proveriGodisnji(godisnji.godisnji_preostalo_2024,godisnji.godisnji_preostalo_2025)">{{ godisnji.ime_prezime }}</td>
                            <td class="text-center">{{ godisnji.godisnji_ukupno_2024 }}</td>
                            <td class="text-center">{{ godisnji.godisnji_ukupno_2025 }}</td>
                            <td class="text-center text-danger"><b>{{ godisnji.godisnji_iskorisceno_2024 }}</b></td>
                            <td class="text-center text-danger"><b>{{ godisnji.godisnji_iskorisceno_2025 }}</b></td>
                            <td class="text-center text-success"><b>{{ godisnji.godisnji_preostalo_2024 }}</b></td>
                            <td class="text-center text-success"><b>{{ godisnji.godisnji_preostalo_2025 }}</b></td>

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
            <div class=" col-md-4">
                <div v-if="prikazi" class="card" >
                    <div class="card-header">
                        <h5 class="text-center">Ažuriranje godišnjeg</h5>
                       
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="izmeniNaServeru">
                            <div class="row">
                                <div class="col">
                                    
                                    <input disabled v-model="trenutniGodisnji.ime_prezime" type="text" class="form-control" placeholder="First name" aria-label="First name">
                                </div>
                                
                            </div>
                            <hr>
                            <div class="row">
                                <div class="col">
                                    <label for=""><b>Preostali za 2024</b></label>
                                    <input disabled v-model="trenutniGodisnji.godisnji_preostalo_2024" type="text" class="form-control" placeholder="" aria-label="First name">
                                </div>
                                <div class="col">
                                    <label for=""><b>Preostali za 2025</b></label>
                                    <input disabled  v-model="trenutniGodisnji.godisnji_preostalo_2025" type="text" class="form-control" placeholder="" aria-label="Last name">
                                </div>
                            </div>
                            <hr>
                            <div class="row">
                                <div class="col">
                                    <label for=""><b>Iskoristi za 2024</b></label>
                                    <input v-model="iskoristi2024" type="number" class="form-control" placeholder="" aria-label="First name">
                                </div>
                                <div class="col">
                                    <label for=""><b>Iskoristi za 2025</b></label>
                                    <input v-model="iskoristi2025" type="number" class="form-control" placeholder="" aria-label="Last name">
                                </div>
                            </div>
                            <hr>
                            <div class="d-flex justify-content-between">
                                <span><button type="submit" class="btn btn-primary btn-sm">Sacuvaj izmene</button></span>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
export default {
    name: "Godisnji",
    data() {
        return {
            sviGodisnji : [],
            trenutnaStrana: 1,
            poStrani: 10,
            trenutniGodisnji: {
                id: null,
                ime: "",
                godisnji_ukupno_2024 : null,
                godisnji_ukupno_2025 : null,
                godisnji_iskorisceno_2024 : null,
                godisnji_iskorisceno_2025 : null,
                godisnji_preostalo_2024 : null,
                godisnji_preostalo_2025 : null,
            },
            iskoristi2024: null,
            iskoristi2025: null,
            prikazi: false,
            pretraga: "",
        }
    },
    methods: {
        async dohvatiPodatke(){
            const response = await axios.get('http://127.0.0.1:5000/godisnji')
            if(!response){
                console.log('GRESKA PRILIKOM DOHVATANJA PODATAKA')
                return
            }
            this.sviGodisnji = response.data.data.data
            
        },
        azurirajGodisnji(godisnji){
            this.trenutniGodisnji = godisnji
            this.iskoristi2024 = 0
            this.iskoristi2025 = 0
            console.log(this.trenutniGodisnji)
            this.prikazi = true
            
        },
        izmeniNaServeru(){
            console.log('menjam na serveru')
            // formatiranje podataka
            if(this.iskoristi2024 > this.trenutniGodisnji.godisnji_preostalo_2024){
                this.$toast.error('Radnik nema dovoljan broj dana za korišćenje.')
                return
            }
            if(this.iskoristi2025 > this.trenutniGodisnji.godisnji_preostalo_2025){
                this.$toast.error('Radnik nema dovoljan broj dana za korišćenje.')
                return
            }
            this.trenutniGodisnji.godisnji_preostalo_2024 -= this.iskoristi2024
            this.trenutniGodisnji.godisnji_preostalo_2025 -= this.iskoristi2025
            this.trenutniGodisnji.godisnji_iskorisceno_2024 += this.iskoristi2024
            this.trenutniGodisnji.godisnji_iskorisceno_2025 += this.iskoristi2025

            console.log(this.trenutniGodisnji) // OVO JE SADA FORMATIRAN OBJEKAT KOJI TREBA DA PROSLEIDM AXIOSU ZA UPDATE

            axios.post('http://127.0.0.1:5000/azuriraj-godisnji', this.trenutniGodisnji)
            .then(response => {
                console.log('Podaci su uspešno poslati:', response);
                // Možete dodati logiku za obaveštavanje korisnika ili ažuriranje UI-a
                // location.reload()
                this.$toast.success(`Usešno ste iskoristili godisnji.`)
            })
            .catch(error => {
                console.error('Greška prilikom slanja podataka:', error);
            });
            this.prikazi = false
            this.iskoristi2024 = 0
            this.iskoristi2025 = 0
            
        },
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
        idiNaStranu(strana){
            this.trenutnaStrana = strana    
        },
        proveriGodisnji(godisnji2024, godisnji2025){
            if(godisnji2024 == 0 && godisnji2025 == 0){
                return 'isteklo'
            } return 'zeleno'
        }
    },
    computed: {
        ukupnoStrana(){
            return Math.ceil(this.sviGodisnji.length / 10)
        },
        paginisaniGodisnji(){
            const startIndex = (this.trenutnaStrana - 1) * this.poStrani
            const lastIndex = this.trenutnaStrana * this.poStrani
            return this.sviGodisnji.slice(startIndex,lastIndex)
        },
        pretrazeniGodisnji(){
            if(this.pretraga == '') {
                return this.paginisaniGodisnji
            }
            return this.sviGodisnji.filter((godisnji) => godisnji.ime_prezime.toLowerCase().includes(this.pretraga.toLowerCase()))
        }
    },
    mounted() {
        this.dohvatiPodatke()
    },
}
</script>
<style scoped>
    .isteklo{
        background-color: red;
    }
    .zeleno{
        background-color: rgb(7, 238, 80);
    }
</style>