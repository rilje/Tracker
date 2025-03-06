<template >

    <div class="card col-md-8">
        <div class="card-header">
            <h4 class="text-center">LEKARSKI I BZR OBUKA</h4>
            <b><i class="text-dark">Strana {{ trenutnaStrana }} ... {{ ukupnoStrana }}</i></b>
        </div>
        <div class="card-body">
            <table class="table table-bordered table-success">
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
                <tr v-for="radnik,index in pretrazeniRadnici" :key="index">
                <th class="text-center" scope="row">{{ radnik.id }}</th>
                <td  class="text-center">{{ radnik.ime }}</td>
                <td class="text-center"  :class="proveriDatum(radnik.lekarski)">{{radnik.lekarski}}</td>
                <td class="text-center"  :class="proveriDatum(radnik.bzr)">{{ radnik.bzr }}</td>
                <td class="text-center d-flex justify-content-center gap-1">
                    <button @click="azurirajRadnika(radnik)" class="btn btn-primary btn-sm">Ažuriraj</button>
                    <span><button @click="obrisiRadnika(radnik.id)" class="btn btn-danger btn-sm">Obriši</button></span>
                </td>
                </tr>
            </tbody>
            </table>
            <div class="d-flex justify-content-center">
            <nav aria-label="Page navigation example">
                <ul class="pagination">
                <li :class="{disabled : trenutnaStrana == 1}" @click="prethodnaStrana" class="page-item">
                    <a class="page-link" role="button">Previous</a>
                </li>
                <li @click="idiNaStranu(strana)" v-for="strana in ukupnoStrana" class="page-item"><a class="page-link" href="#">{{ strana }}</a></li>
                <li :class="{disabled : trenutnaStrana == ukupnoStrana}" @click="sledecaStrana" class="page-item"><a class="page-link" href="#">Next</a></li>
                </ul>
            </nav>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "Tabela",
    props: {
        pretrazeniRadnici : {
            type : Array,
            required : true
        },
        trenutnaStrana : {
            type: Number,
            required : true
        },
        ukupnoStrana : {
            type: Number,
            required : true
        }

    }
}
</script>
<style >
    
</style>