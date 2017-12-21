
    function dynamic_fill(boxID, tipo_pago, amount, user, orderID, hash){ //parámetros visibles en el browser del cliente
        var public_key;
        var period;
        if (tipo_pago == 'jugada'){ //Para pago de jugadas o Para pago de membresias
            public_key = '21210AA0Q9URBitcoincash77BCHPUB2avCPSe9Rbpq8pX41HD';
            period = '1 MINUTE';
        }
        else if (tipo_pago == 'membresia'){
            public_key = '21215AAZ4HAsBitcoincash77BCHPUBDboZf7ASaFNQRBYwX79'; //El public key del box que voy a poner en el pago de memberias
            period = '1 MONTH';
        }        
        cryptobox_show(boxID, 'bitcoincash', public_key, amount, 0, period, 'en', 'iframe_id', user, 'MANUAL', orderID, '', '', hash, 530, 230);
    }