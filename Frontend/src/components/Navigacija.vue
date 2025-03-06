<template>
    <div>
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">
                    <img class="logoSlika" src="/crni logo.png" alt="">
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li v-for="item,index in navigacija" class="nav-item">
                            <RouterLink class="nav-link active" aria-current="page" :to="item.url"><b><h5>{{item.name}}</h5></b></RouterLink>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </div>
</template>
<script>
export default {
    name: "Navigacija",
    data() {
        return {
            navigacija: [
                {
                    name: 'Lekarski&BZR',
                    url: '/'
                },
                {
                    name: 'GODIŠNJI',
                    url: '/godisnji'
                },
                {
                    name: 'UGOVORI',
                    url: '/ugovori'
                }
            ]
        }
    },
}
</script>
<style >
    .logoSlika{
        width: 150px;
    }
</style>