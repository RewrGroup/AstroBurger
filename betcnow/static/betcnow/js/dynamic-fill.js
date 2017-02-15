
    function dynamic_fill(boxID, tipo_pago, amountUSD, user, orderID, hash){ //parámetros visibles en el browser del cliente
        var public_key;
        var period;
        if (tipo_pago == 'jugada'){ //Para pago de jugadas o Para pago de membresias
            public_key = '8591AAuVNwoBitcoin77BTCPUBZxyHk5A7YNE0bmy2J3gls6vO';
            period = '1 MINUTE';
        }
        else if (tipo_pago == 'membresia'){
            public_key = ''; //El public key del box que voy a poner en el pago de memberias
            period = '1 MONTH';
        }        
        cryptobox_show(boxID, 'bitcoin', public_key, 0, amountUSD, period, 'en', 'iframe_id', user, 'MANUAL', orderID, '', '', hash, 530, 230);
    }