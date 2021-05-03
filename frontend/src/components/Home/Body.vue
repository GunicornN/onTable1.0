<template>
    <div>
        <div>
            <div>
                <img src="../../assets/home/plat.png" alt="plats">
            </div>

            <div>
                <SearchBar/>
            </div>
            <div>
                <h2>UN ENGAGEMENT AUPRÈS DES RESTAURATEURS ET RESTAURATRICES</h2>
                
                <p>Durant la période du confinement nous avons imaginé une façon SIMPLE pour les restaurateurs / restauratrices de laisser tomber leurs cartes traditionnelles, sources de propagation du virus, pour que celles-ci apparaissent directement dans le téléphone de leurs clients.
                Le contexte sanitaire que nous connaissons nous a amenés à développer cette idée, et proposer un service mis à disposition GRATUITEMENT, permettant aux restaurateurs de diffuser leurs cartes aux clients via un QR Code.</p>
            </div>
        </div>

        <h1>FACILE À INSTALLER</h1>

        <div>
            <div>
                <div>01</div>
                <h2>INSCRIVEZ-VOUS GRATUITEMENT SUR NOTRE SITE</h2>
                <p>Quelques clics suffisent pour mettre en place OnTable dans votre établissement.</p>
            </div>

            <div>
                <iframe class="embed-responsive-item" src="https://www.youtube.com/embed/rOxqTYxFRO0"></iframe>
            </div>
        </div>

        <div>
            <div>
                <img src="../../assets/home/upload_easly.png" alt="connexion macintosh">
            </div>

            <div>
                <div>02</div>
                <h2>METTEZ EN LIGNE VOS CARTES ET MENUS</h2>
                <p>Il suffit de mettre en ligne vos cartes/menus en format pdf depuis notre site afin de les rendre disponibles pour vos clients.</p>
            </div>

        </div>

        <div>
            <div>
                <div>03</div>
                <h2>METTEZ LE QR-CODE À DISPOSITION DE VOS CLIENTS</h2>
                <p>Pour finir, il ne reste plus qu'à télécharger votre QR-Code depuis l'interface de gestion et à le laisser à la vue de vos clients.</p>
            </div>

            <div>
                <img src="../../assets/home/presentoir.png" alt="presentoir">
            </div>
        </div>

        <div>
            SIMPLE à utiliser 
        </div>

        <div>
            <div>
                <img src="../../assets/home/capture_qrcode.png" alt="capture qrcode">
                <div>
                    <h2>FAIRE SON CHOIX N'A JAMAIS ÉTÉ AUSSI SIMPLE</h2>
                    <p>Pour voir vos cartes et menus, vos clients n'ont qu'à flasher le QR-Code disponible dans votre établissement ou peuvent se rendre directement sur ontable.fr et entrer le code-établissement.</p>
                </div>
            </div>

            <div>
                <img src="../../assets/home/menu_iphone.png" alt="lire le menu depuis votre téléphone">
                <div>
                    <h2>VOS PRODUITS DANS LE SMARTPHONE DE CHAQUE CLIENT</h2>
                    <p>Une fois connecté, un client aura accès à vos menus et cartes, il n'aura plus que l'embarras du choix.</p>
                </div>
            </div>
        </div>

        <div>
            GRATUIT SANS ENGAGEMENT
        </div>

        <div>
            <h2>NOTRE SERVICE EST GRATUIT</h2>
            <p>OnTable ne peut pas fonctionner sans fonds.
            En échange de nos services, nous affichons un discret bandeau publicitaire en-dessous de vos menus.</p>
            <img src="../../assets/home/pig.png" alt="faites nous un don !">
        </div>

        <div>
            <div>
                <img src="../../assets/home/qrcodes.png" alt="achetez un présentoir">
            </div>
            <h2> ACHETEZ DES STICKERS ET PRÉSENTOIRS</h2>
            <p>Si vous ne désirez pas imprimer vous-même vos QR-Code, nous pouvons le faire pour vous. Nous proposons des stickers et présentoirs personnalisés fabriqués en France.</p>
        </div>
    </div>

    
</template>


<script>

import SearchBar from '../main/Search.vue'

export default {
  name: 'BodyHomePage',
  components: {
      SearchBar,
  },
}
</script>
