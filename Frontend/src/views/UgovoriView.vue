<template >
    <div>
        <div class="card col-md-9">
            <div class="card-header">
                
                <div class="d-flex justify-content-center">
                    <form class="d-flex col-md-8" role="search">
                        <input v-model="pretraga" class="form-control me-2" type="search" placeholder="Pretrazi po imenu..." aria-label="Search">
                        <button class="btn btn-outline-primary" type="submit">Pretrazi</button>
                    </form>
                </div>
            </div>
            <div class="card-body">
                <!-- <p class="text-center"><b><i class="text-dark">Strana {{ trenutnaStrana }} ... {{ ukupnoStrana }}</i></b></p> -->
                <table class="table table-bordered table-light">
                    <thead>
                    <tr>
                        <th class="text-center" scope="col">ID</th>
                        <th class="text-center" scope="col">Ime radnika</th>
                        <th class="text-center" scope="col">Tip zaposlenja</th>
                        <th class="text-center" scope="col">Pocetak ugovora</th>
                        <th class="text-center" scope="col">Kraj ugovora</th>
                        <th class="text-center" scope="col">Slava</th>
                        <th class="text-center" scope="col">Datum slave</th>
                        <th class="text-center" scope="col">Opcije</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="ugovor,index in pretrazeniUgovori" :key="index">
                        <td class="text-center" scope="row">{{ ugovor.id }}</td>
                        <td class="text-center">{{ ugovor.ime_radnika }}</td>
                        <td class="text-center">{{ ugovor.tip_zaposlenja }}</td>
                        <td class="text-center">{{ ugovor.datum_pocetka }}</td>
                        <td class="text-center"><b>{{ ugovor.datum_zavrsetka }}</b></td>
                        <td class="text-center"><b>{{ ugovor.slava }}</b></td>
                        <td class="text-center"><b>{{ ugovor.datum_slave }}</b></td>                     
                        <td class="text-center d-flex justify-content-center gap-1">
                            <button @click="azurirajGodisnji(ugovor)" class="btn btn-primary btn-sm">Ažuriraj</button>
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
    </div>
</template>
<script>
import axios from 'axios';
export default {
    name: "UgovoriView",
    data() {
        return {
            sviUgovori : [],
            trenutnaStrana : 1,
            poStrani : 10,
            pretraga : ""
        }
    },
    methods: {
        async dohvatiPodatke(){
            const response = await axios.get('http://127.0.0.1:5000/ugovori')
            if(!response){
                console.log('Greska prilikom dohvatanja podataka iz baze!')
                return 
            }
            console.log(response)
            this.sviUgovori = response.data.data.data
            console.log(this.sviUgovori)
        },
        idiNaStranu(strana){
            this.trenutnaStrana = strana
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
    },
    computed: {
        ukupnoStrana(){
            console.log(this.sviUgovori.length)
            return Math.ceil(this.sviUgovori.length / 10)

        },
        paginisaniUgovori(){
            const startIndex = (this.trenutnaStrana - 1) * this.poStrani
            const lastIndex = this.trenutnaStrana * this.poStrani
            return this.sviUgovori.slice(startIndex,lastIndex)
        },
        pretrazeniUgovori(){
            if(this.pretraga == ''){
                return this.paginisaniUgovori
            }
            return this.sviUgovori.filter((ugovor) => ugovor.ime_radnika.toLowerCase().includes(this.pretraga.toLowerCase()))
        }
    },
    mounted() {
        this.dohvatiPodatke()
    },
}
</script>
<style scoped>
    
</style>