if(localStorage.getItem('panier') == null){
    panier = {};

  }else{
    panier = JSON.parse(localStorage.getItem('panier'));
  }
  for(item in panier){
    let nom = panier [item][1];
    let quantite = panier[item][0];
    let itemString = `<h3>${nom}</h3>
        <input type="number" name="" id="" value="${quantite}">`;
        $('#item-list').append(itemString);
  }
  